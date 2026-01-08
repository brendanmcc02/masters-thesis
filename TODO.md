# TODO

- [ ] create social work/youth work?
    * communication disorders, etc
- [ ] create psychology category? separate from social science?
    * social science has good accuracy for correct predictions, but awful mis-predicts quite often
    * how can we resolve this?
    * what if i downsample psych?
- [ ] when clustering/masking categories, also cluster/mask their relevant interests
- [ ] think about points
    * should we even recommend courses outside a points range? aysha got recommended a 370 point course despite having 625
        * findmycollegecourse actually has a point range preference - should we add this as a preference too?
    * should the points dimension be a number between 0 and 625? instead of 0-1.0?
    * or do we remove the points dimension entirely, calculate the cosine sim, then multiply it by a normalised points difference value?
- [ ] do I actually have to recommend 10 courses?
    * can I recommend more?
    * think again about the implications for evaluation
- [ ] think about "joint honours" / "arts" courses with multi-options, can I deal with them in a smarter way?
    * or at the very least, review their RIASEC and categories, I'm a bit sus
- [ ] think about how to phrase LC subject question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) studying this subject at college?"*`
- [ ] think about how to phrase RIASEC question:
    * e.g. `"On a scale of 0-4, how much would you enjoy (or how interesting would you find) doing these activities as part of a college course?"`
    * **note:** there is a discrepancy here, because the original dataset was trained on the question: *"on a 1-5 scale of how much they would like to perform that task"*
- [ ] create a usable interface

```
* social work/youth development etc is healthcare
    * there are a lot of social work-related questions, I think the model could do a good job of predicting this & differentiating from med, nursing, etc.
* create a languages category?
    * humanities feels way too broad
    * you have to consider there are 1-2 languages in the LC too, so there will be a good bit of data on this
    * lots of courses have languages as an option, so this could really make sense actually
    * e.g. if they love computers and german, german + cs would get recommended
    * i would have to check the dataset pre-processing again tbh
    * no similarly-worded question from the 48Q dataset, but there are humanity-related questions
    * ngl LC subjects are the banker for this
* psychology category?
    * a lot of similarities with social science
    * but it does have a bit more bio focus e.g. neuroscience, biological factors behind human behaviour and the mind
```

Analysis of the dataset:

Poor performance on:
* foreign languages
    * but there are LC subjects to compensate for this, so I don't think it's a huge issue
* law
    * 3 LC subjects on it - business, politics and climate action
    * so this can compensate for it
* physical science
    * not the best, but that's because there are no physical science questions
    * but LC subjects compensate for this
* solid accuracy on social science
    * but it also predicts other categories **a lot**
    * I wonder if doing some adjustments here could drastically improve model performance?
        * e.g. downsampling


Social Science:

* theoretical social science: interest in human behaviour - mostly 'I' and 'A':
    * psych - could downsample this?
    * econ
    * sociology
    * geography
* applied social science - mostly 'R' and 'S':
    * counseling
    * social work
    * rehabilitation
