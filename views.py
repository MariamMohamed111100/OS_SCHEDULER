import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import round_robin, fcfs, priority_non_preemptive, sjf_preemptive
from utils import get_random_color, draw_gantt_chart, print_table, generate_random_processes

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms")

        # Initialize frames
        self.input_frame = tk.Frame(self.root)
        self.algo_frame = tk.Frame(self.root)
        self.output_frame = tk.Frame(root)
        self.gantt_frame = tk.Frame(self.output_frame)
        self.table_frame = tk.Frame(self.output_frame)
        self.avg_frame = tk.Frame(self.output_frame)

        # Set theme
        self.theme = "light"  # Can be "light" or "dark"
        if self.theme == "dark":
            self.set_dark_mode()
        else:
            self.set_light_mode()

        # Add theme toggle button
        self.theme_button = tk.Button(self.root, text="🌙 Dark Mode", command=self.toggle_theme,
                                    font=("Arial", 12), bg=self.button_bg, fg=self.button_fg, relief="flat")
        self.theme_button.pack(pady=5)

        # Pack frames
        self.input_frame.pack(pady=10, fill=tk.X, padx=20)
        self.algo_frame.pack(pady=10)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        self.gantt_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.avg_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add input fields
        self.n_entry = self.add_label_entry(self.input_frame, "Enter number of processes:")
        self.arrival_mean_entry = self.add_label_entry(self.input_frame, "Enter arrival mean:")
        self.arrival_std_entry = self.add_label_entry(self.input_frame, "Enter arrival std dev:")
        self.burst_mean_entry = self.add_label_entry(self.input_frame, "Enter burst mean:")
        self.burst_std_entry = self.add_label_entry(self.input_frame, "Enter burst std dev:")
        self.priority_lambda_entry = self.add_label_entry(self.input_frame, "Enter priority lambda:")

        # Add buttons
        self.load_file_button = tk.Button(self.input_frame, text="Load Data from File", 
                                        command=self.load_data_from_file,
                                        font=("Arial", 12), bg=self.button_bg, fg=self.button_fg, relief="flat")
        self.load_file_button.pack(pady=10)

        # Algorithm selection
        tk.Label(self.algo_frame, text="Choose scheduling algorithm:", 
                font=("Arial", 13, "bold"), bg=self.bg_color, fg=self.fg_color).pack()

        self.algorithm_var = tk.StringVar(value="FCFS")
        for algo in ["FCFS", "Round Robin", "Priority Non-Preemptive", "SJF Preemptive"]:
            rb = tk.Radiobutton(self.algo_frame, text=algo, variable=self.algorithm_var, value=algo,
                              font=("Arial", 12), bg=self.bg_color, fg=self.fg_color, anchor="w",
                              selectcolor=self.radio_color)
            rb.pack(anchor="w")

        self.quantum_entry = self.add_label_entry(self.algo_frame, "Enter quantum (if Round Robin)")

        # Action buttons
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm,
                                  font=("Arial", 12, "bold"), bg=self.button_bg, fg=self.button_fg, relief="flat")
        self.run_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_processes,
                                    font=("Arial", 12, "bold"), bg="orange", fg="white", relief="flat")
        self.reset_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Processes to File", 
                                   command=self.save_processes_to_file,
                                   font=("Arial", 12, "bold"), bg=self.button_bg, fg=self.button_fg, relief="flat")
        self.save_button.pack(pady=10)

        self.compare_button = tk.Button(root, text="Compare Algorithms", 
                                     command=self.compare_algorithms,
                                     font=("Arial", 12, "bold"), bg=self.button_bg, fg=self.button_fg, relief="flat")
        self.compare_button.pack(pady=10)

        # Initialize process data
        self.generated_processes = []
        self.generated_arrival = []
        self.generated_burst = []
        self.generated_priorities = []

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.theme_button.config(text="☀️ Light Mode")
            self.set_dark_mode()
        else:
            self.theme = "light"
            self.theme_button.config(text="🌙 Dark Mode")
            self.set_light_mode()

    def set_dark_mode(self):
        self.bg_color = "#2e2e2e"
        self.fg_color = "#f5f5f5"
        self.entry_bg = "#333333"
        self.entry_border = "#444444"
        self.button_bg = "#444444"
        self.button_fg = "#f5f5f5"
        self.radio_color = "#2e2e2e"

        self.root.configure(bg=self.bg_color)
        self.input_frame.configure(bg=self.bg_color)
        self.algo_frame.configure(bg=self.bg_color)
        self.output_frame.configure(bg=self.bg_color)
        self.gantt_frame.configure(bg=self.bg_color)
        self.table_frame.configure(bg=self.bg_color)
        self.avg_frame.configure(bg=self.bg_color)

        # Update all widgets recursively
        self.update_widget_colors(self.root, dark=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=self.bg_color, foreground=self.fg_color, rowheight=30,
                       fieldbackground=self.bg_color, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#444444", foreground=self.fg_color)
        style.map('Treeview', background=[('selected', '#555555')])

    def set_light_mode(self):
        self.bg_color = "#f0f4f8"
        self.fg_color = "black"
        self.entry_bg = "white"
        self.entry_border = "#ccc"
        self.button_bg = "#3b82f6"
        self.button_fg = "white"
        self.radio_color = "#f0f4f8"

        self.root.configure(bg=self.bg_color)
        self.input_frame.configure(bg=self.bg_color)
        self.algo_frame.configure(bg=self.bg_color)
        self.output_frame.configure(bg=self.bg_color)
        self.gantt_frame.configure(bg=self.bg_color)
        self.table_frame.configure(bg=self.bg_color)
        self.avg_frame.configure(bg=self.bg_color)

        # Update all widgets recursively
        self.update_widget_colors(self.root, dark=False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=30,
                       fieldbackground="white", font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3b82f6", foreground="white")
        style.map('Treeview', background=[('selected', '#c7dfff')])

    def update_widget_colors(self, widget, dark):
        # Recursively update widget colors
        for child in widget.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.bg_color)
                self.update_widget_colors(child, dark)
            elif isinstance(child, tk.Label):
                child.configure(bg=self.bg_color, fg=self.fg_color)
            elif isinstance(child, tk.Entry):
                child.configure(bg=self.entry_bg, fg=self.fg_color if dark else "black", insertbackground=self.fg_color if dark else "black")
            elif isinstance(child, tk.Button):
                child.configure(bg=self.button_bg, fg=self.button_fg, activebackground=self.button_bg, activeforeground=self.button_fg)
            elif isinstance(child, tk.Radiobutton):
                child.configure(bg=self.radio_color, fg=self.fg_color, selectcolor=self.radio_color, activebackground=self.radio_color, activeforeground=self.fg_color)

    def add_label_entry(self, parent, text):
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=5)

        label = tk.Label(frame, text=text, width=30, anchor="w", 
                        font=("Arial", 12), bg=self.bg_color, fg=self.fg_color)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(frame, font=("Arial", 12), bg=self.entry_bg, 
                        fg=self.fg_color if self.theme == "dark" else "black",
                        relief="flat", highlightbackground=self.entry_border, highlightthickness=1)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        return entry

    def load_data_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                try:
                    self.n_entry.delete(0, tk.END)
                    self.n_entry.insert(0, lines[0].strip())

                    arrival_values = lines[1].strip().split()
                    if len(arrival_values) >= 2:
                        self.arrival_mean_entry.delete(0, tk.END)
                        self.arrival_mean_entry.insert(0, arrival_values[0])
                        self.arrival_std_entry.delete(0, tk.END)
                        self.arrival_std_entry.insert(0, arrival_values[1])
                    else:
                        raise IndexError

                    burst_values = lines[2].strip().split()
                    if len(burst_values) >= 2:
                        self.burst_mean_entry.delete(0, tk.END)
                        self.burst_mean_entry.insert(0, burst_values[0])
                        self.burst_std_entry.delete(0, tk.END)
                        self.burst_std_entry.insert(0, burst_values[1])
                    else:
                        raise IndexError

                    self.priority_lambda_entry.delete(0, tk.END)
                    self.priority_lambda_entry.insert(0, lines[3].strip())

                except IndexError:
                    messagebox.showerror("Error", "File format is incorrect. Please ensure it has the correct number of lines.")

    def save_processes_to_file(self):
        if not self.generated_processes:
            messagebox.showwarning("Warning", "No process data to save. Please run an algorithm first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(f"{len(self.generated_processes)}\n")
                    file.write("Process\tArrival\tBurst\tPriority\n")
                    for i in range(len(self.generated_processes)):
                        file.write(f"P{self.generated_processes[i]}\t{self.generated_arrival[i]}"
                                 f"\t{self.generated_burst[i]}\t{self.generated_priorities[i]}\n")
                messagebox.showinfo("Success", "Process data saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def reset_processes(self):
        try:
            n = int(self.n_entry.get())
            arrival_mean = float(self.arrival_mean_entry.get())
            arrival_std = float(self.arrival_std_entry.get())
            burst_mean = float(self.burst_mean_entry.get())
            burst_std = float(self.burst_std_entry.get())
            priority_lambda = float(self.priority_lambda_entry.get())

            processes, arrival_time, burst_time, priorities = generate_random_processes(
                n, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda)

            self.generated_processes = processes
            self.generated_arrival = arrival_time
            self.generated_burst = burst_time
            self.generated_priorities = priorities

            messagebox.showinfo("Success", "Processes reset and regenerated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset processes: {e}")

    def run_algorithm(self):
        try:
            n = int(self.n_entry.get())
            arrival_mean = float(self.arrival_mean_entry.get())
            arrival_std = float(self.arrival_std_entry.get())
            burst_mean = float(self.burst_mean_entry.get())
            burst_std = float(self.burst_std_entry.get())
            priority_lambda = float(self.priority_lambda_entry.get())

            if not self.generated_processes:
                processes, arrival_time, burst_time, priorities = generate_random_processes(
                    n, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda)

                self.generated_processes = processes
                self.generated_arrival = arrival_time
                self.generated_burst = burst_time
                self.generated_priorities = priorities
            else:
                processes = self.generated_processes
                arrival_time = self.generated_arrival
                burst_time = self.generated_burst
                priorities = self.generated_priorities

            algorithm = self.algorithm_var.get()

            if algorithm == "Round Robin":
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    messagebox.showerror("Error", "Quantum must be greater than 0 for Round Robin.")
                    return
                completion_time, execution_log = round_robin(processes, arrival_time, burst_time, quantum)
            elif algorithm == "FCFS":
                completion_time, execution_log = fcfs(processes, arrival_time, burst_time)
            elif algorithm == "Priority Non-Preemptive":
                completion_time, execution_log = priority_non_preemptive(processes, arrival_time, burst_time, priorities)
            elif algorithm == "SJF Preemptive":
                completion_time, execution_log = sjf_preemptive(processes, arrival_time, burst_time)

            result_window = tk.Toplevel(self.root)
            result_window.title(f"Results - {algorithm}")
            result_window.geometry("800x600")

            gantt_frame = tk.Frame(result_window)
            gantt_frame.pack(pady=10)

            table_frame = tk.Frame(result_window)
            table_frame.pack(pady=10)

            avg_frame = tk.Frame(result_window)
            avg_frame.pack(pady=10)

            draw_gantt_chart(algorithm, execution_log, gantt_frame)
            self.display_table_and_averages(processes, arrival_time, burst_time, completion_time, table_frame, avg_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def display_table_and_averages(self, processes, arrival_time, burst_time, completion_time, table_frame, avg_frame):
        n = len(processes)
        turnaround_time = [completion_time[i] - arrival_time[i] for i in range(n)]
        waiting_time = [turnaround_time[i] - burst_time[i] for i in range(n)]

        # Style for the Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Create the Treeview frame
        tree_frame = tk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame,
                           columns=("Process", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"),
                           show="headings")

        # Configure columns
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data rows
        for i in range(n):
            tree.insert("", "end", values=(f"P{processes[i]}", arrival_time[i], burst_time[i],
                                         completion_time[i], turnaround_time[i], waiting_time[i]))

        # Adjust height based on number of rows
        rows_to_show = min(n, 20)
        tree.config(height=rows_to_show)

        tree.pack(fill=tk.BOTH, expand=True)

        # Calculate and display averages
        avg_tat = sum(turnaround_time) / n
        avg_wt = sum(waiting_time) / n

        avg_label = tk.Label(avg_frame,
                           text=f"Average Turnaround Time = {avg_tat:.2f}   |   Average Waiting Time = {avg_wt:.2f}",
                           font=("Arial", 14, "bold"))
        avg_label.pack(pady=10)

    def compare_algorithms(self):
        if not self.generated_processes:
            messagebox.showwarning("Warning", "No process data to compare. Please run or reset processes first.")
            return

        processes = self.generated_processes
        arrival_time = self.generated_arrival
        burst_time = self.generated_burst
        priorities = self.generated_priorities

        results = {}

        # FCFS
        ct, _ = fcfs(processes, arrival_time, burst_time)
        tat = [ct[i] - arrival_time[i] for i in range(len(processes))]
        wt = [tat[i] - burst_time[i] for i in range(len(processes))]
        results["FCFS"] = sum(wt) / len(processes)

        # Round Robin
        try:
            quantum = int(self.quantum_entry.get())
        except:
            quantum = 2  # Default quantum

        ct, _ = round_robin(processes, arrival_time, burst_time, quantum)
        tat = [ct[i] - arrival_time[i] for i in range(len(processes))]
        wt = [tat[i] - burst_time[i] for i in range(len(processes))]
        results["Round Robin"] = sum(wt) / len(processes)

        # Priority Non-Preemptive
        ct, _ = priority_non_preemptive(processes, arrival_time, burst_time, priorities)
        tat = [ct[i] - arrival_time[i] for i in range(len(processes))]
        wt = [tat[i] - burst_time[i] for i in range(len(processes))]
        results["Priority Non-Preemptive"] = sum(wt) / len(processes)

        # SJF Preemptive
        ct, _ = sjf_preemptive(processes, arrival_time, burst_time)
        tat = [ct[i] - arrival_time[i] for i in range(len(processes))]
        wt = [tat[i] - burst_time[i] for i in range(len(processes))]
        results["SJF Preemptive"] = sum(wt) / len(processes)

        # Sort algorithms by lowest average waiting time
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        best_algo, best_avg = sorted_results[0]

        # Create comparison window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Algorithm Comparison")
        chart_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(6, 4))
        algos = list(results.keys())
        values = list(results.values())
        colors = ['#3b82f6' if algo != best_algo else '#10b981' for algo in algos]

        ax.bar(algos, values, color=colors)
        ax.set_title("Average Waiting Time per Algorithm", fontsize=14)
        ax.set_ylabel("Average Waiting Time", fontsize=12)
        ax.set_xticks(range(len(algos)))
        ax.set_xticklabels(algos, rotation=30, ha='right')

        for i, v in enumerate(values):
            ax.text(i, v + 0.1, f"{v:.2f}", ha='center', fontsize=10)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Display best algorithm
        tk.Label(chart_window, text=f"Best Algorithm: {best_algo} (Avg WT = {best_avg:.2f})",
                font=("Arial", 16, "bold"), fg="green").pack(pady=10) 