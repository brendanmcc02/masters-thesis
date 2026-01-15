#```get riasec makeup of each category - could apply this as a mask to the user's riasec profile?
import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

categories_dict = {}
r_i = ["realistic", "investigative", "artistic", "social", "enterprising", "conventional"]

for course in courses:
    title = course["title"].lower()

    if "sport" in course["categories"] and "conventional" in course["interests"]:
        print(title)

    for cat in course["categories"]:
        if cat not in categories_dict:
            categories_dict[cat] = [0] * 6

        for inte in course["interests"]:
            categories_dict[cat][r_i.index(inte)] += 1

print("\n")
for k, v in categories_dict.items():
    norm = [round(float(i)/max(v), 2) for i in v]

    print(k + ": " + str(norm))

# with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
#     json.dump(courses, outfile, indent=4)
