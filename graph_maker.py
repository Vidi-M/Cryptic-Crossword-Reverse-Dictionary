import matplotlib.pyplot as plt
import numpy as np

# Data
x = [0, 1, 2, 3, 4]
right = [59.90, 29.08, 45.51, 39.86, 41.73]
almost = [4.89, 13.16, 11.09, 11.50, 13.20]

# Create bar chart
fig, ax = plt.subplots()

# Bar width
bar_width = 0.35

# Plot data
p1 = ax.bar(x, right, bar_width, label='Right')
p2 = ax.bar(x, almost, bar_width, bottom=right, label='Almost')

# Add labels
ax.set_xlabel('Prompt Number')
ax.set_ylabel('Percentage')
ax.set_title('Stacked Bar Chart of Right and Almost Percentages for Llama3-8b Model')
ax.set_xticks(x)
ax.set_xticklabels(x)
ax.legend()

# Set y-axis to start from 20%
ax.set_ylim(0, 70)

# Add grid lines
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Display the chart
plt.show()
