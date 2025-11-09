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

result = np.random.random() < DNA_FOUND_CHANCE
print('here', result)

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced]
pore = [0, data[0], 0, 0, 0]

for second in range(runtime):
    result = np.random.random() < DNA_FOUND_CHANCE
    if not pore[0]:  # idle
        if result:  # found DNA
            pore[0] = True
            pore[2] = avg_molecule_length
        else:
            pass
    else:  # currently sequencing
        pore[2] -= BPS
        sequenced_now = BPS if pore[2] >= 0 else (BPS + pore[2])  # handle last partial read
        pore[3] += sequenced_now

        # If molecule finished
        if pore[2] <= 0:
            pore[0] = False  # back to idle
            pore[2] = 0
    print(pore)