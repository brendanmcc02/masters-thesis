import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    title = course['title'].lower()
    ow = course["overview"].lower()

    if "environmental science" in title or "sustainability" in title or "conservation" in title or "climate" in title or "environment" in title:
        course["categories"].append("environment")

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
