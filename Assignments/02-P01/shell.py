"""
This file is about using getch to capture input and handle certain keys 
when they are pressed and execute commands accordingly
"""
import os
import sys
from time import sleep
import re
from  getch_helper import Getch
from command_helper import CommandHelper
from cmds.history import add_to_history
from cmds.chmod import chmod
from cmds.executecommand import execute_history_command 
from cmds.whoami import prompt


command_history=[]

# create instance of our getch class
getch = Getch()                            


def print_cmd(cmd):
    """ This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    terminal_width, _ = os.get_terminal_size()
    prompt_str = prompt()
    
    # Calculate the maximum width available for the command
    max_cmd_width = terminal_width - len(prompt_str) - 2  # Reserve 2 characters for padding
    
    # Check if the command is longer than the available width
    if len(cmd) > max_cmd_width:
        # Adjust the prompt width to accommodate the long command
        prompt_str = prompt_str[:max_cmd_width - len(cmd) - 3] + "...$:"  # Truncate and add ellipsis
    
    padding = " " * (terminal_width - len(prompt_str) - len(cmd) - 1)
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt_str + cmd)
    sys.stdout.flush()



def save_output_to_file(output, output_file):
    print("\r")
    try:
        # Save the captured output to the specified file
        file_name=output_file
        #file_name = os.path.basename(output_file) if  "/"in output_file else output_file
        if re.match(r'^-[^\-]', file_name):
          mode = 'a'  
          file_name=file_name.rsplit(">", 1)[-1].strip()
        else :
           mode='w'

        with open(file_name, mode) as file:
              file.write(output)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':

    ch = CommandHelper() 

    cmd_text = ""         # empty cmd variable

    print_cmd(cmd_text)     # print to terminal
                         
    index = 0
    history_list = []
    while True:     

        char = getch()    # read a character (but don't print)
        if char == '\x03' or cmd_text == 'exit': # ctrl-c
            raise SystemExit(" Bye.")
        
        elif char == '\x7f':   # back space pressed
                    
            cmd_text = cmd_text[:-1]
            print("\b \b", end='')  # Move the cursor back and erase the character
            print_cmd(cmd_text)
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                # index -= 1
                if history_list == []:
                    print_cmd(" ")
                elif index > 0:
                    print_cmd(history_list[index])
                    index -= 1
                elif index == 0:
                    print_cmd(history_list[0])
                
                sleep(0.3)
                
            if direction in 'B':            # down arrow pressed
                if history_list == []:
                    print_cmd(" ")
                elif index  < length:
                    print_cmd(history_list[index])
                    index += 1
                elif index == length:
                    print_cmd(history_list[index])
                sleep(0.3)
            
            if direction in 'C':            # right arrow pressed    
                sys.stdout.write("\033[C")  # Move the cursor right by one position
                sys.stdout.flush()

            if direction in 'D':   # left arrow pressed             
                    sys.stdout.write("\033[D")  # Move the cursor left by one position
                    sys.stdout.flush()
                    
        elif char in '\r':  # return pressed
            
            left_value, redirect_value = cmd_text.split('>', 1) if '>' in cmd_text else (cmd_text, '')
            commands = left_value.split("|")
            captured_output = ""
            if len(commands)>1 and commands[0].split()[0].strip()=="ls": # handle formated print of ls
                captured_output="ls"
            for comnnad in commands:
                # Split the command using spaces outside of quotes
                parts = re.findall(r'[^"\s\']+|"[^"]*"|\'[^\']*\'', comnnad)
                # The first part is the command itself
                cmd = parts[0].strip() if parts else ""                    
                        
                # collect parameters and flags
                params = [part.strip() for part in parts[1:] if not part.startswith('-')]
                flags = [part.lstrip("-").strip() for part in parts[1:] if re.match(r'^-[^\-]', part)]
                helps = [part.lstrip("-").strip() for part in parts[1:] if re.match(r'^--[^-]', part)]

            # if command exists in our shell
                if ch.exists(cmd):
                    if helps:
                       captured_output= ch.invoke(cmd=cmd, params=params,flags=''.join(flags),input=captured_output,help=''.join(helps))
                    else:
                        captured_output= ch.invoke(cmd=cmd, params=params,flags=''.join(flags),input=captured_output)

                else:
                    print("\r")
                    execute_history_command(cmd_text)
                    if not cmd_text.startswith('!'):
    
                        print("Error: command %s doesn't exist." % (cmd))   

                (history_list,length) = add_to_history(comnnad, flags)
                index = length

            if redirect_value:
                save_output_to_file(captured_output,redirect_value)  
            else:
                print("\r")
                print(captured_output)
                  
            sleep(1)    
            cmd_text = ""                        # reset command to nothing (since we just executed it)

            print_cmd(cmd_text)   
                           # now print empty cmd prompt
        elif char == ':':
            char = getch()  # Read the next character
            if char.isdigit():
                history_index = int(char)
                while char.isdigit():
                    char = getch()
                    if char.isdigit():
                        history_index = history_index * 10 + int(char)
                    else:
                        break
                if history_index >= 0 and history_index <= len(command_history):
                    selected_command = command_history[history_index - 1]
                    print_cmd(selected_command)
                    cmd_text = selected_command
                else:
                    print("Invalid history index.")
            else:
                print("Invalid history command format.")
        else:
            cmd_text += char        # add typed character to our "cmd"
            print_cmd(cmd_text)     # print the cmd out
    