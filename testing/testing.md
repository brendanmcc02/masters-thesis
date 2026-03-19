- [x] Declan
    * did it with substring match
    * could generate recs md again and ask him to do part-2-survey?
    * did it with similarity scores visible on set 2 - would definitely affect the trust metric
    * did it with equal number of recs per category as opposed to proportional to their interests
    * downside with this is that they both know how set 2's algorithm works
    * **re-generated recs and asked him to re-do part 2!**
- [x] Tom Gilbride
    * did it with substring match
    * did it with similarity scores visible on set 2 - would definitely affect the trust metric
    * did it with equal number of recs per category as opposed to proportional to their interests
    * could generate recs md again and ask him to do part-2-survey?
    * downside with this is that they both know how set 2's algorithm works
- [x] Brendan #McCann
- [x] Sam Taylor
    * did it with similarity scores visible on set 2 - would definitely affect the trust metric
        * he said the similarity score might have affected trust values
    * did it with baseline being sorted by points as opposed to cosine similarity
        * I think this would have effected his overall trust in set 2
    * not worth asking him to re-evaluate trust again imo, he would know which set is which
- [x] Sean Somers
    * did it with baseline sorted by cosine similarity as opposed to points
- [x] lalith
    * didn't rec law despite liking law category
    * did it with baseline sorted by cosine similarity as opposed to points
    * **I re-did some law & chem riasec interests, could ask him again!** 
    * scored >0.9 in like 7 categories, pretty extreme case of having **a lot** of interests
    * as a result, found the baseline to be very effective, also because of the high point courses and being ambitious
    * could talk about points as a bias
    * **re-generated recs and asked him to re-do part 2!**
- [x] Aysha
    * did it with baseline sorted by cosine similarity as opposed to points
- [x] Cian Moriarty
    * did it with baseline sorted by points (back to normal)
    * i don't think sorting baseline by relevance is a representative baseline because the relevance measurement is not super objective and is subject to my algorithm, a baseline by nature should be objective and standardised across different algorithms and approaches
- [x] Liam Murphy
- [x] Jake
- [x] Daniel Farushev
    * almost all CS + eng (i think)
    * interesting case of limited interests, good that I did recs proportionately to category interests as opposed to just top 5 categories + 5 recs each
- [x] Mauv
    * first person to use a baseline with only <=625 courses
    * he suggested adding "as a living" to each question because as time went on he forgot it was "for a living" and not as interest
        * as a result, I added the statemnet "as a living" to each question, also as a reminder
        * i found myself forgetting it too, and falling into the trap of "ooh, this is cool" and forgetting it's for a living and not recreational interests
- [x] Ramy
- [x] Mahir
- [x] Doill
    * lots of interests, preferred baseline
    * similar case to lalith - the "trend" (sample size of 2 so not statistically significant at all yet) is that if you have a diverse variety of interests, you may prefer the baseline because it's complete lack of pattern - it's just high points courses
- [x] Conal
- [ ] Oscar
    * not organized
- [x] Vivi
- [x] Aaron
- [x] Muneeb
    * he responded positively to the social science/education questions in the context of med
    * social science is relevant to med
    * this kind of nuance is incredibly difficult to capture to be honest
        * if anything, I think it's good the system was "simplistic" because a psych course could be a good suggestion for him, in his case though he wasn't interested
- [ ] Kash
    * not organized
- [x] Cian Tracey
    * first and only humanities person
    * said that there were still many questions that were tailored to him, so there wasn't any notion of exclusion
- [x] Grainne
    * got a lot of nursing recs - quite expected given her interest towards healthcare
    * she herself was more thinking animal science though
    * the education courses were a result of high quiz results, but when I asked her she said she wouldn't actually consider doing it as a course
        * once again, another case of people answering the question relatively "recreationall" as opposed to thinking about the college course
        * perhaps this isn't purely down to human error? maybe the question could be phrased better
        * e.g. `I would like to study this activity as part of a college course"`
- [x] Matthew
    * the question phrasing: ditto comments for adam
    * gave equal trust score to both sets - maths courses in set 1 reduced his trust - stragglers on bottom of list - could consider a threshold for recommending?
    * there were some courses he couldn't take because of subjects - he doesn't do a science
        * subject requirements - something to implement if more time, couldn't implement because of time limitations and excessive manual labour
- [x] Adam
    * liked the questions and the focus on jobs ("as a living") as opposed to recreational interests
        * he thought this was good because it's more reflective of what a career quiz should be: match career interests, not hobbies
    * he liked how the questions were more focused and particular, as opposed to general, vague interests
    * compared to the previous OP quiz where it felt more focused on interests
    * he responded positively to one question about economics: "Analyze how rising prices change the way people spend money", which is classed under social science
        * the algorithm recommended sociology as a result of this, and it was his number 1 category so that really threw him off
    * should probably create new categories for "economics" and "psychology" from social science?
- [x] Ben Hennessy
    * felt some of the questions were repetitive, "felt like he was answering the same things a few times"
- [x] Kevin
- [ ] Alex
    * travelling to germany this week
- [x] Mati
    * speaking foreign language question doesn't really make sense in context to "i would like to do this for a living"
    * otherwise he thought phrasing of "i would like to do this for a living" was pretty straightfoward and made sense
- [x] Beth
    * thought many of the questions were CS/science based
    * thought there could be more humanities questions
    * felt she was answering to very few questions
- [x] kaden
    * thought the phrasing was good, leaned towards "livign" as opposed to recreation
    * courses were very strained due to his points being too low - ~300 points, and put down TCD, UCD, UCC, GY, etc.
    * some awful recs tbh due to above reasons
    * could consider asking him to re-do colleges & nfq levels? then re-evaluate?
    * part 1 timetstamp is `12/02/2026 17:21:53`
    * part 2 timestamp is `12/02/2026 17:37:09`
- [ ] Dillon
- [x] michael connolly
    * responded postiively to the communications questions despite being well aware of "I'd like to do this for a living"
    * when i asked him if he would like to do journalism to study, he said no
    * i found this quite contradictory to be honest, it's a good demonstration of human inconsistency
    * i myself was guilty of this, I put down chemical science + life science, but then when I thought about it I wasn't sure if I'd study bio/chem
- [ ] rob
- [x] hugh finnegan
    * he picked questions knowing if they made money
        * good demonstration of putting power into the hands of the user
        * at the end of the day, it's their recs and their choices, and the RS should serve that and it shoudln't work "against" the user
        * this kind of thinking was a bit more common amongst CS people, who had a greater general understanding of how rec algorithms work, so they could kind of "game" the system and tune the RS to what they wanted
    * mentioned an interesting point - people have an interesting relationship to points
    * he said that in some of the questions he did not demonstrate an interest in a particular category, e.g. law
    * but then when he saw the law course and the high points associated with it, he changed his mind towards the course and grew more interested in it
        * just for the sake of course status (trinity law, also high points = smart)
        * also for the status of the job (lawyer)
        * also for money
    * good demonstration of human inconsitency/changeability, but also the role of status/internal drivers towards certain courses, often independent of interests
        * interestingly, a person **can** learn the skills in a course and humans are adaptable, so even if you don't demonstrate an interest in the field, it can grow
            * cite carol dweck's passion-learning study!
