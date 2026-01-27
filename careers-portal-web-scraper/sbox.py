#```get riasec makeup of each category - could apply this as a mask to the user's riasec profile?
import json
from collections import defaultdict


file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

ids = set()
reps = defaultdict(int)
for course in courses:
    if course["id"] in ids:
        reps[course["id"]] += 1
    else:
        ids.add(course["id"])

for k in reps.keys():
    print(str(k) + ": " + str(reps[k]))