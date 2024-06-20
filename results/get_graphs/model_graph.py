import os
import matplotlib.pyplot as plt

# Define the base directory and results file path
BASE_DIR = os.getcwd()
RESULTS_FILE = os.path.join(BASE_DIR, 'results/tables/individual_results.txt')

# Function to read data from the results file
def read_results(file_path):
    data = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            current_model = None
            for line in lines:
                line = line.strip()
                if line in models:
                    current_model = line
                    data[current_model] = []
                elif line.startswith('prompt') or not line:
                    continue
                else:
                    parts = line.split(" || ")
                    if len(parts) < 5:
                        continue
                    prompt = int(parts[0])
                    right_pct = float(parts[2].replace("%", "").strip())
                    almost_pct = float(parts[3].replace("%", "").strip())
                    data[current_model].append([right_pct, almost_pct])
    except FileNotFoundError:
        print(f"Results file {file_path} not found.")
    return data

# Data
prompts = [0, 1, 2, 3, 4]
models = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']
data = read_results(RESULTS_FILE)

# Creating separate bar charts for each prompt
fig, axes = plt.subplots(1, 5, figsize=(25, 5), sharey=True)

# Plotting each prompt
for i, prompt in enumerate(prompts):
    prompt_data = [data[model][prompt] for model in models if prompt < len(data[model])]
    max_height = max(sum(data_pair) for data_pair in prompt_data)
    for j, (bottom, top) in enumerate(prompt_data):
        bottom_bar = axes[i].bar(j, bottom, color='skyblue', label='Right results' if j == 0 else "")
        top_bar = axes[i].bar(j, top, bottom=bottom, color='orange', label='Almost results' if j == 0 else "")
        total_value = top + bottom
        if total_value == max_height:
            axes[i].annotate(f'{total_value:.1f}%', xy=(top_bar.patches[0].get_x() + top_bar.patches[0].get_width() / 2, top+bottom),
                             xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    axes[i].set_xlabel('Models')
    axes[i].set_title(f'Prompt {prompt}')
    axes[i].set_ylim(0, 70)
    axes[i].set_xticks(range(len(models)))
    axes[i].set_xticklabels(models, rotation=90, ha='center')
    axes[i].grid(True, linestyle='--')

axes[0].set_ylabel('Percentage Accuracy')

# Adding legend
axes[0].legend(loc='upper left')

plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the figure instead of showing it
plt.savefig('results/graphs/model_graph.png')

# Clear the current figure to release memory
plt.clf()
