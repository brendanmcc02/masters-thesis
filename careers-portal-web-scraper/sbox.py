#```get riasec makeup of each category - could apply this as a mask to the user's riasec profile?
import json



file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

courses_s = set()
for course in courses:

    if course["college"] not in courses_s and course["region"] == "Dublin":
        courses_s.add(course["college"])

    
for c in courses_s:
    print(c)
