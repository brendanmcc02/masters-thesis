const puppeteer = require('puppeteer');
// const cheerio = require('cheerio');
const fs = require('fs');

async function main() {
    const courses = await getCourses();
    fs.writeFileSync("../datasets/careers-portal/careers-portal-courses.json", JSON.stringify(courses, null, 4));
    return;
}

async function getCourses() {
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    let courses = [];

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle0' }); // networkidle0 may be faulty apparently

    while (true) {
        let courseCards = await page.$$("div.group\\/card");
        
        // DL847
        // CAO
        // Level
        // 8
        // 4 Years
        // QQI Links
        // 605
        // #

        // let targetElements = await courseCard.$$("div.grid > div > span");
        // console.log(targetElements.length);
        // const openButton = await courseCard.$('label');
        // if (openButton) {
        //     console.log("we here!")
        //     await openButton.click();
        // }

        // use waitForSelector!!!
        for (const courseCard of courseCards) {
            const idElement = await courseCard.$("span.text-slate-500.font-bold"); 
            const id = idElement 
                ? await idElement.evaluate(el => el.textContent.trim()) 
                : "";

            // TODO doesn't work
            const typeElement = await courseCard.$("div.grid > div:nth-child(2) > span:nth-child(2)");
            const type = typeElement 
                ? await typeElement.evaluate(el => el.textContent.trim()) 
                : "";

            const titleElement = await courseCard.$(".font-display.font-bold.text-skin-fill-primary.leading-tight.my-1");
            const title = titleElement 
                ? await titleElement.evaluate(el => el.textContent.trim()) 
                : "";

            const collegeElement = await courseCard.$(".text-sm.leading-tight");
            const college = collegeElement 
                ? await collegeElement.evaluate(el => el.textContent.trim()) 
                : "";

            const durationElement = await courseCard.$("div.grid > div:nth-child(2) > span:nth-child(2)");
            const duration = durationElement 
                ? await durationElement.evaluate(el => el.textContent.trim()) 
                : "";

            const pointsElement = await courseCard.$("div.text-sm span.font-bold");
            const points = pointsElement 
                ? await pointsElement.evaluate(el => el.textContent.trim()) 
                : "";

            // TODO isAdditionalPortfolioTestInterviewRequired
            const pointsContainer = await courseCard.$('div.col-span-1.flex.flex-col.items-center.justify-center.font-display div');
            const pointsText = pointsContainer 
                ? await pointsContainer.evaluate(el => el.textContent) 
                : "";
            // Note: The original HTML shows "#" with surrounding spaces/text: <span class=""> # </span>
            const isAdditionalPortfolioTestInterviewRequired = pointsText.includes('#');

            // TODO nfqLevel
            const nfqLevelElement = await courseCard.$("div.grid > div:nth-child(7) > span.sr-only:last-child");
            const nfqLevel = nfqLevelElement 
                ? await nfqLevelElement.evaluate(el => el.textContent.trim()) 
                : "";

            courses.push({ 
                id: id, 
                type: type, 
                title: title, 
                college: college, 
                duration: duration, 
                points: points,
                isAdditionalPortfolioTestInterviewRequired: isAdditionalPortfolioTestInterviewRequired,
                nfqLevel: nfqLevel 
            });
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