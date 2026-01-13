# TODO

## new approach

### cao course re-classification
- [ ] revise the gemini questions, i think some of them have different intentions or ideas of what kinds of courses or qualities their looking for
    * e.g. "environment" should reflect the social policy/sustainability focus, and also the climate/env eng/science investigative part
    * similar with agriculture

- [ ] work with only level 8?
- [ ] work with only dublin courses?
    * PoC?
- [ ] need to readjust weights
    * category weights look good imo
    * riasec interests are quite overinflated
        * or maybe the question classifies them poorly, idk
- [ ] when clustering/masking categories, also cluster/mask their relevant interests
    * don't cluster for:
        1. education
        2. languages
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
    * there's also some "heritage" course
    * also `*science - *`* UCD courses there are loads!
    * general science courses
- [ ] think about how to phrase the question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) doing this activity for work or study?"*`

- [ ] create a usable interface

```
my 10 UNIQUE courses:

tcd cs
tcd math
ucd econ fi
tcd tp
tcd dent
rcsi med
ucd vet med
ucd arch
tcd psych
ucd actuarial financial studies

my 2026 CAO:
tcd cs
ucd cs

my 2020 CAO:
tcd cs
ucd cs
tud cs
```


sustainability - social science/law


my problem is that "environment" is really broad - it could be social policy/advocate focused (social science/law), or scientific (e.g. env eng/sci)
i guess i could merge it with the relevant category, that's what i did with agri anyways (e.g. agri + science, agri + business)