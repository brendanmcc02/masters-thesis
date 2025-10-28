const pptr = require('puppeteer-extra')
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
const fs = require('fs');
const NEXT_BUTTON_SELECTOR = "button.MuiButtonBase-root.MuiPaginationItem-root.MuiPaginationItem-sizeMedium.MuiPaginationItem-text.MuiPaginationItem-circular.MuiPaginationItem-previousNext.css-1xr9krm";
const COURSE_HANDLES_SELECTOR = "div.group\\/card";

pptr.use(StealthPlugin())

async function main() {
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    let courses = [];

    const browser = await pptr.launch({ headless: true, defaultViewport: null, args: ['--start-maximized', '--window-size=1920,1080', '--no-sandbox', '--disable-setuid-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({width: 1920, height: 1080});
    await page.goto(url, { waitUntil: 'networkidle0' });

    const pagesToSkip = 3;
    for (let i = 1; i <= pagesToSkip; i++) {
        let nextButtons = await page.$$(NEXT_BUTTON_SELECTOR);

        if (nextButtons.length > 1) {
            await nextButtons[1].evaluate(el => el.scrollIntoView({ behavior: 'smooth', block: 'center' }));
            await nextButtons[1].click();

            await sleepForMs(3000);

            await page.waitForSelector(COURSE_HANDLES_SELECTOR, { visible: true, timeout: 10000 });
        } else {
            await browser.close();
        }
    }

    let prevTitle = "";
    while (true) {
        let courseHandles = await page.$$(COURSE_HANDLES_SELECTOR);
        const newTitle = await getHandleTextFromSelector(courseHandles[0], "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

        if (prevTitle === newTitle) {
            await browser.close();
            return;
        }

        for (let courseHandle of courseHandles) {
            const id = await getHandleTextFromSelector(courseHandle, "span.text-slate-500.font-bold");

            if (id.toLowerCase().includes("cancelled")) {
                console.log("Course is cancelled, skipping: " + id);
                continue;
            }

            const type = await getHandleTextFromSelector(courseHandle, "span.text-slate-300.text-\\[10px\\]");
            let title = await getHandleTextFromSelector(courseHandle, "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

            if (title.toLowerCase().includes("cancelled")) {
                console.log("Course is cancelled, skipping: " + id + ", " + title);
                continue;
            }

            title = cleanCourseTitle(title);

            const college = await getHandleTextFromSelector(courseHandle, "div.col-span-2.flex.flex-col.items-start.justify-center.font-display > a.text-sm.leading-tight");
            const duration = await getHandleTextFromSelector(courseHandle, "span.text-sm.leading-tight");
            const nfqLevel = parseInt(await getHandleTextFromSelector(courseHandle, "div > span.sr-only:last-child"));
            const points = await getPoints(courseHandle);

            const additionalPortfolioTestInterviewRequiredText = await getHandleTextFromSelector(courseHandle, "div.text-sm > span:nth-child(2)");
            const isAdditionalPortfolioTestInterviewRequired = additionalPortfolioTestInterviewRequiredText.includes('#');
            
            await courseHandle.evaluate(el => el.scrollIntoView({ behavior: 'smooth', block: 'center' }));
            await sleepForMs(1000);

            const expandButton = await courseHandle.$("div.flex.flex-col.items-center.justify-center.doNotPrint.font-display > label");
            await expandButton.click();

            const overviewElementSelector = "div.prose.max-w-none.prose-sm.prose-slate.prose-headings\\:font-display.prose-headings\\:font-bold > div:nth-of-type(1)";
            
            try {
                await courseHandle.waitForSelector(overviewElementSelector, { visible: true, timeout: 10000 });
            } catch (TimeoutError) {
                courses.push({ 
                    id: id,
                    type: type,
                    title: title,
                    college: college,
                    duration: duration,
                    nfqLevel: nfqLevel,
                    points: points,
                    isAdditionalPortfolioTestInterviewRequired: isAdditionalPortfolioTestInterviewRequired,
                    overview: "",
                    careerOpportunities: "",
                    interests: []
                });
                console.log("Timeout waiting for " + overviewElementSelector + " on " + id + ". Pushed incomplete course to dataset.");
                continue;
            }
            
            const overview = await getHandleTextFromSelector(courseHandle, overviewElementSelector);

            const careerOpportunities = await getHandleTextFromSelector(courseHandle, "div.prose.max-w-none.prose-sm.prose-slate.prose-headings\\:font-display.prose-headings\\:font-bold > div:nth-of-type(2)");

            let interests = []
            const interestsHandles = await courseHandle.$$("div.mt-8.flex.flex-wrap.items-center.gap-2 span");
            for (const interestsHandle of interestsHandles) {
                interests.push(await interestsHandle.evaluate(el => el.textContent.trim()));
            }

            console.log("Pushed " + id);
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
                careerOpportunities: careerOpportunities,
                interests: interests
            });

            await sleepForMs(10000);
        }

        fs.writeFileSync("../datasets/careers-portal/careers-portal-courses.json", JSON.stringify(courses, null, 4));

        prevTitle = await getHandleTextFromSelector(courseHandles[0], "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

        // I have no idea why, but the first thing that matches the selector is not the button we're looking for.
        // even though the html clearly only shows one button that matches the descriptor
        // maybe it's hidden or something, idc. this works.
        const nextButtons = await page.$$(NEXT_BUTTON_SELECTOR);
        await nextButtons[1].evaluate(el => el.scrollIntoView({ behavior: 'smooth', block: 'center' }));
        await nextButtons[1].click();

        await sleepForMs(20000);

        await page.waitForSelector(COURSE_HANDLES_SELECTOR, { visible: true, timeout: 10000 });
    }
}

async function getHandleTextFromSelector(elementHandle, selector) {
    const element = await elementHandle.$(selector); 
    const text = element 
        ? await element.evaluate(el => el.textContent.trim()) 
        : "";

    return text;
}

async function sleepForMs(ms) {
    await new Promise(r => setTimeout(r, ms));
}

async function getPoints(courseHandle) {
    const points = await getHandleTextFromSelector(courseHandle, "div.col-span-1.flex.flex-col.items-center.justify-center.font-display > div.text-sm > span");

    if (points === "AQA") {
        // TODO is 0 the best thing to return here?
        return 0;
    } else if (points !== null) {
        return parseInt(points);
    }

    const isNewCourseText = await getHandleTextFromSelector(courseHandle, "div.text-xs.bg-skin-fill-secondary.rounded-full.px-2.text-white.font-bold");
    if (isNewCourseText === "New!") {
        // TODO is 0 the best thing to return here?
        return 0;
    }

    return null;
}

function cleanCourseTitle(courseTitle) {
  // \s* - Matches zero or more whitespace characters (to remove space before parenthesis)
  // \(        - Matches the opening parenthesis literally
  // [^)]* - Matches any character except a closing parenthesis, zero or more times
  // campus    - Matches the literal string "campus" (case-insensitive due to the 'i' flag)
  // [^)]* - Matches any character except a closing parenthesis, zero or more times
  // \)        - Matches the closing parenthesis literally
  
  const campusPattern = /\s*\([^)]*campus[^)]*\)/gi;
  
  // Use String.prototype.replace() with the regular expression
  return courseTitle.replace(campusPattern, '');
}

main();