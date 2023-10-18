#onetime create db and tables

from helper.sqLiteCRUD import SQLiteconn   
from helper.fileSystem import FileSystem
import time

conn = SQLiteconn("filesystem.db")
table_name = "files_data"
user_table="user"
history_table="history"
"""
id _====> 	A unique identifier for each file system entry (primary key).
pid	_====> 	The id of the parent folder.
name _====> 		The name of the file or directory.
type	_====> 	A text field representing the type of the file (e.g., "file" or "directory").
size	_====> 	The size of the file in bytes. This can be NULL for directories.
user_id ====> 		id of user table
permissions	_====> 	A text field representing the file permissions in the format "rwxr-xr-x" (example).
modification_time	_====> 	The date and time when the file was last modified.
content	_====> 	A BLOB column where you can store the file's contents directly. This is suitable for small file contents.
hidden_====> (Optional) Doesn't need to be a column as you could look for the dot in front of the filename. Up to you.
"""

files_columns = ["id INTEGER PRIMARY KEY", "pid INTEGER NOT NULL",
         "name TEXT NOT NULL", "type TEXT NOT NULL",
         "user_id INTEGER NOT NULL",
         "created_date TEXT NOT NULL", "modified_date TEXT NOT NULL", 
         "size REAL NOT NULL","permissions TEXT NOT NULL",
         "hidden NUMBER DEFAULT 0 ","content BLOB DEFAULT NULL",
         ]
conn.drop_table(table_name)
# Call the add_unique_constraint method to add the UNIQUE constraint
unique_constraint = "UNIQUE (name,type,pid)"
conn.create_table(table_name, files_columns,unique_constraint)
print(conn.describe_table(table_name))
time.sleep(2)

##add user table 
user_columns = ["id INTEGER PRIMARY KEY","owner TEXT NOT NULL","groop TEXT NOT NULL","password TEXT NOT NULL"]
conn.drop_table(user_table)
conn.create_table(user_table, user_columns,"UNIQUE (owner)")
print(conn.describe_table(user_table))
time.sleep(2)

fs = FileSystem(conn)
##add root as admin
fs.mkdir(params=["/home/root"])
fs.adduser(params=["root","toor"])

his_columns = [
    "id INTEGER PRIMARY KEY",
    "user_id INTEGER",
    
    "commands TEXT"
]
conn.drop_table(history_table)
conn.create_table(history_table, his_columns, unique_constraint="UNIQUE (id)")
print(conn.describe_table(history_table))
time.sleep(2)

conn.close_connection()
        