# TODO

## new approach

### cao course re-classification
- [ ] agriculture - horticulture, plants, crops, animal
- [ ] architecture & construction
- [ ] environment - sustainablity, etc.
- [ ] manufacturing & processing
- [ ] separate BHHS with personal services and welfare


- [ ] need to readjust weights
    * category weights look good imo
    * riasec interests are so overinflated
        * or maybe the question classifies them poorly, idk
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
- [ ] think about how to phrase the question:
    * e.g. `*"On a scale of 0-4, how much would you enjoy (or how interesting would you find) studying this subject at college?"*`
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
