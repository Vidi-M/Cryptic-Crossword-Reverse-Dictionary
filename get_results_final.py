import os
import csv
import pandas as pd

# Function to read right.csv and return a DataFrame
def read_right_csv(folder):
    # Path to the right.csv file in the folder
    file_path = os.path.join(folder, 'right.csv')
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)
    return df

# Function to read almost.csv and return a DataFrame
def read_almost_csv(folder):
    # Path to the almost.csv file in the folder
    file_path = os.path.join(folder, 'almost.csv')
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)
    return df

def read_wrong_csv(folder):
    # Path to the almost.csv file in the folder
    file_path = os.path.join(folder, 'wrong.csv')
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)
    return df

# Function to read summary.csv and return a tuple of totals
def read_summary_csv(csv_file_path):
    total_right = 0
    total_almost = 0
    total_wrong = 0
    total_time = 0
    
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            headings = next(reader)
            info = next(reader)
            total_right = int(info[1])
            total_almost = int(info[2])
            total_wrong = int(info[3])
            total_time = float(info[4])
    except StopIteration:
        pass
    
    return total_right, total_almost, total_wrong, total_time

# Function to filter words in df_almost that are not in df_right
def filter_words(df_right, df_almost):
    # print(f"right \n {df_right}")
    # print(f"almost \n {df_almost}")
    words_in_right = set(df_right['CLUE'])
    unique_df_almost = df_almost[~df_almost['CLUE'].isin(words_in_right)]
    # print(f"filtered \n {unique_df_almost}")
    return unique_df_almost

# Function to compare all DataFrames based on a column and count similarities and differences
def compare_dataframes(df_list, column, almost):
    if len(df_list) < 2:
        raise ValueError("At least two DataFrames are required for comparison.")
    
    # Start with the first DataFrame
    merged = df_list[0]
    # print("################### 1 #######################")
    # print(merged)
    # print("################### 2 #######################")
    # print(df_list[1])
    
    # Merge with each subsequent DataFrame on the specified column
    for i, df in enumerate(df_list[1:]):
        merged = pd.merge(merged, df, on=column, how='outer', suffixes=(f"_x{i}", f"_y{i}"))
    
    # Count the number of similarities
    intersect = len(merged)
    
    # Count the number of differences
    #union = sum(len(df) for df in df_list) - intersect
    concatenated = pd.concat(df_list, ignore_index=True)
    unique_df = concatenated.drop_duplicates(subset='CLUE')
    union = len(unique_df)
    
    # if almost:
    #     print("############ unique #############")
    #     print(unique_df)
    #     print("#########################")
    
    return unique_df, union

# Define the range of folders
start = 0
end = 200
num_prompts = 5



# List of folders to iterate through
folder_names = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']
#folder_names = ['llama3-8b']

# Base directory (update this if the folders are in a different location)
base_dir = os.getcwd()

for folder in folder_names:
    #print(folder)
    
    # Initialize sums for each column
    total_chunks = 0
    total_prompts = 0
    total_prompts_b = 0
    total_union_right = 0
    total_union_almost = 0
    total_union_wrong = 0
    total = 0
    
    for i in range(start, end):
        #print(i)
        filtered_almosts = []
        folder_paths = [os.path.join(base_dir, f"{folder}/prompt{j}/chunk{i}") for j in range(0, num_prompts)]           
        # Check if all chunk folders exist
        for folder_path in folder_paths:
            if not os.path.isdir(folder_path):
                print(f"Prompt folders for {folder_path} do not exist.")
                continue
        
        # Specify the column to compare
        column_to_compare = 'CLUE'
        
        # Initialize DataFrames for right and almost
        df_rights = [read_right_csv(folder_path) for folder_path in folder_paths]
        df_almosts = [read_almost_csv(folder_path) for folder_path in folder_paths]
        df_wrongs = [read_wrong_csv(folder_path) for folder_path in folder_paths]
        
        # Initialize filtered almost DataFrames
        # for j in range(0, num_prompts):
        #     for k in range(0, num_prompts):
        #         if j != k:
        #             filtered_almosts.append(filter_words(df_rights[j], df_almosts[k]))
        #         print("##### 0 2 #####")
        #         print(filter_words(df_rights[0], df_almosts[2]))
        #         print("##### 1 2 #####")
        #         print(filter_words(df_rights[1], df_almosts[2]))
        
        # Compare DataFrames
        unique_right, union_right = compare_dataframes(df_rights, 'CLUE', False)
        total_union_right += union_right
        unique_almost, _ = compare_dataframes(df_almosts, 'CLUE', True)
        total_union_almost += len(filter_words(unique_right, unique_almost))
        # total_union_wrong += compare_dataframes(df_wrongs, 'CLUE', False)
        # Read summary.csv for each prompt and accumulate totals
        for folder_path in folder_paths:
            file_path = os.path.join(folder_path, 'wrong.csv')
            df_wrong = pd.read_csv(file_path)
            total += len(df_wrong)
            
            file_path = os.path.join(folder_path, 'almost.csv')
            df_almost = pd.read_csv(file_path)
            total += len(df_almost)
            
            file_path = os.path.join(folder_path, 'right.csv')
            df_right = pd.read_csv(file_path)
            total += len(df_right)
            
            csv_file_path = os.path.join(folder_path, 'summary.csv')
            
            if not os.path.isfile(csv_file_path):
                #print("csv not found: {csv_file_path}")
                continue
            
            total_right, total_almost, total_wrong, _ = read_summary_csv(csv_file_path)
            total_prompts += total_right + total_almost + total_wrong
    
    # Calculate and print the new accuracy
    #print(total)
    #print(total/ num_prompts)
    new_right_acc = (total_union_right / (total / num_prompts)) * 100
    new_almost_acc = (total_union_almost / (total / num_prompts)) * 100
    new_wrong_acc = (total_union_wrong / (total / num_prompts)) * 100
    print(f"{folder} || {new_right_acc:.1f} || {new_almost_acc:.1f}")
    
    