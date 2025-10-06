# Why doesn't a person just use ChatGPT?

* **The average person isn't surrounded by good career advice**
    * I have been surrounded by solid career advice (thx Dad) my whole life, however, that is not common.
    * as well as this, I have done weeks of rigorous academic research into this topic to figure out what is best for people.
    * not everyone will put in that kind of work - even though they rationally should, because that's something they will potentially do for the rest of their life
    * this is not just a "chatgpt wrapper" - it is informed from rigorous scientific research
* **This is research, not a business product.**
    * Doing a deep dive into the literature regarding college/career counselling, and then applying that to a domain such as Recommender Systems, is still useful and interesting as a form of research.
* **Prompt engineering is a skill**
    * Part of getting good recommendations from an LLM is knowing how to craft good prompts, and not everybody is capable of doing that frankly.
* **Serendipitiy and Novelty are key**
    * an LLM is like an echo chamber - based only on your given context (which we've already established is a skill, but also requires a lot of domain knowledge), ChatGPT will recommend courses to you
    * however, these courses will be safe, which has it's benefits
    * but, they won't recommend any novel or serendipitous recs *unless explicitly specified*
        * this also takes some domain knowledge of RS and how LLM's work, which is not known to everyone
* **Collaborative filtering can be utilised**
    * an LLM doesn't have access to a database that can be leveraged for collaborative filtering
    * however, an external, separate product to ChatGPT could have a database like this

## Gemini Prompt Examples

* [Just listing my passions in the prompt](https://gemini.google.com/u/1/app/2cc7dc441e5ecc44)
    * it recommends a bunch of film studies/arts courses
    * LLM's do what you say to them - confirmation bias
    * it didn't ask me about my skills, personalities, interest in doing meaningful/impactful work, interest in makimg money/having a career, etc.
    * these are questions that any good career counsellor would ask
    * "follow your passion" is limited, poor advice and many people are frankly unaware
* [Expertly crafted prompt, using all of my domain knowledge](https://gemini.google.com/u/1/app/5c2d3e9a8fb677b4)
    * I provided my RIASEC score, and also mentioned some personal characteristics of mine (ambitious, deeply curious, strong social skills)
    * I mentioned to only mention college courses in Dublin
    * **really good results**
    * I then probed it by mentioning I would like work that is meaningful/fulfilling, and asked it for more recs
    * Results were still solid
    * I then talked to it about **serendipitiy** and **novelty** in RS, and encouraged it to be more adventurous and risky in it's recs
        * this requires awareness gathered from my domain knowledge of RS
    * results were pretty good
    * The only limitation with this approach is that there isn't any collborative filtering, which could be leveraged by an external product
    * But if i'm being honest, if you have very good awareness/knowledge of career counselling/advice, then ChatGPT is a great solution
        * **but not everyone knows the great advice or is aware!**
* [Ask for career advice, and then based on those results, ask for course recommendations](https://gemini.google.com/u/1/app/6d57137f5e1034b6)
    * It's first recommendation was SWE lol
    * **solid results**
    * it recommends careers/courses in different categories, good for novelty and serendipity
    * then gives actionable steps:
        1. research the courses it recommended
        2. try testing out the vocation, e.g. do some coding, etc.
        3. reach out to people working in the field and see what it's really like
    * when I prompt it further for 10 courses, it's kind of only giving engineering, and CS options really, with little variation - lacking novelty and serendipity

# Guidance Counselling in Practice

## [Asking Gemini about methodology of Guidance Counselling](https://gemini.google.com/u/1/app/52f7a5c7537b50d5)

# What factors
* Skills & Personality
* Procilivity for social impact/meaning
* Interesting/engaging work
* money
    * weak correlator between money and career success
    * but it's still something people really value/want out of work
* Working with people
    * some want more, some want less
* autonomy
    * entrepeneur types want more autonomy for example
* work-life balance
* physical work environment
    * some prefer outdoors
    * other office spaces

# My Initial Thoughts

*Some of these thoughts are not backed by data - just a blend of my intuition and experience.*

* What people **want** out of a course is often not the same as what is **best** for them.
    * In this context, a good RS should recommend courses that are the intersection of **wants** and **aptitudes**
    * I would also argue that the RS should rec courses that they haven't said they wanted for **serendipity & novelty**
* What do people **want** out of a career or course?
    * **sometimes people might want different things with a career vs a course**
        * for example, people might see a course as an opportunity to explore their interests
            * more likely for someone with a higher social class/affluent background, who can afford to waste time/money
                * aka they have less financial risk tolerance
                * people from these socioeconomic backgrounds (and parents with educational backgrounds) generally tend towards careers with lower early-career earnings, but higher long-term earnings (slower, but better ROI)
            * e.g. study maths/physics at college, and then work in finance
        * and a career as something stable to make money
            * more likely for someone with a lower social class, who can't waste money or resources
                * people from these socioeconomic backgrounds generally tend towards courses with more **defined** careers, with higher early-career earnings (quicker ROI)
    * I would say that is not a popular case. If that is something the person wants, then a good RS should be able to accomodate that through natural language (e.g. Conversational RS) or other means
    * For an RS like this, you need to profile a person's interests (aptitudes), and also their **wants**
        * However, we should not only recommend courses that intersect with a person's aptitudes and their wants
            * Firstly, this would be an uninteresting RS producing non-novel results
            * But also, people often **construct their preferences** *(see preference construction)*
                * so, a course would get recommended to them that might conflict with something they thought they wanted, but from this experience they may learn that isn't something they want
            * So, recommending courses that don't align with their wants (but aligns with their aptitudes) not only is beneficial because of **serendipity and novelty**, but it may also challenge and develop a person's preferences
* How do you determine that a course or career is successful for someone?
    * I would argue this is **subjective** and it depends on what the person answered to the questions: ***"What do people want out of a course?"***
    * As I've already established, people want different things out of their course/career:
    * Back to the original question, what then are the success metrics?
        * For some people, the success metric is **money**
            * they see work as a means for living
        * for some people, the success metric is how **meaningful** their work is.
            * they want to make a difference
        * for some people, the success metric is how **passionate** they are about their work.
            * they want to do something they love
        * for some people, the success metric is a **challenging and engaging** job
            * they want to do something that they can apply their skills and grow them
    * Observe that the above four points are all present in **Ikigai**
    * It would be important for the RS to gauge **how important** each of these 4 components are to their work
    * **On second thought,** I think reducing it down to these 4 factors is **reductionisitic**
        * **Prestige** and social perception is also a factor
        * **Work/life balance** too
* **Culture** is also a major factor in course/career selection
    * for example, western attitudes will differ from eastern ones
    * when looking at academic papers, consider this bias
* Consider **survivorship bias:**
    * Not everyone goes to college
    * Not every career requires college, some might require apprenticeships
    * When you interview college students, or consider samples of college students only, remember this bias.
