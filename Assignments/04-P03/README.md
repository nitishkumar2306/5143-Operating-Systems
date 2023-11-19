## Nov 3 2023

## Cpu Scheduling - Simulation

## Group Members
- Nitish Kumar Erelli
- Madhav Adhikari
- Naga Vamshi Krishna Jammalamadaka

## Overview:
Cpu scheduling is a classic and contemporary computer science problem that started when early computers had processors that remained idle much of the time. The goal initially was to get multiple programs loaded into memory, so they could run back to back. This was still inefficient and needed improvement.  That soon evolved into multiple programs loaded into memory and when one process blocked itself, the cpu would work on another available process (multi-programming). This, of course, kept evolving into our multi-threaded / multi-processor world. Yet, we still need to be cognizant of keeping the cpu(s) busy! So what does a scheduler do?

## Supported algorithms
- First Come First Serve / FCFS
- Round-Robin / RR
- Priority Based

## Built with
- Python
- rich

## Installation Process :
Navigate to the folder using the terminal and execute the following commands to run the program. Ensure to choose the appropriate Python version. If you utilize python3 for executing Python files, please use pip3 accordingly. Additionally, for the subsequent command, make sure to use 
```
pip install -r requirement.txt
```
After completing all the necessary packages run one of the following commands
```
   python3 sim.py type=RR cpus=5 ios=5 timeslice=5 input=small.dat speed=0.01
   python3 sim.py type=FCFS cpus=5 ios=5 input=small.dat
   python3 sim.py type=PB cpus=5 ios=5 input=small.dat

   Required Parameters:
        type   = algorithm type [FCFS or RR or PB]
        cpus   = number of CPU (e.g., 5, 2)
        ios    = number of IO (e.g., 2, 6)
        input  = process contain file (e.g., small.dat)  
   Optional Parameters:
        timeslice = required for RR, default 5
        speed     = default 0.01 or accepts any values
```
### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [sim.py](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/sim.py) | file that holds driver python code |
|   2  | [requirements.txt](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/requirements.txt) | file that holds list of dependencies for this project |
|   3   | [walkthrough.py](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/walkthrough.txt) | file that holds series of commands to run the program |
|   4   | [job_stats_FCFS_1_1_small_file.dat](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/job_stats_FCFS_1_1_small_file.dat) | file that holds FCFS job stats |
|   5   | [message_FCFS_1_1_small_file.dat](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/message_FCFS_1_1_small_file.dat)      | file that holds FCFS messages |
|   6   | [overall_stats_FCFS_1_1_small_file.dat](https://github.com/nitishkumar2306/5143-Opsys-102/blob/main/Assignments/04-P03/overall_stats_FCFS_1_1_small_file.dat) | file that holds FCFS overall stats |

  
