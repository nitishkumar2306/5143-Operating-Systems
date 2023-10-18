
"""
This file is about walkthrough of FS """
import sys
from time import sleep
import re
from helper.sqLiteCRUD import SQLiteconn
from helper.fileSystem import FileSystem
from rich import print
import subprocess
import time

if __name__ == '__main__':

    print(f"[green]++++++++++++++++ create database +++++++++++[/green]")
    time.sleep(1)
    subprocess.run(["python3", "create_table.py"])


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


    command_list=[
         "who",
        "adduser Leo 1234",
        "su Leo",
        "who",
        "pwd",
        "ls",
        "mkdir helper",
        "mkdir helper/java",
        "mkdir helper/python",
        "touch shell.py",
        "ls -h",
        "ls helper",
        "insert 2.jpg .",
        "insert helper/utils.py helper/python",
        "cd helper/python",
        "cd ..",
        "ls -h",
        "cat python/utils.py",
        "cp python/utils.py .",
        "ls -lah",
        "chmod 000 utils.py",
        "ls -lah",
        "chmod 777 utils.py",
        "ls -lah",
        "mv utils.py python/common.py",
        "ls python",
        "ls -lah",
        "rm -rf python",
        "ls -lah",
        "history"


    ]

try:
    print(f"[green]++++++++++++++++ FS walkthrough +++++++++++[/green]")
    for cmd_text in command_list:
        time.sleep(2)
        base_url=fs.base_url()
        user, user_id=fs.current_usr()
        print('[bold blue] '+base_url +':[/bold blue] ', end='')
        print(cmd_text)
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
                print(f'[red] Command "{cmd}" not found. Try again.[/red]')

            # print("\r")
            # print(captured_output)
        print("")    


except KeyboardInterrupt:
    print("[red]\nProgram terminated by user (Ctrl+C)[/red]")
    conn.close_connection()
    sys.exit(0)
