import os
import sys



# ░██████╗░█████╗░██████╗░████████╗  ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░
# ██╔════╝██╔══██╗██╔══██╗╚══██╔══╝  ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗
# ╚█████╗░██║░░██║██████╔╝░░░██║░░░  ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║
# ░╚═══██╗██║░░██║██╔══██╗░░░██║░░░  ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║
# ██████╔╝╚█████╔╝██║░░██║░░░██║░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝
# ╚═════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░


def sort(params, flags, input):
    """
    Used to sort the contents of the given files.
    """
    try:
        # Determine the sorting order based on flags
        reverse_order = '-r' in flags
        numeric_sort = '-n' in flags

        # Determine the input source (either file or standard input)
        if input:
            data = input  # Use provided input
        else:
            # Check if a file is specified as the first parameter
            if params:
                input_file = params[0]
                if os.path.isfile(input_file):
                    with open(input_file, 'r') as file:
                        data = file.read()
                else:
                    raise FileNotFoundError(f"File '{input_file}' not found.")
            else:
                # If no input provided and no file specified, read from standard input
                data = sys.stdin.read()

        # Split the input data into lines and sort them
        lines = data.splitlines()
        sorted_lines = sorted(lines, reverse=reverse_order, key=lambda x: int(x) if numeric_sort else x)

        # Print the  result 
        sorted_output = "\n".join(sorted_lines)
        print('\n')
        print(sorted_output)
        return ""

    except Exception as e:
        print(f"Error: {str(e)}")

