import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    for lang in ["Modern Language"]:
        if lang in course['title']:
            if "humanities" in course['categories']:
                idx = course['categories'].index("humanities")
                course['categories'][idx] = "foreign languages"

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
