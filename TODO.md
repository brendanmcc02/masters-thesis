# TODO

- [ ] when clustering/masking categories, also cluster/mask their relevant interests
    * don't cluster for:
        1. education
        2. languages
- [ ] how many courses are being recommended?
- [ ] limit number of recs for different categories?
    * e.g. architecture 3, maths 3?
    * it depends how many courses get recommended though so idk
- [ ] what about masking adjacent categories?
- [ ] is it necessary to distribute the weight for multi-category courses?
- [ ] think about points
    * should we even recommend courses outside a points range? aysha got recommended a 370 point course despite having 625
        * findmycollegecourse actually has a point range preference - should we add this as a preference too?
    * should the points dimension be a number between 0 and 625? instead of 0-1.0?
    * or do we remove the points dimension entirely, calculate the cosine sim, then multiply it by a normalised points difference value?
- [ ] think about "joint honours" / "arts" courses with multi-options, can I deal with them in a smarter way?
    * or at the very least, review their RIASEC and categories, I'm a bit sus
    * there's also some "heritage" course
    * also `*science - *`* UCD courses there are loads!
    * general science courses
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
