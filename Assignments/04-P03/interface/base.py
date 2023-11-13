from utils.utils import CPU, IO, SysClock, PCB, NewQueue, ReadyQueue, WaitQueue, TerminatedQueue
from ui.ui_print import OverallStat
from datetime import datetime
import os


class Simulator:
    """The Simulator class serves as a process scheduling simulation framework. It initializes with key parameters such as the data 
       file path, CPU and IO counts, time slice, and scheduler type. The class manages various queues, CPUs, IO devices, and simulation 
       parameters to facilitate process execution and data recording
"""
    def __init__(self, datfile, cpuCount, ioCount, time_slice, kind):
        self.kind = kind
        current_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.datfile = datfile
        self.new = NewQueue()
        self.wait = WaitQueue()
        self.ready = ReadyQueue()
        self.terminated = TerminatedQueue()
        self.cpuCount = cpuCount
        self.ioCount = ioCount
        self.running = self.create_cpus()
        self.io = self.create_io()
        self.readData()
        self.total_processes = self.new.length()
        self.terminated_process_count = 0
        self.clock = SysClock()
        self.time_slice = time_slice
        self.time_slice_copy = time_slice
        self.total_tat = 0
        self.total_rwt = 0
        self.total_iwt = 0
        self.message = []
        # 'a' appends to the file, create if not exists
        file_name=kind+"_"+str(self.cpuCount)+"_"+str(self.ioCount)+"_"+self.datfile.split("/")[-1]
        self.message_file = self.open_file("message_"+file_name)
        self.job_stats_file = self.open_file("job_stats_"+file_name)
        self.overall_stats_file = self.open_file(  "overall_stats_"+file_name)
       # self.header_file = self.open_file("header_"+kind+"_"+current_time, 'a')
        self.header_written = False
        self.priority_req = False

    def create_cpus(self):
        cpu_list = []
        for i in range(self.cpuCount):
            cpu_list.append(CPU())
        return cpu_list

    def create_io(self):
        io_list = []
        for i in range(self.ioCount):
            io_list.append(IO())
        return io_list

    def __str__(self):
        s = ""
        s += "datfile: " + self.datfile + "\n"
        s += "new queue:\n" + "".join(str(pcb)
                                      for pcb in self.new.queue) + "\n"
        s += "wait:\n" + "".join(str(pcb) for pcb in self.wait.queue) + "\n"
        return s

    def condition_to_run(self):
        return self.terminated_process_count != self.total_processes

    def readData(self):
        try:
            with open(self.datfile) as f:
                self.data = f.read().split("\n")

            for process in self.data:
                if len(process) > 0:
                    parts = process.split(' ')
                    arrival = parts[0]
                    pid = parts[1]
                    priority = parts[2]
                    bursts = parts[3:]

                    self.new.addPCB(PCB(pid, bursts, arrival, priority))
        except FileNotFoundError:
            print(f"No such file or directory: {self.datfile}")

    def move_new_ready(self):
        ready_processes = [process for process in self.new.queue if int(
            process.arrivalTime) == self.clock.getClock()]
        for process in ready_processes:
           # print(f"At time: {self.clock.getClock()} job [ pid_{process.pid} {process.get_current_burst_time()}] entered ready queue \n")
            self.message.append(
                f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{process.pid}[/bold gold1] [bold green]{process.get_current_burst_time()}[/bold green]] [cyan]entered ready queue[/cyan] \n")
            self.ready.addPCB(process)
            self.new.queue.remove(process)
        if self.priority_req:
            self.ready.sort_by_priority()

    def ready_to_running(self):
        i = 1
        for cpu in self.running:
            # load one PCB to ech CPU from ready and remove from ready
            if cpu.is_idle and len(self.ready.queue):
                self.time_slice = self.time_slice_copy
                cpu.load_job(self.ready.removePCB())
                self.message.append(
                    f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained CPU_{i}[/cyan] \n")
            i += 1

    def waiting_to_io(self):
        i = 1
        for io in self.io:
            # load one IO to ech IO  from ready and remove from wait
            if io.is_idle and len(self.wait.queue):
                io.load_job(self.wait.removePCB())
                # print(f"At time: {self.clock.getClock()} job [ pid_{io.current_job.pid} {io.current_job.get_current_burst_time()}] obtained IO_{i} \n")
                self.message.append(
                    f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{io.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained IO_{i}[/cyan] \n")
            i += 1

    def printQueues(self):
        print("New Queue:")
        for pcb in self.new.queue:
            print(pcb)  # Assuming PCB objects have a meaningful __str__ method
        print("\nReady Queue:")
        for pcb in self.ready.queue:
            print(pcb)
        print("\nRunning Queue:")
        for cpu in self.running:
            print(cpu.current_job)
        print("\nwaiting Queue:")
        for pcb in self.wait.queue:
            print(pcb)
        print("\nIO Queue:")
        for io in self.io:
            print(io.current_job)
        print("\nTerminated Queue:")
        for pcb in self.terminated.queue:
            print(pcb)

    def cal_stat(self):
        # ATAT ARWT AIWT CPU_utilization IO_utilization
        total_io_uti_time = 0
        for io in self.io:
            total_io_uti_time += io.total_execution_time

        total_cp_uti_time = 0
        for cpu in self.running:
            total_cp_uti_time += cpu.total_execution_time

        ATAT = self.total_tat/self.terminated_process_count
        ARWT = self.total_rwt/self.terminated_process_count
        AIWT = self.total_iwt/self.terminated_process_count
        cpu_util = (total_cp_uti_time /
                    (self.clock.getClock()*self.cpuCount))*100
        io_util = (total_io_uti_time/(self.clock.getClock()*self.ioCount))*100
        # print(f"ATAT= {ATAT} ARWT={ARWT} AIWT= {AIWT} cpu_util= {cpu_util} io_util={io_util}" )
        overall_stat = OverallStat(ATAT, ARWT, AIWT, cpu_util, io_util)
        overall_stat.display_table()
        self.write_stat_overall(f'{ATAT},{ARWT},{AIWT},{cpu_util},{io_util}')

    def write_message(self, message):
        for msg in message:
            self.message_file.write(msg)

    def write_stat(self, stat):
        if not self.header_written:
            # Write the header
            # ST = Time entered system
            # TAT = Turn Around Time (time exited system - time entered)
            # RWT = Time spent in ready queue
            # IWT = Time spent in wait queue
            header = "Pid,ST,TAT,RWT,IWT\n"
            self.job_stats_file.write(header)
            # Set the flag to True to indicate that the header has been written
            self.header_written = True
        self.job_stats_file.write(stat)

    def write_stat_overall(self, overall_stat):
        self.overall_stats_file.write("ATAT,ARWT,AIWT,CPU_UTIL,IO_UTIL\n")
        self.overall_stats_file.write(overall_stat)

    # def write_header_file(self):
    #     self.header_file.write("File_Name,CPU_Count,IO_Count\n")
    #     self.header_file.write(
    #         f'{self.datfile},{self.cpuCount},{self.ioCount}\n')

    def close_files(self):
        self.message_file.close()
        self.job_stats_file.close()
        self.overall_stats_file.close()
       # self.header_file.close()
    def open_file(self,file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        return open(file_name, 'a')    

