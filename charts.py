import matplotlib.pyplot as plt
import numpy as np

# Data for the chart
categories = ['Minimal LRU', 'Detailed LRU', 'Minimal FIFO', 'Detailed FIFO', 'Minimal LIFO', 'Detailed LIFO']
cyclic = [60, 0, 0, 0, 50, 60]
random = [55, 55, 50, 55, 50, 60]
locality = [65, 55, 60, 55, 70, 65]

# X-axis positions for grouped bars
x = np.arange(len(categories))

# Width of each bar
width = 0.25

# Create the grouped bar chart
plt.figure(figsize=(12, 7))
plt.bar(x - width, cyclic, width, label='Cyclic', color='blue', edgecolor='black')
plt.bar(x, random, width, label='Random', color='orange', edgecolor='black')
plt.bar(x + width, locality, width, label='Locality', color='green', edgecolor='black')

# Labeling
plt.title('Cache Performance by Prompting Technique and Sequence Type', fontsize=14)
plt.xlabel('Prompting Technique', fontsize=12)
plt.ylabel('Hit Ratio (%)', fontsize=12)

# Rotate x-axis labels more clearly
plt.xticks(ticks=x, labels=categories, rotation=30)

# Move legend slightly further from the chart
plt.legend(title='Sequence Type', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout for better spacing
plt.tight_layout()

# Show the chart
plt.show()
