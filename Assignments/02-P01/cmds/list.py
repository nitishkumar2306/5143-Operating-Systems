"""
This file is about  ls and ll comands.
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


# ██╗░░░░░██╗░██████╗████████╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██║░░░░░██║██╔════╝╚══██╔══╝  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░░░░██║╚█████╗░░░░██║░░░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░░░░██║░╚═══██╗░░░██║░░░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ███████╗██║██████╔╝░░░██║░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚══════╝╚═╝╚═════╝░░░░╚═╝░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░


def format_file_info(**kwargs):
    ''' This method will retrieves details of files and return with foramted  output

    - **Params:**
      - kwargs: file and human flag
    
    - **Returns:**
      - (object) : formated output
    '''
    file=kwargs["file"]
    if "human" in kwargs:
        human=kwargs["human"]
    else:
        human=False
    if "param" in kwargs:
        param=kwargs["param"]
        if not param.endswith(os.path.sep):
                 file_path= param + os.path.sep
        else:
                file_path= param
    else:
        param=""     
    file_path=file_path+file
    
    file_stat = os.stat(file_path)
    permissions = stat.filemode(file_stat.st_mode)
    num_links = file_stat.st_nlink
    owner = pwd.getpwuid(file_stat.st_uid).pw_name
    group = grp.getgrgid(file_stat.st_gid).gr_name
    size = humanize.naturalsize(file_stat.st_size) if human==True else file_stat.st_size
    last_modified = time.strftime("%b %d %H:%M", time.localtime(file_stat.st_mtime))
    if os.path.isdir(file_path):
            return "{:<4} {:<2} {:<4} {:<4} {:>4} {:<4} {:<4}".format(permissions, num_links, owner, group, size, last_modified, Fore.BLUE + file + Style.RESET_ALL)
    elif os.access(file_path, os.X_OK):
            return "{:<4} {:<2} {:<4} {:<4} {:>4} {:<4} {:<4}".format(permissions, num_links, owner, group, size, last_modified, Fore.RED + file + Style.RESET_ALL)

    else:
        return "{:<4} {:<2} {:<4} {:<4} {:>4} {:<4} {:<4}".format(permissions, num_links, owner, group, size, last_modified,  file )
    
def calculate_total_blocks(**kwargs):

    ''' This method will calculated  the total block size

    - **Params:**
      - kwargs: files and human flag
    
    - **Returns:**
      - (object) : total block size
    '''

    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]  
    if "human" in kwargs:
        human=kwargs["human"]
    else:
        human=False
    if "param" in kwargs:
        param=kwargs["param"]
        if not param.endswith(os.path.sep):
                 file_path= param + os.path.sep
        else:
                file_path= param
    else:
        param=""          
    total_blocks = 0
    for filename in Files:
            path=file_path+filename
            stat_info = os.stat(path)
            total_blocks += (stat_info.st_blocks * 512) // 1024  # Convert to 1024-byte blocks
    total_blocks =  humanize.naturalsize(total_blocks) if human==True else total_blocks
    return total_blocks


def ls_style_listing(**kwargs):
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]  
    if "param" in kwargs:
        param=kwargs["param"]
        if not param.endswith(os.path.sep):
                 file_path= param + os.path.sep
        else:
                file_path= param
    else:
        param=""  

    if "hidden" in kwargs:
        hidden=kwargs["hidden"]
    else:
        hidden=False
    if not Files:
        return

    max_width = max(len(entry) for entry in Files)
    column_width = max_width + 2  # Add some padding

    # Get the terminal width (number of columns)
    try:
        _, columns = os.popen('stty size', 'r').read().split()
        columns = int(columns)
    except (ValueError, FileNotFoundError):
        columns = 80  # Default to 80 columns if terminal size can't be determined

    # Calculate the number of columns based on the terminal width
    num_columns = columns // column_width

    # Print the contents with dynamic formatting
    for i, file in enumerate(Files, 1):
        if hidden and file.startswith("."):
            continue
        path=file_path+file
        #print(file.ljust(max_width), end=' ' * 2)  # Adjust spacing for alignment
        if os.path.isdir(path):
            print(Fore.BLUE + file.ljust(max_width) + Style.RESET_ALL, end=' ' * 2)
        elif os.access(path, os.X_OK):
            print(Fore.RED + file.ljust(max_width) + Style.RESET_ALL, end=' ' * 2)
        else:
            print(file.ljust(max_width), end=' ' * 2)
        if i % num_columns == 0:
            print()  # Start a new line after reaching the specified number of columns

    # Ensure a final newline if necessary
    if len(Files) % num_columns != 0:
        print()

def la(**kwargs):

    ''' This method will manage la flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]    
    print("total",calculate_total_blocks(Files=Files,param=kwargs["param"])) 

    for file in Files:
        formatted_info = format_file_info(file=file,human=False,param=kwargs["param"])
        print(formatted_info)        

def alh(**kwargs):

    ''' This method will manage alh flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]  

    print("total",calculate_total_blocks(Files=Files,human=True,param=kwargs["param"])) 

    for file in Files:
        formatted_info = format_file_info(file=file,human=True,param=kwargs["param"])
        print(formatted_info)

def ah(**kwargs):

    ''' This method will manage ah flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    input = kwargs["input"] if "input" in kwargs else []
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]  
    if "ll" in kwargs["ll"]:
        print("total",calculate_total_blocks(Files=Files,human=True,param=kwargs["param"])) 
        for file in Files:
                formatted_info = format_file_info(file=file,human=True,param=kwargs["param"])
                print(formatted_info)
    else:
        if input:
            for file in Files:
                     print(file)
        else:   
            ls_style_listing( Files=Files,hidden=False,param=kwargs["param"])

def hl(**kwargs):

    ''' This method will manage hl flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]    
    print("total",calculate_total_blocks(Files=Files,human=True,param=kwargs["param"])) 

    for file in Files:
        if not file.startswith("."):
            formatted_info = format_file_info(file=file,human=True,param=kwargs["param"])
            print(formatted_info)

def a(**kwargs):

    ''' This method will manage a flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    input = kwargs["input"] if "input" in kwargs else []
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]   
   
        
    if "ll" in kwargs["ll"]:
        print("total",calculate_total_blocks(Files=Files,human=False,param=kwargs["param"])) 
        for file in Files:
                formatted_info = format_file_info(file=file,human=False,param=kwargs["param"])
                print(formatted_info)
    else:
        if input:
            for file in Files:
                     print(file)
        else:   
            ls_style_listing( Files=Files,hidden=False,param=kwargs["param"])
            

def l(**kwargs):

    ''' This method will manage l flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]    
    print("total",calculate_total_blocks(Files=Files,param=kwargs["param"])) 

    for file in Files:
        if not file.startswith("."):
            formatted_info = format_file_info(file=file,human=False,param=kwargs["param"])
            print(formatted_info) 

def h(**kwargs):

    ''' This method will manage h flag

        - **Params:**
        - kwargs: files
        
        - **Returns:**
        -  None
        '''
    input = kwargs["input"] if "input" in kwargs else []
    if "Files" in kwargs:
        Files=kwargs["Files"]
    else:
        Files=[]    

    if "ll" in kwargs["ll"]:
        print("total",calculate_total_blocks(Files=Files,human=True,param=kwargs["param"])) 

        for file in Files:
            if not file.startswith("."):
                formatted_info = format_file_info(file=file,human=True,param=kwargs["param"])
                print(formatted_info)
    else:
        if input:
            for file in Files:
                if not file.startswith("."):
                     print(file)
        else:   
            ls_style_listing( Files=Files,hidden=True,param=kwargs["param"])
            

def handle_flags(**kwargs):
                
                ''' This method will manage  flages method

                - **Params:**
                - kwargs: files and  ll
                
                - **Returns:**
                -  None
                '''
                input = kwargs["input"] if "input" in kwargs else []
                if "flags" in kwargs:
                    flags = kwargs["flags"]
                else:
                     flags = [] 
                if "Files" in kwargs:
                    Files=kwargs["Files"]
                else:
                     Files=[]  
                if "ll" in  kwargs:   
                    ll=kwargs["ll"]
                else:
                     ll=""        
                flag_actions = {
                    ('a', 'h', 'l'): alh,
                    ('a', 'l'): la,
                    ('a', 'h'): ah,
                    ('h', 'l'): hl,
                    ('a',): a,
                    ('l',): l,
                    ('h',): h,
                }
        
                action = flag_actions.get(tuple(sorted(flags)), None)

                if action:
                    action(Files=Files,ll=ll,param=kwargs["param"],input=input)
                else:
                     print("Error: flag %s doesn't exist." % (flags)) 


def ls(**kwargs):
    """ Usage: ls [OPTION]... [FILE]...
        List information about the FILEs (the current directory by default).
        Flags:
        -a, --all                  do not ignore entries starting with .
        -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
        -l                         use a long listing format
        --help     display this help and exit
 """
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        input = kwargs["input"] if "input" in kwargs else []
        if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else ["."]
        else:
            params = ["."]
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []    

        for param in params:
            param= re.sub(r'[\'"]', '', param) 
            Files=sorted(os.listdir(param))
            if Files:
                print("\r")
                if(len(Files)>1):
                    if param !=".":
                        print(param," :\n") 
                if flags:
                    handle_flags(flags=flags,Files=Files,param=param,input=input)
    
                else: 
                   if input:
                     for file in Files:
                        if not file.startswith("."):
                            print(file)
                   else:
                     ls_style_listing( Files=Files,hidden=True,param=param)
            else:
                print("\r")          
                          
    except Exception:
        print(f"\r Error: Directory/Files '{param}' not found.")                
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output                



def ll(**kwargs):
    """ Usage: ls [OPTION]... [FILE]...
        List information about the FILEs (the current directory by default)
        Flags:
        -a, --all                  do not ignore entries starting with .
        -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
        -l                         use a long listing format
        --help     display this help and exit
        """

    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else ["."]
        else:
            params = ["."]
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []
        for param in params:
            param= re.sub(r'[\'"]', '', param) 
            Files=sorted(os.listdir(param))
            if Files:
                print("\r")
                if(len(Files)>1):
                    if param !=".":
                        print(param," :\n") 
                #print("total",calculate_total_blocks(Files=Files))

                if flags:
                    handle_flags(flags=flags,Files=Files,ll="ll",param=param)

        
                else:    
                    for file in Files:
                        #file_path = os.path.join(path, file)
                        if not file.startswith("."):
                            formatted_info = format_file_info(file=file,param=param)
                            print(formatted_info) 
            else:
                print("\r")                  
    except Exception:
        print(f"\r Error: Directory/Files '{param}' not found.")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

   