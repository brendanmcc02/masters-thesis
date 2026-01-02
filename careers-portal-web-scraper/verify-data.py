import json

file = open("../datasets/cao-college-courses/cao-college-courses.json")
courses = json.load(file)

print("num courses: " + str(len(courses)) + "\n")

# ids = set()
# types = set()
# titles = set()
# colleges = set()
# regions = set()
# durations = set()
# nfqLevels = set()
# points = set()
# overviews = set()
# repeatedOverviews = set()
# careerOpportunities = set()
# repeatedcareerOpportunities = set()
# interests = set()
for course in courses:
    # if not course["id"] or course["id"] == "":
    #     print("null or empty id!!!!!!!!!!!!!!!!!!!!!!!!:" + str(course["id"]))
    
    # ids.add(course["id"])

    # if not course["type"] or course["type"] == "":
    #     print("null or empty type!!!!!!!!!!!!!!!!!!!!!!!!:" + str(course["id"]))
    
    # types.add(course["type"])

    # if not course["title"] or course["title"] == "":
    #     print("null or empty title!!!!!!!!!!!!!!!!!!!!!!!!" + str(course["id"]))
    
    # titles.add(course["title"])
        
    # if not course["college"] or course["college"] == "":
    #     print("null or empty college!!!!!!!!!!!!!!!!!!!!!!!!:" + str(course["id"]))
    
    # colleges.add(course["college"])

    # if not course["region"] or course["region"] == "":
    #     print("null or empty region!!!!!!!!!!!!!!!!!!!!!!!!:" + str(course["id"]))
    
    # regions.add(course["region"])

    # if not course["duration"] or course["duration"] == "":
    #     print("null or empty duration!!!!!!!!!!!!!!!!!!!!!!!!: " + str(course["id"]))
    
    # durations.add(course["duration"])

    # if not course["nfqLevel"] or course["nfqLevel"] == "":
    #     print("null or empty nfqLevel!!!!!!!!!!!!!!!!!!!!!!!!: " + str(course["id"]))
    
    # nfqLevels.add(course["nfqLevel"])

    # if course["points"] != 0 and not course["points"]:
    #     print("null: " + str(course["id"]))
    # else:
    #     points.add(course["points"])

    # if course["overview"] != "":
    #     if course["overview"] in overviews:
    #         repeatedOverviews.add(course["overview"])

    #     overviews.add(course["overview"])

    # if course["careerOpportunities"] != "":
    #     if course["careerOpportunities"] in careerOpportunities:
    #         repeatedcareerOpportunities.add(course["careerOpportunities"])

    #     careerOpportunities.add(course["careerOpportunities"])

    if len(course["interests"]) == 0:
        print("empty interests: " + str(course["id"]))
    

# ids = sorted(list(ids))
# print("ID's:\n")
# for id in ids:
#     print(str(id))

# types = sorted(list(types))
# print("Types:\n")
# for type in types:
#     print(str(type))

# titles = sorted(list(titles))
# print("titles:\n")
# for title in titles:
#     print(str(title))
    
# colleges = sorted(list(colleges))
# print("Colleges:\n")
# for college in colleges:
#     print(str(college))

# regions = sorted(list(regions))
# print("Regions:\n")
# for region in regions:
#     print(str(region))

# durations = sorted(list(durations))
# print("durations:\n")
# for duration in durations:
#     print(str(duration))

# nfqLevels = sorted(list(nfqLevels))
# print("nfqLevels:\n")
# for nfqLevel in nfqLevels:
#     print(str(nfqLevel))

# points = sorted(list(points))
# print("points:\n")
# for point in points:
#     print(str(point))

# repeatedOverviews = sorted(list(repeatedOverviews))
# print("repeatedOverviews:\n")
# for repeatedOverview in repeatedOverviews:
#     print(str(repeatedOverview) + "\n")

# repeatedcareerOpportunities = sorted(list(repeatedcareerOpportunities))
# print("repeatedcareerOpportunities:\n")
# for repeatedcareerOpportunitie in repeatedcareerOpportunities:
#     print(str(repeatedcareerOpportunitie) + "\n")

# interests = sorted(list(interests))
# print(str(len(interests)))
# print("interests:\n")
# for interests in interests:
#     print(str(interests) + "\n")

for course in courses:
    if "healthcare" in course['categories'] and "life science" not in course['categories']:
        print(course['title'])
