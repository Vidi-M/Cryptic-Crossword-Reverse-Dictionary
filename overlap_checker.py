import pandas as pd
import os

# Function to read right.csv and return a DataFrame
def read_right_csv(folder):
    # Path to the right.csv file in the folder
    file_path = os.path.join(folder, 'right.csv')
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)
    return df

# Function to compare two DataFrames based on a column and count similarities and differences
def compare_dataframes(df1, df2, column):
    # Merge the two DataFrames on the specified column
    merged = pd.merge(df1, df2, on=column, how='inner')
    # Count the number of similarities
    num_same = len(merged)
    # Count the number of differences
    num_diff = len(df1) - num_same
    return num_same, num_diff

# Define folders
folder_a = 'llama3-8b/prompt0/chunk0'
folder_b = 'llama3-8b/prompt1/chunk0'

print('folders found')

# Read right.csv from both folders
df_a = read_right_csv(folder_a)
df_b = read_right_csv(folder_b)

print('folders read')
# Specify the column to compare
column_to_compare = 'CLUE'

# Compare DataFrames
num_same, num_diff = compare_dataframes(df_a, df_b, column_to_compare)

# Print the results
print(f"Number of rows with the same '{column_to_compare}' in both folders: {num_same}")
print(f"Number of rows with different '{column_to_compare}' in the two folders: {num_diff}")
