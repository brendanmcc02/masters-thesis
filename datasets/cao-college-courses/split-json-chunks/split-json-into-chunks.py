import json
import math

def split_json(input_file, chunk_size=100):
    # 1. Load the large JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Ensure the data is a list
    if not isinstance(data, list):
        print("Error: The root of the JSON file is not a list. Cannot split.")
        return

    total_items = len(data)
    print(f"Total objects found: {total_items}")

    # 2. Calculate how many files we will create
    num_files = math.ceil(total_items / chunk_size)

    # 3. Loop through data and create chunks
    for i in range(num_files):
        # Calculate start and end indices for the slice
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        
        # Slice the list to get the next 100 items
        chunk = data[start_index:end_index]
        
        # Generate a filename (e.g., output_part_1.json)
        output_filename = f"output_part_{i + 1}.json"
        
        # 4. Write the chunk to a new file
        with open(output_filename, 'w', encoding='utf-8') as out_f:
            json.dump(chunk, out_f, indent=4, ensure_ascii=False)
            
        print(f"Created {output_filename} with {len(chunk)} objects.")

# --- usage ---
# Replace 'your_dataset.json' with the actual name of your file
split_json('cao-college-courses.json', chunk_size=100)