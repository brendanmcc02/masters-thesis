import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    title = course['title'].lower()
    ow = course["overview"].lower()

    if "nursing" in title and ("intellectual" in title or "mental health" in title):
        if "behavioural health and human services" in course["categories"]:
            course["categories"].remove("behavioural health and human services")
            course["categories"].append("social science")

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
