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

    const browser = await puppeteer.launch({ headless: true, defaultViewport: null, args: ['--start-maximized', '--window-size=1920,1080', '--no-sandbox', '--disable-setuid-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({width: 1920, height: 1080});
    await page.goto(url, { waitUntil: 'networkidle0' });

    while (true) {
        let courseHandles = await page.$$("div.group\\/card");

        for (const courseHandle of courseHandles) {
            const id = await getTextFromSelector(courseHandle, "span.text-slate-500.font-bold");
            const type = await getTextFromSelector(courseHandle, "span.text-slate-300.text-\\[10px\\]");
            const title = await getTextFromSelector(courseHandle, "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");
            const college = await getTextFromSelector(courseHandle, "a.text-sm.leading-tight.hover\\:text-skin-fill-secondary.hover\\:underline");
            const duration = await getTextFromSelector(courseHandle, "span.text-sm.leading-tight");
            const nfqLevel = await getTextFromSelector(courseHandle, "div > span.sr-only:last-child");
            const points = parseInt(await getTextFromSelector(courseHandle, "div.text-sm > span.font-bold"));

            const additionalPortfolioTestInterviewRequiredText = await getTextFromSelector(courseHandle, "div.text-sm > span:nth-child(2)");
            const isAdditionalPortfolioTestInterviewRequired = additionalPortfolioTestInterviewRequiredText.includes('#');
            
            const expandButton = await courseHandle.$("div.flex.flex-col.items-center.justify-center.doNotPrint.font-display > label");
            await expandButton.click();
            
            const overviewElementSelector = "div.prose.max-w-none.prose-sm.prose-slate.prose-headings\\:font-display.prose-headings\\:font-bold > div";
            await courseHandle.waitForSelector(overviewElementSelector, { visible: true, timeout: 10000 });
            const overviewHandles = await courseHandle.$$(overviewElementSelector + ":first-child > p");
            console.log("2?" + overviewHandles.length);
            // const overview = await Promise.all(
            //     overviewHandles.map(handle => handle.evaluate(el => el.textContent.trim()))
            // );
            let overview = "";
            for (overviewHandle of overviewHandles) {
                overview += await getTextFromSelector(overviewHandle, "p") + "\n";
            }

            courses.push({ 
                id: id,
                type: type,
                title: title,
                college: college,
                duration: duration,
                nfqLevel: nfqLevel,
                points: points,
                isAdditionalPortfolioTestInterviewRequired: isAdditionalPortfolioTestInterviewRequired,
                overview: overview,
                summary: "",
                interests: [""]
            });

            // TODO temp
            await browser.close();
            return courses;
        }
        
        if (isNextButtonDisabled()) {
            // TODO
            // click next button
            // refresh html or something
            continue;
        } else {
            await browser.close();
            return courses;
        }
    }
}

async function getTextFromSelector(elementHandle, selector) {
    const element = await elementHandle.$(selector); 
    const text = element 
        ? await element.evaluate(el => el.textContent.trim()) 
        : "";

    return text;
}

// TODO
function isNextButtonDisabled() {
    return false;
}

main();