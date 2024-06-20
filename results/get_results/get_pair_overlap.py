import os
import csv
import pandas as pd

def read_csv(folder, filename):
    """Read a CSV file from the specified folder and return a DataFrame."""
    file_path = os.path.join(folder, filename)
    return pd.read_csv(file_path)

def filter_words(df_right, df_almost):
    """Filter out words in 'df_almost' that are already in 'df_right'."""
    words_in_right = set(df_right['CLUE'])
    return df_almost[~df_almost['CLUE'].isin(words_in_right)]

def compare_dataframes(df1, df2, column):
    """Compare two DataFrames based on a column and count similarities."""
    merged = pd.merge(df1, df2, on=column, how='outer')
    intersect = len(merged)
    return intersect

def read_summary(csv_file_path):
    """Read the summary CSV file and return the counts of right, almost, and wrong."""
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip headings
            info = next(reader)
            return int(info[1]), int(info[2]), int(info[3])
    except (StopIteration, ValueError, FileNotFoundError):
        return 0, 0, 0

def process_folders(base_dir, folder, num_prompts, start, end, output_file):
    """Process the folders to compare prompts and calculate new accuracies."""
    folder_base = os.path.join(base_dir, 'outputs', folder)
    with open(output_file, 'a') as f:
        f.write(f"{folder}\n")
        f.write("A & B || new right || new almost\n")
        for num_prompt_a in range(num_prompts - 1):
            for num_prompt_b in range(num_prompt_a + 1, num_prompts):
                total_prompts_a = total_prompts_b = 0
                total_union_right = total_union_almost = total_union_wrong = 0

                for i in range(start, end):
                    folder_a = os.path.join(folder_base, f"prompt{num_prompt_a}", f"batch{i}")
                    folder_b = os.path.join(folder_base, f"prompt{num_prompt_b}", f"batch{i}")

                    if not os.path.isdir(folder_a) or not os.path.isdir(folder_b):
                        continue

                    try:
                        df_right_a = read_csv(folder_a, 'right.csv')
                        df_right_b = read_csv(folder_b, 'right.csv')

                        df_almost_a = read_csv(folder_a, 'almost.csv')
                        df_almost_b = read_csv(folder_b, 'almost.csv')

                        filtered_almost_a = filter_words(df_right_b, df_almost_a)
                        filtered_almost_b = filter_words(df_right_a, df_almost_b)

                        total_union_right += compare_dataframes(df_right_a, df_right_b, 'CLUE')
                        total_union_almost += compare_dataframes(filtered_almost_a, filtered_almost_b, 'CLUE')

                        summary_file_a = os.path.join(folder_a, 'summary.csv')
                        summary_file_b = os.path.join(folder_b, 'summary.csv')

                        total_right_a, total_almost_a, total_wrong_a = read_summary(summary_file_a)
                        total_right_b, total_almost_b, total_wrong_b = read_summary(summary_file_b)

                        total_prompts_a += total_right_a + total_almost_a + total_wrong_a
                        total_prompts_b += total_right_b + total_almost_b + total_wrong_b

                    except Exception as e:
                        print(f"Error processing folders {folder_a} and {folder_b}: {str(e)}")

                avg_prompts = (total_prompts_a + total_prompts_b) / 2
                if avg_prompts > 0:
                    new_right_acc = (total_union_right / avg_prompts) * 100
                    new_almost_acc = (total_union_almost / avg_prompts) * 100

                    f.write(f"{num_prompt_a} & {num_prompt_b} || {new_right_acc:.2f} || {new_almost_acc:.2f}\n")

# Define parameters
start = 0
end = 200
num_prompts = 5
folder_names = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']
base_dir = os.getcwd()
output_file = 'results/tables/pairwise_results.txt'

# Process each folder
with open(output_file, 'w') as f:
    for folder in folder_names:
        print(f"Processing {folder}...")
        f.write(f"{folder}\n")
        f.write("A & B || new right || new almost\n")
        process_folders(base_dir, folder, num_prompts, start, end, output_file)

print(f"Results written to {output_file}")
