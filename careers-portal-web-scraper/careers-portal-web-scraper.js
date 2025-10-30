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

    const pagesToSkip = 0;
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
        console.log("New page");
        let courseHandles = await page.$$(COURSE_HANDLES_SELECTOR);
        let newTitle = await getHandleTextFromSelector(courseHandles[0], "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

        if (prevTitle === newTitle) {
            console.log("prev:" + prevTitle);
            console.log("new:" + newTitle);
            await browser.close();
            return;
        }

        for (let courseHandle of courseHandles) {
        // for (let i = 99; i < courseHandles.length; i++) {
            const id = await getHandleTextFromSelector(courseHandle, "span.text-slate-500.font-bold");

            if (id.toLowerCase().includes("cancelled")) {
                continue;
            }

            const type = await getHandleTextFromSelector(courseHandle, "span.text-slate-300.text-\\[10px\\]"); // TODO if i'm only doing college courses then this is irrelevant
            let title = await getHandleTextFromSelector(courseHandle, "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

            if (title.toLowerCase().includes("cancelled") || title.toLowerCase().includes("graduate entry") || title.includes("replaced") || title.includes("mature")) {
                continue;
            }

            title = cleanCourseTitle(title);

            const college = await getHandleTextFromSelector(courseHandle, "div.col-span-2.flex.flex-col.items-start.justify-center.font-display > a.text-sm.leading-tight");
            const region = getRegion(college);
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
                    type: type, // TODO if i'm only doing college courses then this is irrelevant
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
            
            let overview = await getHandleTextFromSelector(courseHandle, overviewElementSelector);
            if (overview === "Data will be updated as soon as it becomes available") {
                overview = "";
            }

            const careerOpportunities = await getHandleTextFromSelector(courseHandle, "div.prose.max-w-none.prose-sm.prose-slate.prose-headings\\:font-display.prose-headings\\:font-bold > div:nth-of-type(2)");

            const interests = await getInterests(courseHandle);

            console.log("Pushed " + id);
            courses.push({ 
                id: id,
                type: type, // TODO if i'm only doing college courses then this is irrelevant
                title: title,
                college: college,
                region: region,
                duration: duration,
                nfqLevel: nfqLevel,
                points: points,
                isAdditionalPortfolioTestInterviewRequired: isAdditionalPortfolioTestInterviewRequired,
                overview: overview,
                careerOpportunities: careerOpportunities,
                interests: interests
            });

            await sleepForMs(7500);
        }

        fs.writeFileSync("../datasets/cao-college-courses/cao-college-courses.json", JSON.stringify(courses, null, 4));

        prevTitle = await getHandleTextFromSelector(courseHandles[0], "a.font-display.font-bold.text-skin-fill-primary.leading-tight.my-1.hover\\:text-skin-fill-secondary.hover\\:underline");

        // I have no idea why, but the first thing that matches the selector is not the button we're looking for.
        // even though the html clearly only shows one button that matches the descriptor
        // maybe it's hidden or something, idc. this works.
        const nextButtons = await page.$$(NEXT_BUTTON_SELECTOR);
        // scroll to bottom of the DOM (scrolling to the html element is unreliable)
        await page.evaluate(() => {
            window.scrollTo(0, document.body.scrollHeight);
        });
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
        return 0;
    }

    return parseInt(points);
}

function cleanCourseTitle(courseTitle) {
  // \s* - Matches zero or more whitespace characters (to remove space before parenthesis)
  // \(        - Matches the opening parenthesis literally
  // [^)]* - Matches any character except a closing parenthesis, zero or more times
  // campus    - Matches the literal string "campus" (case-insensitive due to the 'i' flag)
  // [^)]* - Matches any character except a closing parenthesis, zero or more times
  // \)        - Matches the closing parenthesis literally
  // gi -> global (match all occurences), and i (case-insensitive)

  const campusInParenthesesPattern = /\s*\([^)]*campus[^)]*\)/gi;
  return courseTitle.replace(campusInParenthesesPattern, '');
}

async function getInterest(interestsHandle) {
    const interest = await interestsHandle.evaluate(el => el.textContent.trim());

    switch (interest) {
        case "Realist":
            return "Realistic";
        case "Investigative":
            return interest;
        case "Creative":
            return "Artistic";
        case "Social":
            return interest;
        case "Enterprising":
            return interest;
        case "Administrative":
            return "Conventional";
        case "Naturalist":
            return "Realistic";
        case "Linguistic":
            return "Artistic";
        default:
            console.log("INTEREST DOESN'T MATCH!!!: " + interest);
            return ("INTEREST DOESN'T MATCH!!!: " + interest);
    }
}

async function getInterests(courseHandle) {
    let interests = [];
    const interestsHandles = await courseHandle.$$("div.mt-8.flex.flex-wrap.items-center.gap-2 span");
    for (const interestsHandle of interestsHandles) {
        const interest = await getInterest(interestsHandle);

        if (!interests.includes(interest)) {
            interests.push(interest);
        }
    }

    return interests;
}

function getRegion(collegeName) {
    switch (collegeName) {
        case "ATU Donegal":
            return "Ulster";
        
        case "University College Cork - UCC":
            return "Munster";
        case "MTU Cork Campus":
            return "Munster";
        case "MTU Kerry Campus":
            return "Munster";
        case "TUS Midwest":
            return "Munster";
        case "TUS Midwest (Thurles)":
            return "Munster";
        case "TUS Midlands":
            return "Munster";
        case "Griffith College Cork":
            return "Munster";
        case "Griffith College Limerick":
            return "Munster";
        case "University of Limerick - UL":
            return "Munster";
        case "SETU Waterford Campus":
            return "Munster";
        case "Mary Immaculate College":
            return "Munster";
        case "National Maritime College of Ireland (NMCI)":
            return "Munster";
        case "Shannon College of Hotel Management":
            return "Munster";
        
        case "Carlow College":
            return "Leinster (excluding Dublin)";
        case "Dundalk Institute of Technology - DKIT":
            return "Leinster (excluding Dublin)";
        case "Maynooth University":
            return "Leinster (excluding Dublin)";
        case "St. Patrick's Pontifical University":
            return "Leinster (excluding Dublin)";
        case "SETU Carlow Campus":
            return "Leinster (excluding Dublin)";
        case "SETU Wexford Campus":
            return "Leinster (excluding Dublin)";

        case "Galway Business School":
            return "Connacht";
        case "University of Galway - UG":
            return "Connacht";
        case "ATU Galway / Mayo":
            return "Connacht";
        case "ATU Sligo":
            return "Connacht";
        case "ATU Donegal":
            return "Connacht";
        case "ATU Connemara":
            return "Connacht";
        case "ATU Sligo St. Angelas":
            return "Connacht";

        case "American College":
            return "Dublin";
        case "BIMM Institute Dublin":
            return "Dublin";
        case "CCT College Dublin":
            return "Dublin";
        case "Dorset College":
            return "Dublin";
        case "Dublin Business School - DBS":
            return "Dublin";
        case "Dublin City University - DCU":
            return "Dublin";
        case "Griffith College Dublin":
            return "Dublin";
        case "IBAT College. Dublin": // yes there's supposed to be a . there
            return "Dublin";
        case "ICD Business School":
            return "Dublin";
        case "Institute of Art, Design and Technology Dun Laoghaire - IADT":
            return "Dublin";
        case "Marino Institute of Education":
            return "Dublin";
        case "National College of Art and Design - NCAD":
            return "Dublin";
        case "National College of Ireland - NCI":
            return "Dublin";
        case "RCSI University of Medicine and Health Sciences":
            return "Dublin";
        case "Setanta College":
            return "Dublin";
        case "Trinity College Dublin - TCD":
            return "Dublin";
        case "University College Dublin - UCD":
            return "Dublin";
        case "TU Dublin - Tallaght":
            return "Dublin";
        case "TU Dublin - Grangegorman":
            return "Dublin";
        case "TU Dublin - Blanchardstown":
            return "Dublin";
        case "TU Dublin - Aungier Street":
            return "Dublin";
        case "TU Dublin - Bolton Street":
            return "Dublin";

        default:
            console.log("region doesn't match! " + collegeName);
            return "";
    }
}

main();
