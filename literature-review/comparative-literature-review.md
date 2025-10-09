# Academic Papers

* From my research, almost all academic papers in this area lack significant grounding in guidance counselling literature
    * generally, they make a brief introduction, and then they talk a lot about RS and then dive into architecture
    * this is an edge I can push for in my thesis: it's informed from strong scientific research

## **[Career Counselling Recommendation System](https://www.preprints.org/frontend/manuscript/cf467753c75a6dcc24ac4aaf70ce013f/download_pub)**
* Does a meta-analysis/survey on RS solutions to the area of career counselling
    * i.e. they don't propose any methods themselves, more of a survey
* The abstract is well-written
    * Talks about the concerns with RS being applied in this domain
* Author talks about issue with real-time labour market
    * is that an issue with courses? imo, not a big concern
* possible ethical concerns:
    * Academic scores
        * very likely need to be used in RS
        * e.g.: no point recommending 500-point courses to someone who can achieve 350 max
    * Aptitudes profile
        * I guess this is considered sensitive?
    * Personal interests & extracurriculars
        * Is that relevant? IMO, no.
        * It would add unnecessary noise to the data
        * More dimensions does not necessarily mean more accuracy, sometimes it's actually worse.
* they make a good point about autonomy
    * the RS should be a starting point/helping hand, it shouldn't make the decisions for the student
* in terms of literature review, it's very focused on RS as opposed to guidance counselling
* they mention MyCareerAid, an example of a successful career RS
    * but I can't find it online, so it probably doesn't exist anymore `:(`
    * they profiled:
        1. academic record
        2. skill assessments (could be anything, quite vague)
        3. survey responses
            * this might not be directly relevant to the course recs itself, maybe a survey of their satisfaction with the service or something? idk

## [RECOMMENDER SYSTEMS TO SUPPORT STUDENTS' EMPLOYABILITY: THE CASE STUDY OF CAREPROFSYS](https://library.iated.org/view/BIRZANEANU2024REC)
* Recommending careers, as opposed to courses
* They ask students to take a personality test (I'm assuming OCEAN?)
    * they don't specify
* They also get info from their social media (interesting) and CV

## [A comparative analysis of different recommender systems for university major and career domain guidance](https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf)
* According to their work, a **hybrid RS with CF and KB (supported by Case-Based Reasoning and Ontology) yielded the best results.**
    * I find this interesting, because I would have thought CF is a poor idea in the case of course/career.
    * I could be wrong about the CF assumption though
* This has a potentially useful reference for *"Choosing a university major or a career domain is a challenging task overflowing with concern that makes students distracted"* [here](https://www.sciencedirect.com/science/article/pii/S0360131521001421?via%3Dihub)
* Their work lacks a lot of scientific research into guidance counselling and is very much RS-focused, by comparing the different types of RS'

## [PCRS: Personalized Career-Path Recommender System for Engineering Students](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9268112)
* They profile the following info off students:
     1. personal interests (hobbies)
     2. skills (unsure exactly what that is) 
     3. academic scores 
     4. personality type (they use MBTI).
     5. gender (wouldn't agree with this personally)
* Similar to mine, but for engineering students, concept should be the same
* **Interesting:** Their dataset is only from under/postgrad engineers who are **satisfied** with their degree

## [Smart Career Guidance and Recommendation System](https://rjwave.org/ijedr/papers/IJEDR1903111.pdf)
* Recommends careers to CS students
* Uses & compares multiple ML methods to generate results
* Almost no talk about guidance counsellor literature 
* Kinda ass paper ngl

## [Envisioning Tomorrow: AI Powered Career Counseling](https://ieeexplore.ieee.org/abstract/document/10426016)
* Can't get full access
* They profile student's:
    1. Grades
    2. Extracurriculars
    * and based off that, they recommend courses
* very limited profiling imo

## [Counselling Career with Artificial Intelligence: A Systematic Review](https://pdfs.semanticscholar.org/d292/5cd666cd4f1184eeecdc23e334061447dbd2.pdf)
* Survey of AI in Career counselling
* It is worth mentioning this paper is more concerned with guidance counselling in it's entirety
    * guidance counselling is so much more than taking inventory of a person and recommending courses to them (which is what I'm trying to achieve with my thesis)
    * it's a process where the human element is crucial
    * this paper is more concerned with the human-emotional element of counselling, and the implications of AI being involved in that
* kinda ass paper ngl

## [A Novel Approach for Better Career Counselling Utilizing Machine Learning Techniques](/literature-review/papers/s11277-024-11612-3.pdf)
* They test various ML techniques:
    * Random Forest, SVM, Naive Bayes, KNN, etc.
* The profile student's:
    1. hobbies
    2. grades
    3. interests (what exactly, idk)
    4. achievements
* So poorly written ngl

# Real-world products

* From my research, there is **no AI/ML solution to course recommendations in Ireland!**

1. [Advisor AI](https://joinadvisorai.com/)
    * very specialised to the US system
        * I can push mine to fit the Irish system, as an edge
        * but then again, now I'm thinking of it like a product, instead of research
    * they do have assistance with selecting a major
        * but from initial research, I don't see if they are profiling the students based on personality tests, their wants, etc.
        * seems like it's from their resume + academic scores
    * the platform also helps guidance counsellors to manage students, and other features, so it's not just major recommendation, all-in-one platform
    * helps students pick classes at college
        * also very specific to US
    * helps them get internships and resume & career guidance
2. [KapAdvisor](https://www.kaptest.com/college-prep/ai-advisor?srsltid=AfmBOorz2_TZQVt8N68srekEPO81P3vT1cWx33Gjr3c74smOkAAwzY2W)
    * Also very specialised to the US system, assistance with:
        * admission letters
        * matching a college
        * trying to get into ivy league
        * admission guidance
    * doesn't seem so much about guidance for a specific major
    * this is what the free version offers
    * paid version asks for academic scores and report cards
        * it gauges strengths and weaknesses based off that
        * I think that's limiting, especially compared to a Holland code/personality test
        * grades don't tell you everything
3. [iDreamCareer](https://idreamcareer.com/)
    * focused on Indian market
4. [Univariety](https://www.univariety.com/home/)
    * Indian too I believe
    * all-in-one-platform for alumni management, etc.
    * not just career recs

# The edge of my Thesis
* There is no course recommender system for the Irish college system
* In almost all of the peripheral literature I could find, there is a lack of scientific grounding with guidance counselling
* In almost all the papers I've seen, they are either using traditional/ML methods for recs, as opposed to LLM-based recs