"""
Used to find the current logged in user
"""
import os
import pwd
import grp
import time
import stat
import re
import logging
import sys
import humanize
from cmds.printCaptureLogger import PrintCaptureLogger
from colorama import Fore, Style


# ░██╗░░░░░░░██╗██╗░░██╗░█████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ░██║░░██╗░░██║██║░░██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ░╚██╗████╗██╔╝███████║██║░░██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░░████╔═████║░██╔══██║██║░░██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ░░╚██╔╝░╚██╔╝░██║░░██║╚█████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░╚════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░

def who(params, flags, input):
    """
    Used to find the current logged in user
"""
    print('\n')
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
   
    try:
        # Execute the 'who' command using os.system
        print('\r')
        os.system('who')
        
   
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        sys.stdout = sys.__stdout__  
    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

