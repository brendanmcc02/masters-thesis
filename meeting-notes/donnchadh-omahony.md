# the website
* he doesn't do holland codes, he created his own vocational interest quiz
* tries to replicate what he does in a 1:1 session
* rather than using holland's taxonomy, he uses cao's categorization
categorized by how cao does it -> todo?

# these filter the recs
the website will ask:
* what lc subjects they are taking
* what grades they expect to get in each subject
* points category (500-600, 400-500, etc.)
* if they have an irish exemption
* where you'd like to study
* private college
* nfq level

# practical use with real guidance counsellors
* he mentioned that a lot of their work now is counse*lling as opposed to course counselling
* **this product could help off-load work and give a head-start**
* they created a dashboard so real guidance counsellors can use it and see the student's results before they walk into a session

# aptitude tests
* aptitude tests -> most do cat4, dats is redundant he says
    * he says to double check if dats is redundant
* cat is english company
* he often goes back on to cat4 for people who score very high (e.g. 625)
* 1 student scored below average on cat but got 625
    * goes to show it can be very limiting, 

# what he does in a guidance counselling session
* first asks what subjects are they doing -> at what level
    * he says right away this can filter many, many courses
    * e.g. if they don't do a science/language
* what is your fav/least fav subject and why??
* the key thing he looks out for is what the student is **passionate** about

* **personality tests** - he doesn't use ocean at all -> in college he was told they were for over-18s

# limitations & frustrations with findmycollegecourse.ie
* as a guidance counsellor he would like to oversee it, as in:
    * if he could actually see their body language when answering certain questions
    * find out what question they struggled with or took a long time to answer
    * he says this can tell you a lot
* you can't do the interest test more than once
    * practical reason so you can't share it with all of your friends
    * but can change points, filters, location, etc.
* the pain of admin -> new courses, changing points, requirements, etc.
    * that's a headache
    * this seems like a product problem as opposed to a research problem
* he isn't so happy with the chatbot
    * his main issue is the wrong information
    * risk with hallucination, risk with reputation
* that's his only issue with the chatbot, satisfied with everything else
    * 3-6 second response

# the technical implementation
* *keep in mind he does not have a technical background*
* he says it's mostly filtering/process of elimination
    * doesn't really seem complex at all, seems quite basic
* if you score over 60% in a category (e.g. engineering), it will rec courses in that category, otherwise it won't
* he has an ai chatbot integrated into the website
    * he scraped info off course websites, and cao points
    * you can also have a guidance counselling discussion with it
        * e.g. "i like maths, what courses can you recommend"
        * he said he was quite happy with it, so I'd be interested to learn more
        * it has the text to speech capability, can speak into it, etc.
* there are some course edge cases
    * e.g. arts in maynooth covers a bunch of sciences, arts and humanities
        * can't really categorize it effectively
    * this shouldn't be a problem because careers portal (aka my dataset) sub-categorizes maynooth arts
        * e.g. `Arts - Computer Science` and `Arts - Accounting`

