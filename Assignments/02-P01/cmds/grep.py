"""
This file is about  grep command.
"""

import os
import pwd
import grp
import time
import stat
import re
import logging
import sys
from cmds.printCaptureLogger import PrintCaptureLogger

# from rich import print
from colorama import Fore, Style


# ls -la | grep "madhav 4096"  k.txt
#  ls -la | grep madhav
#  grep  madhav ... error
# grep madhav text
# grep madhav k.txt m.txt
# ls | grep madhav k.txt


# ░██████╗░██████╗░███████╗██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔════╝░██╔══██╗██╔════╝██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░██╗░██████╔╝█████╗░░██████╔╝  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░╚██╗██╔══██╗██╔══╝░░██╔═══╝░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ╚██████╔╝██║░░██║███████╗██║░░░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def grep(**kwargs):
    """ Usage: grep [OPTION]... PATTERNS [FILE]...
              Search for PATTERNS in each FILE.
              Example: grep -i 'hello world' menu.h main.c
              -i, --ignore-case         ignore case distinctions in patterns and data
              -l, --files-with-matches  print only names of FILEs with selected lines
 """
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
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
            search_pattern = re.sub(r'[\'"]', '', params[0])  # remove quotes
            files = params[1:]
            unique_files = set()
            if files:
                for file in files:
                    with open(file, 'r') as file:
                        for line in file:
                            if "i" in flags:
                                if re.search(search_pattern, line, re.IGNORECASE):
                                    print(line.strip()) if not "l" in flags else unique_files.add(file.name)

                            else:
                                if re.search(search_pattern, line):
                                    print(line.strip()) if not "l" in flags else unique_files.add(file.name)
                if "l" in flags:
                    for f in unique_files:
                        print(f)                    

            else:
                lines = input.split("\n")
                if ("l" in flags) and len(lines)>1:
                     print("(standard input)")

                else:
                    for line in lines:
                        if "i" in flags:
                            if re.search(search_pattern, line, re.IGNORECASE):
                                print(line.strip()) 

                        else:
                            if re.search(search_pattern, line):
                                print(line.strip()) 
        else:
            print("Search pattern or file name required")
    except FileNotFoundError:
        print(f"\rless: cannot open '{file}' for reading: No such file or directory")
    except Exception as e:
        print(f"\rAn error occurred: {e}.\nTry 'less --help' for more information.")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
