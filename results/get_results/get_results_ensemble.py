import os
import csv
import pandas as pd

# Function to read a CSV and return a DataFrame
def read_csv(file_path):
    return pd.read_csv(file_path)

# Function to read summary.csv and return a tuple of totals
def read_summary_csv(csv_file_path):
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            headings = next(reader)
            info = next(reader)
            total_right = int(info[1])
            total_almost = int(info[2])
            total_wrong = int(info[3])
            total_time = float(info[4])
            return total_right, total_almost, total_wrong, total_time
    except (StopIteration, FileNotFoundError):
        return 0, 0, 0, 0

# Function to filter words in df_almost that are not in df_right
def filter_words(df_right, df_almost):
    words_in_right = set(df_right['CLUE'])
    return df_almost[~df_almost['CLUE'].isin(words_in_right)]

# Function to compare DataFrames and count unique values based on a column
def compare_dataframes(df_list, column):
    if len(df_list) < 2:
        raise ValueError("At least two DataFrames are required for comparison.")
    
    concatenated = pd.concat(df_list, ignore_index=True)
    unique_df = concatenated.drop_duplicates(subset=column)
    return unique_df, len(unique_df)

# Define the range of folders
start = 0
end = 200

# List of folders to iterate through
folder_names = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']

# Base directory (update this if the folders are in a different location)
base_dir = os.getcwd()

# File to write the results
results_file_path = 'results/tables/ensemble_results.txt'

with open(results_file_path, 'w') as results_file:
    for folder in folder_names:
        results_file.write(f"\n{folder}\n")
        
        # Initialize sums for each column
        total_union_right = 0
        total_union_almost = 0
        total_union_wrong = 0
        total_prompts = 0
        total = 0
        
        for i in range(start, end):
            folder_paths = [os.path.join(base_dir, f"outputs/{folder}/prompt{j}/batch{i}") for j in range(3)]
            
            # Check if all chunk folders exist
            if not all(os.path.isdir(folder_path) for folder_path in folder_paths):
                continue
            
            # Initialize DataFrames for right, almost, and wrong
            df_rights = [read_csv(os.path.join(folder_path, 'right.csv')) for folder_path in folder_paths]
            df_almosts = [read_csv(os.path.join(folder_path, 'almost.csv')) for folder_path in folder_paths]
            df_wrongs = [read_csv(os.path.join(folder_path, 'wrong.csv')) for folder_path in folder_paths]
            
            # Compare DataFrames
            unique_right, union_right = compare_dataframes(df_rights, 'CLUE')
            total_union_right += union_right
            unique_almost, _ = compare_dataframes(df_almosts, 'CLUE')
            total_union_almost += len(filter_words(unique_right, unique_almost))
            
            # Read summary.csv for each prompt and accumulate totals
            for folder_path in folder_paths:
                total += len(read_csv(os.path.join(folder_path, 'wrong.csv')))
                total += len(read_csv(os.path.join(folder_path, 'almost.csv')))
                total += len(read_csv(os.path.join(folder_path, 'right.csv')))
                
                csv_file_path = os.path.join(folder_path, 'summary.csv')
                if not os.path.isfile(csv_file_path):
                    continue
                
                total_right, total_almost, total_wrong, _ = read_summary_csv(csv_file_path)
                total_prompts += total_right + total_almost + total_wrong
        
        # Calculate the new accuracy
        if total > 0:  # Ensure total is not zero to avoid division by zero
            new_right_acc = (total_union_right / (total / 5)) * 100
            new_almost_acc = (total_union_almost / (total / 5)) * 100
            new_wrong_acc = (total_union_wrong / (total / 5)) * 100
        else:
            new_right_acc = new_almost_acc = new_wrong_acc = 0
        
        # Write results to the file
        results_file.write(f"Right: {new_right_acc:.1f}% || Almost: {new_almost_acc:.1f}% || Wrong: {new_wrong_acc:.1f}%\n\n")

print(f"Results have been written to {results_file_path}")
