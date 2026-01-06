# TODO

- [ ] test on different local profiles
- [x] test on aysha
    * should we even recommend courses outside a points range? she got recommended a 370 point course despite having 625
    * should the points dimension be a number between 0 and 625? instead of 0-1.0?
    * or do we remove the points dimension entirely, calculate the cosine sim, then multiply it by a normalised points difference value?
- [ ] think about how to phrase LC subject question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) studying this subject at college?"*`
- [ ] think about how to phrase RIASEC question:
    * e.g. `"On a scale of 0-4, how much would you enjoy (or how interesting would you find) doing these activities as part of a college course?"`
    * **note:** there is a discrepancy here, because the original dataset was trained on the question: *"on a 1-5 scale of how much they would like to perform that task"*
- [ ] create a usable interface
