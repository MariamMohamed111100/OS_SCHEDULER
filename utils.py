import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

def get_random_color():
    return "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

def draw_gantt_chart(title, execution_log, frame):
    fig, ax = plt.subplots(figsize=(12, 3))
    current_y = 10
    process_colors = {}
    patches = []  # For storing legend patches

    for process_id, start, end in execution_log:
        if process_id not in process_colors:
            process_colors[process_id] = get_random_color()

    for process_id, start, end in execution_log:
        color = process_colors[process_id]
        ax.broken_barh([(start, end - start)], (current_y, 9), facecolors=color, edgecolors='black')
        ax.text((start + end) / 2, current_y + 4.5, f"P{process_id}", 
                ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        ax.text(start, current_y - 1.5, f"{start}", ha='center', va='top', fontsize=9)

        if not any(patch.get_label() == f"P{process_id}" for patch in patches):
            patches.append(plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10, label=f"P{process_id}"))

    last_end = execution_log[-1][2]
    ax.text(last_end, current_y - 1.5, f"{last_end}", ha='center', va='top', fontsize=9)

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f"Gantt Chart - {title}")
    ax.set_xlim(0, last_end + 1)
    ax.set_ylim(5, 25)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(handles=patches, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

def print_table(algorithm, processes, arrival_time, burst_time, completion_time, frame):
    n = len(processes)
    turnaround_time = [completion_time[i] - arrival_time[i] for i in range(n)]
    waiting_time = [turnaround_time[i] - burst_time[i] for i in range(n)]

    # Create table frame
    table_frame = tk.Frame(frame)
    table_frame.pack(side=tk.LEFT, padx=10)

    tree = ttk.Treeview(table_frame, columns=("Process", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"), show="headings")
    tree.heading("Process", text="Process")
    tree.heading("Arrival", text="Arrival")
    tree.heading("Burst", text="Burst")
    tree.heading("Completion", text="Completion")
    tree.heading("Turnaround", text="Turnaround")
    tree.heading("Waiting", text="Waiting")

    # Insert data rows
    for i in range(n):
        tree.insert("", tk.END, values=(f"P{processes[i]}", arrival_time[i], burst_time[i], completion_time[i], turnaround_time[i], waiting_time[i]))

    tree.pack(side=tk.LEFT, padx=10, pady=10)

    avg_tat = sum(turnaround_time) / n
    avg_wt = sum(waiting_time) / n

    avg_label = tk.Label(frame, text=f"Average Turnaround Time = {avg_tat:.1f}\nAverage Waiting Time = {avg_wt:.1f}")
    avg_label.pack(side=tk.LEFT, padx=10)

def generate_random_processes(n, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda):
    processes = [i+1 for i in range(n)]
    arrival_time = [max(0, int(random.gauss(arrival_mean, arrival_std))) for _ in range(n)]
    arrival_time.sort()  # Ensure processes arrive in order
    burst_time = [max(1, int(random.gauss(burst_mean, burst_std))) for _ in range(n)]
    priorities = [np.random.poisson(priority_lambda) for _ in range(n)]
    return processes, arrival_time, burst_time, priorities

def read_parameters_from_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        n = int(lines[0])
        arrival_mean, arrival_std = map(float, lines[1].split())
        burst_mean, burst_std = map(float, lines[2].split())
        priority_lambda = float(lines[3])
    return n, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda 