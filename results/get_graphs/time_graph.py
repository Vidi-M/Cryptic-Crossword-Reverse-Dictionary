import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# Define the range of folders and number of prompts
START = 0
END = 200
NUM_PROMPTS = 4

# Folder names
FOLDER_NAMES = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']

# Base directory (update this if the folders are in a different location)
BASE_DIR = os.getcwd()

# Dictionary to hold all times for each folder and prompt
all_times = {folder: [[] for _ in range(NUM_PROMPTS + 1)] for folder in FOLDER_NAMES}

def process_csv_file(csv_file_path):
    """Read the time from the CSV file."""
    try:
        with open(csv_file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip headings
            info = next(reader)
            return float(info[4])
    except (StopIteration, ValueError, FileNotFoundError):
        return None

def collect_times():
    """Collect times from all relevant folders."""
    for folder in FOLDER_NAMES:
        for num_prompt in range(NUM_PROMPTS + 1):
            for i in range(START, END):
                folder_name = f"outputs/{folder}/prompt{num_prompt}/batch{i}"
                folder_path = os.path.join(BASE_DIR, folder_name)

                if not os.path.isdir(folder_path):
                    continue

                csv_file_path = os.path.join(folder_path, 'summary.csv')
                time = process_csv_file(csv_file_path)
                if time is not None:
                    all_times[folder][num_prompt].append(time)

def plot_boxplots():
    """Create a figure for box plots."""
    fig, axes = plt.subplots(1, len(FOLDER_NAMES), figsize=(20, 5), sharey=True)

    for i, (folder, ax) in enumerate(zip(FOLDER_NAMES, axes)):
        ax.boxplot(all_times[folder], positions=np.arange(NUM_PROMPTS + 1))
        ax.set_xlabel('Prompt Number')
        if i == 0:
            ax.set_ylabel('Average Time per Batch (seconds)')
        ax.set_title(folder)
        ax.set_xticks(np.arange(NUM_PROMPTS + 1))
        ax.set_xticklabels([f'{i}' for i in range(NUM_PROMPTS + 1)])

    plt.tight_layout()
    # Save the figure instead of showing it
    plt.savefig('results/graphs/time_graph.png')
    # Clear the current figure to release memory
    plt.clf()

# Collect times and plot boxplots
collect_times()
plot_boxplots()
