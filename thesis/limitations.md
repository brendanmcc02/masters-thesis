# limitations - implementation
* some colleges (e.g. UCD) have language requirements - my RS doesn't take that into account
* most subjects have subject or grade requirements - my RS doesn't take that into account
* languages maybe should be specific to a language - e.g. getting recommended Polish if you studied German
    * would probably need some edge case or additional quiz
    * e.g. if "languages" is in your top-5, then you should tick off which languages you would be interested in studying


# findings from experiment
* humanities, creative arts, social science are very broad and could be narrowed down
* the RS could have a feedback loop, where the user is prompted again if they want to change their college course course
    * e.g. declan only putting down tcd, ucd when he actually got recommended a lot of arts courses, could have benefitted from BIMM, IADT, etc.
        * e.g. me wanting education but not doing dcu/marino/
    * there are a looot of colleges and people are frankly unaware of what they do
    * maybe the RS should run on all colleges (no filter, despite what the user puts down)- and if there are courses being recommended for those colleges, the system could ask the user: "hey, we got some course suggestions from these colleges because you scored highly in these areas, would you like to include these colleges in your final recommendation list?
        * **when running test with doill he talked about this, mention it!!!**
    * but it's a trade-off: if you over-engineer the system with feedback you can make the user drop out of the system - owen's advice
* cater the number of recs to the persons interests - someone like daniel farushev who basically only expressed interest in computers (0.93), and eng (0.3), then everything else was either 0.0 or 0.05
    * 20 is a bit excessive in this case
* and then compare this to someone like lalith who scored >0.9 in like 7 categories


# future work
