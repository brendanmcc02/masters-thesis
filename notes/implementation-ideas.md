* don't aggregate the RIASEC categories - leave them as individual?
    * by aggregating them together, i'd argue some vital information is lost
* could use an ML model
    * 48 input variables, 15 categorical output variables
    * get a ranking score and normalize it
    * return top n (e.g. 3 or 5)
* replicating the open psychometrics riasec dataset would be **very easy**
    * it means I can replicate the individual category-level granularity
* by asking friends/family rn, they are just giving me an aggregated RIASEC score
    * as I said, this potentially loses a lot of valuable information

* I think aggregating the results all together into just a dataset of 15 is a bad idea
    * there is so much information being lost in that aggregation process
* and i actually have use of a large dataset (~77k entries) that could be ideal for training
    * i could even make the data more granular by using specific college majors as opposed to categories
        * i am still a bit concerned about this though, likely will be a bias towards majors with more data (e.g. psych)
        * especially compared to majors with very little data


***I will be using college major category as the output class here***
1. Answer 48 RIASEC questions
    * ML model will be trained on OpenPsychometrics dataset
        * Test the following ML models:
            1. Multinomial Naive Bayes
            2. Categorical Naive Bayes (likely worse performance but still try)
            3. Logistic regression
            4. Vectorized model with Cosine Similarity (likely worse performance, but maybe worth trying)
    * Use softmax to get class probabilities
        * try with/without normalization and see how it impacts results
2. ask for their LC subjects and how much they like/find it interesting (0 - 4)
    * this would be factored into their RIASEC
3. simplifiy the RIASEC from 8+ (including factored additional LC subjects) dimensions per RIASEC category to one number
    * in other words, 48+ goes down to 6 dimensions, where each represents a holland taxonomy: RIASEC
    * try with/without normalization and see how it impacts results
    * I feel like normalizing would inflate percentage matches, e.g. if you answered really low to everything on the OP quiz, that should be reflected in the percentage matching
        * so i don't think it should be normalized, but try it anyway
4. ask the person for their expected LC points
5. represent each college course as a vector: `[R, I, A, S, E, C, points, category_0, ..., category_14]`
6. represent the person as a vector: `[R, I, A, S, E, C, points, category_0, ..., category_14]`
7. cosine similarity, return the top matches
8. Ask an LLM to explain/justify the suggestions
