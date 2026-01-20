# TODO

- [ ] figure out question!
    * ask donnchadh
    * ask adam and matthew
- [ ] evaluation


# Option 1

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

## Concerns or potential disadvantages
* the **and for a living** is a double-edged sword
    * it's good for people who want to create a career that is more direct from the degree
        * e.g. CS for software engineering, med for physician, etc.
    * but it's a bit ignorant of the fact that not all degrees link directly to careers
        * e.g. maths/physics then work in finance/insurance
        * e.g. psych/social science then work in HR
    * but at 17 you don't really have knowledge beyond what happens after grad, so I think "and for a living" is still a pretty good marker

```md
On a scale of 1 to 5 where 1 = Strongly Disagree and 5 = Strongly Agree, how much would you agree with the following statement?

**I would like to study this activity for a college course and for a living.**

*what about **related college course**?*
*study or do?*

*For example, if you love an activity as a hobby (e.g. Music), but do not want to study and work in that field, you should give the activity a low score (e.g. 1 or 2).*
```

# Option 2
* Sam made a good point and I agree - this does limit and reduce the nuance behind a college course decision
* it's not just something you find interesting or enjoyable
* could be because you're good at it
* or you like the status/job that comes with it, etc.
    * e.g. me with vet med
* i think option 1 is much better
```
On a scale of 1 to 5 where 1 = Hate and 5 = Love, how enjoyable or interesting would you find studying a college course that involves this activity?

For example, if you love music as a hobby, but don't want to study music at college, you should give a low score to an activity like "Compose and perform an original piece of music".
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


