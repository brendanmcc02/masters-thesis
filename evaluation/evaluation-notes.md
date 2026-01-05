# Evaluation

* the study participants will know me, in most cases, are friends with me
* this will bias their recommendations, and they will be more likely to respond positively to the recommendation ratings, because subconsciously they want my thesis results to look well
* this is where RL could come in - we could design the system so that thumbs down does not have a negative implication, you are simply telling the system **what you don't like**, which is very important in discovering what you do like
* in charu aggarwal's book, he mentions that users can make biased decisions when they are under the awareness they are being tested (chapter 7, book pg 227)

# baseline
* at first I was thinking of just doing a random course selection
    * but that's a shit baseline ngl
* a better one would just be sorted by points, which is a popularity measure (sort of)
* ~~what do we think about using ChatGPT?~~
    * I think 1 baseline is sufficient, we are already asking the users many questions and we don't want decision fatigue

# RS metrics to evaluate/measure

## Relevance
* for simplicity, I should just do binary relevance: thumbs up/down
    * anything more complicated would be unnecessary and lead to decision fatigue - don't over-engineer!

### Precision
* use **precision:** `(number of relevant items)/(total number of recommended items)`
* precision also has it's limits, because you may not have large coverage, so that's where **recall** comes in
* think about `p@5`, `p@10`, etc.

### [Recall](https://gemini.google.com/u/1/app/acae7b12e67f4cfa)
* `(number of recommended relevant items)/(all possibly relevant items)`
* the challenge is how to calculate `(all possibly relevant items)`
* one idea: ask user to pick out 10-20 (`n`) courses they would realistically consider studying
    * after generating the recs, ask the user to mark any relevant courses
    * add these unique courses to their list of `n` courses
    * this becomes your `(all possibly relevant items)`
    * I think 20 courses would be too much
        * realistically, a CAO has only 10 courses for level 8, and then another 10 for level 6/7
        * I think 10 courses might be more realistic

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

### objective measurements
* assuming we have a set of `known relevant items`, the formula is simply: `recs not in known relevant items/known relevant items`
* this doesn't take into account the **relevance** of the recommendation!
* you could have 100% novelty and rec dogshit, irrelevant courses
* that's where [serendipity](#serendipity) comes in

### subjective measurements
* ask the user to rate 1-5 (likert) on a question: `"The recommended courses were not original or novel."`

## serendipity
* novelty just measures the originality of the rec, not it's relevance/usefulness
* serendipity measures **originality and relevance**
* formula: `(recs that are not in known relevant items AND recs that are relevant)/known relevant items`

## trust
* ask the user to rate 1-5 (likert) on the following question: `"I trust that the system recommended courses that are well-suited to my interests and preferences."`
* could consider switching the question around (negatively-focused), so to ask the user if they don't trust the system

# guidance counsellors
* owen suggested using a GC, and gemini thinks so too
* but honestly, I think the profiles are such limited snapshots of people
* I'd imagine the GC's wouldn't be the biggest fan of it, because of the limited snapshot
* but maybe we could ask them to do it anyway and to be very aware of the limitations, mention it to them and in the thesis
