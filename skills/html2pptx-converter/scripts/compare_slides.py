#!/usr/bin/env python3
"""
compare_slides.py - Side-by-side comparison image of original PNG and PPTX thumbnail.

Usage:
    python scripts/compare_slides.py <original_png> <thumbnail_image> <output_path>
"""

import argparse
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# ---------------------------------------------------------------------------
# PIL Import Guard
# ---------------------------------------------------------------------------

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print(
        "오류: Pillow 라이브러리가 설치되어 있지 않습니다.\n"
        "설치 명령어: pip install Pillow",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_HEIGHT = 800          # px — maximum height for each slide image
GAP = 20                  # px — horizontal gap between two images
LABEL_HEIGHT = 40         # px — space above each image for text labels
BORDER_WIDTH = 1          # px — border around each image
BACKGROUND_COLOR = (245, 245, 245)   # light gray canvas background
BORDER_COLOR = (180, 180, 180)       # thin gray border
LABEL_BG_COLOR = (245, 245, 245)     # same as canvas — no separate label bg
LABEL_TEXT_COLOR = (60, 60, 60)      # dark gray text
LABEL_FONT_SIZE = 16
JPEG_QUALITY = 90

LABEL_LEFT = "Original HTML"
LABEL_RIGHT = "PPTX Result"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_image(path: str) -> Image.Image:
    """Open image and convert to RGB."""
    img = Image.open(path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if img.mode == "RGBA":
        # Composite onto white background so JPEG export works cleanly
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    return img


def resize_to_height(img: Image.Image, target_height: int) -> Image.Image:
    """Resize image preserving aspect ratio to match target_height."""
    if img.height == target_height:
        return img
    ratio = target_height / img.height
    new_width = max(1, int(img.width * ratio))
    return img.resize((new_width, target_height), Image.LANCZOS)


def draw_border(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color, width: int = 1):
    """Draw a rectangle border (outline only) around the given region."""
    for i in range(width):
        draw.rectangle(
            [x - i, y - i, x + w - 1 + i, y + h - 1 + i],
            outline=color,
        )


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """
    Attempt to load a readable font. Falls back to PIL default if no TTF found.
    Tries common system font paths on Windows, macOS, and Linux.
    """
    candidate_paths = [
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        # macOS
        "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidate_paths:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:  # noqa: BLE001
                continue
    # PIL built-in fallback (very small, no size control)
    return ImageFont.load_default()


def center_text_x(draw: ImageDraw.ImageDraw, text: str, font, region_x: int, region_width: int) -> int:
    """Calculate x coordinate to center text within a region."""
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    except AttributeError:
        # Older Pillow fallback
        text_width, _ = draw.textsize(text, font=font)
    return region_x + max(0, (region_width - text_width) // 2)


# ---------------------------------------------------------------------------
# Core Comparison Builder
# ---------------------------------------------------------------------------

def build_comparison(
    original_path: str,
    thumbnail_path: str,
    output_path: str,
) -> str:
    """
    Create side-by-side comparison image.

    Returns the absolute path of the saved output file.
    """
    # Load images
    img_left = load_image(original_path)
    img_right = load_image(thumbnail_path)

    # Determine shared display height (use smaller of the two, capped at MAX_HEIGHT)
    natural_height = min(img_left.height, img_right.height)
    display_height = min(natural_height, MAX_HEIGHT)

    # Resize both to display_height
    img_left = resize_to_height(img_left, display_height)
    img_right = resize_to_height(img_right, display_height)

    w_left = img_left.width
    w_right = img_right.width
    total_width = w_left + GAP + w_right
    total_height = LABEL_HEIGHT + display_height

    # Create canvas
    canvas = Image.new("RGB", (total_width, total_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)

    font = get_font(LABEL_FONT_SIZE)

    # Draw labels
    label_y = (LABEL_HEIGHT - LABEL_FONT_SIZE) // 2
    label_y = max(4, label_y)

    x_label_left = center_text_x(draw, LABEL_LEFT, font, 0, w_left)
    draw.text((x_label_left, label_y), LABEL_LEFT, fill=LABEL_TEXT_COLOR, font=font)

    x_label_right = center_text_x(draw, LABEL_RIGHT, font, w_left + GAP, w_right)
    draw.text((x_label_right, label_y), LABEL_RIGHT, fill=LABEL_TEXT_COLOR, font=font)

    # Paste images
    y_img = LABEL_HEIGHT
    canvas.paste(img_left, (0, y_img))
    canvas.paste(img_right, (w_left + GAP, y_img))

    # Draw borders around each image
    draw_border(draw, 0, y_img, w_left, display_height, BORDER_COLOR, BORDER_WIDTH)
    draw_border(draw, w_left + GAP, y_img, w_right, display_height, BORDER_COLOR, BORDER_WIDTH)

    # Ensure output directory exists
    out_path = Path(output_path)
    os.makedirs(out_path.parent, exist_ok=True)

    # Save — force JPEG extension awareness
    save_path = str(out_path)
    suffix = out_path.suffix.lower()
    if suffix in (".jpg", ".jpeg", ""):
        if suffix == "":
            save_path += ".jpg"
        canvas.save(save_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    else:
        # For .png or anything else, save as-is
        canvas.save(save_path)

    return os.path.abspath(save_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def validate_input_file(path: str, label: str):
    """Exit with error message if file does not exist or is not a file."""
    if not os.path.exists(path):
        print(f"오류: {label} 파일을 찾을 수 없습니다: '{path}'", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(path):
        print(f"오류: {label} 경로가 파일이 아닙니다: '{path}'", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="원본 HTML 스크린샷과 PPTX 썸네일을 나란히 비교하는 이미지를 생성합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/compare_slides.py output/slide_00.png output/thumbnail.png output/compare.jpg
  python scripts/compare_slides.py screenshots/original.png thumbnails/result.jpg comparisons/side_by_side.jpg
        """,
    )
    parser.add_argument(
        "original_png",
        help="원본 웹페이지 스크린샷 경로 (PNG 또는 JPG)",
    )
    parser.add_argument(
        "thumbnail_image",
        help="PPTX 썸네일 이미지 경로 (thumbnail.py 생성 결과, 단일 이미지 또는 그리드)",
    )
    parser.add_argument(
        "output_path",
        help="비교 이미지 저장 경로 (예: output/comparison.jpg)",
    )
    args = parser.parse_args()

    # Validate inputs
    validate_input_file(args.original_png, "original_png")
    validate_input_file(args.thumbnail_image, "thumbnail_image")

    print(f"원본 이미지   : {args.original_png}")
    print(f"썸네일 이미지 : {args.thumbnail_image}")
    print(f"출력 경로     : {args.output_path}")
    print("비교 이미지 생성 중...")

    try:
        saved_path = build_comparison(
            original_path=args.original_png,
            thumbnail_path=args.thumbnail_image,
            output_path=args.output_path,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"오류: 비교 이미지 생성 실패 — {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"완료: 비교 이미지 저장됨 → {saved_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
