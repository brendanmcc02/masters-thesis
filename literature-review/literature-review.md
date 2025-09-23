**Potential Title:** 

***What course should I choose? Applying a Recommender Systems-Model to University Course Counselling***

# Misc Notes

## First Meeting w Owen

* By xmas, have a:
    1. **clear research question/defined project**
    2. **review of literature done**
    3. **solid draft of lit review chapter**
* In a masters thesis, you don't have feasible time to do a proper lit review
    * he calls it "pseudo-systematic"
    * be *'inspired' by PRIMSA, but don't follow it exactly
* Owen: *"often hardest part of a thesis to write is the lit review"*
* In a Masters, novelty is not essential with theses
    * your work must still be justified of course
* Ask yourself what you get excited about/interested in,
    * **use that to fuel your research/reading of lit**
* For now, just **skim** papers. Just read:
    1. Title
    2. Abstract
    3. Introduction (Owen didn't mention it, but I think it's worth reading)
    4. Conclusion

# RS Papers

## TODO research these:
* novelty in rec sys
* serendipity in rec sys
* bias in RS
    * course idea:
        * gender
        * social class
        * race
* human's preferences change over time
    * investigate the evolution of this
* history of RS
    * doesn't have to be in depth, mostly for intro/abstract tbh

## LLM's in Rec Sys

### [Towards Next-Generation LLM-based Recommender Systems: A Survey and Beyond](https://arxiv.org/pdf/2410.19744)
* investigates LLM-based RS
* LLM's have the capacity for reasoning, which is an advantage over DL.
* They are also endowed with common-sense knowledge and are trained on large corpora, it's not tunnel-visioned on the only task it was designed for.
* They have a section on Challenges and Opportunities for LLM integration with RS. *Could be useful.*

### [Recommender Systems in the Era of Large Language Models (LLMs)](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10506571)
* Surveys LLM usage in RS
* It is mentioned that RS's are specialised to work for an exact problem, and are not "one-size-fits-all" solutions
    * that being said, LLM's such as ChatGPT are generalized, "one-size-fits-all" solutiions, **but** they learn in-context.

### [Exploring the Impact of Large Language Models on Recommender Systems: An Extensive Review](https://arxiv.org/pdf/2402.18590)
* Talks about specific LLM models are being used in RS
* The main advantage of LLM's being used in RS is their ability to **utilise language**
    * I see this pop around a lot

### [Retrieval-augmented Recommender System: Enhancing Recommender Systems with Large Language Models](https://dl.acm.org/doi/pdf/10.1145/3604915.3608889)
* Examines LLM's ability to do Recommendations

### [Large Language Models are Zero-Shot Rankers for Recommender Systems](https://arxiv.org/pdf/2305.08845)
* Examines LLM usage in RS
* According to the paper: 
    * LLM-based RS suffer from position and popularity bias
        * But they provide a solution in the paper
    * LLM's struggle to perceive the order of given sequential interaction history
        * Can be alleviated through good prompt engineering
        * probably not so relevant for me tbh, but who knows

### [Leveraging Large Language Models in Conversational Recommender Systems](https://arxiv.org/pdf/2305.07961)
* Uses Conversational RS (CRS), pretty interesting.
    * They call it RecLLM
* **A conversational element could be really useful to integrate with my course idea**
    * Obviously, the recs are generated using known user profile (e.g. aptitudes, grades)
    * But this can also be augmented with a conversational chat agent, where the user can query and push the recs/RS
* They go into architecture too which would be relevant if I would go down the CRS path

## XAI

* **Fairness, Accountability & Transparency** pops up a lot.

### **[European Union regulations on algorithmic decision-making and a “right to explanation”](https://arxiv.org/pdf/1606.08813)**
* **Important:** EU legislation about explainability in AI/RS
* Individuals *"have the right to not to be subject to a decision based solely on automated processing, including profiling"*
    * this does not mean you **can't** do it of course
    * if an individual consents to it, they can be profiled, which is essential in the case of RS.
* GDPR has a list of what they consider "sensitivive data"
    * Academic scores, personal interests/aptitudes would not fall into this list, thankfully
* They discuss **uncertainty bias** - algorithms will choose under-represented samples less often because the sparsity of data
    * algorithms are designed for success, and under-represented samples pose a risk that algorithms may want to avoid
    * does this apply in my case?
* *"Articles 13 and 14 state that, when profiling takes place, a data subject has the right to “meaningful information about the logic involved.”"*
    * This is what the paper refers to as the **right to explain**

### [Recommender Systems: An Explainable AI Perspective](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9548125)

* Provides overview/synthesis of XAI in rec sys and how it's being used in this field

### [A Comparative Review of Expert Systems, Recommender Systems, and Explainable AI](literature-review/papers/I2CT2022Paper0834.pdf)

* Provides overview/synthesis of architectural similarities between RS and XAI

### [The effects of explainability and causability on perception, trust, and acceptance: Implications for explainable AI](https://www.sciencedirect.com/science/article/pii/S1071581920301531)

* Talks about human perception and trust of AI, in the context of XAI/RS
* **Causability:** *the potential for one thing to cause another, or the quality of being able to be caused*
* The paper argues that in AI systems: **causability is an antecendent to explainability.**

### [Evolution of AI-Driven Decision Making with Decision Support Systems, Expert Systems, Recommender Systems, and XAI](https://www.tandfonline.com/doi/abs/10.1080/02564602.2025.2512086)

* Comparative analysis of Expert Systems (ES), RS and XAI

### [Peeking Inside the Black-Box: A Survey on Explainable Artificial Intelligence (XAI)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8466590&tag=1)

* Analyis/overview of XAI

## Explainability & Scrutability

* [Gemini's explanation](https://gemini.google.com/u/1/app/376a1fa53f4a3bd0)

### Explainability
* Providing compelling reasons and transparency as to how & why a RS arrived at a recommendation
* Some papers will use the term **interpretability** interchangeably

### Scrutability
* The ability to modify or control a RS
    * Correct false assumptions of the system
        * e.g: it thinks you like action films, so you can explicitly request to not get action recs
    * you might gain a new interest or change your preferences over time
        * a good RS should accomodate this
* a conversational LLM-based RS could really enhance scrutability
    * for instance, let's say my RS recommends 10 courses
    * you might like the idea of 3 of them, and say why you like them
    * you might not like the idea of 4 of them, and say why
    * with this in a prompt, you can push the conversational RS LLM more, and through this it can modify its profile of you based on what you said: scrutability

### [Enhancing Explainability and Scrutability of Recommender Systems](https://universaar.uni-saarland.de/bitstream/20.500.11880/32590/1/azin_ghazimatin_phd_thesis.pdf)
* Provides practical frameworks & solutions for enhancing explainability and scrutability in RS
* **Counter-factual explanations:** it explains that with the absence of a subset of data, the recommendation would have been different
    * the paper acknowledges this would be very expensive and potentially inefficent, calling for more research in the area
    * counter-factual explanations provide insight into scrutability - the user now knows if they didn't rate those subset of items, they would have gotten different recs
* They have a section (2.2.2) on the importance of explanability, might be useful.
* This paper really goes into depth on explainability, really useful if I plan to do something similar with my thesis.

### [Trustworthy Recommender Systems](https://dl.acm.org/doi/pdf/10.1145/3627826)
* Section 2.2 talks about aspects of a Trustworthy RS
* Section 2.3 has a useful diagram
* Section 3: the author talks about a paradigm shift from "accuracy-oriented RSs" to "trustworthy-oriented RSs"

## Human-in-the-Loop (HITL)

* There are 2 types of users with a course RS:
    1. Student who is discovering courses
    2. Guidance counsellor who uses this tool to aid his suggestions for the student
* With HITL, the guidance counsellor would be the "human-in-the-loop" and strongly modify the RS to cater to what they perceive as important
* However, I don't think that would be in scope for this thesis
    * I want to focus on a student end-user experience
* With regards to HITL for students, I think a conversational LLM could be useful, and this gives more power to the end user
    * this would be more useful compared to recommending x courses, and providing simple thumbs up/down RL

### [Is the Human-in-the-Loop Concept Applied in Educational Recommender Systems?](https://www.researchgate.net/profile/Paola-Palomino-2/publication/374908511_Virtual_Classroom_and_the_Impact_of_E-Skills_on_the_Performance_of_Peruvian_University_Students/links/6807d4d6d1054b0207dc27e0/Virtual-Classroom-and-the-Impact-of-E-Skills-on-the-Performance-of-Peruvian-University-Students.pdf#page=659)
* The context of this paper is Educational RS
* Mentions an example of teachers being able to modify an Educational RS for a student
    * in this case, the teacher would be the HITL for this Educational RS

### [A survey of human-in-the-loop for machine learning](https://tinyurl.com/yc7upec6)
* Useful, comprehensive survey if needed

## Conversational RS (CRS)

* A traditional CRS learns the user profile through conversation, i.e. natural language
* that isn't exactly what I had in mind for my course idea
    * if this was my idea, then there is no good reason for a user to use the CRS over a tool like ChatGPT
* That being said, I think some conversational agent would be useful post-hoc to the recs
* in other words, a conversational LLM could tune the recs and learn more about user preferences

### [A Survey on Conversational RS](https://dl.acm.org/doi/pdf/10.1145/3453154)
* TODO read

## RS/DL/AI applied to course counselling or similar

### [The POWER of Ikigai: Optimizing Life Fulfillment with an Integrated User Simulator and Adaptive Hobby Recommender](/literature-review/papers/35159-Article%20Text-39226-1-2-20250410.pdf)
* Predicts a user's ikigai level
* Based on this, it recommends hobbies

### [RECOMMENDER SYSTEMS TO SUPPORT STUDENTS' EMPLOYABILITY: THE CASE STUDY OF CAREPROFSYS](https://library.iated.org/view/BIRZANEANU2024REC)
* Hybrid RS for **careers**, not courses.

### **[A comparative analysis of different recommender systems for university major and career domain guidance](https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf)**
* **IMPORTANT PAPER!**
* According to their work, a **hybrid RS with CF and KB (supported by Case-Based Reasoning and Ontology) yielded the best results.**
    * I find this interesting, because I would have thought CF is a poor idea in the case of course/career.
    * I could be wrong about the CF assumption though
* This has a potentially useful reference for *"Choosing a university major or a career domain is a challenging task overflowing with concern that makes students distracted"* [here](https://www.sciencedirect.com/science/article/pii/S0360131521001421?via%3Dihub)

### [PCRS: Personalized Career-Path Recommender System for Engineering Students](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9268112)
* Similar to mine, but for engineering students, concept should be the same
* **Interesting:** Their dataset is only from under/postgrad engineers who are **satisfied** with their degree

### [Smart Career Guidance and Recommendation System](https://rjwave.org/ijedr/papers/IJEDR1903111.pdf)
* Recommends careers to CS students
* Uses & compares multiple ML methods to generate results
* Kinda ass paper ngl

### **[Career Counselling Recommendation System](https://www.preprints.org/frontend/manuscript/cf467753c75a6dcc24ac4aaf70ce013f/download_pub)**
* **Great paper to reference if I am going with this idea**
* Does a meta-analysis on RS/ML solutions to the area of career counselling
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

### [Envisioning Tomorrow: AI Powered Career Counseling](https://ieeexplore.ieee.org/abstract/document/10426016)
* Didn't read, saving for later

### [Counselling Career with Artificial Intelligence: A Systematic Review](https://pdfs.semanticscholar.org/d292/5cd666cd4f1184eeecdc23e334061447dbd2.pdf)
* Didn't read, saving for later

### [A Novel Approach for Better Career Counselling Utilizing Machine Learning Techniques](/literature-review/papers/s11277-024-11612-3.pdf)
* Didn't read, saving for later
* ~~**Done by someone in TCD in 2024!**~~
    * incorrect i think idk

### [A comparative analysis of different recommender systems for university major and career domain guidance](https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf#page=27&zoom=100,66,377)
* Didn't read, saving for later

# Course/Career Papers
* What do people **want** out of a career or course?
    * **sometimes people might want different things with a career vs a course**
        * for example, people might see a course as an opportunity to explore their interests
        * and a career as something stable to make money
        * e.g. study maths/physics at college, and then work in finance
    * **should I even be considering career at all?**
        * on one hand, yes - a course is intended to prepare you for your career.
            * but most people end up working in a field different to their college major
                * but that doesn't justify people studying whatever they want
                * that happens because people either:
                    1. make bad choices in the course they choose
                    2. make a locally good decision, but their preferences/abilities change over time
                        * which is completely natural, and shouldn't be considered as something bad
            * **TODO get stats on this**
        * but that could also be considered scope creep?
            * rn, no. I'd say it's still relevant, and I don't want to throw it out too early.
* How do you determine that a course or career is successful for someone?
    * I would argue this is **subjective** and it depends on what the person answered to the questions: ***"What do people want out of a course?"***
    * As I've already established, people want different things out of their course/career:
    * Back to the original question, what then are the success metrics?
        * For some people, the success metric is **money**
            * they see work as a means for living
        * for some people, the success metric is how **meaningful** their work is.
            * they want to make a difference
        * for some people, the success metric is how **passionate** they are about their work.
            * they want to do something they love
        * for some people, the success metric is a **challenging and engaging** job
            * they want to do something that they can apply their skills and grow them
    * Observe that the above four points are all present in **Ikigai**
    * It would be important for the RS to gauge **how important** each of these 4 components are to their work
* **Culture** is also a major factor in course/career selection
    * for example, western attitudes will differ from eastern ones
    * when looking at academic papers, consider this bias
* Consider **survivorship bias:**
    * Not everyone goes to college
    * Not every career requires college, some might require apprenticeships
    * When you interview college students, consider this bias.

## [Gemini's Report when asked similar questions](https://gemini.google.com/u/1/app/b86675ee95bf927b)
* College major/career choice is a complex, multi-dimensional problem
    * one factor is **socio-demographic**
* if you are from a poor background, do you value finances more?
* similarly, if you are from a rich background, do you value finance or passion more?
* according to Gemini, your choice in college major is **vastly impacted by:**
    1. your socio-economic background
    2. your parents educational background
* **Explanable and scrutable RS is crucial, because a user will want to know why the course was recommended.**
* **TODO research these theories of career choice:**
    1. Holland's Theory of Career Choice
    2. Super's Life-Span, Life-Space Theory
    3. Social Cognitive Career Theory

## [Holland's Theory of Career Choice](https://www.ebsco.com/research-starters/economics/hollands-theory-career-choice)
* Posits that an individual's vocational interests reflect their personality traits, suggesting that people achieve greater career fulfillment when their jobs align with their personal attributes.
* He categorises personalities into 6 types:
    1. Realistic (Doers)
    2. Investigative (Thinkers)
    3. Artistic (Creatives)
    4. Social (Helpers)
    5. Enterprising (Persuaders)
    6. Conventional (Organizers)
* The theory also emphasises that a person may be a mix of the 6 traits - they are not **mutually exclsuive**
* The theory has immense success, being used by career counsellors and even the US government
* Still used and cited today apparently
* He has a test for determining your **Holland code**
    * **TODO look into this**   
* Over the years he has refined his work, and remarked that many other factors contribute to a person's vocational choice:
    * educational level of the individual
        * I would also include parents educational background
    * health
    * employment opportunities

## [Job satisfaction](https://www.ebsco.com/research-starters/business-and-management/job-satisfaction)
* **TODO**

## Academic Papers

### [Why Students Select their College Major: An Investigative Study](https://digitalcommons.kennesaw.edu/cgi/viewcontent.cgi?article=1370&context=amj)
* "Survey data was collected from 1,177 undergraduates at a southeastern U.S. university"
    * results may be biased towards western attitudes
    * most participants were white (78.5%) or African-american (14%)
* Their findings: *"The highest ranked reason is interest and passion, followed by fit with personality type."*
    * *"This was similar for students who changed majors. "*
* Consider survivorship bias in this study: they asked college students about their college major choice, which doesn't include a sample of blue-collar workers or potentially unrepresentative those from working class backgrounds
* Their intro has some good stats that I can maybe use
* clear benefits:
    1. less time spent in college
    2. less money spent on tuition
    3. higher job satisfaction/course fit
    4. higher graduation rates
* They analyse the case of why students change majors. 
    * According to other papers, it's mostly due to internal factors:
        1. interesting subject matter
        2. course enjoyment
    * interestingly, family influence was shown to play a smaller role when students changed their major.

### [How do young people choose college majors?](https://www.sciencedirect.com/science/article/pii/S0272775701000541)

# Human Pyschology Papers

## Human Decision-Making

### [Chapter 18 Human Decision Making and Recommender Systems](https://www.researchgate.net/profile/Martijn-Willemsen/publication/275152080_Human_Decision_Making_and_Recommender_Systems/links/566b36d208ae1a797e39d8de/Human-Decision-Making-and-Recommender-Systems.pdf)

* there are many different models for how people approach decision-making
* Socially Based Choice (18.2.4)
    * in the context of picking a course, collaborative filtering could be problematic due to social expectations
        * people are influenced by society and their decisions, and CF could reinforce this

### [Human Decision Making and Recommender Systems](https://dl.acm.org/doi/pdf/10.1145/2533670.2533675)

* **Preference Construction:** *[...] humans often do not have a clear picture of
their preferences from the very beginning but rather develop their preferences within
the context of a decision process*