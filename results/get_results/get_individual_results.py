import os
import csv
import numpy as np

# Define the range of folders and number of prompts
START = 0
END = 200
NUM_PROMPTS = 4

FOLDER_NAMES = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']

# Output file path
OUTPUT_FILE = "results/tables/individual_results.txt"

# Base directory (update this if the folders are in a different location)
BASE_DIR = os.getcwd()

# Function to process a single CSV file
def process_csv_file(csv_file_path):
    try:
        with open(csv_file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            headings = next(reader)
            info = next(reader)
            return [int(info[0]), int(info[1]), int(info[2]), int(info[3]), float(info[4])]
    except (StopIteration, ValueError):
        return [0, 0, 0, 0, 0.0]

# Open file for writing
with open(OUTPUT_FILE, 'w') as file:
    for folder in FOLDER_NAMES:
        print(f"**** {folder} ****")
        file.write(f"\n{folder} \n")
        file.write("prompt || accuracy || right || almost || wrong \n")
        for num_prompt in range(NUM_PROMPTS + 1):
            total_chunk = total_right = total_almost = total_wrong = 0
            all_times = []

            # Iterate through each chunk folder
            for i in range(START, END):
                folder_name = f"outputs/{folder}/prompt{num_prompt}/batch{i}"
                folder_path = os.path.join(BASE_DIR, folder_name)

                if not os.path.isdir(folder_path):
                    file.write(f"Folder {folder_name} does not exist.\n")
                    continue

                csv_file_path = os.path.join(folder_path, 'summary.csv')
                if not os.path.isfile(csv_file_path):
                    continue

                chunk, right, almost, wrong, time = process_csv_file(csv_file_path)
                total_chunk += chunk
                total_right += right
                total_almost += almost
                total_wrong += wrong
                all_times.append(time)

            total = total_right + total_almost + total_wrong

            if total > 0:
                accuracy = ((total_right + total_almost) / total * 100)
                right_pct = (total_right / total * 100)
                almost_pct = (total_almost / total * 100)
                wrong_pct = (total_wrong / total * 100)

                print(f"{num_prompt} || {accuracy:.2f}% || {right_pct:.2f}% || {almost_pct:.2f}% || {wrong_pct:.2f}%")
                file.write(f"{num_prompt} || {accuracy:.2f}% || {right_pct:.2f}% || {almost_pct:.2f}% || {wrong_pct:.2f}% \n")

# File is automatically closed at the end of the `with` block
print(f"Results written to {OUTPUT_FILE}")