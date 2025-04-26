class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def __str__(self):
        return f"Process {self.pid}: Arrival={self.arrival_time}, Burst={self.burst_time}, Priority={self.priority}"

class ExecutionLog:
    def __init__(self):
        self.log = []

    def add_entry(self, process_id, start_time, end_time):
        self.log.append((process_id, start_time, end_time))

    def get_log(self):
        return self.log 