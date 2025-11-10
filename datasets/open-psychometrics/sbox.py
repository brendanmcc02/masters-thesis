from fuzzywuzzy import fuzz
from utils import fuzzy_match
# import pandas as pd

# print(preprocess_text("I.T/computing&networking and physics"))
# print(preprocess_text("computer science"))

majors = ["compt scienc", "infomtion technolog", "physics"]
# print(str(fuzzy_match("computer scienc", majors)))

print(str(fuzz.ratio("socilsg", "socilog")))
