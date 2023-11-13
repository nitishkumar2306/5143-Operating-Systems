import os
from algo.fcfs import FCFS
from algo.rb import RB
from algo.pb import PB
import sys
from rich import print 
def usages():
     help_message = """Example:
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
            """
     print(help_message)

if __name__=='__main__':


        # todo color the message 
        # todo graphic 
        # readme file
        
        arguments = sys.argv[1:]

        parsed_args = {}
        required_args = ['type','cpus','ios','input']

        for arg in arguments:
            if '=' in arg:
                key, value = arg.split('=')
                
                if not value:
                    print(f"Missing value for argument: {key}\n")
                    usages()
                    sys.exit(1)

                if key == "input":
                    if not os.path.exists(value):
                        print(f"No such file or directory: {value}\n")
                        usages()
                        sys.exit(1)  # Exit the program if the input file does not exist

                parsed_args[key] = value

        # Check for missing required arguments
        missing_args = [arg for arg in required_args if arg not in parsed_args]
        if missing_args:
            print(f"Missing required arguments: {', '.join(missing_args)}\n")
            usages()
            sys.exit(1)
        
        if parsed_args['type']=="RR" and "timeslice" not in parsed_args.keys():
                    print(f"Missing required arguments: timeslice\n")
                    usages()
                    sys.exit(1) 
        

        cpuCount = int(parsed_args['cpus'])
        ioCount = int(parsed_args['ios'])
        algorithm = parsed_args['type']
        datfile=parsed_args['input']
        timeslice= int(parsed_args.get('timeslice', 5))
        speed=float(parsed_args.get('speed', 0.01))
            
        if(algorithm == "FCFS"):
             fcfs_scheduler = FCFS(datfile,cpuCount,ioCount,timeslice,algorithm,speed)
             fcfs_scheduler.run()
             fcfs_scheduler.cal_stat() 
            # fcfs_scheduler.write_header_file()
             fcfs_scheduler.close_files()
        elif(algorithm == "RR"):
            fcfs_scheduler = RB(datfile,cpuCount,ioCount,timeslice,algorithm,speed)
            fcfs_scheduler.run()   
            fcfs_scheduler.cal_stat() 
           # fcfs_scheduler.write_header_file()
            fcfs_scheduler.close_files()
        elif(algorithm == "PB"):
            fcfs_scheduler = PB(datfile,cpuCount,ioCount,timeslice,algorithm,speed)
            fcfs_scheduler.run()   
            fcfs_scheduler.cal_stat() 
          #  fcfs_scheduler.write_header_file()
            fcfs_scheduler.close_files()
        else:
             print("Algorithm type should be only FCFS or RR or PB \n ") 
             usages()
             sys.exit()   
        
