import numpy as np

# Specify parameters
mean = 7472.521
std_dev = 3024.544
n = 1

# Generate random numbers
data = np.random.normal(mean, std_dev, n).astype(int)
data = np.clip(data, 1, None)

# Display the generated number
print(data)