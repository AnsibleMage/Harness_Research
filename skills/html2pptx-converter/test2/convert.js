const pptxgen = require('pptxgenjs');
const html2pptx = require('../engine/html2pptx');
const path = require('path');

async function main() {
  const pptx = new pptxgen();

  // CUSTOM layout for wireframe (995pt x 720pt)
  const widthInches = 995 / 72;
  const heightInches = 720 / 72;
  pptx.defineLayout({ name: 'CUSTOM', width: widthInches, height: heightInches });
  pptx.layout = 'CUSTOM';

  pptx.author = 'html2pptx';
  pptx.title = 'TestCorp Portal Wireframe';

  // Convert slide
  const slideHtml = path.join(__dirname, 'slides', 'slide_00.html');
  console.log(`Converting: ${slideHtml}`);

  const { slide, placeholders } = await html2pptx(slideHtml, pptx);
  console.log(`Slide created. Placeholders: ${placeholders.length}`);

  // Save
  const outputPath = path.join(__dirname, 'presentation.pptx');
  await pptx.writeFile({ fileName: outputPath });
  console.log(`Created: ${outputPath}`);
}

main().catch(err => {
  console.error('Conversion failed:', err.message);
  process.exit(1);
});
