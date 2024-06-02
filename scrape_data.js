const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeData() {
    // Launch headless browser
    const browser = await puppeteer.launch();

    // Create a new page
    const page = await browser.newPage();

    // Navigate to the webpage
    await page.goto('https://www.cubmu.com/play/live-tv?id=4028c68574537fcd0174be58644c5901&genreId=10');

    // Wait for the element indicating the video has started
    await page.waitForSelector('.video-element-playing');

    // Wait for dt-custom-data element to appear
    await page.waitForSelector('dt-custom-data');

    // Extract the value of dt-custom-data
    const data = await page.$eval('dt-custom-data', element => element.innerText);

    // Close the browser
    await browser.close();

    // Save the data to a file
    fs.writeFileSync('data.txt', data, 'utf-8');
}

// Call the function to scrape data
scrapeData().then(() => console.log('Data scraped successfully')).catch(error => console.error('Error scraping data:', error));
