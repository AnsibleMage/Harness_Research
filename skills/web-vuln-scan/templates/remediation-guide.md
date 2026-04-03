# 웹 취약점 수정 가이드

## 개요
본 문서는 점검에서 발견된 주요 취약점에 대한 언어별 수정 방안을 제공합니다.
각 취약점별로 취약 코드와 안전 코드를 비교합니다.

---

## 1. 입력데이터 검증 및 표현

### MOIS-IV-01 SQL 인젝션 (CWE-89)

#### Python
취약:
```python
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
cursor.execute("SELECT * FROM users WHERE id=" + user_id)
```

안전:
```python
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))  # SQLite
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))  # MySQL
```

#### Java
취약:
```java
Statement stmt = conn.createStatement();
stmt.execute("SELECT * FROM users WHERE id=" + userId);
```

안전:
```java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id=?");
ps.setString(1, userId);
ResultSet rs = ps.executeQuery();
```

#### PHP
취약:
```php
$result = mysqli_query($conn, "SELECT * FROM users WHERE id=" . $_GET['id']);
```

안전:
```php
$stmt = $conn->prepare("SELECT * FROM users WHERE id=?");
$stmt->bind_param("s", $_GET['id']);
$stmt->execute();
```

#### JavaScript (Node.js)
취약:
```javascript
db.query(`SELECT * FROM users WHERE id=${req.params.id}`);
```

안전:
```javascript
db.query("SELECT * FROM users WHERE id=?", [req.params.id]);
```

---

### MOIS-IV-03 크로스사이트 스크립팅 XSS (CWE-79)

#### JavaScript (프론트엔드)
취약:
```javascript
document.getElementById('output').innerHTML = userInput;
```

안전:
```javascript
document.getElementById('output').textContent = userInput;
// 또는 DOMPurify
document.getElementById('output').innerHTML = DOMPurify.sanitize(userInput);
```

#### Python (Flask/Django)
취약:
```python
return f"<div>{user_input}</div>"
```

안전:
```python
return render_template("page.html", content=user_input)  # Jinja2 자동 이스케이프
```

#### PHP
취약:
```php
echo "<div>" . $_GET['name'] . "</div>";
```

안전:
```php
echo "<div>" . htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8') . "</div>";
```

---

### MOIS-IV-04 OS 명령어 삽입 (CWE-78)

#### Python
취약:
```python
os.system("ping " + user_input)
subprocess.call("ls " + dirname, shell=True)
```

안전:
```python
subprocess.run(["ping", user_input], shell=False)
subprocess.run(["ls", dirname], shell=False)
```

#### PHP
취약:
```php
system("ping " . $_GET['host']);
```

안전:
```php
$host = escapeshellarg($_GET['host']);
system("ping " . $host);
```

---

### MOIS-IV-10 CSRF (CWE-352)

#### Python (Flask)
취약:
```python
@app.route("/transfer", methods=["POST"])
def transfer():
    amount = request.form["amount"]  # CSRF 토큰 없음
```

안전:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

@app.route("/transfer", methods=["POST"])
def transfer():
    amount = request.form["amount"]  # Flask-WTF 자동 CSRF 검증
```

---

## 2. 보안 기능

### MOIS-SF-04 취약한 암호화 알고리즘 (CWE-327)

#### Python
취약:
```python
import hashlib
hashlib.md5(password.encode()).hexdigest()
hashlib.sha1(password.encode()).hexdigest()
```

안전:
```python
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# 또는
import hashlib, os
salt = os.urandom(32)
hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
```

---

### MOIS-SF-05 중요정보 평문저장 (CWE-312)

취약 (모든 언어):
```
config = {"db_password": "mypassword123", "api_key": "sk-abc123"}
```

안전:
```python
import os
config = {"db_password": os.environ["DB_PASSWORD"], "api_key": os.environ["API_KEY"]}
```

---

### MOIS-SF-07 하드코드된 비밀번호 (CWE-259)

취약:
```
password = "admin123"
API_KEY = "sk-1234567890"
```

안전:
```python
password = os.environ.get("APP_PASSWORD")         # Python
```
```java
String password = System.getenv("APP_PASSWORD");   // Java
```
```php
$password = getenv("APP_PASSWORD");                // PHP
```
```javascript
const password = process.env.APP_PASSWORD;         // Node.js
```

---

## 3. 에러 처리

### MOIS-EH-01 오류 메시지를 통한 정보노출 (CWE-209)

#### Python
취약:
```python
except Exception as e:
    return str(e)  # 스택 트레이스 노출
```

안전:
```python
except Exception as e:
    logger.error(f"Error: {e}")  # 서버 로그에만 기록
    return "처리 중 오류가 발생했습니다.", 500
```

---

### MOIS-EH-03 부적절한 예외 처리 (CWE-396)

취약:
```python
try:
    process()
except:
    pass  # 모든 예외 무시
```

안전:
```python
try:
    process()
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
    return default_value
except IOError as e:
    logger.error(f"IO error: {e}")
    raise
```

---

## 4. 코드 오류

### MOIS-CE-05 신뢰할 수 없는 데이터의 역직렬화 (CWE-502)

#### Python
취약:
```python
import pickle
data = pickle.loads(user_input)  # 원격 코드 실행 가능
```

안전:
```python
import json
data = json.loads(user_input)  # JSON만 허용
```

#### Java
취약:
```java
ObjectInputStream ois = new ObjectInputStream(inputStream);
Object obj = ois.readObject();  // 역직렬화 공격
```

안전:
```java
// JSON 라이브러리 사용 (Jackson, Gson)
ObjectMapper mapper = new ObjectMapper();
MyClass obj = mapper.readValue(jsonString, MyClass.class);
```

---

> **참고**: 이 가이드는 주요 취약점만 포함합니다.
> 전체 49개 보안약점의 상세 수정 방안은 행안부 「소프트웨어 개발보안 가이드」를 참조하세요.

---
*수정 가이드 | Claude Code /web-vuln-scan*
