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
    std_alive = sum(1 for pore in standard_flow_cell if pore[1] > 0)
    std_seq = sum(1 for pore in standard_flow_cell if pore[0])
    
    graph_data['std_total_bases'].append(std_total)
    graph_data['std_target_bases'].append(std_target)
    graph_data['std_alive_pores'].append(std_alive)
    graph_data['std_sequencing_pore_num'].append(std_seq)
    
    # adaptive pores
    adp_total = sum(pore[3] for pore in adaptive_flow_cell)
    adp_target = sum(pore[4] for pore in adaptive_flow_cell)
    adp_alive = sum(1 for pore in adaptive_flow_cell if pore[1] > 0)
    adp_seq = sum(1 for pore in adaptive_flow_cell if pore[0])
    
    graph_data['adp_total_bases'].append(adp_total)
    graph_data['adp_target_bases'].append(adp_target)
    graph_data['adp_alive_pores'].append(adp_alive)
    graph_data['adp_sequencing_pore_num'].append(adp_seq)

def display_graph(graph_data, total_runtime):
    """
    Plots three separate graphs showing standard and adaptive pore data over time.

    Graph 1: Total bases sequenced
    Graph 2: Target bases sequenced
    Graph 3: Alive pores
    """

    # extract data from graph_data
    time_points = graph_data['time_points']

    std_total_bases = graph_data['std_total_bases']
    adp_total_bases = graph_data['adp_total_bases']

    std_target_bases = graph_data['std_target_bases']
    adp_target_bases = graph_data['adp_target_bases']

    std_alive = graph_data['std_alive_pores']
    adp_alive = graph_data['adp_alive_pores']

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

    # --- Graph 3: Alive pores ---
    plt.figure(figsize=(5, 5))
    plt.plot(time_points, std_alive, label='Standard', color='blue')
    plt.plot(time_points, adp_alive, label='Adaptive', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Alive Pores')
    plt.title('Alive Pores Over Time')
    plt.xlim(0, total_runtime)
    plt.ylim(0, 100)  # Maximum number of pores
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
