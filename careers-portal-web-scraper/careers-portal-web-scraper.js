const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');

async function main() {
    const courses = await getCourses();
    writeToJson(courses, "../datasets/careers-portal/careers-portal-courses.json");
}

function writeToJson(data, filepath) {
    const stringData = JSON.stringify(data, null, 4);

    fs.writeFileSync(filepath, stringData, (error) => {
        if (error) {
            writeMetadata("error", startTime, error.name, error.message);
            throw error;
        }
    });
}

async function getCourses() {
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    let courses = {};

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    // while true:
        // for each course:
        //      puppeteer to expand course
        //      get all data

        // if next button is not disabled:
            // click button
        // else:
            // break loop

    return courses;
}

main();