## 28 Sep 2023

## 5143 Shell Project

## Group Members
- Nitish Kumar Erelli
- Madhav Adhikari
- Naga Vamshi Krishna Jammalamadaka
  
## Overview:
We use a shell quite often . This project implemented expected shell behavior using python. Below is a brief overview of top-level shell behavior:
- After start-up processing, your program repeatedly should perform these actions:
  - Print to stdout a prompt consisting of a  user name ,current path and percent sign followed by a space (example: madhav: /home/madhav/Documents/univeristy/5143-Opsys-102-private/Assignments/00-P01$: )
  -  Read a line from stdin (getch()).
  - logically analyze the line and create an array of command parts (tokens) ( handle the piping of commands)
  - Anyalized and create list of arguments and flags for commands
  - Once identified, the proper command is executed
  - if we have multiple commands then it will take input from the previous command and execute child command automatically
  - if output redirection exists then the output will be dumped to the files instead of print in shell console.
    
## Instructions
- Make sure you install all dependencies from requirments.txt
- Run shell.py (example : python3 shell.py)
- Type commands as per your requirements ( example: ls -la ) and also if you need a description of the command type the command followed with --help (example : ls --help)


### Commands:


|   Command   | Description | Author | Notes |
| :---: | ----------- | ---------------------- | ---------------------- |    
|ls|	listing files and directories |Madhav	|Flags: combination of ahl	and  none or multiple paramters|
|mkdir|	Make folder  on current directory or desired location|Madhav	|Flags: -p for make parent directories as needed  |
|cd	|Change the shell working directory |Madhav	|param: ~ change to the home directory or ..  change  to parent	 folder or desired folder|
|echo	|Print strings in console |Madhav	|param: strings values|
|grep	|Search for patterns in a  file |Madhav	|Flags: -i for ignore cases, -l for print matched files name, param: search pattern and file name as needed|
|pwd	|Show current working directory |Madhav	||
|command > file	| redirect standard output to a file | Madhav| File will be created on the current directory if the path is not provided | 
|command >> file |append standard output to a file | Madhav |File will be created/appended on the current directory if the path is not provided |
|command1 \| command2	|pipe the output of command1 to the input of command2| Madhav |
| History  | shows history of commands used in terminl | Naga |   |
| wc | shows word character and length  in the file | Naga |  |
|Sort | Sort command will sort the words or numbers depending on flag in terminal | Naga|
|!x |  executable command is used the use commands from the history |Naga |
|chmod| chmod is used to change the file permissions |Naga |
| who | print information about users who are currently logged in |Naga |
| whoami | Displays user, group and privileges information for the user who is currently logged | Naga|
| ps |  to display a list of your processes that are currently running|Naga |
| ifconfig | to assign an address to a network interface |Naga |
|cat|	 Concatenate FILE(s) to standard output |Nitish	Kumar||
|less|allows to view and navigate through text files |Nitish Kumar||
|head|Print the first 5 lines of each FILE to standard output |Nitish	Kumar|Flags: -n print the first NUM lines instead of the first 5|
|tail|Print the last 5 lines of each FILE to standard output |Nitish Kumar|Flags: -n print the last NUM lines instead of the first 5|
|touch|A FILE argument that does not exist is created empty |Nitish Kumar||
|cp|Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY| Nitish	Kumar |-R, -r, --recursive  copy directories recursively|
|mv| Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY | Nitish	Kumar ||
|rm|It is used to delete files/directories|Nitish	Kumar|-f ignore nonexistent files and arguments. -r, -R, --recursive   remove directories and their contents recursively|








### Non-Working Components
- Input redirection is not working
- 
## References
- http://www.pixelbeat.org/talks/python/ls.py.html
- https://docs.python.org/3/py-modindex.html
