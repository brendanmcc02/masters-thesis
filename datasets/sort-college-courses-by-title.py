import json

with open('cao-college-courses.json', 'r') as f:
    courses = json.load(f)

courses.sort(key=lambda x: x['title'].lower())

with open('cao-college-courses.json', 'w') as f:
    json.dump(courses, f, indent=4)