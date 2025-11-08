import numpy as np

# Specify parameters
mean = 7472.521
std_dev = 3024.544
n = 100

BPS = 450
DNA_FOUND_CHANCE = 0.5632678551

# Generate random numbers
data = np.random.normal(mean, std_dev, n).astype(int)
data = np.clip(data, 1, None)

# Display the generated number
print(data)

runtime = input('Enter runtime: ')
avg_molecule_length = input('Enter Average Molecule Length: ')

result = np.random.random() < DNA_FOUND_CHANCE
print('here', result)