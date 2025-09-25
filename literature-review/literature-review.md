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
    * be *'inspired'* by PRIMSA, but don't follow it exactly
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
* What people **want** out of a course is often not the same as what is **best** for them.
    * In this context, a good RS should recommend courses that are the intersection of **wants** and **aptitudes**
    * I would also argue that the RS should rec courses that they haven't said they wanted for **serendipity & novelty**
* What do people **want** out of a career or course?
    * **sometimes people might want different things with a career vs a course**
        * for example, people might see a course as an opportunity to explore their interests
            * more likely for someone with a higher social class/affluent background, who can afford to waste time/money
        * and a career as something stable to make money
            * more likely (I guess)for someone with a lower social class, who can't waste money or resources
        * e.g. study maths/physics at college, and then work in finance
    * I would say that is not a popular case. If that is something the person wants, then a good RS should be able to accomodate that through natural language (e.g. Conversational RS) or other means
    * For an RS like this, you need to profile a person's interests (aptitudes), and also their **wants**
        * However, we should not exclusively recommend courses that intersect with a person's aptitudes and their wants
            * Firstly, this would be an uninteresting RS producing non-novel results
            * But also, people often **construct their preferences** *(see preference construction)*
                * so, a course would get recommended to them that might conflict with something they thought they wanted, but from this experience they may learn that isn't something they want
            * So, recommending courses that don't align with their wants (but alings with their aptitudes) not only is beneficial because of **serendipity and novelty**, but it may also challenge and develop a person's preferences
    
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
    * I think reducing it down to these 4 factors is **reductionisitic**
        * **Prestige** and social perception is also a factor
        * **Work/life balance** too
* **Culture** is also a major factor in course/career selection
    * for example, western attitudes will differ from eastern ones
    * when looking at academic papers, consider this bias
* Consider **survivorship bias:**
    * Not everyone goes to college
    * Not every career requires college, some might require apprenticeships
    * When you interview college students, or consider samples of college students only, remember this bias.

## [Gemini's Report when asked similar questions](https://gemini.google.com/u/1/app/b86675ee95bf927b)
* College major/career choice is a complex, multi-dimensional problem
    * one factor is **socio-demographic**
* if you are from a poor background, do you value finances more?
* similarly, if you are from a rich background, do you value finance or passion more?
* according to Gemini, your choice in college major is **vastly impacted by:**
    1. your socio-economic background
    2. your parents educational background
* **Explanable and scrutable RS is crucial, because a user will want to know why the course was recommended.**
* **Didn't think about this** - Gemini reckons that the RS should be a tool that shouldn't be a single-use thing: i.e. sign up, get your profile, get recs, and then leave. It should be something that stays with them throughout their career journey
    * this fits with the idea that career is not one, single decision, but a continually changing process.
    * while I think this is interesting, I'm not sure about the applicability of it. People's preferences change a lot over time, their personalities less so. Would you wipe the context completely, or partially (as Owen suggested)?
    * If I am focusing the tool just on second-level students, making a choice for college is a single thing. Obviously that doesn't mean you are stuck in that course/career for the rest of your life, but you do have to commit yourself to **one course.** That would be your starting point.

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
* A potential limitation of this theory is that it does not take cultural factors into account

## Frank Parson's Theory
* Similar concept to Holland
* Find out your personality traits
* Find out the personality traits required for a job
* See how they match up

## [Life-Span, Life-Space Theory](https://d1wqtxts1xzle7.cloudfront.net/51286605/0001-8791_2880_2990056-120170110-8091-lvww3k-libre.pdf?1484070807=&response-content-disposition=inline%3B+filename%3DA_life_span_life_space_approach_to_caree.pdf&Expires=1758709042&Signature=bwtIUxZfD8AIaYZRtqH5JxYzXsiw80A41MSW1pFB72i9yPkjHzEAaDh-WCAj23~GzzcNMXfyM-rsRmYdK8jORh8VDJABhJI6D4wjo9Su0AuUWQuiu58dUs-BFuaMxYb9zSe4F3y36lakDGhr9DZLsgDHcwCRp47YTQTsN9bYZ-o2TdCPKeiC6F9kCdNSV05p~TrGlWPxSY8L6SJfQjggpog~Yy3GtSg1U17vK6g44O9vQTiMjaY9Rknesa86oGGrQLcGi-zb8MTrs2vxRRp8a5H-AyXFdQtVzPiUZ5tkGVvCFJjKgNetMgEFOYpDytLW4m~b9eNQZKW5FiOsMCfwlQ__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)
* career is a developmental process where a person evolves their self-concept over time
* it is a developmental process spanning one's life, as opposed to one, specific decision
* people evolve through different roles throughout their career: student, worker, spouse, parent, pensioner
* Super's theory is more concerned with the **development** of an individual through their lifelong career, so my case, I don't think this is incredibly relevant.

## [Social Cognitive Career Theory (SCCT)](https://www.ebsco.com/research-starters/business-and-management/social-cognitive-career-theory-scct)
* Similar to Life-Span, Life-Space Theory, this theory is concerned with individual's career decisions throughout their life
    * whereas my thesis specifically addresses the case of college students choosing the starting point of their career
* Theorizes the decision-making process in career decisions and exploration.
* three essential concepts to this theory:
    1. Self-efficacy
        * an individual's belief they can complete certain tasks or challenges
    2. Personal goals
        * self explanatory
    3. Outcomes Expectations
        * anticipated consequences of career decisions
* However, they recognise these factors would be reductionistic, and there are also other influences at play: cultural factors, social supports and inhibitors.
* It is a dynamic loop: people are more likely to make career decisions that they believe will yield good outcomes and feel capable of succeeding (self-efficacy). When this results in success, it will increase their outcome expectations and self-eficacy as a result, reinforcing it. This would encourage them to set higher goals (Personal Goals).
* Gemini concludes that 'interest/passion' is the number 1 intrinsic driver in an individual, and number 2 is 'personality fit'. It's source for that is [this](https://digitalcommons.kennesaw.edu/cgi/viewcontent.cgi?article=1370&context=amj),  a sample of 1177 undergrads in south US, not the most representative sample ever, and it's one study, so take Gemini's confident claim with a grain of salt.
* It mentions three factors that influence a college major decision:
    1. Intrinsic Drivers
        * personality, preferences.
    2. Extrinsic Factors
        * e.g. salary, job security, defined career path, prestige.
    3. Social influences
        * socio-economic background, parental education.
* Money is not a simple variable, you can't just put a single value like "average graduate salary".
    * That does not tell the full story
    * Some careers have longer ROI, others lead to quicker ROI.
* Gemini claims that social influence (e.g. friends, teachers, etc.) is **not uniform across cultures**
    * it's source is one study that found African-Americans are more influenced by high-school teachers than whites
* In my prompt, I asked about a link between college majors and career
    * for some people, they see college as a place to equip them with specified skills for a more defined career
        * e.g. study CS to be a software engineer
    * in rarer cases, they see college as a place to improve their critical thinking, communication and problem-solving skills
        * e.g. study liberal arts, philosophy
* **good suggestion:** ask the user if they want to explore career paths (arts & humanities), or if they want a more defined career path through their career.
* they mention the RS should factor in the user's **financial risk tolerance**, and whether they prefer high early-career earnings (quick ROI), or longer term higher salaries.

## [Job satisfaction](https://www.ebsco.com/research-starters/business-and-management/job-satisfaction)
* **TODO**

## Cultural Differences
* [Gemini Report](https://gemini.google.com/u/1/app/509512f9309b9786)
* Culture is a big influence on course/career choices, particularly on high-school age where they have less autonomy, life experience and generally more susceptible to parental/societal influence.

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
* My opinion is that this is quite a **reductionist** study
* They use a mathematical formula for caluclating a student's perceived probability of success in that major
    * In this formula, they factor in **financial earnings** of a college major, and the riskiness of the major.
    * I think this is very reductionistic and doesn't take countless factors into account, e.g. aptitudess, cultural attitude towards college/career, wants, how much they value money, etc.
* According to the paper, women are less influenced by expected earnings of a college major than men
* And non-whites are less influenced by expected earnings of a college major than whites

### [Rich Grad, Poor Grad](https://docs.iza.org/dp16099.pdf)
* great title btw
* They see a **strong correlation** between a student's college major choice and their family's educational background.
* Interestingly, parental income has a weak influence on a student's college major choice.
    * However, the parental income is a large influence on the institution their child attends, but not necessarily the major.
* Students with more educated parents will often pick college majors with low early-career earnings, but deferred gratification, and much faster earnings growth.
    * I belive this is also from greater financial risk tolerance.
* Students with less educated parents will often pick college majors with higher early-career earnings and a more defined career path.
    * I believe this is due to less financial risk tolerance, so they prioritise "safer" paths.

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