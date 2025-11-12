* don't aggregate the RIASEC categories - leave them as individual?
    * by aggregating them together, i'd argue some vital information is lost
* could use an ML model
    * 48 input variables, 15 categorical output variables
    * get a ranking score and normalize it
    * return top n (e.g. 3 or 5)
* replicating the open psychometrics riasec dataset would be **very easy**
    * it means I can replicate the individual category-level granularity
* by asking friends/family rn, they are just giving me an aggregated RIASEC score
    * as I said, this potentially loses a lot of valuable information

* I think aggregating the results all together into just a dataset of 15 is a bad idea
    * there is so much information being lost in that aggregation process
* and i actually have use of a large dataset (~77k entries) that could be ideal for training
    * i could even make the data more granular by using specific college majors as opposed to categories
        * i am still a bit concerned about this though, likely will be a bias towards majors with more data (e.g. psych)
        * especially compared to majors with very little data
