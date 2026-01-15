# TODO

- [ ] when masking categories, also mask their relevant interests
    * don't cluster for:
        1. education
        2. languages
- [ ] what about masking adjacent categories?
- [ ] is it necessary to distribute the weight for multi-category/interest courses?
- [ ] how many courses are being recommended?
    * I think 20 (5 categories and 4 courses each) is really solid
- [ ] what should happen if recs get exhausted for a category?
    * add them to "reserves", then do a 6th category
- [ ] think about points
    * should we even recommend courses outside a points range? aysha got recommended a 370 point course despite having 625
        * findmycollegecourse actually has a point range preference - should we add this as a preference too?
    * should the points dimension be a number between 0 and 625? instead of 0-1.0?
    * or do we remove the points dimension entirely, calculate the cosine sim, then multiply it by a normalised points difference value?
- [ ] think about how to phrase the question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) doing this activity for work or study?"*`
        * I actually think this might not be a good idea, a 17 year-old might have no idea what they'd like doing in a work or study context
        * this is best used as an exploratory tool, before they have a lot of knowledge in many things
- [ ] create a usable interface
- [ ] ~~work with only level 8?~~
    * might not be worth it anymore ngl, idk
- [ ] ~~work with only dublin courses?~~
    * might not be worth it anymore ngl, idk
    * PoC?

```
my 2020 CAO:

check email!
?
tcd cs
ucd cs
tud cs
tcd math
tcd tp
actuarial and finance
msiss
```
