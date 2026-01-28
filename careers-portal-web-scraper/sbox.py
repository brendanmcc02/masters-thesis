import json
from collections import defaultdict


file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

ids = set()
reps = defaultdict(int)
for course in courses:
    if len(course["id"]) == 5:
        print(course["id"])
