''''
import numpy as np

# Specify parameters
mean = 7472.521
std_dev = 3024.544
n = 10

BPS = 450
DNA_FOUND_CHANCE = 0.5632678551

# Generate random numbers
data = np.random.normal(mean, std_dev, n).astype(int)
data = np.clip(data, 1, None)

# Display the generated number
print(data)

runtime = int(input('Enter runtime: '))
avg_molecule_length = int(input('Enter Average Molecule Length: '))
target_fraction = float('Enter fraction of target molecules to enrich (Decimal): ')

result = np.random.random() < DNA_FOUND_CHANCE

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced]
standard_pore = [False, int(data[0]), 0, 0, 0]

for second in range(runtime):
    if not standard_pore[0]:  # idle
        result = np.random.random() < DNA_FOUND_CHANCE
        if result:  # found DNA
            standard_pore[0] = True
            standard_pore[2] = int(max(1, round(np.random.normal(avg_molecule_length, np.sqrt(avg_molecule_length)))))
        else:
            standard_pore[1] -= 1
    else:  # currently sequencing
        standard_pore[2] -= BPS
        sequenced_now = BPS if standard_pore[2] >= 0 else (BPS + standard_pore[2])  # handle last partial read
        standard_pore[3] += sequenced_now

        # If molecule finished
        if standard_pore[2] <= 0:
            standard_pore[0] = False  # back to idle
            standard_pore[2] = 0
    standard_pore[4] = int(round(standard_pore[3] * target_fraction))
    print(standard_pore)
'''

import numpy as np

# Specify parameters
mean = 7472.521
std_dev = 3024.544
n = 10

BPS = 450
DNA_FOUND_CHANCE = 0.5632678551

# Generate random numbers
data = np.random.normal(mean, std_dev, n).astype(int)
data = np.clip(data, 1, None)

# Display the generated number
print(data)

# Command line user inputs
runtime = int(input('Enter runtime (s): '))
avg_molecule_length = int(input('Enter Average Molecule Length (Bases): '))
target_fraction = float(input('Enter fraction of target molecules to enrich (Decimal): '))

result = np.random.random() < DNA_FOUND_CHANCE

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced, target/non target]
adaptive_pore = [False, int(data[0]), 0, 0, 0, False]

for second in range(runtime):
    if not adaptive_pore[0]:  # idle
        result = np.random.random() < DNA_FOUND_CHANCE
        if result:  # found DNA
            adaptive_pore[0] = True
            adaptive_pore[2] = int(max(1, round(np.random.normal(avg_molecule_length, np.sqrt(avg_molecule_length)))))
            if np.random.random() < target_fraction:
                adaptive_pore[5] = True
            else:
                adaptive_pore[5] = False
        else:
            adaptive_pore[1] -= 1
    else:  # currently sequencing
        adaptive_pore[2] -= BPS
        sequenced_now = BPS if adaptive_pore[2] >= 0 else (BPS + adaptive_pore[2])  # handle last partial read
        adaptive_pore[3] += sequenced_now

        # If molecule finished
        if adaptive_pore[2] <= 0:
            adaptive_pore[0] = False  # back to idle
            adaptive_pore[2] = 0
            
        if not adaptive_pore[5]:
            # eject molecule (no longer sequencing)
            adaptive_pore[0] = False
            adaptive_pore[2] = 0
        else:
            adaptive_pore[4] += sequenced_now
            
    print(adaptive_pore)