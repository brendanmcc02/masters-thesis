# Scraping

## Course Type
* [all courses](https://careersportal.ie/courses/coursefinder) - change the filter on "course type"
    * I honestly don't know what to include, paradox of choice
* [cao only](https://careersportal.ie/courses/coursefinder?types_in=2)

* from  url, you can potentially scrape:
    * course id
    * course type (CAO, PLC, etc.)
    * course title
        * some courses with parentheses have the campus in the title
            * e.g: `Agriculture and Environmental Management (Mountbellew Campus)`
        * figure out if all courses with parentheses have a campus in them, so we can just ignore all cases
    * college
    * nfq level
    * duration
    * points
        * a `#` indicates additional portfolio/test/interview
            * e.g. HPAT, architecture portfolio, etc.
    * on the same page, you can expand the course (with a down button) to get:
        * course overview (text blob)
        * career opportunities (text blob)
        * RIASEC categories
* I'll also need region:
    * this will need to be done manually, with a map of college -> region most likely
    * regions:
        * connacht
        * greater dublin area
        * leinster (excluding dublin)
        * munster
        * ulster
* 100 results per page
    * changing to 500 results doesn't change the url, so will likely have to stick with 100
    * clicking "next page" button doesn't change url
    * repeat until button is grayed out/unavailable

# Translating RIASEC to CareersPortal Interests
* Instead of RIASEC, Careers Portal has:
    * Realistic -> Realist
    * Investigative -> Investigative
    * Artistic -> Creative
    * Social -> Social
    * Enterprising -> Enterprising
    * Conventional -> Administrative
    * and then an additional **Naturalist and Linguistic, where to translate these?**
* **or should I use careers portal's taxonomy instead and find out their test?**