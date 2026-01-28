from college_course_recommender_system_utils import *
import json

file = open("../datasets/cao-college-courses.json")
courses = json.load(file)

for course in courses:
    if len(course["id"]) == 5:

        id, title = parse_id_and_title_from_cao_college_course(course["id"] + course["title"])

        print(id)
