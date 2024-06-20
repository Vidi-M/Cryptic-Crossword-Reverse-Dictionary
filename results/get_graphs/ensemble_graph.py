import matplotlib.pyplot as plt
import numpy as np

# Data
models = ['phi3-3.8b', 'phi3-14b', 'gemma-7b', 'llama2-7b', 'llama2-13b', 'llama3-8b']
right = [47.9, 65.2, 54.1, 63.1, 64.9, 71.5]
almost = [24.2, 14.6, 8.1, 8.5, 10.5, 6.7]

# Creating a stacked bar chart
fig, ax = plt.subplots()

bar_width = 0.5
bar_1 = np.array(right)
bar_2 = np.array(almost)

# Plotting bars
bars_1 = ax.bar(models, bar_1, bar_width, color='skyblue', label='Right results')
bars_2 = ax.bar(models, bar_2, bar_width, color='orange', bottom=bar_1, label='Almost results')

# Adding labels and title
ax.set_ylabel('Percentage Accuracy')
ax.set_xlabel('Models')
ax.set_ylim(0,90)
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', axis='y')

for i, (bar1, bar2) in enumerate(zip(bars_1, bars_2)):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    total = height1 + height2
    ax.text(bar1.get_x() + bar1.get_width() / 2, total + 1, f'{total:.1f}%', ha='center', va='bottom')

# Show plot
plt.xticks(rotation=0, ha='center')
fig.tight_layout()
# Save the figure instead of showing it
plt.savefig('results/graphs/ensemble_graph.png')

# Clear the current figure to release memory
plt.clf()

