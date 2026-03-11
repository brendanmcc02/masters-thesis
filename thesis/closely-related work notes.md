# closely-related work notes

## simple tech
* careersportal
    * take quiz
    * filter college courses by preferences
        * college location
        * career interests + sector

* qualifax
    * can filter courses by career sector

### limitations
* still choice overload, not pruned results
* no sense of personalisation or tailored recommendations
* essentially just a glorified course search, rather than personalisation

## college course quizzes

* [meetyourclass](https://www.meetyourclass.com/what-should-i-major-in)
    * 15 questions: interests and goals and work preferences (e.g. work alone, etc.)
    * personality type and personal preferences
        * study habits, mbti, hobbies
        * a loooot of info here that is frankly not relevant
    * more general college majors as opposed to specific college courses
    * not a lot of questions being asked

* [superprof](https://www.superprof.com/blog/college-major-quiz/)
    * 10 questions, not exhaustive at all
    * recommends general areas of study (e.g. stem, social sciences)
    * doesn't really narrow choice beyond that, limiting

* [anderson.edu](https://anderson.edu/persona-quiz/)
    * 25 questions
    * keep in mind this is a college as opposed to a neutral 3rd party
    * clusters you into 8 archetypes
    * college majors are then put into these 8 archetypes (e.g. game changer, investigator, etc.)

* [marquette.edu](https://www.marquette.edu/academics/majors/choose-your-major/)
    * 10 questions
    * clusters you into archetypes
    * college majors are then put into these archetypes (e.g. communicator - english, languages, etc.)

### limitations
* many of the questions feel a bit irrelevant or just noisy
    * e.g. meetyourclass asking about greek life preferences, party life, studying in a room or on campus
    * we want our RS to be grounded in the literature - proving the utility of our background review
* the quizzes are short, and this lack a sense of exhaustiveness
    * pretty crazy considering this is a big decision and has a lot of impact on your life, as outlined in the intro motivation
* they recommend very general areas of study, often lacking specificity
    * also so many new courses are being added every year (i think it was 50 new courses in 2025 or something)
    * and these recommend very generic college majors/study e.g. math, psych as opposed to specific courses
* naturally, college courses are very country-specific, and this research focuses on ireland, so are there any college quizzes based on ireland?
    * segue to FMCC!

### [FMCC](https://findmycollegecourse.ie/)
* mention that to the best of our knowledge, this is the only quiz/RS in ireland for college courses

# RS

outside of the irish scope, we will examine other college/career RS's in the literature

## [1](https://www.preprints.org/frontend/manuscript/cf467753c75a6dcc24ac4aaf70ce013f/download_pub)
* analysis of college course/career technologies being used in career counseling
* they talk about a few ethical concerns that may be good to mention
    * e.g. data privacy
    * bias in recommendations
* ngl otherwise not greeeat paper

## [A comparative analysis of different recommender systems for university major and career domain guidance](https://link.springer.com/content/pdf/10.1007/s10639-022-11541-3.pdf)
* compare a bunch of different RS approaches to college course recs:
    * CBF
    * CF
    * KB with case-based reasoning
    * Demographic
* According to their work, a **hybrid RS with CBF and KB (supported by Case-Based Reasoning and Ontology) yielded the best results.**

## [PCRS: Personalized Career-Path Recommender System for Engineering Students](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9268112)
* They profile the following info off students:
     1. personal interests (hobbies)
     3. academic scores 
     4. personality type (they use MBTI).
     5. gender (wouldn't agree with this personally)
* for eng students

## [Envisioning Tomorrow: AI Powered Career Counseling](https://ieeexplore.ieee.org/abstract/document/10426016)
* They profile student's:
    1. Grades
    2. Extracurriculars
    * and based off that, they recommend courses
    * very limited profiling imo
* hybrid CF + CBF
* they use adaboost

## [A Novel Approach for Better Career Counselling Utilizing Machine Learning Techniques](/literature-review/papers/s11277-024-11612-3.pdf)
* They test various ML techniques:
    * Random Forest, SVM, Naive Bayes, KNN, etc.
* RF had the best accuracy
* The profile student's:
    1. hobbies
    2. grades
    3. interests (what exactly, idk)
    4. achievements

### limitations
* questions asked are not so relevant or grounded in literature
    * e.g. grades being a limited view of a person
        * talk about how at least in ireland, alongside irish + english + maths, students pick at least 4 subjects, they may have an interest in something beyond these subjects and the LC list is by no means exhaustive
* once again, not for irish context which is what we are looking for

# research gap
* irish context
* questions that are relevant and grounded in literature
