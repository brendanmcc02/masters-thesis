import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    title = course['title'].lower()

    if "agri" in title:
        if "life science" in course["categories"]:
            course["categories"].remove("life science")

        course["categories"].append("agriculture")

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
