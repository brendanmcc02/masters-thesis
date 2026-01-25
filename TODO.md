# TODO

- [ ] evaluation metrics
- [ ] **ask owen** - can i recommend 30 courses?
- [ ] who is the second reader

## Advantages
* "like" is very subjective, and that's intentional - this puts it in the hands of the user
* they may like the activity because it's:
    * enjoyable
    * makes money
    * respectable activity (status)
    * interesting/engaging
    * meaningful/socially impactful
    * good work/life balance
    * they're good at it

```
On a scale of 1 to 5 where 1 = Strongly Disagree and 5 = Strongly Agree, how much would you agree with the following statement?

**I would like to do this activity for a living.**

*For example, if you love an activity as a hobby (e.g. Music), but do not want to work in that field, you should give the activity a low score (e.g. 1 or 2).*
```

# Google Form
## CAO options
* free-form paragraph text in the format of CAO email:
```
1.  TR033 Computer Science
2.  DN201 Computer Science (Common Entry)
etc.
```

## Quiz itself
* Google forms can shuffle questions
    * need to ensure it only shuffles quiz questions! Not trust/other shit
* saves to google sheets
    * column headers are the question itself
    * could link these with `user_interest_questions.csv`
    * just gotta be careful of DRY

## Show Recommendations
* Could run it locally, then send a screenshot?
    * baseline and actual recs should be mixed (i.e. random between set A and B)
    * need to generate a decent looking interface
        * console? make it look as nice as possible
        * or tkinter
* ask the user to mark relevant courses
    * how do I phrase the question?
    * **I would realistically consider studying this course.**
    ```
    * TR033 Computer Science
    * TR032 Mathematics
    ```
* save the results to a separate .csv file with the recs appended
    * get the timestamp value and use that as a user id

## Evaluation Questions
* Perceived/subjective Diversity x2 for recs A and B
* Perceived/subjective Trust x2 for recs A and B
