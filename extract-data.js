const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeData() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://www.cubmu.com/play/live-tv?id=4028c68574537fcd0174be58644c5901&genreId=10');
    await page.waitForSelector('dt-custom-data'); // Wait for dt-custom-data element to load
    const data = await page.$eval('dt-custom-data', element => element.innerText);
    await browser.close();
    return data;
}

scrapeData().then(data => {
    fs.writeFileSync('data.txt', data, 'utf-8');
});
