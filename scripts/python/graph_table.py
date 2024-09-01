import pandas as pd
import matplotlib.pyplot as plt
import sys

# Load the CSV file
file_path = sys.argv[1]
data = pd.read_csv(file_path)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['start_date'], data['net_profit'], marker='o')

# Formatting the plot
plt.title('Net Earnings Over Time')
plt.xlabel('start_date')
plt.ylabel('Net Earnings ($)')
plt.grid(True)
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
