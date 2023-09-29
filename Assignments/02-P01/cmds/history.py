"""
    This file have function related to maintain command history.
"""
import readline
from cmds.printCaptureLogger import PrintCaptureLogger
import sys

command_history = []


# ██╗░░██╗██╗░██████╗████████╗░█████╗░██████╗░██╗░░░██╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██║░░██║██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚██╗░██╔╝  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ███████║██║╚█████╗░░░░██║░░░██║░░██║██████╔╝░╚████╔╝░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██╔══██║██║░╚═══██╗░░░██║░░░██║░░██║██╔══██╗░░╚██╔╝░░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██║░░██║██║██████╔╝░░░██║░░░╚█████╔╝██║░░██║░░░██║░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═╝░░╚═╝╚═╝╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def add_to_history(command,flags):
    # print_capture_logger = PrintCaptureLogger()
    # sys.stdout = print_capture_logger
    # print('\n')
    
    try:
        # Check if the --help option is provide
        if command.strip():
                    command_history.append(command.strip())
    except Exception as e:
        print("An error occurred:", e)
    
    return command_history, (len(command_history)-1)
    
    # finally:
    #     sys.stdout = sys.__stdout__  # Restore the original stdout

    #     captured_output = ''.join(print_capture_logger.log_content)
    #     return captured_output



               



def show_history(**kwargs):
    """
    Shows the history of commands executed in the current session
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        print("\n")
        if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else ["."]
        else:
            params = ["."]
        if "flags" in kwargs:
            flags = kwargs["flags"]
            if '--help' in flags:
                help_text = """

"""
        else:
            flags = []   
        
        for index, item in enumerate(command_history, start=1):
            
            print(index, item)
    except Exception as e:
        print("An error occurred while displaying history:", e)
    
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

        captured_output = ''.join(print_capture_logger.log_content)
        return captured_output
   
    


