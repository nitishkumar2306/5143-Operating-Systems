import os
from datetime import datetime
from rich import print
from rich.table import Table
from rich.box import SIMPLE
import humanize
def get_file_info(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    except OSError:
        return None, None



def get_file_list(path):
    file_info_list = []

    if os.path.isdir(path):
        # If it's a directory, collect file paths and sizes
        for f in os.listdir(path):
            full_path = os.path.join(path, f)
            if os.path.isfile(full_path):
                file_path, file_size = get_file_info(full_path)
                if file_path and file_size is not None:
                    file_info_list.append((file_path, file_size))
    elif os.path.isfile(path):
        # If it's a file, collect the file path and size
        file_path, file_size = get_file_info(path)
        if file_path and file_size is not None:
            file_info_list.append((file_path, file_size))
    else:
        print(f"'{path}' is not a valid directory or file path")
    return file_info_list    

def convertToBinaryData(filename):
        # Convert digital data to binary format
        
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

def convertToDigitalData(filename, binaryData):
    directory = "Images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    full_path = os.path.join(directory, filename)

    with open(full_path, 'wb') as file:
        file.write(binaryData)

def current_time():
        # Get the current time as a datetime object
        current_time = datetime.now()

        # Format the datetime object as a string in the desired format
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time


def display_ls(files,flags):
    table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
    table.add_column("Name", style="dim", width=20)

    table.add_column("Name", style="dim", width=20)
    table.add_column("Type", style="dim", width=10)
    table.add_column("Owner", width=10)
    table.add_column("Permissions", width=15)
    table.add_column("Size", justify="right")
    table.add_column("modified_date", width=20) # name, type,user.owner, modified_date, size, permissions, hidden
   #calculate folder size recursively 
    if files: 
        for data in files:
            id,name,type,owner, date,size, perms,hidden=data
            if not "a" in flags and hidden==1:
                continue
            if "h" in flags:
                size=humanize.naturalsize(size)     
            table.add_row(str(id),name, type,owner, perms, str(size),str(date))
        print(table)