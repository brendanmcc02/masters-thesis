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

### Precision
* for simplicity I could just do binary relevance: thumbs up/down
* use **precision:** `(number of relevant items)/(total number of recommended items)`
* precision also has it's limits, because you may not have large coverage, so that's where **recall** comes in

### [Recall](https://gemini.google.com/u/1/app/acae7b12e67f4cfa)
* `(number of recommended relevant items)/(all possibly relevant items)`
* the challenge is how to calculate `(all possibly relevant items)`
* gemini has a few suggestions:
    
    1. ask user to pick out 5-20 (leaning towards 20) courses they would realistically consider studying
        * this would not be factored in by the RS in making the recs ofc, just for evaluation
        * after generating the recs, ask the user to mark any relevant courses
        * add these unique courses to their list of 10 courses
        * this becomes your `(all possibly relevant items)`
        * very limited though because it's not considering many courses that could be rated highly by them
    2. ask the user to pick out every course they would realistically consider studying
        * the downside is the time and effort for the participant - cognitive overload, decision fatigue
        * but this would generate a pretty solid ground truth
        * you can really try to mitigate this task by having filters by points, nfq level, location, colleges
        * when I applied my own filters (points, nfq level, location, colleges), it trimmed the list down to 434 courses
    3. **alternative to 2:** 
        * ask the user to pick out 25-50 courses they would be interested in studying
        * this can be our `(all possibly relevant items)`
        * it's worth noting this is not an incredibly objective metric, because it's a list of **known relevant items**
    4. ask a GC
        * I don't like this idea
        * firstly because of what I already mentioned - a GC has such a limited snapshot of a person
        * the person itself would generate a better ground truth as opposed to a GC who doesn't even know them and only has access to a limited snapshot
        * it's also time-consuming for them

## diversity

### subjective/perceived diversity
* could ask the user to rate 1-5 (likert scale) on the following question: `The courses recommended offered a diverse variety of choices (e.g. different fields of study, colleges, etc.)`
* **interesting** - gemini says that users are more likely to notice a lack of diversity, so the question should be reversed: `"The recommended courses felt too similar to one another."`

### objective diversity
* could use a word embeddings model, e.g. BERT
* and then use cosine similarity between the course titles, and that would be the "similarity" metric
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
