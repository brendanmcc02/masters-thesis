# TODO

- [ ] instead of relying on Gemini for categories, try to capture the bulk of it by using the same logic as in categorizing the OP data
    * more consistency
    * but then again it does a really good job ngl
    * my approach categorises courses into one category, but in most cases they can be multiple, e.g. medicine is healthcare & life science
- [ ] figure out courses with portfolios
    * or maybe just don't filter them out no matter what points the person puts?
        * if points > 625, then set points = 625
- [ ] make all healthcare courses life science too? realistically, you'd have to study life science in the course so?
- [ ] more sophisticated duplicate removal -> consider substring matches with tokens
- [ ] find out the model's accuracy for each college major category - analyse the results - might need a confusion matrix or some shi idk bro
