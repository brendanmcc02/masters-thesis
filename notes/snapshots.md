# Snapshots

A thesis is over 8 months. During that time, there will be an immense evolution into my thinking, and in this document, I will attempt to document this. I am only starting this in mid-November, so before that it may not be entirely accurate, but I will do my best

# September

Dove into literature and got exposed to the many facets and influences that go into choosing a college.

There are a lot of practical limitations as to choosing the college itself, which of course has an influence on the course you choose.
Prestige of the college is also a factor - reputation.
Also if your parents are alumni, or if your friends are going.
Or to not be away from home because of a relationship, family situation.

Choosing a college course is very multi-faceted. There are many, many reasons:
* money
* enjoyment
* interest
* work/life balance
* autonomy
* aptitude/natural inclination
* nobility - sense of meaning in their future work
* wanting to work with people or alone
* wanting to work outdoors or at a desk

around this time, I was thinking of integrating these questions quite explicity into my system, as this would help inform the career path of the student.

i was also thinking about ikigai too, but that also is quite simplistic, because it reduces it down to 4 dimensions of want/need in a job, and as shown above, there are a lot more than 4 factors that go into a job.

There are many, many external influences:
* multitude of Socioeconomic factors that influence you:
    * if your parents are not college educated, you are more likely to pick a degree that gives you a more defined career path and has higher, early ROI
    * if your parents are college educated, you are less likely to do that in comparison
    * if your parents have a lot of money, you have a safety net to pursue courses that are classed as risky (e.g. the arts)
* parents (big one)
* family
* friends
* gender

while these are influential, external factors to be aware of, i do not want to integrate them into my RS, for a fear of bias. owen agreed with this.

that being said, just because the RS is blind to bias, doesn't mean the human picking the courses is unbiased either. but, that is a task well beyond the scope of this thesis, and frankly i don't care.

during this time i was also exposed to many theories of career and career choice.
holland and parson's theory of fit could be easily translatable to a computational-inspired method.

also theories of career such as SCCT. while this was interesting to read about, i didn't think it was incredibly relevant because the focus is college courses. of course, they are not independent processes, but as aoife said, it's almost impossible to predict your future career. things change, and the person does too.

a lot of the peripheral literature is about career recommendations, lots of similarities ofc but still a key difference imo when compared to college course recs 
* or maybe it's not that different and i'm just coping lol, probably a loot of parallels ngl

during this time i was thinking a lot about the conflict between:
1. what is best for the person (given current literature surrounding job/career satisfaction)
2. what they want

at the time, i was thinking of some hybrid system or something, or even just only recommending what is objectively best for them based on data.
but now (november), i'm leaning towards giving a lot more power and autonomy to the user. it's their life, their college course, and my RS should augment that process.

# October

began to dive into web scraping careers-portal.ie

began to data wrangle riasec college major dataset (open psychometrics)

around this time i began to realise i may have over complicated my system by asking for a multitude of factors.
often the best systems are the simplest, and even better, they can read between the lines from the fewer questions they ask.
a good model can read between the lines and make inferences, it will be wrong sometimes of course, but it can be novel.

i was talking with many GC's around this time, and that's when they (aoife + donnchadh) were telling me the main thing they focus on in their meetings is asking
about school subjects.

this led me to think about integrating this somehow into my RS - even better, the possibility of integrating natural language was very promising.
for example, i could ask: "why do you like maths" or "why do you like biology". The natural-language capability of LLM's to make inferences based off this has **a lot** of potential.

aoife mentioned something very interesting, and this helped to inform the direction/intention of my research, but careers are much more fluid nowaways, and a majority of careers that will exist in the future do not exist right now. she said that so much can happen and change in 5 years time, and it's almost impossible to predict it. so she prefers to look at things more locally, and just consider what college course people should study, not their career, because at 16-18, that can be very difficult to think about, and with almost absolute certainty, your wants when it comes to career will change.

# November

owen asked me to make a one-pager: around this time is when i started to formulate my research question.
in my one-pager, i claimed one of my main research questions is: *How can computational methods (e.g. AI) be used to assist in the Guidance Counselling (GC) process?*
but when i thought about it more, i realised that i don't actually want to focus on the specific GC process and the integration of computational methods into that.
i told owen today that talking with a GC is a tiny fraction of the time you spend thinking about what college course you want to study.
what i'm interested in, is integrating a tool that can augment/aid the student's independent research process.
a student spends loads of time doing their own research, and thinking about what college course is good for them. in most cases, they might have one or two conversations with 
a GC, adn that's all over 1-3 years of senior cycle.
so, a rough draft of my refined research question is: ***How can the integration of an RS assist in a student's college course research process?***

in my one-pager, i discussed some challenges:
1. what data do we gather from the student to make informed recs?
    * atm, i'm thinking holland code + LC subjects
2. what RS do I integrate?
    * i thought about using a 100% traditional one, but it's simplicity was its biggest downside, and as I said, there is a lot of potential with integrating natural language, seeing as this is a very human process.
    * i also don't want to offhand everything to an LLM. Owen agreed saying that from a research perspective, that is disappointing.

that's when I realised perhaps I could do a hybrid method - after all, that's what netflix is doing:

a ML/DL model trims to a smaller list (called candidate generation), and then an LLM does the finishing touches.
this is mostly for computational efficiency reasons, but in my case, it's important.

in my meeting with owen, he mentioned that i should think about my system architecture - he agrees the hybrid model looks exciting and promising, likely the way to go.
he said I should think about the demarcation of responsibilities.

off the top of my head:

The more traditional RS (likely done with CF/CBF, or more advanced like ML/DL) would do candidate generation.
a looot of courses can be filtered out by points, nfq level, location, portfolio btw - also LC subject/grade requirements can really filter things out.
the RS would also be the SST, storing the dataset of college courses. this is very important because it can be used for RAG (i think), and ground the LLM and limit hallucinations.
the RS would then feed this to the LLM, asking it to not only make sophisticated recs, but to also provide compelling justifications.

the justifications is a double-edged sword - on the one hand, it could be very insightful. i also make a strong point about novelty/serendipity, and justifications are a very key part of that. 
for example, when I was toying around with gemini, if it just suggested law and criminology to me, i would have likely shrugged it off, because of my preconceived concepts. 
but when it gave a justification, and when it was reasonable/insightful (not always the case - this is a downside to LLM's), that was my eureka moment.
the moment of serendipity was there. with a computer generated, natural language justification, it really made me think. 
this goes back to preference construction or discovery, and in that moment it gave credence to the idea that my preferences were evolving (preference discovery).

i realised a pretty big flaw with the riasec dataset - all the I questions are biological/health-related. it's obviously a problem because there 
are no questions about physics, maths, cs, chemistry, ag science, etc.

i created a basic model inspired by film-rec - categorise each person in the dataset under a college major category (15 of them), and amalgamate their scores together and mean everything.

so we have a dataset of 15 college major categories, each representing a 6-dimensional (RIASEC) vector. each college major category would get cosine sim'd with the person's riasec, and the top 3 college major categories would be returned.

i asked friends to fill our the same riasec quiz, and to provide their top 3 college course categories.
i used NDCG to evaluate and compare my model's top 3 with their top 3.
performance was quite promising for a model as simple as this, with a score of 0.441 (35 friend's data), and the baseline (random predictions) with a score of 0.2.

## challenges or things i'm thinking about

when i asked friends/family for their riasec scores, a few people said should they pick college major categories based on enjoyment, or whether they would want to study it.
i think this is a key thing to ask, because enjoyment is one factor of **many** that goes into picking a college course, and picking things just based off that is narrow-minded and not a reality of the world.
as aoife said in our conversation, a lot of kids (mostly from her school, which has high SES in rathdown south dublin) are very aware of financial reality, and would rather pick a course that promises them lots of money even if they don't like it, compared to a course they enjoy but don't make a lot of money. 

the open pyschometric questions are framed as: do you enjoy this? and that's key, because enjoyment/liking is at the heart of it.
dad is opinionated about this, and me too, but we are skeptical of enjoyment, because in many cases that leads to career paths that do not pay well.
as is clearly established, a lot of people are not simply looking for jobs they enjoy.

but interestingly, both aoife and donnchadh talked a lot about enjoyment. donnchadh even said at the end of the day we are trying to figure out what the person enjoys.

one workaround i am thinking, is the questions should be phrased differently - we shouldn't ask: would you enjoy studying in this college course/category?
we should ask: would you want to study in this college course/category?
the **want** is intentionally open-ended, because people want many but different things from college courses, and we should leave that up to the student.
this goes back to the reading between the lines thing.

*instead of want, we could say 'like to' instead?* ig it's the same thing tbh

if someone wants a course they enjoy, they will highly rank fields that they think they will like.
if a person wants to make money, they will highly rank fields that they think will make money.
if a person wants status, social impact, etc. etc. etc. they will highly rank fields that they think will align with what they want.

i think that's a great workaround, because it gives more power to the user, which is incredibly important because this is such a multi-faceted problem, and I have hesitations about over-simplifying the process and exerting too much control over the user, putting them in a box, which would result in a frustrating RS experience.
i also really like this because it doesn't over complicate the problem and avoids over-engineering, for example badgering the user with tens of questions about "how much do i value money in work, etc.". it **reads between the lines!**

the only problem with this is the open psychometrics dataset I am using (and which will potentially be instrumental in my RS) was asked "would you enjoy x".
if the question was asked differently, it may have yielded different results.
but i think this limitation is something to acknowledge in my thesis, and i can ask for owen's opinion on it.

## lc subjects - thinking out loud

i have been quite tunnel-visioned on holland codes if I am being completely honest. aoife expressed concerns about them, saying they are a 1/200 snapshot of a person. i think about this a lot. i disagree with her, but that's mostly on an emotional level, because a part of me really wants it to be a great representation of someone. why? because it can be so easily translated to a computational problem. a 6-dimensional vector, the beauty, simplicity and power behind that.

as my friends were sending me data though, i realised it may hold some limitations, and i will likely need something else additionally. both donnchadh and aoife mentioned that a lot of information can be gleamed from students by asking about their lc subjects, so i want to think out loud here.

we can ask more close-ended questions, such as asking them on a scale of 1-5 how much they enjoy or find the specific subject interesting.

this 1-5 can be normalized as a weight, and perhaps we could attach 1+ RIASEC taxonomies to each subject, and this could inform their RIASEC score potentially? e.g. physics would be I, construction would be R, etc.

now that i think about it, i'm not so sold or convinced on this. does this really provide any additional info that could be gleamed from the RIASEC quiz? the only limitation with that dataset is the lack of diversity in the I questions, but that can be changed tbh.

i also think lc subjects do not cover all areas of study, whereas the open psychometrics dataset has a solid coverage.
then again, we use the RIASEC scores to **infer** other courses, the goal of this is not to say "what specific course do they want", we are trying to get some sort of vocational inventory of the person, and use this to make inferences about potentially strong-fitting college courses.

I think this is where the LLM comes in, and we can ask a student **why** they like/dislike a subject, or what they do/don't find interesting about it.
