import os
import csv

# Define the range of folders
start = 0
end = 200

# Initialize sums for each column
total_chunk = 0
total_right = 0
total_almost = 0
total_wrong = 0
total_time = 0.0

# Base directory (update this if the folders are in a different location)
base_dir = os.getcwd()

# Iterate through each chunk folder
for i in range(start, end):
    folder_name = f"llama2-7b/prompt4/chunk{i}"
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
    
    # Read the CSV file and sum the values
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            total_chunk += int(row['CHUNK'])
            total_right += int(row['RIGHT'])
            total_almost += int(row['ALMOST'])
            total_wrong += int(row['WRONG'])
            total_time += float(row['TIME'])

# Print the results
print(f"{total_right / 10000} + {total_almost/ 10000} = {(total_right + total_almost) / 10000} ")
print(f"Total RIGHT: {total_right}")
print(f"Total ALMOST: {total_almost}")
print(f"Total WRONG: {total_wrong}")
print(f"Average TIME: {(total_time / 200):.6f}")
