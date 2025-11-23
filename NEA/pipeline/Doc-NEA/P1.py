import numpy as np

# Specify parameters
mean = 7472.521
std_dev = 3024.544
n = 10

BPS = 450
DNA_FOUND_CHANCE = 0.5632678551

# Generate random numbers
idle_seconds_until_death = np.random.normal(mean, std_dev, n).astype(int)
idle_seconds_until_death = np.clip(idle_seconds_until_death, 1, None)

# Display the generated number
print(idle_seconds_until_death)

runtime = int(input('Enter runtime: '))
avg_molecule_length = int(input('Enter Average Molecule Length: '))
target_fraction = float(input('Enter fraction of target molecules to enrich (Decimal): '))

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced]
standard_pore = [False, int(idle_seconds_until_death[0]), 0, 0, 0]
print('standard: ', standard_pore)

for second in range(runtime):
    if standard_pore[1] > 0:     
        if not standard_pore[0]:  # idle
            is_DNA_found = np.random.random() < DNA_FOUND_CHANCE
            if is_DNA_found:  # found DNA
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

# Generate random numbers
idle_seconds_until_death = np.random.normal(mean, std_dev, n).astype(int)
idle_seconds_until_death = np.clip(idle_seconds_until_death, 1, None)

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced, target/non target]
adaptive_pore = [False, int(idle_seconds_until_death[0]), 0, 0, 0, False]
print('adpative: ', adaptive_pore)

for second in range(runtime):
    if adaptive_pore[1] > 0:
        if not adaptive_pore[0]:  # idle
            is_DNA_found = np.random.random() < DNA_FOUND_CHANCE
            if is_DNA_found:  # found DNA
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
                
print('standard: ', standard_pore)
print('adpative: ', adaptive_pore)