"""
This file is about  cd command.
"""
from cmds.printCaptureLogger import PrintCaptureLogger
import sys
import os
from cmds.whoami import prompt
import re


# ░█████╗░██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░╚═╝██║░░██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░██╗██║░░██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ╚█████╔╝██████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░╚════╝░╚═════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def cd(**kwargs):
    """
    Change the shell working directory.
    
    Change the current directory to DIR.  The default DIR is the value of the
    HOME shell variable.

 """
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    prompt()
    
    try:
        input = kwargs["input"] if "input" in kwargs else []
        if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else []
        else:
            params = []
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []

        print("\r")
        if params:
          for param in params:  
            try:
                param= re.sub(r'[\'"]', '', param) 
                if param == "~":
                    os.chdir(os.path.expanduser("~"))  # Change to the home directory
                elif param == "..":
                    os.chdir("..")  # Change to the parent directory
                else:
                    os.chdir(param)  # Change to the named directory
                print(f"Changed to directory: {os.getcwd()}")
            except FileNotFoundError:
                print(f"Error: Directory '{param}' not found.")
            except PermissionError:
                print(f"Error: Permission denied for directory '{param}'.")
            except Exception as e:
                print(f"Error: {e}")
        else:
          os.chdir(os.path.expanduser("~"))  # Change to the home directory
          print(f"Changed to directory: {os.getcwd()}")

    finally:
            sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
        