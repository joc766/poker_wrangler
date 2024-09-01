import pandas as pd
import matplotlib.pyplot as plt
import sys

# Load the CSV file
file_path = sys.argv[1]
data = pd.read_csv(file_path)

# Assuming your CSV has columns named 'Date' and 'Net_Earnings', ensure they are in the correct format
data['start_date'] = pd.to_datetime(data['start_date'])

# Sort the data by date in case it's not sorted
data = data.sort_values(by='start_date')
data['net_profit'] = data['win/loss'].cumsum()

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
