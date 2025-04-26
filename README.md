# Process Scheduler

A CPU scheduling simulator with a graphical user interface that implements various scheduling algorithms.

## Features

### Multiple Scheduling Algorithms:
- **First Come First Serve (FCFS)**
- **Round Robin (RR)**
- **Preemptive Shortest Remaining Time First (SRTF/SJF Preemptive)**
- **Non-preemptive Priority Scheduling**

### Performance Metrics:
- Average Turnaround Time
- Average Waiting Time

## Project Structure

```
OS_SCHEDULER/
├── main.py          # Application entry point
├── algorithms.py    # Scheduling algorithm implementations
├── views.py         # GUI components
└── utils.py         # Helper functions
```

## Component Descriptions

### main.py
- Entry point for the application
- Initializes the main window and starts the application loop

### algorithms.py
- Contains implementations of all scheduling algorithms
- Each algorithm returns execution order and performance metrics

### views.py
- Contains all GUI components using tkinter
- MainWindow: Main application window
- ProcessInputFrame: Frame for process input parameters
- ResultsFrame: Frame for displaying scheduling results

### utils.py
- Helper functions for process generation and metrics calculation
- `generate_random_processes()`: Creates random processes for testing
- `calculate_metrics()`: Computes average turnaround and waiting times

## How to Use

### Setup:
- Ensure Python 3.6+ is installed
- Install required packages:
  ```bash
  pip install numpy matplotlib
  ```

### Running the Application:
- Navigate to the project directory
- Run:
  ```bash
  python main.py
  ```

### Using the GUI:
- Enter process details or generate random processes
- Select a scheduling algorithm
- Click "Run" to see the results
- View results in the results window

## Development
To extend the application:
- Add new algorithms to `algorithms.py`
- Create new GUI components in `views.py`
- Update the main window to include new features

## Team Contributions
- **Mohamed**
  - Developed the complete GUI from start to finish
  - Integrated and collected code from all team members
  - Managed the overall project structure and implementation
- **Nadine**
  - Implemented Round Robin (RR) algorithm
  - Implemented Preemptive Shortest Remaining Time First (SRTF) algorithm
- **Melissia**
  - Implemented Non-preemptive Priority Scheduling algorithm
- **Abdelrahman**
  - Implemented First Come First Serve (FCFS) algorithm

## Requirements
- Python 3.6+
- numpy
- matplotlib

## License

[Your chosen license] 