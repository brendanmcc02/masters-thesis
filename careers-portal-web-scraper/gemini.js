// gemini: https://gemini.google.com/u/1/app/7543a701fa11a9f7

const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');

/**
 * Main function to scrape course data from CareersPortal.ie.
 */
async function scrapeCareersPortal() {
    const coursesData = {};
    const url = 'https://careersportal.ie/courses/coursefinder?types_in=2';
    
    // --- Configuration ---
    const COURSE_CONTAINER_SELECTOR = '.group\\/card'; 
    const NEXT_BUTTON_SELECTOR = '.MuiPaginationItem-previousNext:last-child';
    const DISABLED_CLASS = 'Mui-disabled';

    // Launch a headless browser for dynamic interaction
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    console.log(`Navigating to ${url}...`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });

    let pageNum = 1;

    while (true) {
        console.log(`\n--- Scraping Page ${pageNum} ---`);
        
        // Find all course containers on the current page
        const courseHandles = await page.$$(COURSE_CONTAINER_SELECTOR);

        for (let i = 0; i < courseHandles.length; i++) {
            const courseHandle = courseHandles[i];
            
            // 1. Basic Data Extraction (using Puppeteer's evaluate for fast, isolated parsing)
            const basicData = await courseHandle.evaluate(el => {
                const getText = (selector) => el.querySelector(selector)?.textContent.trim() || 'N/A';
                
                // Selectors based on inspecting a typical structure:
                const header = getText('.flex-1.p-4'); 
                const idMatch = header.match(/^([A-Z0-9]{3,6})/); // e.g., 'DL846'
                const typeMatch = header.match(/\(([A-Z]+)\)/); // e.g., 'CAO'
                const titleMatch = header.match(/-\s(.*?)\s\(/); // Title between '-' and '('
                
                // College, NFQ Level, Duration
                const college = getText('span.text-sm.text-gray-600'); 
                const levelDuration = getText('span.text-xs.text-gray-500'); 
                const nfqMatch = levelDuration.match(/NFQ Lvl: (\d+)/);
                const durationMatch = levelDuration.match(/Duration: (.+?)(?:\s|$)/);
                
                // Points (ignoring the increase/decrease below it)
                const points = getText('.text-xl.font-semibold.text-blue-600').split(/\s+/)[0].replace(/[\*\#\+]+$/, '');
                
                // RIASEC categories (Interests)
                const interestElements = el.querySelectorAll('.flex.flex-wrap > span'); 
                const interests = Array.from(interestElements).map(span => span.textContent.trim());

                return {
                    id: idMatch ? idMatch[1] : 'N/A',
                    type: typeMatch ? typeMatch[1] : 'N/A',
                    title: titleMatch ? titleMatch[1].trim() : 'N/A',
                    college: college,
                    nfq_level: nfqMatch ? parseInt(nfqMatch[1]) : 'N/A',
                    duration: durationMatch ? durationMatch[1] : 'N/A',
                    points: points, 
                    interests: interests,
                };
            }, courseHandle);

            if (basicData.id === 'N/A') {
                console.log(`Skipping course ${i} due to parsing issues.`);
                continue;
            }
            
            // 2. Interactive Detail Scraping (Overview & Careers)
            try {
                // Find the expand button (assuming it's a button with a dropdown icon or toggle role)
                const expandButton = await courseHandle.$('button');
                
                // Click to expand the course details
                await expandButton.click();
                
                // Wait for the details section to fully load (AJAX content)
                await page.waitForTimeout(1000); // 1-second pause for content load is often necessary with AJAX

                // Get the updated HTML for Cheerio parsing
                const html = await page.content();
                const $ = cheerio.load(html);
                
                // Re-locate the specific course container in the Cheerio DOM
                const courseEl = $(COURSE_CONTAINER_SELECTOR).eq(i); 
                
                // ASSUMED SELECTORS for the expanded content:
                // Assuming the overview and careers are inside sections with specific headings.
                const overviewSection = courseEl.find('h4:contains("Course Overview")').next();
                const careersSection = courseEl.find('h4:contains("Career Opportunities")').next();
                
                const overview = overviewSection.length ? overviewSection.text().trim() : 'N/A';
                const career_opportunities = careersSection.length ? careersSection.text().trim() : 'N/A';

                // Store the full data
                coursesData[basicData.id] = {
                    ...basicData,
                    overview: overview,
                    career_opportunities: career_opportunities,
                };

                console.log(`Scraped details for ${basicData.id}: ${basicData.title}`);

                // Click again to collapse the details
                await expandButton.click();
                await page.waitForTimeout(100); 

            } catch (error) {
                console.error(`Error scraping details for ${basicData.id}: ${error.message}`);
                // Save what we have, even if details failed
                coursesData[basicData.id] = { ...basicData, overview: 'N/A', career_opportunities: 'N/A' };
            }
        }
        
        // --- Pagination Logic ---
        const nextButton = await page.$(NEXT_BUTTON_SELECTOR);
        
        // Check if the next button is disabled
        const isDisabled = await nextButton.evaluate(btn => btn.classList.contains('Mui-disabled'));
        
        if (isDisabled) {
            console.log('\nLast page reached. Next button is disabled.');
            break; // Exit the loop
        }
        
        // Click the next button
        await nextButton.click();
        
        // Wait for the new content to load
        await page.waitForSelector(COURSE_CONTAINER_SELECTOR); 
        await page.waitForTimeout(2000); // Wait for content stability
        
        pageNum++;
    }

    await browser.close();

    // Write the final JSON output
    const outputFilename = 'careers-portal.json';
    fs.writeFileSync(outputFilename, JSON.stringify(coursesData, null, 4));
    
    console.log(`\n✅ Scraping complete! Total courses scraped: ${Object.keys(coursesData).length}`);
    console.log(`Output written to ${outputFilename}`);
}

// execute the scraper function
scrapeCareersPortal();