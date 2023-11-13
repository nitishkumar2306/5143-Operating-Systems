from interface.base import Simulator
from ui.ui_print import UI_Layout
from rich.live import Live

import time

# ██████╗░██████╗░██╗░█████╗░██████╗░██╗████████╗██╗░░░██╗  ██████╗░░█████╗░░██████╗███████╗██████╗░
# ██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗░██╔╝  ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
# ██████╔╝██████╔╝██║██║░░██║██████╔╝██║░░░██║░░░░╚████╔╝░  ██████╦╝███████║╚█████╗░█████╗░░██║░░██║
# ██╔═══╝░██╔══██╗██║██║░░██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░  ██╔══██╗██╔══██║░╚═══██╗██╔══╝░░██║░░██║
# ██║░░░░░██║░░██║██║╚█████╔╝██║░░██║██║░░░██║░░░░░░██║░░░  ██████╦╝██║░░██║██████╔╝███████╗██████╔╝
# ╚═╝░░░░░╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░  ╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═════╝░

# ░█████╗░██╗░░░░░░██████╗░░█████╗░██████╗░██╗████████╗██╗░░██╗███╗░░░███╗
# ██╔══██╗██║░░░░░██╔════╝░██╔══██╗██╔══██╗██║╚══██╔══╝██║░░██║████╗░████║
# ███████║██║░░░░░██║░░██╗░██║░░██║██████╔╝██║░░░██║░░░███████║██╔████╔██║
# ██╔══██║██║░░░░░██║░░╚██╗██║░░██║██╔══██╗██║░░░██║░░░██╔══██║██║╚██╔╝██║
# ██║░░██║███████╗╚██████╔╝╚█████╔╝██║░░██║██║░░░██║░░░██║░░██║██║░╚═╝░██║
# ╚═╝░░╚═╝╚══════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝
class PB(Simulator):
    """
        PB (Priority-Based) class is a simulator that implements a priority-based scheduling algorithm.

        Attributes:
        - datfile: Name of the datafile containing process information.
        - cpuCount: Number of CPUs available in the system.
        - ioCount: Number of I/O devices available in the system.
        - time_slice: Time quantum for round-robin scheduling (unused in this algorithm).
        - kind: Type of scheduling algorithm.
        - priority_req: Flag indicating whether the priority information is required (True for PB).
        - speed: Speed factor controlling the simulation speed.

        Methods:
        - __init__: Initializes the PB simulator with the provided parameters.
        - run: Executes the simulation loop for the priority-based scheduling algorithm, updating the UI and handling process states.
"""

    def __init__(self, datfile, cpuCount, ioCount, time_slice, kind, speed):
        super().__init__(datfile, cpuCount, ioCount, time_slice, kind)
        self.priority_req = True
        self.speed = speed

    def run(self):
        # make this condition in base class and just call it
        # terminated pop after tick

        with Live(UI_Layout(self.new.queue, self.ready.queue, self.running, self.wait.queue, self.io,
                            self.terminated.queue, self.clock.getClock(), self.message, self.total_processes, self.terminated_process_count, self.cpuCount, self.ioCount, self.kind), refresh_per_second=10) as live:
            while self.condition_to_run():  # todo no ready but running in cpur or io or waiting
                time.sleep(self.speed)
                # time.sleep(1)
                # vertical_overflow= todo
                self.message = []
                self.move_new_ready()
                self.ready.incrementTime()
                for p in self.ready.queue:
                    p.setPriority()
                if len(self.ready.queue) > 0:
                    self.ready_to_running()
                i = 1
                for cpu in self.running:
                    if not cpu.is_idle:
                        """ get current CPU brust 
                            Decrement time for that brust 
                            Add excution time for cal runninng time
                            check time_silce :   "Job {cpu.runningPCB.pid}: preempted"")
                            and move to ready stat 
                            if all brust compelted so move to terminate 
                            else run wait and IO
                        """
                        cpu.increment_execution_time()
                        # if (int(self.ready.returnPriority()) > int(cpu.current_job.priority[1])) and self.time_slice > 0:
                        if (int(self.ready.returnPriority()) >= int(cpu.current_job.priority[1])):
                            cpu.current_job.decrement_burst_time()
                            complete_job = cpu.complete_job()
                            self.message.append(
                                f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]is running in CPU_{i}[/cyan] \n")

                            if complete_job:
                                complete_job.pending_brust()
                                if complete_job.released_process():  # all brust complete so terminated
                                    self.terminated.addPCB(complete_job)
                                    complete_job.TurnAroundTime = self.clock.getClock() - complete_job.arrivalTime
                                    self.terminated_process_count += 1
                                    self.total_tat += complete_job.TurnAroundTime
                                    self.total_rwt += complete_job.CPUWaitTime
                                    self.total_iwt += complete_job.IOWaitTime
                                    self.message.append(
                                        f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] {complete_job.get_current_burst_time()}] [red]terminated[/red]\n")
                                    self.write_stat(
                                        (f'{complete_job.pid},{complete_job.arrivalTime},{complete_job.TurnAroundTime},{complete_job.CPUWaitTime},{complete_job.IOWaitTime}\n'))
                                    cpu.set_idle()
                                else:
                                    self.wait.addPCB(complete_job)
                                    self.wait.sort_by_priority()
                                    self.wait.incrementTime()
                                    self.message.append(
                                        f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered wait queue[/cyan] \n")
                                    cpu.set_idle()
                        else:
                            # cpu.current_job.ready_cpu_wait += 1
                            # cpu.current_job.setPriority()
                            self.ready.addPCB(cpu.current_job)
                            self.ready.sort_by_priority()
                            self.message.append(
                                f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [red]interrupted and entered ready queue[/red] \n")
                            cpu.set_idle()
                    i += 1
                if (len(self.wait.queue) > 0):
                    self.waiting_to_io()
                for io in self.io:
                    if not io.is_idle:
                        io.increment_execution_time()
                        if (int(self.wait.returnPriority()) >= int(io.current_job.priority[1])):
                            io.current_job.decrement_burst_time()
                            self.message.append(
                                f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{io.current_job.get_current_burst_time()}[/bold green]] [cyan]is running in IO_{i}[/cyan] \n")
                            complete_job = io.complete_job()
                            if complete_job:
                                complete_job.pending_brust()
                                self.ready.addPCB(complete_job)
                                self.ready.sort_by_priority()
                                self.message.append(
                                    f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]IO completed and entered ready queue[/cyan] \n")
                                io.set_idle()
                        else:
                            io.current_job.wait_io_wait += 1
                            self.wait.addPCB(io.current_job)
                            self.wait.sort_by_priority()
                            self.message.append(
                                f"[green]At time: {self.clock.getClock()} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] {io.current_job.get_current_burst_time()}] [red]interrupted and entered ready queue[/red] \n")
                            io.set_idle()

                self.clock.increment()
                self.time_slice -= 1
                self.write_message(self.message)
                # total_process,finished_process,cpu_count,io_count
                live.update(UI_Layout(self.new.queue, self.ready.queue, self.running,
                                      self.wait.queue, self.io, self.terminated.queue,
                                      self.clock.getClock(), self.message, self.total_processes, self.terminated_process_count, self.cpuCount, self.ioCount, self.kind))
        self.priority_req = False


# if __name__ == '__main__':

#     fcfs_scheduler = PB("small.dat", 3, 1, 2, "PB")
#     fcfs_scheduler.run()
#     fcfs_scheduler.cal_stat()
#     fcfs_scheduler.write_header_file()
#     fcfs_scheduler.close_files()
