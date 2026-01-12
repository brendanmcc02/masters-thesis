import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    title = course['title'].lower()
    ow = course["overview"].lower()

    if ("manufactur" in title or "automation" in title or "process" in title or "industrial" in title or "production" in title or "materials" in title) and "manufacturing and processing" not in course["categories"]:
        print(title)
        # course["categories"] = []
        
        # if "engineer" in title:
        #     course["categories"].append("engineering")

        # course["categories"].append("manufacturing and processing")

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
