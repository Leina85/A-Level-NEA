import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit

file_path = r"C:\Users\Leina School\OneDrive - Wymondham High Academy Trust\Desktop\NEA-Git\NEA\sequencing_summary_PAG07165_2dfda515.txt"
#create data frame using tab separated data from .txt file
# Load only needed columns
use_cols = ['read_id', 'channel', 'mux', 'start_time', 'duration']
df = pd.read_csv(file_path, sep='\t', usecols=use_cols)

#sort by channel, then mux, then start time to group data appropriately
df = df.sort_values(by=['channel', 'mux', 'start_time'], ascending=True)

# Compute end times and idle times
df['end_time'] = df['start_time'] + df['duration']
df['prev_end_time'] = df.groupby(['channel', 'mux'])['end_time'].shift(1)
df['idle_time'] = df['start_time'] - df['prev_end_time']

# Filter for reasonable idle times (< 600 s)
df_filtered = df[df['idle_time'] < 600].dropna(subset=['idle_time'])

# Compute cumulative total idle time per channel/mux
df_filtered['cumul_idle_time'] = df_filtered.groupby(['channel', 'mux'])['idle_time'].cumsum()

# Show preview
print(df_filtered.head(15))

#counts, bin_edges = np.histogram(df_filtered['idle_time'], bins=600, density=False)
#used first and last value within each bin to find midpoint
#bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

#define exponential decay function
#def exp_decay(x, A, k, C):
#    return A * np.exp(-k * x) + C

#initial guess for parameters
#initial_guess = (max(counts), 0.1, min(counts))

#fits exponential decay equation to the histogram data
#parameters, covariance = curve_fit(exp_decay, bin_centers, counts, p0=initial_guess)

#generates fitted values
#x_fit = np.linspace(bin_centers[0], bin_centers[-1], 1000)
#y_fit = exp_decay(x_fit, *parameters)

#plots histogram and fitted curve
#plt.figure(figsize=(8, 5))
#plt.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), alpha=0.6, label='Histogram (data)')
#plt.xlim(0, 50)
#plt.plot(x_fit, y_fit, 'r-', lw=2, label='Fitted Exponential Decay')
#plt.title('Fitting Exponential Decay to a Frequency Distribution')
#plt.xlabel('Idle Time (s)')
#plt.ylabel('Frequency')
#plt.legend()
#plt.grid(True)
#plt.tight_layout()
#plt.show()

#outputs the fitted parameters
#print(f"Fitted parameters:\nA = {parameters[0]:.3f}, k = {parameters[1]:.3f}, C = {parameters[2]:.3f}")

# Total idle time per channel/mux (ignoring NaN)
idle_summary = (
    df_filtered.groupby(['channel', 'mux'], as_index=False)['idle_time']
      .sum()
      .rename(columns={'idle_time': 'total_idle_time'})
)

print(idle_summary.head(10))

plt.figure(figsize=(8, 5))
plt.hist(idle_summary['total_idle_time'], bins=50, alpha=0.7)
plt.xlabel('Total Idle Time per Channel/Mux (s)')
plt.ylabel('Count')
plt.title('Distribution of Total Idle Time Across Channels/Mux')
plt.grid(True)
plt.tight_layout()
plt.show()
