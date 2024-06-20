import matplotlib.pyplot as plt
import numpy as np

# Data
prompts = [0, 1, 2, 3, 4]
models = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']

data = {
    'phi3-3.8b': [[31.66, 23.27], [26.88, 24.89], [27.26, 24.65], [17.30, 31.93], [18.09, 31.15]],
    'phi3-14b': [[43.01, 14.75], [35.18, 20.26], [42.64, 17.89], [29.50, 19.84], [33.82, 20.72]],
    'gemma-7b': [[43.53, 5.75], [31.52, 10.07], [33.07, 8.64], [21.03, 8.83], [21.97, 8.51]],
    'llama2-7b': [[47.71, 6.77], [33.64, 11.77], [41.18, 9.14], [38.33, 10.39], [37.94, 11.26]],
    'llama2-13b': [[43.92, 6.63], [40.91, 15.03], [43.77, 15.23], [42.29, 15.07], [42.56, 16.01]],
    'llama3-8b': [[59.90, 4.89], [29.08, 13.16], [45.51, 11.09], [39.86, 11.50], [41.73, 13.20]]
}

# Transposing data
transposed_data = {model: np.array([data[model][i] for i in range(len(prompts))]).T for model in models}

# Creating separate bar charts for each model
fig, axes = plt.subplots(1, len(models), figsize=(15, 5), sharey=True)

# Plotting each model
for i, model in enumerate(models):
    model_data = [data[model][prompt] for prompt in prompts]
    max_height = max(sum(data_pair) for data_pair in model_data)
    for j, (bottom, top) in enumerate(model_data):
        ind = np.arange(len(prompts))
        bottom_bar = axes[i].bar(j, bottom, color='skyblue', label='Right results' if j == 0 else "")
        top_bar = axes[i].bar(j, top, bottom=bottom, color='orange', label='Almost results' if j == 0 else "")
        total_value = top + bottom

        if total_value == max_height:
            axes[i].annotate(f'{total_value:.1f}%', xy=(top_bar.patches[0].get_x() + top_bar.patches[0].get_width() / 2, top + bottom),
                             xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    axes[i].set_title(model)
    axes[i].set_xlabel('Prompts')
    axes[i].set_xticks(ind)
    axes[i].set_xticklabels(prompts)
    axes[i].grid(True, linestyle='--')

axes[0].set_ylabel('Percentage Accuracy')

plt.tight_layout()
# Save the figure instead of showing it
plt.savefig('results/graphs/pairs_graph.png')

# Clear the current figure to release memory
plt.clf()

