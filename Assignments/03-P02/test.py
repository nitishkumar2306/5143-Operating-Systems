import os

# Input folder or file path
path = "file.txt"

def get_file_info(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    except OSError:
        return None, None

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

# Now 'file_info_list' contains tuples with file paths and their sizes
print(file_info_list)
for file in file_info_list:
    file_name=file[0]
    file_size=file[1]
    print(file_name)
    print(file_size)