"""
    This file have function related to execute history command.
"""
import os
from cmds.history import add_to_history, show_history, command_history


def execute_command(command_to_execute):
    """ 
    Executes a given command and returns the output.
"""
    try:
        # Use os.system to run the command and redirect output to /dev/null (Unix) or nul (Windows)
        if os.name == 'posix':  # Unix-based system
            os.system(f"{command_to_execute} > null")
        elif os.name == 'nt':  # Windows system
            os.system(f"{command_to_execute} > null")
        
        # Since the command output is redirected, return an empty string
        return ""
    except Exception as e:
        return f"Error: {str(e)}"

def execute_history_command(cmd_text):
    if cmd_text.startswith('!'):
        try:
            print('\n')
            index = int(cmd_text[1:])
            if 1 <= index <= len(command_history):
                command_to_execute = command_history[index - 1]
                if command_to_execute.strip() == "history":
                    # Skip execution of the "history" command
                    return ""
                else:
                    os.system(command_to_execute)
                    return ""
            else:
                return f"Error: Command history index {index} out of range."
        except ValueError:
            return "Error: Invalid command history index."
    else:
        return ""
