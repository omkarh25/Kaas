const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://gptme.org/docs/tools.html');
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
