import json

# 1. Load the data from the JSON file
with open('cao-college-courses.json', 'r') as f:
    courses = json.load(f)

# 2. Sort the list of dictionaries by the 'title' key
# Using .lower() ensures that the sort is case-insensitive (e.g., 'art' comes before 'Business')
courses.sort(key=lambda x: x['title'].lower())

# 3. Write the sorted data back to a new file
with open('cao-college-courses.json', 'w') as f:
    json.dump(courses, f, indent=4)