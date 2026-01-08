import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    # if ['psychology', 'child development', 'clinical psychology', 'counselling', 'occupational therapy', 'mental health', 'social work', 'speech and language therapy'] in course['title'].lower():
    #     course['categories'].append("behavioural health and human services")
    #     if "social science" in course['categories']:
    #         course['categories'].remove("social science")

    course["categories"] = sorted(list(set(course["categories"])))
    course["interests"] = sorted(list(set(course["interests"])))

with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
    json.dump(courses, outfile, indent=4)
