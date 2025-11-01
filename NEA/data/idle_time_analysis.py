import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit

file_path = r"C:\Users\Leina School\Desktop\CodingProjects\Schoolwork\NEA\sequencing_summary_PAG07165_2dfda515.txt"
#create data frame using tab separated data from .txt file
df = pd.read_csv(file_path, sep='\t')

#sort by channel, then mux, then start time to group data appropriately
df = df.sort_values(by=['channel', 'mux', 'start_time'], ascending=True)

#add column for end time
df.insert(11, 'end_time', df['start_time'] + df['duration'])
#find previous end time for mux and channel and use to find idle time
df['prev_end_time'] = df.groupby(['channel', 'mux'])['end_time'].shift(1)
df.insert(11, 'idle_time', df['start_time'] - df['prev_end_time'])

#isolate columns of interest in secondary dataframe
df2 = df[['start_time', 'end_time', 'duration', 'prev_end_time', 'idle_time', 'read_id', 'channel', 'mux']]
df2_filtered = df2[df2['idle_time'] < 600]

#print first 15 columns
print(df2.head(15))

counts, bin_edges = np.histogram(df2_filtered['idle_time'], bins=600, density=False)
#used first and last value within each bin to find midpoint
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

#define exponential decay function
def exp_decay(x, A, k, C):
    return A * np.exp(-k * x) + C

#initial guess for parameters
initial_guess = (max(counts), 0.1, min(counts))

#fits exponential decay equation to the histogram data
parameters, covariance = curve_fit(exp_decay, bin_centers, counts, p0=initial_guess)

#generates fitted values
x_fit = np.linspace(bin_centers[0], bin_centers[-1], 1000)
y_fit = exp_decay(x_fit, *parameters)

#plots histogram and fitted curve
plt.figure(figsize=(8, 5))
plt.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), alpha=0.6, label='Histogram (data)')
plt.xlim(0, 600)
plt.plot(x_fit, y_fit, 'r-', lw=2, label='Fitted Exponential Decay')
plt.title('Fitting Exponential Decay to a Frequency Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#outputs the fitted parameters
print(f"Fitted parameters:\nA = {parameters[0]:.3f}, k = {parameters[1]:.3f}, C = {parameters[2]:.3f}")
