import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'NFDB_large_fires.csv'  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Exclude invalid years (-999) and group by valid years
valid_years = df[df['YEAR'] >= 0]
fires_per_year = valid_years.groupby('YEAR').size()

# Plotting the time-series line chart
plt.figure(figsize=(12, 6))
plt.plot(fires_per_year.index, fires_per_year.values, color='red', linewidth=2)
plt.title('Total Number of Fires Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Fires')
plt.grid(True)
plt.show()
