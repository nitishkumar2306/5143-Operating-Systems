
import os
import sys
from cmds.printCaptureLogger import PrintCaptureLogger


# ░█████╗░██╗░░██╗███╗░░░███╗░█████╗░██████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔══██╗██║░░██║████╗░████║██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ██║░░╚═╝███████║██╔████╔██║██║░░██║██║░░██║  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ██║░░██╗██╔══██║██║╚██╔╝██║██║░░██║██║░░██║  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ╚█████╔╝██║░░██║██║░╚═╝░██║╚█████╔╝██████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░╚════╝░╚═════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░
def chmod(**kwargs):
    """ 
    Usage: chmod [OPTION]... MODE[,MODE]... FILE...
Change the file mode bits.

Options:
  
  --help         display this help and exit
"""
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    print('\n')

    try:
        params = kwargs.get("params", [])
        flags = kwargs.get("flags", [])


        # Check if MODE and FILE arguments are provided
        if not params:
            print("Error: Please provide at least one MODE and one FILE.")
            return ""

        # Separate the modes and files
        modes = []
        files = []
        for param in params:
            if os.path.exists(param):
                files.append(param)
            else:
                modes.append(param)

        if not files:
            print("Error: Please provide at least one valid FILE.")
            return ""

        for mode in modes:
            try:
                mode_int = int(mode, 8)  # Convert the octal mode string to an integer
                for file in files:
                    os.chmod(file, mode_int)  # Change the file mode
                    print(f"Changed mode of {file} to {oct(mode_int)[2:]}")
            except Exception as e:
                print(f"Error changing mode: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output


