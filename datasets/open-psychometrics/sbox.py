import fuzzywuzzy
from utils import *

print(preprocess_text("I.T/computing&networking and physics"))
print(preprocess_text("computer science"))


# comput scienc
#
# computer science

# I.T/computing&networking and physics
# inform technolog comput network physic

# information technology
# computer networks
# physics

# tokenize -> try every substring (biggest first)
# 
