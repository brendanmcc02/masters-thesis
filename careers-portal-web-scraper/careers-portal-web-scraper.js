const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');
const { title } = require('process');

async function main() {
    const courses = await getCourses();
    fs.writeFileSync("../datasets/careers-portal/careers-portal-courses.json", JSON.stringify(courses, null, 4));
    return;
}

async function getCourses() {
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    let courses = {};

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle0' });

    while (true) {
        let courseCards = await page.$$("div.group\\/card");

        for (const courseCard of courseCards) {
            const idElement = await courseCard.$("span.text-slate-500.font-bold");
            const id = idElement 
                ? await idElement.evaluate(el => el.textContent.trim()) 
                : "";

            const typeElement = await courseCard.$("span.text-slate-300.text-\\[10px\\]");
            const type = typeElement 
                ? await typeElement.evaluate(el => el.textContent.trim()) 
                : "";


            const titleElement = await courseCard.$("a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1");
            const title = titleElement 
                ? await titleElement.evaluate(el => el.textContent.trim()) 
                : "";

            if (id) {
                courses[id] = { id: id, type: type, title: title };
            }
        }
        
        if (isNextButtonDisabled()) {
            continue;
        } else {
            await browser.close();
            return courses;
        }
    }
}

function isNextButtonDisabled() {
    return false;
}

main();