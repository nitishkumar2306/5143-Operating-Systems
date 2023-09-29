"""
    This file have function related to cat, touch, less, tail, head, rm, cp, mv.
"""
import os
import sys
import shutil
from cmds.printCaptureLogger import PrintCaptureLogger
from getch_helper import Getch

# from rich import print
from colorama import Fore, Style


getch = Getch()


# commmands to be executed 
# mv pm.txt bana
# cp /home/jarvis/Documents/others/test1.txt /home/jarvis/Documents/others/test_dir
# rm -rf bana
# cat write.txt
# less test.py
# head -n 10 abc.txt
# tail -n 10 abc.txt
# touch <filename>


# ░█████╗░░█████╗░████████╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔══██╗██╔══██╗╚══██╔══╝  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░╚═╝███████║░░░██║░░░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░██╗██╔══██║░░░██║░░░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ╚█████╔╝██║░░██║░░░██║░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def cat(**kwargs):
    """
    Usage: cat [OPTION]... [FILE]...
    Concatenate FILE(s) to standard output.
    With no FILE, or when FILE is -, read standard input.
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        try:
            if kwargs["input"] != "" and kwargs["params"] == []:
                filename = kwargs["input"].splitlines()[1]
                print(filename)
            elif kwargs["params"] != []:
                for filename in kwargs["params"]:
                    print("\r")
                    with open(filename, "r") as file:
                        lines = file.readlines()[:]
                        # print lines to console
                        for line in lines:
                            print(line, end="")
                    print("\r")
            else:
                print(
                    f"\ncat: missing file operand.\nTry 'cat --help' for more information.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output



# ██╗░░░░░███████╗░██████╗░██████╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██║░░░░░██╔════╝██╔════╝██╔════╝  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░░░░█████╗░░╚█████╗░╚█████╗░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░░░░██╔══╝░░░╚═══██╗░╚═══██╗  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ███████╗███████╗██████╔╝██████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚══════╝╚══════╝╚═════╝░╚═════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def less(**kwargs):
    """
    The "less" shell command is a terminal pager that allows 
    users to view and navigate through text files, 
    displaying content one screen at a time,
    with search and scroll capabilities.
"""
    
    try:
        if kwargs["params"] != []:
            filename = kwargs["params"][0]
            with open(filename, "r") as file:
                lines = file.readlines()
            content = " "

            page_size = 5  # Number of lines to display at a time
            current_line = 0
            print('\r')
            while True:
                # Display the current page of lines
                for i in range(current_line, min(current_line + page_size, len(lines))):
                    print(lines[i], end="")
                # print(content, end="")

                # Ask the user to continue or quit
                user_input = input(
                    "Press 'q' to quit, 'n' for the next page: ")
                if user_input.lower() == "q":
                    break
                elif user_input.lower() == "n":
                    current_line += page_size
                    if current_line >= len(lines):
                        break
        else:
            print(f"\nless: invalid trailing option -- 1.\nTry 'less --help' for more information.")
            
    except FileNotFoundError:
        print(
            f"\rless: cannot open '{filename}' for reading: No such file or directory"
        )
    except Exception as e:
        print(
            f"\rAn error occurred: {e}.\nTry 'less --help' for more information.")



# ██╗░░██╗███████╗░█████╗░██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██║░░██║██╔════╝██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ███████║█████╗░░███████║██║░░██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██╔══██║██╔══╝░░██╔══██║██║░░██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██║░░██║███████╗██║░░██║██████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def head(**kwargs):
    """ 
        Usage: head [OPTION]... [FILE]...
        Print the first 5 lines of each FILE to standard output.
        With more than one FILE, precede each with a header giving the file name.
  
            -n, --lines=[-]NUM      print the first NUM lines instead of the first 5;
                                    with the leading '-', print all but the last
                                    NUM lines of each file    
        
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    count = length = start = 0

    try: 
        try:
            if kwargs["flags"] == "":
                length = 5
                start = 0
            elif kwargs["flags"] == "n" and len(kwargs["params"]) > 0:
                length = int(kwargs["params"][0])
                start = 1
            elif kwargs["flags"] == "n" and kwargs["params"] == []:
                raise Exception(
                    f"head: invalid trailing option -- 1.\nTry 'head --help' for more information."
                )
            if kwargs["params"] != [] and kwargs["input"] == "":
                count = len(kwargs["params"])
                for i in range(start, count):
                    filename = kwargs["params"][i]
                    if os.path.isfile(filename):
                        print("==> ",filename," <==")
                    with open(filename, 'r') as file:
                        lines = file.readlines()[:length]
                    # print lines to console
                    for line in lines:
                        print(line, end='')
                    print("\r")

            elif kwargs["input"] != "":
                filename = kwargs["input"].splitlines()[1]
                if os.path.isfile(filename):
                    print("==> ",filename," <==")                
                with open(filename, 'r') as file:
                    lines = file.readlines()[:length]
                    # print lines to console
                    for line in lines:
                        print(line, end='')
            else:
                print(
                    f"\nhead: invalid trailing option -- 1.\nTry 'head --help' for more information."
                )
        except FileNotFoundError:
            print(f"\nFile not found: {filename}")
            print(f"\rhead: cannot open '{filename}' for reading: No such file or directory")
        except Exception as e:
            print(f"\nAn error occurred: {e}") 
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output


# ████████╗░█████╗░██╗██╗░░░░░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ╚══██╔══╝██╔══██╗██║██║░░░░░  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ░░░██║░░░███████║██║██║░░░░░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░░░██║░░░██╔══██║██║██║░░░░░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ░░░██║░░░██║░░██║██║███████╗  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚══════╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░

def tail(**kwargs):
    """
    Usage: tail [OPTION]... [FILE]...
    Print the last 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.

        -n, --lines=[+]NUM       output the last NUM lines, instead of the last 5;
                                    or use -n +NUM to output starting with line NUM
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    count = length = start = 0

    try: 
        try:
            if kwargs["flags"] == "":
                length = 5
                start = 0
            elif kwargs["flags"] == "n" and len(kwargs["params"]) > 0:
                length = int(kwargs["params"][0])
                start = 1
            elif kwargs["flags"] == "n" and kwargs["params"] == []:
                raise Exception(
                    f"tail: invalid trailing option -- 1.\nTry 'tail --help' for more information."
                )
            if kwargs["params"] != [] and kwargs["input"] == "":
                count = len(kwargs["params"])
                for i in range(start, count):
                    filename = kwargs["params"][i]
                    if os.path.isfile(filename):
                        print("==> ",filename," <==")
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                    tot_lines = len(open(filename).readlines())
                    length = 2 if tot_lines < 5 else length
                    for i in range(tot_lines - length , tot_lines):
                        print(lines[i], end='')
                    print("\r")
            elif kwargs["input"] != "":
                filename = kwargs["input"].splitlines()[1]
                if os.path.isfile(filename):
                    print("==> ",filename," <==")
                with open(filename, 'r') as file:
                    lines = file.readlines()
                tot_lines = len(open(filename).readlines())
                length = 5 if kwargs["flags"] == "" else length
                for i in range(tot_lines - length , tot_lines):
                    print(lines[i], end='')
            else:
                print(
                    f"\ntail: invalid trailing option -- 1.\nTry 'tail --help' for more information."
                )
        except FileNotFoundError:
            print(f"\nFile not found: {filename}")
            print(f"\rtail: cannot open '{filename}' for reading: No such file or directory")
        except Exception as e:
            print(f"\nAn error occurred: {e}") 
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output


# ████████╗░█████╗░██╗░░░██╗░█████╗░██╗░░██╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ╚══██╔══╝██╔══██╗██║░░░██║██╔══██╗██║░░██║  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ░░░██║░░░██║░░██║██║░░░██║██║░░╚═╝███████║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░░░██║░░░██║░░██║██║░░░██║██║░░██╗██╔══██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ░░░██║░░░╚█████╔╝╚██████╔╝╚█████╔╝██║░░██║  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░░░╚═╝░░░░╚════╝░░╚═════╝░░╚════╝░╚═╝░░╚═╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def touch(**kwargs):
    """
    Usage: touch [OPTION]... FILE...
    Update the access and modification times of each FILE to the current time.

    A FILE argument that does not exist is created empty
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        if kwargs["params"] != []:
            try:
                for filename in kwargs["params"]:
                    if filename != "&&" and not os.path.isfile(filename):
                        open(filename, "w").close()
            except Exception as e:
                print(f"\nAn error occurred: {e}")
        elif kwargs["params"] == [] and kwargs["input"] != []:
            # block for handling input from other command when using pipe
            pass
            
        else:
            print(
                f"\ntouch: missing file operand.\nTry 'touch --help' for more information."
            )
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output


# ░█████╗░██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░╚═╝██████╔╝  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░██╗██╔═══╝░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ╚█████╔╝██║░░░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░╚════╝░╚═╝░░░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def cp(**kwargs):
    """
    Usage: cp [OPTION]... [-T] SOURCE DEST
    or:  cp [OPTION]... SOURCE... DIRECTORY
    or:  cp [OPTION]... -t DIRECTORY SOURCE...
    Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.

    -R, -r, --recursive          copy directories recursively
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        if kwargs["params"] != []:
            try:
                s1 = kwargs["params"]
                if len(s1) == 1:
                    print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")
                elif len(s1) == 2:
                    file1 = s1[0]
                    file2 = s1[1]
                    shutil.copytree(file1, file2) if kwargs["flags"] in ('r','R') else shutil.copy(file1, file2)
                elif len(s1) > 2:
                    dest = s1[-1]
                    if os.path.isdir(dest):
                        for filename in kwargs["params"][:-1]:
                            if os.path.isfile(filename):
                                shutil.copy(filename, dest)
                            else:
                                raise Exception(
                                    f"cp: cannot stat '{filename}': No such file or directory")
                    else:
                        raise Exception(
                            f"cp: target '{dest}' is not a directory")
                elif kwargs["params"] == [] and kwargs["input"] != '':
                    # this block is used Incase an Input is received from a pipe
                    pass

            except FileNotFoundError:
                print(
                    f"\ncp: cannot open '{file2}' for reading: No such file or directory")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output


# ███╗░░░███╗██╗░░░██╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ████╗░████║██║░░░██║  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██╔████╔██║╚██╗░██╔╝  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║╚██╔╝██║░╚████╔╝░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██║░╚═╝░██║░░╚██╔╝░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═╝░░░░░╚═╝░░░╚═╝░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def mv(**kwargs):
    """
    Usage: mv [OPTION]... [-T] SOURCE DEST
    or:  mv [OPTION]... SOURCE... DIRECTORY
    or:  mv [OPTION]... -t DIRECTORY SOURCE...
    Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        if kwargs["params"] != []:
            try:
                s1 = kwargs["params"]
                if len(s1) == 1:
                    print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")
                elif len(s1) == 2:
                    file1 = s1[0]
                    file2 = s1[1]
                    shutil.move(file1, file2)
                elif len(s1) > 2:
                    dest = s1[-1]
                    if os.path.isdir(dest):
                        for filename in kwargs["params"][:-1]:
                            if os.path.isfile(filename):
                                shutil.move(filename, dest)
                            else:
                                raise Exception(
                                    f"mv: cannot stat '{filename}': No such file or directory")
                    else:
                        raise Exception(
                            f"mv: target '{dest}' is not a directory")
                elif kwargs["params"] == [] and kwargs["input"] != '':
                    # this block is used Incase an Input is received from a pipe
                    pass

            except FileNotFoundError:
                print(
                    f"\nmv: cannot open '{file2}' for reading: No such file or directory")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"\nmv: missing file operand\nTry 'mv --help' for more information.")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output


# ██████╗░███╗░░░███╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔══██╗████╗░████║  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██████╔╝██╔████╔██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██╔══██╗██║╚██╔╝██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██║░░██║██║░╚═╝░██║  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═╝░░╚═╝╚═╝░░░░░╚═╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def rm(**kwargs):
    """
    The rm command is used to delete files
    Usage: rm [OPTION]... [FILE]...
    Remove (unlink) the FILE(s).

    -f          ignore nonexistent files and arguments
    -r, -R, --recursive   remove directories and their contents recursively
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    # print(kwargs)
    try:
        if kwargs["params"] != []:
            try:
                for filename in kwargs["params"]:
                    shutil.rmtree(filename) if kwargs["flags"] in ('r','R','rf','fr') else os.remove(filename)
            except Exception as e:
                print(f"\nAn error occurred: {e}")
        elif kwargs["params"] == [] and kwargs["input"] != '':
            filename = kwargs["input"].splitlines()[1]
            os.remove(filename)
            
        else:
            print(
                f"\nrm: missing file operand.\nTry 'rm --help' for more information."
            )
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output
