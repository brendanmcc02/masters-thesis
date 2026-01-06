# TODO

- [ ] test on different local profiles
- [x] test on aysha
- [x] test on vivi
    * good results, really happy tbh
- [ ] test on adam
- [ ] test on matthew
- [ ] revisit "hospitality"
    * I don't think gemini understood it in the same way as the courses are categorised
    * do we get rid of it? or create a different category?
- [ ] think about points
    * should we even recommend courses outside a points range? aysha got recommended a 370 point course despite having 625
        * findmycollegecourse actually has a point range preference - should we add this as a preference too?
    * should the points dimension be a number between 0 and 625? instead of 0-1.0?
    * or do we remove the points dimension entirely, calculate the cosine sim, then multiply it by a normalised points difference value?
- [ ] do I actually have to recommend 10 courses?
    * can I recommend more?
    * think again about evaluation
- [ ] think about "joint honours" / "arts" courses with multi-options, can I deal with them in a smarter way?
    * or at the very least, review their RIASEC and categories, I'm a bit sus
- [ ] think about how to phrase LC subject question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) studying this subject at college?"*`
- [ ] think about how to phrase RIASEC question:
    * e.g. `"On a scale of 0-4, how much would you enjoy (or how interesting would you find) doing these activities as part of a college course?"`
    * **note:** there is a discrepancy here, because the original dataset was trained on the question: *"on a 1-5 scale of how much they would like to perform that task"*
- [ ] create a usable interface
