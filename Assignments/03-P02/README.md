## 28 Sep 2023

## 5143 Filesystem - Implementation of a virtual file system.

## Group Members
- Nitish Kumar Erelli
- Madhav Adhikari
- Naga Vamshi Krishna Jammalamadaka

## Overview:
This project implemented expected FileSystem behavior using python and Sqlite. Below is a brief overview of top-level behavior FileSystem:
-  Using create_table.py, we have created database (filesystem.db) and folowing tables

-  User table with unique constraint (UNIQUE (owner))

| Column Name | Description |
| --- | --- |
| id | A unique identifier for each user entry (primary key) |
| owner | User name |
| group | Group of users |
| password | Credential |

-  history table 

| Column Name | Description |
| --- | --- |
| id | A unique identifier for each  command entry (primary key) |
| user_id | id of user from user table |
| command | command typed from terminal |


-  files_data  table with unique constraint (UNIQUE (name,type,pid))

| Column Name        | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| id                 | A unique identifier for each file system entry (primary key) |
| pid                | The id of the parent folder                                |
| name               | The name of the file or directory                           |
| type               | A text field representing the type of the file (e.g., "file" or "folder") |
| user_id            | id of the user table                                       |
| created_date  | The date and time when the file was created         |
| modified_date  | The date and time when the file was last modified          |
| size               | The size of the file in bytes. This can be NULL for directories. |
| permissions        | A text field representing the file permissions in the format "rwxr-xr-x" (example) |
| content            | A BLOB column where you can store the file's contents directly |
| hidden   | 1 for . or hidden files and 0 for others files/fodlders |

-  We can do function from shell.py like insert files from computer fileSystem to our fileSystem , create folder, create user , swicth user , copy/move/remove files ,change permission 


    
## Instructions
- Make sure you install all dependencies from requirments.txt
- Run create_table.py  for database , tables and root user creation 
- Run shell.py (example : python3 shell.py) for user interation like type commands as per your requirements ( example: ls -la  or mkdir test)

### Commands:


|   Command   | Description | Author | Notes |
| :---: | ----------- | ---------------------- | ---------------------- |    
|ls|	listing files and directories |Madhav	|Flags: combination of ahl	|
|mkdir|	Make folder  on current directory or desired location|Madhav	| It created all folders if it is not exits in our FileSyste |
|cd	|Change working directory |Madhav	|param: ~ change to the home directory or ..  change  to parent	 folder or desired folder|
|pwd	|Show current working directory |Madhav	||
| who | print information about users who are currently logged in |Madhav |
|touch|A FILE argument that does not exist is created empty |Madhav||
|insert| insert files from existing FS to our FS |Madhav| Example: insert 2.jpg  test/3.jpg |
|adduser| add new user credential | Madhav| eg. adduser Tom|
|su | switch user |Madhav| eg. su root|
| History  | shows history of commands used in terminl | Naga |   |
|!x |  executable command is used the use commands from the history |Naga |
|chmod| chmod is used to change the file permissions |Naga |
|cat|	 Concatenate FILE(s) to standard output |Nitish	Kumar||
|cp|Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY| Nitish	Kumar |-R, -r, --recursive  copy directories recursively|
|mv| Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY | Nitish	Kumar ||
|rm|It is used to delete files/directories|Nitish	Kumar|-f ignore nonexistent files and arguments. -r, -R, --recursive   remove directories and their contents recursively|

### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [create_table.py  ](create_table.py)      | file that holds python code for database creation   |
|   2  | [shell.py](shell.py)     | file that holds code to interact with user  |
|   3 | [requirements.txt](requirements.txt)   | file that holds list of dependencies for this project    |


### Non-Working Components
- NOne