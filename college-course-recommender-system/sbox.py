from college_course_title_nlp_utils import *
import json

def get_og_interests(course, og_file):
    id = course["id"]
    preprocessed_title = preprocess_college_title(course["title"])

    for c in og_file:
        if id == c["id"] and preprocessed_title == c["preprocessed_title"]:
            c["interests"].sort()
            return c["interests"]

    return None

file = open("../datasets/cao-college-courses.json")
new = json.load(file)

file_og = open("../datasets/original-cao-college-courses.json")
og = json.load(file_og)

for i in range(len(og)):
    og[i]["preprocessed_title"] = preprocess_college_title(og[i]["title"])

new_interests = []
og_interests = []
changed = 0

for course in new:
    course["og_interests"] = get_og_interests(course, og)

    if not course["og_interests"]:
        
        continue

    if course["og_interests"] != course["riasec_interests"]:
        changed += 1
    

print(str(changed) + " courses changed")