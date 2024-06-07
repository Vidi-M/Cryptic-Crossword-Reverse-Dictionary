import os
import csv
import pandas as pd

# Define the range of folders
start = 0
end = 200
num_prompts = 4


#folder_names = ['phi3-3b', 'phi3-14b', 'gemma-2b', 'gemma-7b', 'llama2-7b', 'llama3-8b']
folder_names = ['llama2-13b']


# Base directory (update this if the folders are in a different location)
base_dir = os.getcwd()
best_accuracy = 0
best_right=0

for folder in folder_names:
    print(folder)
    for num_prompt in range(0, num_prompts + 1):
        # Initialize sums for each column
        total_chunk = 0
        total_right = 0
        total_almost = 0
        total_wrong = 0
        total_time = 0.0
        
        # Iterate through each chunk folder
        for i in range(start, end):
            folder_name = f"{folder}/prompt{num_prompt}/chunk{i}"
            folder_path = os.path.join(base_dir, folder_name)
            
            # Check if the folder exists
            if not os.path.isdir(folder_path):
                print(f"Folder {folder_name} does not exist.")
                continue
            
            # Define the path to the CSV file
            csv_file_path = os.path.join(folder_path, 'summary.csv')
            
            # Check if the CSV file exists
            if not os.path.isfile(csv_file_path):
                print(f"CSV file not found in {folder_name}.")
                continue
            
            try:
                # Read the CSV file and sum the values
                with open(csv_file_path, mode='r') as file:
                    # csv_reader = csv.DictReader(file)
                    reader = csv.reader(file)
                    headings = next(reader)
                    info = next(reader)
                    total_chunk += int(info[0])
                    total_right += int(info[1])
                    total_almost += int(info[2])
                    total_wrong += int(info[3])
                    total_time += float(info[4])
            except StopIteration:
                pass
                
                # total_right += int(row['RIGHT'])
                # total_almost += int(row['ALMOST'])
                # total_wrong += int(row['WRONG'])
                # total_time += float(row['TIME'])
                

        total = total_right  + total_almost + total_wrong

        # Print the results
        # print(f"{total_right / total} + {total_almost/ total} = {(total_right + total_almost) / total} ")
        # print(f"Total RIGHT: {total_right}")
        # print(f"Total ALMOST: {total_almost}")
        # print(f"Total WRONG: {total_wrong}")
        # print(f"Average TIME: {(total_time / 200):.6f}")
        # print(total_chunk)
        # print(total)
        print(f"{num_prompt} || {((total_right + total_almost) / total * 100):.2f}% || {(total_right / total * 100):.2f}% || {(total_almost / total * 100):.2f}% || {(total_wrong / total * 100):.2f}% || {(total_time / end):.0f}")
        #print(f"{num_prompt} || {(total_right / total * 100):.2f}% || {(total_almost / total * 100):.2f}%")
