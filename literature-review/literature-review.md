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

# Papers

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

## LLM's in Rec Sys

### [Towards Next-Generation LLM-based Recommender Systems: A Survey and Beyond](https://arxiv.org/pdf/2410.19744)
* investigates LLM usage instead of traditional rec sys methods

## XAI

* **Fairness, Accountability & Transparency** pops up a lot.

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

## Scrutability

* [Difference between scrutability and explainability in the context of RS](https://gemini.google.com/u/1/app/376a1fa53f4a3bd0)

### [Enhancing Explainability and Scrutability of Recommender Systems](https://universaar.uni-saarland.de/bitstream/20.500.11880/32590/1/azin_ghazimatin_phd_thesis.pdf)
* 

## RS/DL/AI applied to course counselling or similar

### [The POWER of Ikigai: Optimizing Life Fulfillment with an Integrated User Simulator and Adaptive Hobby Recommender](/literature-review/papers/35159-Article%20Text-39226-1-2-20250410.pdf)
* Predicts a user's ikigai level
* Based on this, it recommends hobbies

### [Teachable Agent for Improving Ikigai](https://dr.ntu.edu.sg/server/api/core/bitstreams/89430d25-a913-464d-a1bc-eb9dd1bc3c2f/content)
* Predicts a user's ikigai level
* provides conversational AI agent for the elderly to help with their ikigai

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
* **Done by someone in TCD in 2024!**

### [A comparative analysis of different recommender systems for university major and career domain guidance](https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf#page=27&zoom=100,66,377)
* Didn't read, saving for later


# Areas to research in
* Scrutability, or the idea of understanding how a rec sys arrived at that particular rec
    * with **LLM's**
    * XAI might be relevant
    * also called justifiability/reasoning/interpretability, etc.
* **Guidance with a human**
    * how can the tool be used in conjunction with a human
        * this could be either a casual user (e.g. student)
        * or a professional (e.g. guidance counsellor)
* novelty in rec sys
* serendipity in rec sys
* human's preferences change over time
    * investigate the evolution of this
* bias in RS
    * course idea:
        * gender
        * social class
        * race

# TODO
https://rjwave.org/ijedr/papers/IJEDR1903111.pdf

https://www.preprints.org/frontend/manuscript/cf467753c75a6dcc24ac4aaf70ce013f/download_pub

https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=career+counseling+ai&btnG=

https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=career+counseling+machine+learning&btnG=

https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf#page=27&zoom=100,66,377

https://www.sciencedirect.com/science/article/pii/S0360131521001421?via%3Dihub