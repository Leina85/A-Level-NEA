import numpy as np

# Constant Parameters
MEAN = 7472.521
STD_DEV = 3024.544
BPS = 450
DNA_FOUND_CHANCE = 0.5632678551

# User Inputted Parameters
runtime = int(input('Enter runtime: '))
avg_molecule_length = int(input('Enter Average Molecule Length: '))
target_fraction = float(input('Enter fraction of target molecules to enrich (Decimal): '))

# Pore Organisation
num_adaptive = 100
num_standard = 100
total_pores = num_standard + num_adaptive

# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced]
standard_pore = np.array([False, 0, 0, 0, 0], dtype=object)
# [sequencing/not, idle seconds until death, bases remaining of current molecule, total bases sequenced, total target bases sequenced, target/non target]
adaptive_pore = np.array([False, 0, 0, 0, 0, False], dtype=object)

# Generate random numbers
idle_seconds_until_death = np.random.normal(MEAN, STD_DEV, total_pores).astype(int)
idle_seconds_until_death = np.clip(idle_seconds_until_death, 1, None)

standard_flow_cell = np.array([], dtype=object)
adaptive_flow_cell = np.array([], dtype=object)

# Fill standard flow cell
for i in range(num_standard):
    pore = standard_pore.copy()
    pore[1] = int(idle_seconds_until_death[i])
    standard_flow_cell = np.append(standard_flow_cell, [pore])

# Fill adaptive flow cell
for i in range(num_standard, total_pores):
    pore = adaptive_pore.copy()
    pore[1] = int(idle_seconds_until_death[i])
    adaptive_flow_cell = np.append(adaptive_flow_cell, [pore])

# Master flow cell structure
flow_cell = np.array([standard_flow_cell, adaptive_flow_cell], dtype=object)

def generate_length():
    return int(max(1, round(np.random.normal(avg_molecule_length, np.sqrt(avg_molecule_length)))))
            
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