const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const html2pptx = require(path.resolve(__dirname, '..', '..', 'engine', 'html2pptx'));

async function convert() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'html2pptx-converter';
    pptx.company = 'html2pptx-skill';

    const slidesDir = path.join(__dirname, 'slides');

    if (!fs.existsSync(slidesDir)) {
        throw new Error(`slides directory not found: ${slidesDir}`);
    }

    const slideFiles = fs.readdirSync(slidesDir)
        .filter(f => f.endsWith('.html'))
        .sort();

    if (slideFiles.length === 0) {
        throw new Error('No HTML files in slides directory.');
    }

    console.log(`Converting ${slideFiles.length} slides...`);

    for (const file of slideFiles) {
        const htmlPath = path.join(slidesDir, file);
        console.log(`  Processing: ${file}`);
        await html2pptx(htmlPath, pptx);
    }

    const outputPath = path.join(__dirname, 'presentation.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Done: ${outputPath}`);
}

const startTime = Date.now();
convert()
    .then(() => {
        const elapsed = Date.now() - startTime;
        console.log(`Conversion time: ${elapsed}ms`);
    })
    .catch(err => {
        console.error('Conversion failed:', err.message);
        console.error(err.stack);
        process.exit(1);
    });
