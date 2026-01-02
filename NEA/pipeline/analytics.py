import matplotlib.pyplot as plt
import pygame
import io
from PIL import Image

def add_data_point(graph_data, second, standard_flow_cell, adaptive_flow_cell):
    # time
    graph_data['time_points'].append(second)
    
    # standard pores
    std_total = sum(pore[3] for pore in standard_flow_cell)
    std_target = sum(pore[4] for pore in standard_flow_cell)
    std_dead = sum(1 for pore in standard_flow_cell if pore[1] == 0)
    std_seq = sum(1 for pore in standard_flow_cell if pore[0])
    std_idle = sum(1 for pore in standard_flow_cell if pore[0] == 0 and pore[1] > 0)
    
    graph_data['std_total_bases'].append(std_total)
    graph_data['std_target_bases'].append(std_target)
    graph_data['std_dead_pores'].append(std_dead)
    graph_data['std_sequencing_pores'].append(std_seq)
    graph_data['std_idle_pores'].append(std_idle)
    
    # adaptive pores
    adp_total = sum(pore[3] for pore in adaptive_flow_cell)
    adp_target = sum(pore[4] for pore in adaptive_flow_cell)
    adp_dead = sum(1 for pore in adaptive_flow_cell if pore[1] == 0)
    adp_seq = sum(1 for pore in adaptive_flow_cell if pore[0])
    adp_idle = sum(1 for pore in adaptive_flow_cell if pore[0] == 0 and pore[1] > 0)
    
    graph_data['adp_total_bases'].append(adp_total)
    graph_data['adp_target_bases'].append(adp_target)
    graph_data['adp_dead_pores'].append(adp_dead)
    graph_data['adp_sequencing_pores'].append(adp_seq)
    graph_data['adp_idle_pores'].append(adp_idle)

def display_graph(graph_data, total_runtime):
    
    #Plots three separate graphs showing standard and adaptive pore data over time.
    #Graph 1: Total bases sequenced
    #Graph 2: Target bases sequenced
    #Graph 3: Dead, Sequencing and Idle pores

    # extract data from graph_data
    time_points = graph_data['time_points']

    std_total_bases = graph_data['std_total_bases']
    adp_total_bases = graph_data['adp_total_bases']

    std_target_bases = graph_data['std_target_bases']
    adp_target_bases = graph_data['adp_target_bases']

    std_dead = graph_data['std_dead_pores']
    std_seq = graph_data['std_sequencing_pores']
    std_idle = graph_data['std_idle_pores']
    adp_dead = graph_data['adp_dead_pores']
    adp_seq = graph_data['adp_sequencing_pores']
    adp_idle = graph_data['adp_idle_pores']
    

    # --- Graph 1: Total bases sequenced ---
    plt.figure(figsize=(5, 5))
    plt.plot(time_points, std_total_bases, label='Standard', color='blue')
    plt.plot(time_points, adp_total_bases, label='Adaptive', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Total Bases Sequenced')
    plt.title('Total Bases Sequenced Over Time')
    plt.xlim(0, total_runtime)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Graph 2: Target bases sequenced ---
    plt.figure(figsize=(5, 5))
    plt.plot(time_points, std_target_bases, label='Standard', color='blue')
    plt.plot(time_points, adp_target_bases, label='Adaptive', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Target Bases Sequenced')
    plt.title('Target Bases Sequenced Over Time')
    plt.xlim(0, total_runtime)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Graph 3: Dead, Sequencing and Idle pores ---
    plt.figure(figsize=(5, 5))
    plt.plot(time_points, std_dead, label='Standard Dead', color='#F88378')
    plt.plot(time_points, std_seq, label='Standard Sequencing', color='#AFD9AE')
    plt.plot(time_points, std_idle, label='Standard Idle', color='#FFC107')
    plt.plot(time_points, adp_dead, label='Adaptive Dead', color='#F88378', linestyle='--')
    plt.plot(time_points, adp_seq, label='Adaptive Sequencing', color='#AFD9AE', linestyle='--')
    plt.plot(time_points, adp_idle, label='Adaptive Idle', color='#FFC107', linestyle='--')
    plt.xlabel('Time (s)')
    plt.ylabel('Dead/Sequencing/Idle Pores')
    plt.title('Dead/Sequencing/Idle Pores Over Time')
    plt.xlim(0, total_runtime)
    plt.ylim(0, 100)  # Maximum number of pores
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()