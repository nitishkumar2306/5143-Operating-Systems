from rich import print
import time

class Queue:
    """
    Queue class represents a basic First-In-First-Out (FIFO) data structure for managing Process Control Blocks (PCBs).

    Attributes:
    - queue: A list to store PCB objects in the order they are added.

    Methods:
    - __init__: Initializes an empty queue.
    - __str__: Converts the queue elements to a string for easy printing.
    - addPCB(pcb): Adds a Process Control Block (PCB) to the end of the queue.
    - removePCB(): Removes and returns the first PCB from the queue (FIFO).
    - length(): Returns the number of PCBs in the queue.
    - extend(lst): Extends the queue by appending PCBs from a list.
    - emptyq(): Clears the queue, making it empty.
    - sort_by_priority(): Sorts the PCB objects in the queue based on their priority.
    - returnPriority(): Returns the priority of the first PCB in the queue, or a default priority if the queue is empty.
"""
    def __init__(self):
        self.queue = []

    def __str__(self):
        s = " "
        s += "".join(self.queue) + " "
       # s += "".join([element.pid for element in self.queue])
        # s += "".join(str(self.pid)) + " "
        # s += "".join(str(self.bursts)) + "\n"
        return s

    def addPCB(self, pcb):
        self.queue.append(pcb)

    def removePCB(self):
        return self.queue.pop(0)

    def length(self):
        return len(self.queue)

    def extend(self, lst):
        self.queue.extend(lst)

    def emptyq(self):
        self.queue = []

    def sort_by_priority(self):
        # Sort the PCB objects in the queue based on their priority
        self.queue.sort(key=lambda pcb: pcb.priority)

    def returnPriority(self):
        if len(self.queue) > 0:
            return self.queue[0].priority[1]
        else:
            return 10


class NewQueue(Queue):
    """ Holds processes waiting for IO device
    """

    def __init__(self):
        super().__init__()


class ReadyQueue(Queue):
    """ Holds processes ready to run on cpu
    """

    def __init__(self):
        super().__init__()

    def incrementTime(self):
        for p in self.queue:
            p.CPUWaitTime += 1
            p.CPUWaitTime_cpy += 1


class WaitQueue(Queue):
    """ Holds processes waiting for IO device
    """

    def __init__(self):
        super().__init__()

    def incrementTime(self):
        for p in self.queue:
            p.IOWaitTime += 1


class TerminatedQueue(Queue):
    """ Holds  completed jobs
    """

    def __init__(self):
        super().__init__()


class SysClock:
    """
    SysClock class represents a system clock that maintains the global time across the simulation.

    Attributes:
    - _shared_state: Shared state dictionary among instances.
    - time: Represents the current time.

    Methods:
    - __init__: Initializes the shared state and initializes time if it doesn't exist.
    - increment: Increments the time by 1 second after a sleep.
    - getClock: Returns the current time.
"""
    _shared_state = {}  # Shared state dictionary

    def __init__(self):
        self.__dict__ = self._shared_state  # Share the state among instances
        if not hasattr(self, 'time'):
            self.time = 0  # Initialize the time if it doesn't exist

    def increment(self):
        #time.sleep(1)
        self.time += 1

    def getClock(self):
        return self.time


class CPU:
    """
    CPU class represents the central processing unit in the simulation.

    Attributes:
    - is_idle: Indicates whether the CPU is currently idle or processing a job.
    - current_job: Represents the job currently being processed.
    - total_execution_time: Represents the total execution time of the CPU.

    Methods:
    - __init__: Initializes the CPU with default values.
    - __str__: Returns a string representation of the CPU.
    - increment_execution_time: Increments the total execution time by 1.
    - load_job: Loads a job onto the CPU for processing.
    - complete_job: Checks if the current job is complete and returns it if so.
    - set_idle: Sets the CPU to idle state.
"""
    def __init__(self):
        self.is_idle = True
        self.current_job = None
        self.total_execution_time = 0

    def __str__(self):
        s = ""
        s += self.complete_job + " "
        return s

    def increment_execution_time(self):
        self.total_execution_time += 1

    def load_job(self, job):
        self.current_job = job
        self.is_idle = False

    def complete_job(self):
        if self.current_job.get_current_burst_time() == 0:
            completed_job = self.current_job
            # self.set_idle()
            return completed_job

    def set_idle(self):
        self.current_job = None
        self.is_idle = True


class IO:
    """
    IO class represents an Input/Output device in the simulation.

    Attributes:
    - is_idle: Indicates whether the IO device is currently idle or serving a job.
    - current_job: Represents the job currently being served by the IO device.
    - total_execution_time: Represents the total execution time of the IO device.

    Methods:
    - __init__: Initializes the IO device with default values.
    - increment_execution_time: Increments the total execution time by 1.
    - load_job: Loads a job onto the IO device for processing.
    - complete_job: Checks if the current job is complete and returns it if so.
    - set_idle: Sets the IO device to idle state.
"""
    def __init__(self) -> None:
        self.is_idle = True
        self.current_job = None
        self.total_execution_time = 0

    def increment_execution_time(self):
        self.total_execution_time += 1

    def load_job(self, job):
        self.current_job = job
        self.is_idle = False

    def complete_job(self):
        if self.current_job.get_current_burst_time() == 0:
            completed_job = self.current_job
            # self.set_idle()
            return completed_job

    def set_idle(self):
        self.current_job = None
        self.is_idle = True


class PCB:
    """
    PCB class represents a Process Control Block in the simulation.

    Attributes:
    - pid: Process ID.
    - priority: Priority level of the process.
    - arrivalTime: Time at which the process arrives in the system.
    - bursts: List of burst times required by the process.
    - currBurstType: Type of the current burst (e.g., 'CPU', 'IO').
    - currentBrust: Remaining time of the current burst.
    - CPUWaitTime: Time spent in the ready queue.
    - IOWaitTime: Time spent in the wait queue.
    - TurnAroundTime: Total time from start to finish for the process.
    - process_complete: Indicates whether the process has completed.
    - pendingBurst: List of burst times remaining to be processed.
    - terminate_back_count: Counter for terminating the process.
    - ready_cpu_wait: Time spent waiting in the ready queue for CPU.
    - wait_io_wait: Time spent waiting in the wait queue for IO.

    Methods:
    - __init__: Initializes the PCB with default values.
    - __str__: Returns a string representation of the PCB.
    - pending_brust: Updates the current burst and pending burst.
    - decrement_burst_time: Decrements the remaining time of the current burst.
    - get_current_burst_time: Returns the remaining time of the current burst.
    - released_process: Checks if the process has completed.
    - setPriority: Adjusts the priority of the process based on waiting times.
"""
    def __init__(self, pid, bursts, at, priority):
        self.pid = pid
        self.priority = priority
        self.arrivalTime = int(at)
        self.bursts = [int(burst) for burst in bursts]
        self.currBurstType = 'CPU'
        self.currentBrust = self.bursts[0] if len(self.bursts) > 1 else 0
        self.CPUWaitTime = 0
        self.CPUWaitTime_cpy = 0      # Time in ready queue
        self.IOWaitTime = 0           # Time in wait queue
        self.TurnAroundTime = 0       # Time from start to finish
        self.process_complete = False
        self.pendingBurst = self.bursts[1:] if len(self.bursts) > 1 else []
        self.terminate_back_count = 6
        self.ready_cpu_wait = 0
        self.wait_io_wait = 0
        self.priority_order = [f"p{i}" for i in range(1, 101)]

    def __str__(self):
        s = " "
        s += "".join(str(self.arrivalTime)) + " "
        s += "".join(str(self.pid)) + " "
        s += "".join(str(self.priority)) + " "
        s += "".join(str(self.currentBrust)) + " "
        s += "".join(str(self.bursts)) + " "
        s += "".join(str(self.pendingBurst)) + "\n"
        return s

    def pending_brust(self):
        if len(self.pendingBurst) >= 1:
            self.currentBrust = self.pendingBurst[0]
            if len(self.pendingBurst) > 1:
                self.pendingBurst = self.pendingBurst[1:]
            else:
                self.pendingBurst = []

        else:
            self.pendingBurst = []
            self.currentBrust = 0

    def decrement_burst_time(self):
        self.currentBrust -= 1

    def get_current_burst_time(self):
        return self.currentBrust

    def released_process(self):
        if len(self.pendingBurst) == 0:
            self.process_complete = True
        return self.process_complete

    def setPriority(self):
        # (current_priority_index) * 2:
        current_priority_index = self.priority_order.index(self.priority) + 1
        if current_priority_index <= len(self.priority_order):
            if current_priority_index == 2:
                if self.CPUWaitTime_cpy >= 6:
                    self.priority = "p1"
                    self.CPUWaitTime_cpy = 0
            elif current_priority_index > 2:
                if self.CPUWaitTime_cpy >= (current_priority_index + 2) * 2:
                    self.priority = self.priority_order[current_priority_index - 2]
                    self.CPUWaitTime_cpy = 0

