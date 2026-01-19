# Evaluation

* the study participants will know me, in most cases, are friends with me
* this will bias their recommendations, and they will be more likely to respond positively to the recommendation ratings, because subconsciously they want my thesis results to look well
* this is where RL could come in - we could design the system so that thumbs down does not have a negative implication, you are simply telling the system **what you don't like**, which is very important in discovering what you do like
* in charu aggarwal's book, he mentions that users can make biased decisions when they are under the awareness they are being tested (chapter 7, book pg 227)

# baseline
* sort by points
    * points is set by **demand** which is a measure of popularity
* random courses would not be an effective baseline imo
* ~~what do we think about using ChatGPT?~~
    * I think 1 baseline is sufficient, we are already asking the users many questions and we don't want decision fatigue

# [RS metrics to evaluate/measure](https://gemini.google.com/u/1/app/acae7b12e67f4cfa)

* Ask the user: `"Please list up to 10 courses that you would realistically put in your CAO Application. You can list fewer than 10 courses if you wish.`
* the user can put down identical courses, e.g. CS in TCD & CS in UCD
* apply title pre-processing and **uniqueify** the list, this becomes: `user-generated-ground-truth`
* but our RS can't recommend courses with identical titles, so:
    * for example, if a user puts down just four CS courses, and the RS recommends 1 CS course, that would be 100% recall
* If a course with an identical name but different college gets recommended, that should count as a hit in my opinion

## Relevance
* for simplicity, I should just do binary relevance:
* anything more complicated would be unnecessary and lead to decision fatigue - don't over-engineer!
* `*I would realistically consider studying this course.*` and `*I would realistically not consider studying this course.*`
    * or something else?

## Precision
* use **precision:** `(# RELEVANT recommended items)/(number-of-recommended-items)`
    * i.e. (num of relevant recs) / 10
* consider using multiple precision metrics instead of just one, e.g.:
    * `p@5`, `p@10`, etc.
* precision also has it's limits, because you may not have large coverage, so that's where **recall** comes in

## Recall
* recall should be divided by the number of ALL relevant recommendations: `all-relevant-courses`
* this is not necessarily just `user-generated-ground-truth`
    * they may get recs that they become unaware of
    * people can have tunnel-vision on a specific course/strand
* so, add any courses that the user marks as relevant to `user-generated-ground-truth` should get added to `all-relevant-courses`:
    * `all-relevant-courses = user-generated-ground-truth + relevant recs`
* **Recall formula:** `(# RELEVANT recommended courses)/(all-relevant-courses)`

### F1 Score
* could consider using f1 score to harmonise recall and precision?

## diversity

### subjective/perceived diversity
* could ask the user to rate 1-5 (likert scale) on the following question: `The courses recommended offered a diverse variety of choices (e.g. different fields of study, colleges, etc.)`
* **interesting** - gemini says that users are more likely to notice a lack of diversity, so the question should be reversed: `"The recommended courses felt too similar to one another."`

### objective diversity
* could use a word embeddings model, e.g. BERT
* and then use cosine similarity between the course titles, and that would be the "similarity_score" metric
* measure the intra-list diversity using this similarity metric
* that would be a measure of how different the courses itselves were, but diversity also includes differences in colleges, location
    * there are a few edge cases, e.g. if the person only picked one college or location, don't consider that in the metric

## novelty
* the formula is simply: `recs not in user-generated-ground-truth/number-of-recommended-courses))`
    * `number-of-recommended-courses` is **10** FYI
* note: this doesn't take into account the **relevance/usefulness** of the recommendation!
    * for example, you could have 100% novelty and rec dogshit, irrelevant courses
    * that's where [serendipity](#serendipity) comes inasurement would be better

## serendipity
* novelty just measures the originality of the rec, not it's relevance/usefulness
* serendipity measures **originality AND relevance**
* formula: `recs that are not in user-generated-ground-truth AND relevant recs) / number-of-recommended-courses`
    * `number-of-recommended-courses` is **10** FYI

## trust
* ask the user to rate 1-5 (likert) on the following question: `"I trust that the system recommended courses that are well-suited to my interests and preferences."`
* could consider switching the question around (negatively-focused), so to ask the user if they don't trust the system
* [gemini](https://gemini.google.com/u/1/app/acae7b12e67f4cfa) actually suggests keeping the question positive
    * todo figure out why idk bro

# guidance counsellors
* owen suggested using a GC, and gemini thinks so too
* but honestly, I think the profiles are such limited snapshots of people
* I'd imagine the GC's wouldn't be the biggest fan of it, because of the limited snapshot
* but maybe we could ask them to do it anyway and to be very aware of the limitations, mention it to them and in the thesis
