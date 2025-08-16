# Using an LLM agent (persona) to evaluate a recommender system
* as opposed to human testers/other traditional forms of evaluation
* check literature for this
    * looks like it's already done? [source](https://arxiv.org/pdf/2504.12722)
    * also [here](file:///home/brendanmcc02/Desktop/college/masters-thesis33456-Article%20Text-37524-1-2-20250410.pdf)
    * TODO check if these models are open source?
        * can we fine tune hyperparameters?
        * potentially amibtious - can we modify some of the architecture?
* **[Gemini's Research Report](https://gemini.google.com/app/89b27e845a739b3d)**

## Potential Research Gaps:
* Develop robust, quantifiable metrics to assess the **human-likeness** and **trustworthiness** of LLM-powered user simulators (like the two mentioned above).
    * basically a Turing Test for LLM-powered user simulators for Rec Sys

# evaluating trust in an LLM for recommendations
* differences between 
    1. Traditional Methods (content-based/collaborative filtering)
        * shallow reasons, doesn't provide deep/profound links/insights
    2. Deep learning/ML
    3. LLM's
        * they can reason with natural language
        * the challenge is a proclivity to hallucinate
        * or make up non-sensical reasons as to why the product was recommended
    
    in their ability to [interpret/justify/reason](https://gemini.google.com/app/21c341b4ae39804a) their recommendations
* [gemini report](https://gemini.google.com/app/cf66a829e9a2d6fb)
* a good recommender system knows **why/how** it recommended the product.
* this builds trust with the user
    * TODO check literature for rec sys trust
* Compared to traditional methods (shallow reasoning) and deep learning (not transparent), LLM's have great **reasoning** ability.
    * perhaps this could be leveraged?
    * the main problem is hallucination
    * also, the justification may not be a true representation of the algorithm that arrived at the decision
        * e.g. the justification the LLM gives might be different to the real mathematical reason it got recommended in the first place
* [LLM's are very inefficient at generating recommndations](https://gemini.google.com/app/8ec1661cd03d7365)
    * so, atm LLM's are being used as a plug-in
        * i.e. a DL model may generate a list of potential candidates, and an LLM may take items from that pruned list with justifications

# improving the interpretation/justification/reasoning of Deep learning model recommendations
* DL is a black-box and as a result, interpretability is difficult
* researchers have made an attempt to explain things post-hoc
* called explainable AI (XAI)
* some XAI tools already exist for this:
    * LIME (Local Interpretable Model-Agnostic Explanations)
    * SHAP (SHapley Additive exPlanations)
* **investigate their limitations and provide potential solutions**
* the problem with this thesis is that it may be seen as outdated
    * the Rec sys field is moving towards LLM's for recommendations
    * BUT LLM's are very inefficient at generating recommendations, so currently the industry is using a hybrid model
        * TODO verify research on this, I got it from [Gemini](https://gemini.google.com/app/8ec1661cd03d7365)

# using LLM's to enhance rec sys in group settings
* e.g. a group of people together in a room wanting to watch a movie
* the LLM can quickly capture the vibe, and each person's preferences
* few-shot prompting
    * where each 'shot' is each person's preferences

## temporal dynamics of an LLM-based rec sys
* from [this] research paper
* one of the limitations/further opportunities of enhancing an LLM rec sys is to integrate **temporal dynamics**:
    * *"Temporal dynamics enable LLM-based recommender systems to adapt to changing user preferences
    and behaviors. As interests shift with trends and events, advanced temporal modeling is necessary.
    Recommendations should balance recent interactions with historical data, employing weighting and
    decay strategies. Seasonal variations also require contextual adaptation. Strategies like time-aware
    embeddings, temporal attention mechanisms, and real-time data processing enhance personalization
    and deliver timely, relevant recommendations, boosting user satisfaction and engagement."*

# Questions/stuff to research
* do LLM rec sys perform better than DL?