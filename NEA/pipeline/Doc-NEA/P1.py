import numpy as np
import matplotlib.pyplot as plt

def simulation(runtime, avg_molecule_length, target_fraction):
    
    # Constant Parameters
    MEAN = 7472.521
    STD_DEV = 3024.544
    BPS = 450
    DNA_FOUND_CHANCE = 0.5632678551
    INTERVAL_NUM = 100
    
    #convert percentage from input into decimal form
    target_fraction = target_fraction/100

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

    standard_flow_cell = []
    adaptive_flow_cell = []

    # fill standard flow cell
    for i in range(num_standard):
        pore = standard_pore.copy()
        pore[1] = int(idle_seconds_until_death[i])
        standard_flow_cell.append(pore)

    # fill adaptive flow cell
    for i in range(num_standard, total_pores):
        pore = adaptive_pore.copy()
        pore[1] = int(idle_seconds_until_death[i])
        adaptive_flow_cell.append(pore)

    # convert to numpy arrays with object dtype to preserve structure
    standard_flow_cell = np.array(standard_flow_cell, dtype=object)
    adaptive_flow_cell = np.array(adaptive_flow_cell, dtype=object)

    def generate_length():
        return int(max(1, round(np.random.normal(avg_molecule_length, np.sqrt(avg_molecule_length)))))

    update_interval = max(1, runtime // INTERVAL_NUM)

    for second in range(runtime):
        
        # for standard pores
        for i in range(num_standard):
            # loop through the 100 standard pores
            current_pore = standard_flow_cell[i]
            # seperates the array items into variables so the code is easier to follow than using indexes
            is_seq, idle_left, bases_left, total_seq, total_target = current_pore
            
            # checks if pore is still alive
            if idle_left > 0:

                # if pore is idle
                if not is_seq:
                    # check if DNA is found
                    if np.random.random() < DNA_FOUND_CHANCE:
                        is_seq = True
                        bases_left = generate_length()
                    else:
                        # still idle so one less second until pore died
                        idle_left -= 1

                # if pore is already sequencing
                else:
                    # next 450 bases are sequenced
                    bases_left -= BPS
                    
                    # adds the number of bases sequenced to the total (handles if the molecule had >450 bases remaining so the correct number is added)
                    sequenced_now = BPS if bases_left >= 0 else (BPS + bases_left)
                    total_seq += sequenced_now

                    # if molecule is finished sequencing (prevents negative values)
                    if bases_left <= 0:
                        is_seq = False
                        bases_left = 0

                # estimate target base count using target fraction
                total_target = int(round(total_seq * target_fraction))

            # write updated state back into the flow cell back in the array format
            standard_flow_cell[i] = np.array([is_seq, idle_left, bases_left, total_seq, total_target],dtype=object)

        # for adaptive pores
        for j in range(num_adaptive):

            # loop through the 100 adaptive pores
            pore = adaptive_flow_cell[j]
            # seperates the array items into variables so the code is easier to follow than using indexes
            is_seq, idle_left, bases_left, total_seq, total_target, is_target = pore

            # checks if pore is still alive
            if idle_left > 0:

                # if pore is idle
                if not is_seq:
                    # check if DNA is found
                    if np.random.random() < DNA_FOUND_CHANCE:
                        is_seq = True
                        bases_left = generate_length()
                        # determine if molecule is target
                        is_target = (np.random.random() < target_fraction)
                    else:
                        # still idle so one less second until pore died
                        idle_left -= 1

                # if pore is already sequencing
                else:
                    bases_left -= BPS
                    sequenced_now = BPS if bases_left >= 0 else (BPS + bases_left)
                    total_seq += sequenced_now

                    # if molecule is non target it is ejected
                    if not is_target:
                        is_seq = False
                        bases_left = 0
                    #if molecule is target then it is sequenced like the standard pore
                    else:
                        total_target += sequenced_now

                    # if target molecule finishes sequencing bases left is 0
                    if bases_left <= 0:
                        is_seq = False
                        bases_left = 0

            # write updated state back into the flow cell back in the array format
            adaptive_flow_cell[j] = np.array([is_seq, idle_left, bases_left, total_seq, total_target, is_target],dtype=object)

    print(standard_flow_cell[0], adaptive_flow_cell[0])
    return standard_flow_cell, adaptive_flow_cell

'''
print(standard_flow_cell[0], adaptive_flow_cell[0])
print(standard_flow_cell[99], adaptive_flow_cell[99])

# standard:
x = []
for i in range(num_standard):
    x.append(standard_flow_cell[i, 1])

plt.figure(figsize=(8, 5))
plt.hist(x, bins=10, density=True, alpha=0.7, color='skyblue')
plt.show()
plt.savefig('standard_idle_till_death_dist.png')

# adaptive:
x = []
for i in range(num_adaptive):
    x.append(adaptive_flow_cell[i, 1])

plt.figure(figsize=(8, 5))
plt.hist(x, bins=10, density=True, alpha=0.7, color='skyblue')
plt.show()
plt.savefig('adaptive_idle_till_death_dist.png')
'''