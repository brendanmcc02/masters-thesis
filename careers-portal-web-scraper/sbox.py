#```get riasec makeup of each category - could apply this as a mask to the user's riasec profile?
import json

user_college_course_preferences = { "nfq_levels": [8],
                                    "colleges": [
                                                "Trinity College Dublin",
                                                "University College Dublin",
                                                "Royal College of Surgeons in Ireland",
                                                "Dublin City University",
                                                "TU Dublin - Grangegorman",
                                                "TU Dublin - Bolton Street",
                                                "Maynooth University",
                                                "Marino Institute of Education"
                                        ],
                                    "expected_points": 625}


file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

categories_dict = {}
r_i = ["realistic", "investigative", "artistic", "social", "enterprising", "conventional"]
r = 0
for course in courses:
    title = course["title"].lower()

    if "humanities" in course["categories"] and course["college"] in user_college_course_preferences["colleges"] and (course["points"] <= user_college_course_preferences["expected_points"] or course["isAdditionalPortfolioTestInterviewRequired"]) and course["nfqLevel"] in user_college_course_preferences["nfq_levels"]:
        r += 1



    for cat in course["categories"]:
        if cat not in categories_dict:
            categories_dict[cat] = [0] * 6

        for inte in course["riasec_interests"]:
            categories_dict[cat][r_i.index(inte)] += 1

print(str(r))

print("\n")
for k, v in categories_dict.items():
    norm = [round(float(i)/max(v), 2) for i in v]

    print(k + ": " + str(norm))

# with open("../datasets/cao-college-courses/cao-college-courses.json", "w") as outfile:
#     json.dump(courses, outfile, indent=4)
