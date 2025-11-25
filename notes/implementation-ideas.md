# End-to-End idea v1
*I will be using college major category as the output class here*
1. Answer 48 RIASEC questions
    * ML model will be trained on OpenPsychometrics dataset
        * Test the following ML models:
            1. Multinomial Naive Bayes
            2. Categorical Naive Bayes (likely worse performance but still try)
            3. Logistic regression
    * Use softmax to get class probabilities, then normalize the class probabilities
2. ask for their LC subjects and how much they like/find it interesting (0 - 4)
    * this would be factored into their RIASEC
3. simplifiy the RIASEC from 8+ (including factored additional LC subjects) dimensions per RIASEC category to one number
    * in other words, 48+ goes down to 6 dimensions, where each represents a holland taxonomy: RIASEC
        * try with/without normalization and see how it impacts results
        * I feel like normalizing would inflate percentage matches, e.g. if you answered really low to everything on the OP quiz, that should be reflected in the percentage matching
        * so i don't think it should be normalized, but try it anyway
4. ask the person for their expected LC points
    * test with/without points, does it improve results?
5. ask for:
    1. nfq levels
    2. if they're preparing a portfolio, test (e.g. HPAT) or interview
    3. college location preferences
    * filter out courses that don't match them
6. represent each college course as a vector: `[R, I, A, S, E, C, points, category_0, ..., category_14]`
7. represent the person as a vector: `[R, I, A, S, E, C, points, category_0, ..., category_14]`
8. cosine similarity, return the top matches
9. Ask an LLM to explain/justify the suggestions
