const puppeteer = require('puppeteer-extra')
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
const fs = require('fs');

puppeteer.use(StealthPlugin())

async function main() {
    const courses = await getCourses();
    fs.writeFileSync("../datasets/careers-portal/careers-portal-courses.json", JSON.stringify(courses, null, 4));
    return;
}

async function getCourses() {
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    let courses = [];

    const browser = await puppeteer.launch({ headless: true, defaultViewport: null, args: ['--start-maximized', '--window-size=1920,1080', '--no-sandbox', '--disable-setuid-sandbox'] }); // 
    const page = await browser.newPage();
    await page.setViewport({width: 1920, height: 1080});
    await page.goto(url, { waitUntil: 'networkidle0' });
    // await page.content(); // don't think this is necessary

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

            const titleElement = await courseCard.$("a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");
            const title = titleElement 
                ? await titleElement.evaluate(el => el.textContent.trim()) 
                : "";
                                                    
            const collegeElement = await courseCard.$("a.text-sm.leading-tight.hover\\:text-skin-fill-secondary.hover\\:underline");
            const college = collegeElement 
                ? await collegeElement.evaluate(el => el.textContent.trim()) 
                : "";

            const durationElement = await courseCard.$("span.text-sm.leading-tight");
            const duration = durationElement 
                ? await durationElement.evaluate(el => el.textContent.trim()) 
                : "";

            const pointsElement = await courseCard.$("div.text-sm > span.font-bold");
            const points = pointsElement 
                ? await pointsElement.evaluate(el => el.textContent.trim()) 
                : "";

            const pointsContainer = await courseCard.$('div.text-sm > span:nth-child(2)');
            const pointsText = pointsContainer 
                ? await pointsContainer.evaluate(el => el.textContent) 
                : "";
            const isAdditionalPortfolioTestInterviewRequired = pointsText.includes('#');

            const nfqLevelElement = await courseCard.$("div > span.sr-only:last-child");
            const nfqLevel = nfqLevelElement 
                ? await nfqLevelElement.evaluate(el => el.textContent.trim()) 
                : "";

            // const expandButton = await courseCard.$("div.flex.flex-col.items-center.justify-center.doNotPrint.font-display > label");
            // console.log(maybeButton);

            courses.push({ 
                id: id, 
                type: type, 
                title: title, 
                college: college, 
                duration: duration, 
                points: parseInt(points),
                isAdditionalPortfolioTestInterviewRequired: isAdditionalPortfolioTestInterviewRequired,
                nfqLevel: nfqLevel,
                overview: "",
                summary: "",
                interests: [""]
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