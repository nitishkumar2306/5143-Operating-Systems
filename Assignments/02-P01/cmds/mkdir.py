"""
    This file have function related to creating directory.
"""
from cmds.printCaptureLogger import PrintCaptureLogger
import sys
import os
import re

# mkdir  test_123  : current dirc
# mkdir  test_123/1234   : current and append
# mkdir  test/1234  :issue
# mkdir -p   test/1234   : current and append
# mkdir /home/madhav/Documents/univeristy/mkdir_test  : fullpath
# mkdir ../../mkdir_test     working


# ███╗░░░███╗██╗░░██╗██████╗░██╗██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ████╗░████║██║░██╔╝██╔══██╗██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██╔████╔██║█████═╝░██║░░██║██║██████╔╝  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║╚██╔╝██║██╔═██╗░██║░░██║██║██╔══██╗  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██║░╚═╝░██║██║░╚██╗██████╔╝██║██║░░██║  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚═╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░

def mkdir_p(path):
    ''' This method will create multiple folder if they are not exists already

    - **Params:**
      - kwargs: path
    
    - **Returns:**
      - None
    '''
    try:
        os.makedirs(path)
        print(f"Created directory: {path}")
    except OSError as e:
        if e.errno == os.errno.EEXIST and os.path.isdir(path):
            print(f"Directory already exists: {path}")
        else:
            print("Error")


def mkdir(**kwargs):
    """ Usage: mkdir [OPTION]... DIRECTORY...
        Create the DIRECTORY(ies), if they do not already exist.

        Mandatory arguments to long options are mandatory for short options too.
        -p, --parents     no error if existing, make parent directories as needed

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
            for param in params:
                param= re.sub(r'[\'"]', '', param) 
                if flags:
                    if not os.path.isabs(param):
                        current_directory = os.getcwd()
                        new_directory = os.path.join(current_directory, param)
                    else:
                        new_directory = param
                    mkdir_p(new_directory)
                else:
                    if os.path.isabs(param):
                        if os.path.exists(param):
                            print(f"Directory already exists: {param}")
                        else:
                            mkdir_p(param)
                    else:
                        try:
                            os.mkdir(param)
                            print(f"Created directory: {param}")
                        except FileExistsError:
                            print(f"Directory already exists: {param}")
                        except FileNotFoundError:
                            print(f"Directory does not exists: {param}")
        else:
            print("mkdir: missing operand \nTry \'mkdir --help' for more information.")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
