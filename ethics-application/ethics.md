# Questions
* Do I need a consent form?
    * my guess is yes?
* am i processing personal data for participant recruitment?
    * i.e. consent form
    * i guess i am?

# [Ethics Approval](https://www.tcd.ie/research/support/ethics-approval.php)
* [Project Methods recording (last year)](https://eu-lti.bbcollab.com/recording/08fbda64b5bd47ee9f0609745816f7db)


# [TCD Policy on Good Research Practice](https://www.tcd.ie/media/tcd/about/policies/pdfs/Policy-on-Good-Research-Practice_1.1.pdf)
* Parental/guardian consent is required if a participant in a study is under 18
* RIASEC data surely wouldn't be considered sensitive data right?
    * but if we have an LLM integration, the user could prompt about their desires/family wishes, which may be sensitive i guess?

## Risk level of applications - Human Research
1. Very low likelihood
    * **cannot involve children**
    * my project would involve personal data (RIASEC), so **it gets automatically to level 2 or 3**
2. Relatively low likelihood, i.e. research carrying little or no risks or
discomfort to a human participant greater than usually encountered during
normal daily life;
    * **cannot involve children**
    * If I don't involve children, I think it might be possible to get this?
3. Moderate and high likelihood: research risk or discomfort is greater than that usually encountered during normal daily life. This also usually includes research on intrusive personal or sensitive topics  and with populations at risk of vulnerability
    * the only two things that could raise my claim to level 3:
        1. Research where information obtained may have legal, economic or social consequences for  research. participants or their establishments.
            * kind of fuzzy imo, I guess in a round-about way it technically could? but that's very far fetched
                * e.g. push arts courses that do not promise good economic futures
        2. if it involves children, it's automatically level 3
        3. intrusive topics
            * I doubt school subjects/RIASEC would be sensitive or the thought of what you study in the future is sensitive
                * for examples, they say: *"abortion, abuse, bankruptcy, bullying, child abuse, gun  control, self-harm, trauma or whistleblowing."*
    * if participants get paid (over and above token gestures and expenses) - see [gift voucher policy](https://www.tcd.ie/about/policies/assets/pdf/Gift-Voucher-Policy.pdf)

## Data
* [Research Data Storage](https://www.tcd.ie/itservices/working-remotely/research-data/)
* There's quite a few things here regarding the storage of research data
* I didn't read it in depth because it's not relevant **atm**, but may be relevant later, just a heads-up

# [REAMS Background manual](https://www.tcd.ie/research/support/assets/pdf/REAMs%20Background%20Manual%20311024.pdf)
* If the project involves humans, I will have to complete a [Data protection training module](https://www.tcd.ie/itservices/vle/kb/overview-GDPRtraining.php) before submission is permitted
* If you want to recruit Trinity staff/students as participants in your study, then look [here](https://www.tcd.ie/communications/what-we-do--/internal-communications/email-protocol-for-staff-and-student-emails/)

# Data Protection Office (DPO)
* Before/during (idk) making an application to REAMS, you have to answer a form for the DPO
* If you answer yes to any of the [trigger questions](https://www.tcd.ie/dataprotection/assets/202310_DPO_REAMS_reviews.pdf), it will be sent to the DPO for review
* **if the study involves children, it will be sent to the DPO for review (trigger question 4)**
* if your study has >100 participants, it will be sent to the DPO for review

# Questions

* You do not need ethical approval when your research utilises pre-existing datasets
    * In my case, my RS will be built and trained using pre-existing datasets, not any input data
* *but,* I will need some people to **evaluate** my model, which would need ethics approval I'd say (and according to Owen too)
* The exception of course is if the data is **illegally obtained**
    * web scraping is legal
        * so that's not an illegal way of obtaining the data, so it technically follows from the definition
        * but what you do with the data afterwards may be illegal
    * if I were to make this a commercial product, that would be illegal
        * like Owen said in week 1/2
    * but would it be illegal for research?
        * according to Owen, he is ok with it
    * from the [background REAMS manual:](https://www.tcd.ie/research/support/assets/pdf/REAMs%20Background%20Manual%20311024.pdf) *"Overtly public data can be obtained directly, without permission or licence"*
        * they said the risk is low, but still would be assessed in ethics approval

# Owen's Thoughts
* We could circumvent the children thing by using guidance counsellors (e.g. from CBS) as our main evaluator
    * generate student profile's using LLM's, and from that generate some results
    * and then the guidance counsellor could give their opinion
    * imo this is very limited testing and I think it would have skewed results
* another suggestion he had weeks ago was to use adults, and ask them to role play as their 17-year old selves, and then use the product
    * they evaluate courses themselves
    * I think this is quite solid and better, not perfect, but still decent
    * some flaws with this is that if they are currently studying a STEM subject for the last few years (and they are 23), this might've pushed them towards typical STEM qualities, which would potentially skew results
        * but we could remark this as a limitation

# Risks
* Owen has concerns about potential risks, and I do agree there is a form of risk
* however, i'd classify the risk as low (REAMS will ask you to classifiy it as low-medium-high)