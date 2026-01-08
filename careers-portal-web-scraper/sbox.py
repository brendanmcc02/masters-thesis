import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    if "psychology" in course['title'].lower() and "behavioural health and human services" in course['categories'] and "social science" in course['categories']:
        print(course['title'])

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
