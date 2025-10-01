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

# Gemini Prompt Examples

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
    * it's kind of only giving engineering, and CS options really, with little variation
