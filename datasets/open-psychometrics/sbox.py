import fuzzywuzzy
from utils import *

print(preprocess_text("`physics`"))
print(preprocess_text("`psychology`"))


# if we add to stop words:

# what we want:
# [american] studies -> area ethnic studies
# [american] history -> history
# [american] civilization -> civilization
# etc.
