"""
Used to Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.
"""
import os
import sys
from cmds.printCaptureLogger import PrintCaptureLogger


# ░██╗░░░░░░░██╗░█████╗░  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ░██║░░██╗░░██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ░╚██╗████╗██╔╝██║░░╚═╝  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░░████╔═████║░██║░░██╗  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ░░╚██╔╝░╚██╔╝░╚█████╔╝  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░░╚════╝░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░

def wc(**kwargs):
    """
    Usage: wc [OPTION]... [FILE]...
    or: wc [OPTION]... --files0-from=F
    Print newline, word, and byte counts for each FILE, and a total line if
    more than one FILE is specified. A word is a non-zero-length sequence of
    characters delimited by white space.

        -l, --lines            print the newline counts   
    """
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    print('\n')

    try:
        params = kwargs.get("params", [])
        flags = kwargs.get("flags", [])
        input = kwargs.get("input", [])

        

        # Check for the '-l' flag
        count_lines = 'l' in flags
    

        # Check if a file path is specified as an argument
        if params:
            
            file_path = params[0]

            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                lines = len(content.split('\n'))
                words = len(content.split())
                characters = len(content)

                output = ""

                # Include line count if '-l' flag is present
                if count_lines:
                    output += f"{lines} {file_path}"
                else:
                    output += f"{lines}  {words}  {characters} {file_path}"

                # Print the output horizontally
                print(output)
            else:
                print(f"Error: '{file_path}' does not exist.")
        else:
            # No file path provided, read from standard input
            input_text =input
            lines = len(input_text.split('\n'))
            words = len(input_text.split())
            characters = len(input_text)

            output = ""

            # Include line count if '-l' flag is present
            if count_lines:
                output += f"{lines}"
            else:
                output += f"{lines}  {words}  {characters}"
            
        

            # Print the output horizontally
            print(output)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout
        captured_output = ''.join(print_capture_logger.log_content)
        return captured_output
