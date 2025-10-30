import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    del course["careerOpportunities"]

with open("../datasets/cao-college-courses/cao-college-courses.json", 'w') as file:
    jsonDump = json.dumps(courses, indent=4, separators=(',', ': '))

    file.write(jsonDump)
