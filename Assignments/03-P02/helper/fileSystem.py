# Filesystem Starter Class

from helper.sqLiteCRUD import SQLiteconn
from prettytable import PrettyTable
from rich import print
from rich.table import Table
from rich.box import SIMPLE
import humanize
import os
from helper.utils import get_file_list,convertToBinaryData,convertToDigitalData,current_time,display_ls
table_name="files_data"
table_name1="history"
user_table="user"

class FileSystem:
    def __init__(self,conn=None):
        if not conn:
            self.conn = SQLiteconn("filesystem.db")
        else:
            self.conn = conn
        self.user="root"
        self.user_id=1
        self.cwd = "/home/"+self.user
        self.cwdid = 3
        self.user_fid=3
    
    def base_url(self):
        return "/home/"+self.user
    
    def current_usr(self):
        return self.user,self.user_id 

    def getFileId(self,path):
        """ Find a file id using current location + name
        """
        if path.startswith("/"):
                if not path.startswith(self.base_url()):
                    print("Invalid abosulte path ")
                    return None,None
        folders = [folder for folder in path.split('/') if folder]

        url=self.cwd #to construct the URL based on the provided path

        if not path.startswith("/"):
            parent_id=self.cwdid    
        else :
            parent_id=0
        for folder in folders:
            if folder=="..":
                result=self.conn.get_id(table_name,"pid",[ ("type", "folder"),("id", parent_id)])
                if result:
                    folder_id = result[0][0]  # Extract the id from the result
                    parent_id=folder_id
                    url = url.rsplit('/', 1)[0]  # Remove the last component
                    continue
                else:
                    print("[red] Folder is not found[/red] ",folder)
                    return None,None
            else:    
            #check existing folder 
                result=self.conn.get_id(table_name,"id",[("name", folder), ("type", "folder"),("pid", parent_id)])
                if result:
                    folder_id = result[0][0]  # Extract the id from the result
                    parent_id=folder_id
                    url= os.path.join(url, folder)
                    continue
                else:
                    print("[red] Folder is not found [/red]",folder)
                    return None,None
        return parent_id,url


    def ls(self,**kwargs):
        """ List the files and folders in current directory
        """
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []  
        if   kwargs["params"]:
            path=kwargs["params"][0]
            id,url=self.getFileId(path)
        else:
            id =self.cwdid
        if id:
         ## todo print user name istead of id
        #  print(self.conn.read_data("files_data",id))
            #files_before = {
        # "file1.txt": ("user", "-rw-r--r--", "12 KB"),
        # "file2.txt": ("user", "-rw-r--r--", "15 KB")
        # }
            data=self.conn.get_data(table_name,user_table,id)
            table = Table(show_header=True, header_style="bold blue", box=SIMPLE)

            table.add_column("Name", style="dim", width=20)
            table.add_column("Type", style="dim", width=10)
            table.add_column("Owner", width=10)
            table.add_column("Permissions", width=15)
            table.add_column("Size", justify="right")
            table.add_column("modified_date", width=20)
            if data:
                for row in data:
                    #{table_name}.id,name, type,{user_table}.owner, modified_date, size, permissions, hidden 
                    id,name,type,owner, date,size, perms,hidden=row
                    if not "a" in flags and hidden==1:
                        continue
                    if type=="folder":
                      size= self.conn.calculate_folder_size(id)
                    if "h" in flags:
                        size=humanize.naturalsize(size)     
                    table.add_row(name, type,owner, perms, str(size),str(date))
                print(table)
        
        
         

    def mkdir(self,**kwargs):
        """ Make a directory
        """    
        # pid name type  owner groop  created_date modification_time size permissions hidden content
        if not kwargs["params"]:
            print ("[red]No Params[/red]")
            return
        # Split the absolute path into individual folder names
        path=kwargs["params"][0]
        if path.startswith("/"):
            if not path.startswith(self.base_url()):
                print("[red]Invalid abosulte path [/red] ")
                return 
        folders = path.split(os.path.sep)
     
    
        if not path.startswith("/"):
            parent_id=self.cwdid
        else :
            parent_id=0
        # Define the conditions as a list of tuples (column_name, condition_value)
        for folder in folders:
            #check existing folder 
            result=self.conn.get_id(table_name,"id",[("name", folder), ("type", "folder"),("pid", parent_id)])
            if result:
                folder_id = result[0][0]  # Extract the id from the result
            #todo need to hanlde existing folder : create last one
                parent_id=folder_id
                continue
            else:
                hidden="0"
                c_time=current_time()
                if folder.startswith("."):
                 hidden="1"
                data=(parent_id,folder,"folder",self.user_id,c_time,c_time,"0","-rw-rw-r--",hidden,'NULL')
                folder_id=self.conn.insert_data(table_name,data)
                parent_id=folder_id
                print(f"[green] Folder created sucessfully:  [/green] [bold cyan]{folder}[/bold cyan]")

    def makefile(self,file_name,parent_id,content,file_size):
        # todo unique_constraint = "UNIQUE (name,type,pid)" why it is not working 
        # print("Line 135",file_name," ",parent_id," ",content," ",file_size)     
        result=self.conn.get_id(table_name,"id",[("name", file_name), ("type", "file"),("pid", parent_id)])
        c_time= current_time()
        hidden="0"
        if result:
            print("[red]Already exists  file [/red]",file_name)
            file_id=result[0][0] 
            #update the modified date
            #table_name, column, new_value, condition_column, condition_value
            #todo  update content as well "modified_date",c_time, 
            #update_data('your_table', {'column1': 'new_value1', 'column2': 'new_value2'}, 'id', 1)

            self.conn.update_data(table_name, {'modified_date': c_time, 'content': content,'size':file_size},"id", file_id)
            print(f"[green] File updated sucessfully: [/green] [bold cyan]{file_name}[/bold cyan]")

        else:
            if file_name.startswith("."):
                hidden="1"
            data=(parent_id,file_name,"file",self.user_id,c_time,c_time,file_size,"-rw-rw-r--",hidden,content)
            file_id=self.conn.insert_data(table_name,data)
            #parent_id=file_id
            print(f"[green] File created sucessfully: [/green] [bold cyan]{file_name}[/bold cyan]")       



    def touch(self,**kwargs):
        """ Make a empty file
        """    
        # pid name type  owner groop  created_date modification_time size permissions hidden content
        
        # Split the absolute path into individual folder names
        if not kwargs["params"]:
            print ("[red]No Params[/red]")
            return
        path=kwargs["params"][0]
        if path.startswith("/"):
            if not path.startswith(self.base_url()):
                print("[red]Invalid abosulte path [/red]")
                return 
        file_name=path.split('/')[-1]
        directory_path = '/'.join(path.split('/')[:-1])
        parent_id,url=self.getFileId(directory_path)
        self.makefile(file_name,parent_id,'NULL',0)
        
                
        #self.cwdid = self.conn.lastrowid

      #  print(self.conn.describe_table("files_data"))


    def chmod(self,**kwargs):
        """ Change the permissions of a file
            1) will need the file / folder id

            2) select permissions from the table where that id exists
            3) 
        Params:
            id (int) :  id of file or folder
            permission (string) : +x -x 777 644

            if its a triple just overwrite or update table 

        Example:
            +x 
            p = 'rw-r-----'
            p[2] = x
            p[5] = x
            p[8] = x


        """
        pass

    def cd(self,**kwargs):
        """
         Change working directory.
        """
        path=""
        if "params" in kwargs:
            params = kwargs["params"] if kwargs.get("params") else []
            if params:
                path=params[0]
        if path and (not "~" in path):
            parent_id,url= self.getFileId(path)   
            if parent_id:     
                if  path.startswith("/"):
                    self.cwdid=parent_id
                    self.cwd=path
                    print(f"[green] Changed to directory: [/green][bold cyan]{self.cwd}[/bold cyan]")
                else :
                    self.cwdid=parent_id
                    self.cwd=url
                    print(f"[green] Changed to directory: [/green][bold cyan]{self.cwd}[/bold cyan]")
             
        else:
            # Change to the home directory
            self.cwd=self.base_url()
            self.cwdid=self.user_fid
            print(f"[green] Changed to directory: [/green][bold cyan]{self.cwd}[/bold cyan]")

    def pwd(self,**kwargs):
            """ 
                prints current working directory
            """
            print(f"[green] Current Directory: [/green][bold cyan]{self.cwd}[/bold cyan]")
           # print( "Current Directory id: ",self.cwdid)  
            #print( "Current user: ",self.user )  
           # print( "Current user id: ",self.user_id )  

            return self.cwd 

    def isfolder(self,directory_path):
        """
            Used to find the parent_id of the given path
        """
        parent_id,url=self.getFileId(directory_path)
        if parent_id:
            return parent_id
        else:
            return None
        
    def insert(self,**kwargs):
        """ Copy files from existing filesystem to this file system
            insert src_loc dest_location
        """    
        
        if not kwargs["params"] or len(kwargs["params"])<2 :
            print ("[red]No Params[/red]")
            return
        
        dest_loc=kwargs["params"][1]
        src_loc=kwargs["params"][0]
        fileList=get_file_list(src_loc)
        for file_tuple in fileList:
            file_path=file_tuple[0]
            file_size=file_tuple[1]
            content =convertToBinaryData(file_path)
            src_file_name=file_path.split('/')[-1]
        
            if "."==dest_loc :
                parent_id=self.cwdid
                dest_file_name=src_file_name
            else:
                isfolder=self.isfolder(dest_loc)
                if isfolder:
                    dest_file_name=src_file_name 
                    parent_id=isfolder 
                else:           
                    dest_file_name=dest_loc.split('/')[-1]
                    directory_path = '/'.join(dest_loc.split('/')[:-1])
                    parent_id,url=self.getFileId(directory_path)
            
            self.makefile(dest_file_name,parent_id,content,file_size)
                
    #sudo adduser username
    def adduser(self, **kwargs):
        """
            Used to create new user
        """
        params = kwargs["params"] 
        if params:
            user=params[0]
            if len(params) >1:
                password=params[1]
            else:    
                print(f"[bold blue]Enter a password :[/bold blue] ", end='')
                print(f"",end="")
                password=input()
            user_id=self.conn.add_user(user_table,[user,user,password])
            hidden="0"
            c_time=current_time()
            folder_id=self.conn.get_id(table_name,"id",[("name", user),("pid", "2")])
            if not folder_id:
                data=("2",user,"folder",user_id,c_time,c_time,"0","-rw-rw-r--",hidden,None)
                folder_id=self.conn.insert_data(table_name,data)
                self.user_fid=folder_id
            if user_id and folder_id:
             print(f"[green][green] User  created sucessfully: [/green] [bold cyan]{user}[/bold cyan]")       
    
        else:
            print("[red]Username requried [/red]")   

    #swicth username    
    def su(self, **kwargs):  
        """
            Used to switch users
        """
        params = kwargs["params"] 
        if params:

            user=params[0]
            result=self.conn.get_id(user_table,"id",[("owner", user)])
            if result:
                user_id=result[0][0]
                folder_id=self.conn.get_id(table_name,"id",[("name", user),("user_id", user_id),("pid", 2)])
                self.user=user
                self.user_id=user_id
                self.user_fid=folder_id[0][0]

                self.cwd = "/home/"+user
                self.cwdid = folder_id[0][0]
            else:
                print (" [red]User does not exist: [/red]",user)    

            
        else:
            print("[red]Username requried[/red]")   
     

    def who(self, **kwargs): 
        """
            show currently logged in user
        """
        print(f"[green] {self.user}[/green]")


    def get_File_Folder_Id(self,path):
            # print("Line 340",path)
            if path.startswith("/"):
                if not path.startswith(self.base_url()):
                    print("Invalid abosulte path ")
                    return None,None
            folders = [folder for folder in path.split('/') if folder]
            # print("Line 346",folders)

            url=self.cwd #to construct the URL based on the provided path

            if not path.startswith("/"):
                parent_id=self.cwdid    
            else :
                parent_id=0
            for folder in folders:
                data = self.conn.get_id(table_name,"type",[("pid", parent_id),("name",folder)])
                # print(data," ",type(data)," ",data == [])
                if data != []:
                    data = ''.join(data[0][0].split())
                else:
                    return None,None
                # print("Line 356",data[0][0]," ",data == "file")
                storage_type = "file" if data == "file" else "folder"
                if folder=="..":
                    result=self.conn.get_id(table_name,"id",[ ("type", storage_type),("id", parent_id)])
                    if result:
                        folder_id = result[0][0]  # Extract the id from the result
                        parent_id=folder_id
                        url = url.rsplit('/', 1)[0]  # Remove the last component
                        continue
                    else:
                        print("Folder is not found ",folder)
                        return None,None
                else:    
                #check existing folder 
                    # print("Line 370",table_name," ",parent_id," ",folder," ",storage_type)
                    result=self.conn.get_id(table_name,"id",[("name", folder), ("type", storage_type),("pid", parent_id)])
                    if result:
                        folder_id = result[0][0]  # Extract the id from the result
                        parent_id=folder_id
                        url= os.path.join(url, folder)
                        continue
                    else:
                        print("Folder is not found ",folder)
                        return None,None
            return parent_id,url
        
    def copy_comm(self,dest,file_id):
        """
            recursively copies the files inside a directory to destination directory
        """
        data=self.conn.get_data_tuple(table_name,user_table,file_id)
        id_1 = data[0][0]
        files = self.conn.get_id(table_name,"*",[("pid", id_1)])
        while(files != []):
            l1 = files.pop()
            file_name = l1[2].strip()
            fid = l1[0] 
            data=self.conn.get_data_tuple(table_name,user_table,fid)
            content = str(l1[10]) if str(l1[10]) is not None else "NULL" 
            permissions = l1[8]
            size = l1[7]
            hidden = l1[9]
            if "."== dest :
                parent_id = self.cwdid
                dest_file_name = file_name
            else:
                isfolder=self.isfolder(dest)
                if isfolder:
                    dest_file_name = file_name
                    parent_id=isfolder 
                else:           
                    dest_file_name=dest.split('/')[-1]
                    directory_path = '/'.join(dest.split('/')[:-1])
                    parent_id,url=self.getFileId(directory_path)
            if data[0][3].strip().lower() == "folder":
                self.make_file_folder(dest_file_name,parent_id,content,size,hidden,permissions,type="folder")
                dest1 = dest+"/"+file_name+"/"
                self.copy_comm(dest1,fid)
            else:   
                self.make_file_folder(dest_file_name,parent_id,content,size,hidden,permissions,type="file")

    def cp(self, **kwargs):
        """
            Copy files/directory from source directory to destination directory
        """
        if kwargs["params"] != []:
            s1 = kwargs["params"]
            if len(s1) == 1:
                print(f"[red] \ncp: missing file operand[/red] ")
            elif len(s1) == 2:
                source = s1[0]
                dest = s1[1]
                file_id,url = self.get_File_Folder_Id(source)
                source = source.split('/')[-1]
                if not file_id is None:
                    data=self.conn.get_data_tuple(table_name,user_table,file_id)
                    if data[0][3].strip().lower() == "folder":
                        self.copy_comm(dest,file_id)
                    else:
                        content = str(data[0][10]) if str(data[0][10]) is not None else "None"
                        permissions = data[0][8] 
                        size = data[0][7]
                        hidden = data[0][9]   
                        if "."== dest :
                            parent_id = self.cwdid
                            dest_file_name = source
                        else:
                            isfolder=self.isfolder(dest)
                            if isfolder:
                                dest_file_name = source
                                parent_id=isfolder 
                            else:           
                                dest_file_name=dest.split('/')[-1]
                                directory_path = '/'.join(dest.split('/')[:-1])
                                parent_id,url=self.getFileId(directory_path)
                        self.make_file_folder(dest_file_name,parent_id,content,size,hidden,permissions,type="file")
                else:
                    print("cp: cannot stat ",source," : No such file or directory")
            elif len(s1) > 2:
                pass
        else:
            print(f"[red] \ncp: missing file operand[/red] ")
        
    def make_file_folder(self,file_name,parent_id,content,file_size,hidden,permissions,type):    
        result=self.conn.get_id(table_name,"id",[("name", file_name), ("type", type),("pid", parent_id)])
        c_time= current_time()
        hidden="0"
        if result:
            print("[red]Already exists  file [/red]",file_name)
            file_id=result[0][0] 
            self.conn.update_data(table_name, {'modified_date': c_time, 'content': content,'size':file_size,'permissions':permissions,'hidden':hidden},"id", file_id)
            print(f"[green] File updated sucessfully: [/green] [bold cyan]{file_name}[/bold cyan]")
        else:
            if file_name.startswith("."):
                hidden="1"
            data=(parent_id,file_name,type,self.user_id,c_time,c_time,file_size,permissions,hidden,content)
            file_id=self.conn.insert_data(table_name,data)
            print(f"[green] File created sucessfully: [/green] [bold cyan]{file_name}[/bold cyan]")  


    def mv(self, **kwargs):
        """
            Move files/directory from source directory to destination directory
        """
        if kwargs["params"] != []:
            s1 = kwargs["params"]
            if len(s1) == 1:
                print(f"[red] \nmv: missing file operand[/red] ")
            elif len(s1) == 2:
                source = s1[0]
                dest = s1[1]
                file_id,url = self.get_File_Folder_Id(source)
                source = source.split('/')[-1]
                if not file_id is None:
                    data=self.conn.get_data_tuple(table_name,user_table,file_id)
                    if data[0][3].strip().lower() == "folder":
                        self.copy_comm(dest,file_id)
                        self.conn.delete_directory(file_id)
                    else:
                        content = str(data[0][10]) if str(data[0][10]) is not None else "NULL"
                        permissions = data[0][8] 
                        size = data[0][7]
                        hidden = data[0][9]
                        if "."== dest :
                            parent_id = self.cwdid
                            dest_file_name = source
                        else:
                            isfolder=self.isfolder(dest)
                            if isfolder:
                                dest_file_name = source
                                parent_id=isfolder 
                            else:           
                                dest_file_name=dest.split('/')[-1]
                                directory_path = '/'.join(dest.split('/')[:-1])
                                parent_id,url=self.getFileId(directory_path)
                        self.make_file_folder(dest_file_name,parent_id,content,size,hidden,permissions,type="file")
                        self.conn.delete_file(file_id)
                else:
                    print(f"[red]No such file or directory[/red]")
        else:
            print(f"[red] \nmv: missing file operand[/red] ")
    

    def rm(self,**kwargs):
        """
        To remove a file or directory. Use -rf flag to remove a directory.
        """
        flag = kwargs["flags"] if "flags" in kwargs else None
        if kwargs["params"] != []:
            for file in kwargs["params"]:
                file_id,url = self.get_File_Folder_Id(file)
                if not file_id is None:
                    data=self.conn.get_data_tuple(table_name,user_table,file_id)
                    if data[0][3].strip().lower() == "folder":
                        if flag == 'rf':
                            self.conn.delete_directory(file_id)
                        else:
                            print(f"[red]rm: cannot remove {file}: Is a directory. \nUse -rf to delete a directory[/red]")
                    else:
                        self.conn.delete_file(file_id)
                else:
                    print(f"[red]No such file or directory[/red]")
        else:
           print(f"[red] \nrm: missing file operand[/red] ") 
        
    def cat(self,**kwargs):
        """
            To print contents of the file to the console.
        """
        if kwargs["params"] != []:
            for file in kwargs["params"]:
                file_ext = file.split('.')[-1]
                file_id,url = self.get_File_Folder_Id(file)
                if not file_id is None:
                    data=self.conn.get_data_tuple(table_name,user_table,file_id)
                    if data[0][3].strip().lower() == "folder":
                        print(f"[red]cat: {file}: Is a directory[/red]")
                    else:
                        # file = file.split('/')[-1]
                        # if file_ext == "jpg":
                        #     content = data[0][10]
                        #     convertToDigitalData(file, content)
                        # else:
                        content = data[0][10]
                        content = content.decode('utf-8')
                        print(content)
                else:
                    print(f"[red]No such file or directory[/red]")
        else:
           print(f"[red] \ncat: missing file operand[/red] ") 

    def chmod(self, **kwargs):
        if "params" not in kwargs or len(kwargs["params"]) < 2:
            print("Usage: chmod <permissions> <path>")
            return

        permissions = kwargs["params"][0]
        path = kwargs["params"][1]

        #   maps the numeric permissions to the string 
        permission_mapping = {
            "000": "-r--r--r--",
            "777": "-rwx-rwx-rwx",
            "644": "-rw-r--r--",
            "755": "-rwxr-xr-x",
            "666": "-rw-rw-rw-",
            "400": "-r--------",
            "751": "-rwxr-x--x",
            
        }

        # checking if provided permission value is in the mapping
        if permissions in permission_mapping:
            permission_string = permission_mapping[permissions]
        else:
            print(f"[red] Invalid permission value: {permissions} [/red]")
            return

        # extracting the file name and parent directory from the given path
        parent_directory = os.path.dirname(path)
        file_name = os.path.basename(path)

        # finding the entry in the database table
        parent_id, url = self.getFileId(parent_directory)
      #  print(parent_id, url)

        if parent_id is not None:
           
            # updating the permissions in the database table
            result=self.conn.get_id_chmod(user_table,"id",[("owner", self.user)])


            user_id=result[0][0] #then update
            if self.user_id == self.user_id:
                
            # only user has permissions to change the permissions
                update_data = {'permissions': permission_string}
                condition = {'name': file_name, 'type': "file" if "." in path else "folder", 'pid': parent_id}

                try:
                    #  method from SQLiteconn class to update data
                    self.conn.update_data(table_name, update_data, condition_column='name', condition_value=condition['name'])
                    print(f"[green] Permissions updated for {path} to {permission_string}.[/green]")
                except Exception as e:
                    print(f"Error updating permissions: {e}")
            else:
                print("You don't have permission to change permissions for", path)
        else:
            print("File or directory not found:", path)


    def history(self, **kwargs):
        history_data = self.conn.get_data_history('history', 'user', self.user_id)

        if history_data:
            table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
            table.add_column("SNo", style="dim", width=5)
            table.add_column("Command", style="dim", width=25)

            for i, data in enumerate(history_data, 1):
                command_id, command = data[0], data[1]
                table.add_row(str(i), command)
            print(table)
        else:
            print("No command history found.")

