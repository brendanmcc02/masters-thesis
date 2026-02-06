import json
from collections import defaultdict


file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    if "law" in course["categories"] and "investigative" in course["riasec_interests"]:
        print(course["title"])
