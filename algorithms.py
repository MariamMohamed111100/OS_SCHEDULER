import random
import numpy as np
import matplotlib.pyplot as plt
from utils import draw_gantt_chart, print_table

def round_robin(processes, arrival_time, burst_time, quantum):
    n = len(processes)
    remaining_time = burst_time[:]
    completion_time = [0] * n
    t = 0
    done = [False] * n
    ready_queue = []
    visited = [False] * n
    complete = 0
    execution_log = []

    while complete < n:
        for i in range(n):
            if arrival_time[i] <= t and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if not ready_queue:
            t += 1
            continue

        idx = ready_queue.pop(0)
        exec_start = t

        if remaining_time[idx] > quantum:
            t += quantum
            remaining_time[idx] -= quantum
        else:
            t += remaining_time[idx]
            completion_time[idx] = t
            remaining_time[idx] = 0
            done[idx] = True
            complete += 1
        
        exec_end = t
        execution_log.append((processes[idx], exec_start, exec_end))

        for i in range(n):
            if arrival_time[i] <= t and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if remaining_time[idx] > 0:
            ready_queue.append(idx)

    return completion_time, execution_log

def fcfs(processes, arrival_time, burst_time):
    n = len(processes)
    completion_time = [0] * n
    t = 0
    order = sorted(range(n), key=lambda i: arrival_time[i])

    execution_log = []
    for i in order:
        start_time = max(t, arrival_time[i])  # Ensure process starts at arrival time
        t = start_time + burst_time[i]
        completion_time[i] = t
        execution_log.append((processes[i], start_time, t))  # Log process execution
    
    return completion_time, execution_log

def priority_non_preemptive(processes, arrival_time, burst_time, priorities):
    n = len(processes)
    completion_time = [0] * n
    visited = [False] * n
    t = 0
    complete = 0

    execution_log = []
    while complete < n:
        available = [i for i in range(n) if arrival_time[i] <= t and not visited[i]]
        if not available:
            t += 1
            continue
        
        idx = max(available, key=lambda i: priorities[i])
        start_time = max(t, arrival_time[idx])  # Ensure process starts at arrival time
        t = start_time + burst_time[idx]
        completion_time[idx] = t
        visited[idx] = True
        execution_log.append((processes[idx], start_time, t))  # Log process execution
        complete += 1

    return completion_time, execution_log

def sjf_preemptive(processes, arrival_time, burst_time):
    n = len(processes)
    remaining_time = burst_time.copy()
    completion_time = [0] * n
    current_time = 0
    complete = 0
    last_process = -1
    start_time = 0

    execution_log = []
    while complete < n:
        available = [i for i in range(n) if arrival_time[i] <= current_time and remaining_time[i] > 0]
        
        if not available:
            current_time += 1
            continue
        
        idx = min(available, key=lambda i: (remaining_time[i], arrival_time[i], i))
        
        if idx != last_process:
            if last_process != -1 and remaining_time[last_process] > 0:
                execution_log.append((processes[last_process], start_time, current_time))
            start_time = current_time
            last_process = idx
        
        remaining_time[idx] -= 1
        current_time += 1
        
        if remaining_time[idx] == 0:
            execution_log.append((processes[idx], start_time, current_time))
            completion_time[idx] = current_time
            complete += 1
            last_process = -1

    return completion_time, execution_log 