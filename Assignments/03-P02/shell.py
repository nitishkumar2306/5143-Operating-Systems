
"""
This file is about how to use Filesystem """
import sys
from time import sleep
import re
from helper.sqLiteCRUD import SQLiteconn
from helper.fileSystem import FileSystem
from rich import print



if __name__ == '__main__':

    # Define a dictionary mapping command names to method names
    command_mapping = {
        'ls': 'ls',
        'mkdir': 'mkdir',
        'touch': 'touch',
        'mv': 'mv',
        'cp': 'cp',
        'rm': 'rm',
        'cat': 'cat',
        'pwd': 'pwd',
        'insert': 'insert',
        'cd':'cd',
        'adduser':'adduser',
        'su':'su',
        'who':'who',
        'history': 'history',
        'chmod': 'chmod'
    }
    conn = SQLiteconn("filesystem.db")

    fs = FileSystem(conn)

    cmd_text = ""         # empty cmd variable

try:
    while True:
        base_url=fs.base_url()
        user, user_id=fs.current_usr()
        print('[bold blue] '+base_url +':[/bold blue] ', end='')
        # Read user input
        cmd_text = input()
        if not cmd_text:
            continue  # If the input is empty, continue to the next iteration

        if cmd_text == 'exit':  # ctrl-c
            conn.close_connection()
            raise SystemExit(" Bye.")

        left_value, redirect_value = cmd_text.split(
            '>', 1) if '>' in cmd_text else (cmd_text, '')
        commands = left_value.split("|")
        captured_output = ""
        # handle formated print of ls
        if len(commands) > 1 and commands[0].split()[0].strip() == "ls":
            captured_output = "ls"
        for comnnad in commands:
            # Splits the command using spaces 
            parts = re.findall(r'[^"\s\']+|"[^"]*"|\'[^\']*\'', comnnad)
            # The first part is the command itself
            cmd = parts[0].strip() if parts else ""

            # collect parameters and flags
            params = [part.strip()
                      for part in parts[1:] if not part.startswith('-')]
            flags = [part.lstrip("-").strip()
                     for part in parts[1:] if re.match(r'^-[^\-]', part)]
            helps = [part.lstrip("-").strip()
                     for part in parts[1:] if re.match(r'^--[^-]', part)]

           # Check if the command exists in the mapping
            if cmd in command_mapping:
                method_name = command_mapping[cmd]
                method = getattr(fs, method_name, None)
                if method:
                    # Call the corresponding method
                    method(cmd=cmd, params=params, flags=''.join(flags))
                    history_data = [user_id, cmd_text]  # Provide user_id and cmd_text
                    conn.insert_data_history("history", history_data)
                else:
                    print(f'Method for command "{cmd}" not found.')
            else:
                print(f'[red]Command "{cmd}" not found. Try again.[/red]')

            # print("\r")
            # print(captured_output)


except KeyboardInterrupt:
    print("[red]\nProgram terminated by user (Ctrl+C)[/red]")
    conn.close_connection()
    sys.exit(0)
