import json
from collections import defaultdict


file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    if "life science" in course["categories"] and not ("realistic" in course["riasec_interests"]):
        print(course["title"])
