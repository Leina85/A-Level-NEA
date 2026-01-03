import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import pygame

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
    
    # plots three separate graphs showing standard and adaptive pore data over time.
    # graph 1: total bases sequenced
    # graph 2: target bases sequenced
    # graph 3: dead, sequencing and idle standard pores
    # graph 4: dead, sequencing and idle adaptive pores

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
    

    # --- graph 1: total bases sequenced ---
    fig1 = plt.figure(figsize=(3.8, 3.8))
    plt.plot(time_points, std_total_bases, label='Standard', color='blue')
    plt.plot(time_points, adp_total_bases, label='Adaptive', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Total Bases Sequenced')
    plt.title('Total Bases Sequenced')
    plt.xlim(0, total_runtime)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    graph1 = plot_to_surf(fig1)

    # --- graph 2: target bases sequenced ---
    fig2 = plt.figure(figsize=(3.8, 3.8))
    plt.plot(time_points, std_target_bases, label='Standard', color='blue')
    plt.plot(time_points, adp_target_bases, label='Adaptive', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Target Bases Sequenced')
    plt.title('Target Bases Sequenced')
    plt.xlim(0, total_runtime)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    graph2 = plot_to_surf(fig2)

    # --- graph 3: dead, sequencing and idle standard pores ---
    fig3 = plt.figure(figsize=(3.8, 3.8))
    plt.plot(time_points, std_dead, label='Dead', color='#F88378')
    plt.plot(time_points, std_seq, label='Sequencing', color='#AFD9AE', linewidth = 0.5)
    plt.plot(time_points, std_idle, label='Idle', color='#FFC107', linewidth = 0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Dead/Sequencing/Idle Standard Pores')
    plt.title('Dead/Sequencing/Idle Standard Pores')
    plt.xlim(0, total_runtime)
    plt.ylim(0, 100)  # maximum number of pores
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    graph3 = plot_to_surf(fig3)
    
    # --- graph 4: dead, sequencing and idle adaptive pores ---
    fig4 = plt.figure(figsize=(3.8, 3.8))
    plt.plot(time_points, adp_dead, label='Dead', color='#F88378')
    plt.plot(time_points, adp_seq, label='Sequencing', color='#AFD9AE', linewidth = 0.5)
    plt.plot(time_points, adp_idle, label='Idle', color='#FFC107', linewidth = 0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Dead/Sequencing/Idle Adaptive Pores')
    plt.title('Dead/Sequencing/Idle Adaptive Pores')
    plt.xlim(0, total_runtime)
    plt.ylim(0, 100)  # maximum number of pores
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    graph4 = plot_to_surf(fig4)
    
    analytics_graphs = [graph1, graph2, graph3, graph4]
    return analytics_graphs
    
def plot_to_surf(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    
    plt.close(fig)
    surface = pygame.image.load(buffer).convert_alpha()
    
    return surface