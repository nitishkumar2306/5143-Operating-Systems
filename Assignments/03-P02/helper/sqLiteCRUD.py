# conn Class for Sqlite

import sqlite3
from prettytable import PrettyTable
from rich import print   
class SQLiteconn:
    
    def __init__(self, db_path):
        """Initialize database connection and cursor."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __raw_results(self, results):
        """Convert raw results to a list of table names."""
        table = []
        for row in results:
            table.append(row[0])
        return table     

    def __formatted_results(self, results):
        """Format results as a PrettyTable."""
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def create_table(self, table_name, columns,unique_constraint):
        """
        Params:
            table_name (str) - name of table
            columns (list) - ["id INTEGER PRIMARY KEY", "name TEXT", "created TEXT", "modified TEXT", "size REAL","type TEXT","owner TEXT","owner_group TEXT","permissions TEXT"]

        Create a new table with specified columns.
        
        Args:
            table_name (str): Name of the table.
            columns (list): List of column definitions.
        """
        try:
            # Create a table with the given columns 
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)},{unique_constraint} );"

            #create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"

            self.cursor.execute(create_table_query)
            self.conn.commit()
           # self.content_NULL(table_name)
            print(f"[green]Table '{table_name}' created successfully[/green]")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    # def content_NULL(self,table_name):
    #     try:
    #         query = f"UPDATE {table_name} SET content = NULL WHERE content = 'None';"
    #         self.cursor.execute(query)
    #         self.conn.commit()
    #         print(f"[green]Table '{table_name}' created successfully[/green]")
    #     except sqlite3.Error as e:
    #         print(f"Error creating table: {e}")

            

    def show_tables(self,raw=True):
        """Show all tables in the database.
        
        Args:
            raw (bool): Whether to return raw results or formatted table.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()

        if not raw: 
            return self.__formatted_results(results)
        else:
            return self.__raw_results(results)


    def describe_table(self,table_name,raw=False):
        """Describe the structure of a table.
        
        Args:
            table_name (str): Name of the table.
            raw (bool): Whether to return raw data or a PrettyTable.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        table = None
        
        if not raw:
            table = self.__formatted_results(results)
           
        else:
        
            table= []

            for column_info in results:
                column_name = column_info[1]
                data_type = column_info[2]
                is_nullable = "NULL" if column_info[3] == 0 else "NOT NULL"
                table.append({"column_name":column_name,"data_type":data_type,"isnull":is_nullable})
                #print(f"Column Name: {column_name}, Data Type: {data_type}, Nullable: {is_nullable}")
                
        return table
        
            
    def insert_data(self, table_name, data):
        """Insert data into a table.
        
        Args:
            table_name (str): Name of the table.
            data (tuple): Data to insert.
        """
        try:
            # Insert data into the table
            placeholders = ', '.join(['?'] * len(data))
            insert_query = f"INSERT INTO {table_name} (pid, name, type, user_id ,created_date, modified_date, size, permissions, hidden, content) VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            #print("Data inserted successfully.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    
    def get_id(self, table_name, select_column, conditions):
        try:
            condition_values = [value for _, value in conditions]
            condition_str = " AND ".join([f"{col} = ?" for col, _ in conditions])
            select_query = f"SELECT {select_column} FROM {table_name} WHERE {condition_str};"
            # print("Line 141",select_query)
            # print("Line 142", condition_values)
            self.cursor.execute(select_query, condition_values)
            result = self.cursor.fetchall()
            
            return result
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")

    def read_data(self, table_name, condition_id=None):
        """Read data from a table, optionally filtered by id.
        
        Args:
            table_name (str): Name of the table.
            condition_id (int, optional): ID to use in the WHERE clause. Default is None.
        """
        try:
            # Construct the SQL query with an optional WHERE clause
            if condition_id is not None:
                select_query = f"SELECT id,pid,name, type,user_id, created_date, modified_date, size, permissions, hidden FROM {table_name} WHERE pid = ?;"
                self.cursor.execute(select_query, (condition_id,))
            else:
                select_query = f"SELECT * FROM {table_name};"
                self.cursor.execute(select_query)

            result = self.cursor.fetchall()
            if result:
                return self.__formatted_results(result)
            else:
                print("No data found in the table.")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")        

    def get_data(self, table_name, user_table,condition_id=None):
        """Read data from a table, optionally filtered by id.
        
        Args:
            table_name (str): Name of the table.
            condition_id (int, optional): ID to use in the WHERE clause. Default is None.
        """
        try:
            # Construct the SQL query with an optional WHERE clause
            if condition_id is not None:
                select_query = f"SELECT {table_name}.id,name, type,{user_table}.owner, modified_date, size, permissions, hidden \
                                FROM {table_name}  \
                                LEFT JOIN  {user_table} on {table_name}.user_id= {user_table}.id \
                                WHERE pid =?;"
                self.cursor.execute(select_query, (condition_id,))
            else:
                select_query = f"SELECT * FROM {table_name};"
                self.cursor.execute(select_query)

            result = self.cursor.fetchall()
            if result:
                return result
            else:
                print("[red] No data found in the table.[/red]")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")     
    # def update_data(self, table_name, column, new_value, condition_column, condition_value):
    #     """Update data in a table based on a condition.
        
    #     Args:
    #         table_name (str): Name of the table.
    #         column (str): Column to update.
    #         new_value (str): New value to set.
    #         condition_column (str): Column to use in the WHERE clause.
    #         condition_value (str): Value to use in the WHERE clause.
    #     """
    #     try:
    #         # Update data in the table based on a condition
    #         update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition_column} = ?;"
    #         self.cursor.execute(update_query, (new_value, condition_value))
    #         self.conn.commit()
    #         print("Data updated successfully.")
    #     except sqlite3.Error as e:
    #         print(f"Error updating data: {e}")

    def update_data(self, table_name, columns_and_values, condition_column, condition_value):
        """Update data in a table based on a condition.
        
        Args:
            table_name (str): Name of the table.
            columns_and_values (dict): A dictionary of columns and their new values.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        """
        try:
            # Construct the SET part of the SQL query dynamically
            set_clause = ', '.join([f"{column} = ?" for column in columns_and_values])
            
            # Create a tuple of values to set
            values = tuple(columns_and_values.values())
            
            # Update data in the table based on a condition
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = ?;"
            self.cursor.execute(update_query, values + (condition_value,))
            self.conn.commit()
          #  print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

        def delete_data(self, table_name, condition_column, condition_value):
            """Delete data from a table based on a condition.
            
            Args:
                table_name (str): Name of the table.
                condition_column (str): Column to use in the WHERE clause.
                condition_value (str): Value to use in the WHERE clause.
            """
            try:
                # Delete data from the table based on a condition
                delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
                self.cursor.execute(delete_query, (condition_value,))
                self.conn.commit()
                print("Data deleted successfully.")
            except sqlite3.Error as e:
                print(f"Error deleting data: {e}")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
       # print("Database connection closed.")
        
        
    def formatted_print(self,table_name):
        """Print the contents of a table in a formatted manner.
        
        Args:
            table_name (str): Name of the table.
        """
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()
        
        table_info_list = []

        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)

        return table

    def table_exists(self, table_name,db_path=None):
        """Check if a table exists.
        
        Args:
            table_name (str): Name of the table.
            db_path (str, optional): Path to the database. Defaults to the initialized db_path.
        """
        different_conn = False
        if not db_path:
            db_path = self.db_path
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
        else:
            different_conn = True
            conn = self.conn
            cursor = self.conn.cursor()
            
        try:

            # Query the sqlite_master table to check if the table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            result = cursor.fetchone()

            # If result is not None, the table exists
            return result is not None

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

        finally:
            if different_conn:
                conn.close()



    def drop_table(self,table_name):
        """Drop a table by its name.
        
        Args:
            table_name (str): Name of the table to drop.
        """
        try:

            # Drop the table if it exists
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

            # Commit the changes
            self.conn.commit()
            print(f"[red]Table {table_name} Dropped [/red]")
            return True

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        
    def add_user(self, table_name, data):
        """Insert data into a table.
        
        Args:
            table_name (str): Name of the table.
            data (tuple): Data to insert.
        """
        try:
            # Insert data into the table
            placeholders = ', '.join(['?'] * len(data))
            insert_query = f"INSERT INTO {table_name} (owner,groop,password) VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            #print("Data inserted successfully.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def calculate_folder_size(self,folder_id):
   
            self.cursor.execute("SELECT id, type,size FROM files_data WHERE pid = ?", (folder_id,))
            contents = self.cursor.fetchall()
            folder_size = 0

            for content_id, content_type,size in contents:
                if content_type == 'file':
                        file_size = float(size)
                        folder_size += file_size
                elif content_type == 'folder':
                     # Recursively calculate the size of the subfolder and add it to the folder_size
                     subfolder_size = self.calculate_folder_size(content_id)
                     folder_size += subfolder_size
            return folder_size  
    
    
    def get_data_tuple(self, table_name, user_table,condition_id=None):
            """Read data from a table, optionally filtered by id.
            
            Args:
                table_name (str): Name of the table.
                condition_id (int, optional): ID to use in the WHERE clause. Default is None.
            """
            try:
                # Construct the SQL query with an optional WHERE clause
                if condition_id is not None:
                    select_query = f"SELECT * \
                                    FROM {table_name}  \
                                    LEFT JOIN  {user_table} on {table_name}.user_id= {user_table}.id \
                                    WHERE {table_name}.id =?;"
                    self.cursor.execute(select_query, (condition_id,))
                else:
                    select_query = f"SELECT * FROM {table_name};"
                    self.cursor.execute(select_query)

                result = self.cursor.fetchall()
                if result:
                    return result
                else:
                    print("[red]No data found in the table.[/red]")
            except sqlite3.Error as e:
                print(f"Error reading data: {e}")   

    def delete_directory(self,directory_id):
        # Check if the directory exists
        self.cursor.execute("SELECT id FROM files_data WHERE id = ? AND type = 'folder'", (directory_id,))
        dir_exists = self.cursor.fetchone()

        if dir_exists:
            # List contents of the directory 
            self.cursor.execute("SELECT id, type FROM files_data WHERE pid = ?;",(directory_id,))
            contents = self.cursor.fetchall()

            for content_id, content_type in contents:
                if content_type == 'file':
                    # Delete file
                    self.cursor.execute("DELETE FROM files_data WHERE id = ?", (content_id,))
                elif content_type == 'directory':
                    # Recursively delete subdirectory
                    self.delete_directory(content_id)

            # Delete the directory itself
            self.cursor.execute("DELETE FROM files_data WHERE id = ?", (directory_id,))
        else:
            print("Directory not found.")   

    def delete_file(self,file_id):
        # Construct the DELETE query
        delete_query = f"DELETE FROM files_data WHERE id = {file_id};"

        # Execute the DELETE query with the file ID as a parameter
        self.cursor.execute(delete_query)
    
    def update_data_history(self, table_name, columns_and_values, condition_column, condition_value):
        """Update data in a table based on a condition.

        Args:
            table_name (str): Name of the table.
            columns_and_values (dict): A dictionary of columns and their new values.
            condition_column (str): Column to use in the WHERE clause.
            condition_value (str): Value to use in the WHERE clause.
        """
        try:
            # Construct the SET part of the SQL query dynamically
            set_clause = ', '.join([f"{column} = ?" for column in columns_and_values])

            # Create a tuple of values to set
            values = tuple(columns_and_values.values())

            # Update data in the table based on a condition
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = ?;"
            self.cursor.execute(update_query, values + (condition_value,))
            self.conn.commit()
            print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
        

    def insert_data_history(self, table_name, data):
        """Insert data into a table.
        
        Args:
            table_name (str): Name of the table.
            data (tuple): Data to insert, including user_id and commands.
        """
        try:
            # Insert data into the table
            placeholders = ', '.join(['?'] * len(data))
            insert_query = f"INSERT INTO {table_name} (user_id, commands) VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
         #   print("Data inserted successfully.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
    
    def get_id_chmod(self, table_name, select_column, conditions):
        try:
            condition_values = [value for _, value in conditions]
            condition_str = " AND ".join([f"{col} = ?" for col, _ in conditions])
            select_query = f"SELECT {select_column} FROM {table_name} WHERE {condition_str};"

            self.cursor.execute(select_query, condition_values)
            result = self.cursor.fetchall()
            
            return result
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
       

    def read_data_history(self, table_name, condition_id=None):
        """Read data from a table, optionally filtered by id.
        
        Args:
            table_name (str): Name of the table.
            condition_id (int, optional): ID to use in the WHERE clause. Default is None.
        """
        try:
            # Construct the SQL query with an optional WHERE clause
            if condition_id is not None:
                select_query = f"SELECT id,user_id, pid,  commands hidden FROM {table_name} WHERE pid = ?;"
                self.cursor.execute(select_query, (condition_id,))
            else:
                select_query = f"SELECT * FROM {table_name};"
                self.cursor.execute(select_query)

            result = self.cursor.fetchall()
            if result:
                return self.__formatted_results(result)
            else:
                print("No data found in the table.")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
        

    def get_data_chmod(self, table_name, user_table, condition_id=None):
        """Read data from a table, optionally filtered by id.

        Args:
            table_name (str): Name of the table.
            user_table (str): Name of the user-related table.
            condition_id (int, optional): ID to use in the WHERE clause. Default is None.
        """
        try:
            # Construct the SQL query with an optional WHERE clause
            if condition_id is not None:
                select_query = f"SELECT {table_name}.id, {table_name}.name, {table_name}.type, {user_table}.owner, {table_name}.modified_date, {table_name}.size, {table_name}.permissions, {table_name}.hidden \
                                FROM {table_name} \
                                LEFT JOIN {user_table} ON {table_name}.user_id = {user_table}.id \
                                WHERE {table_name}.pid = ?;"
                self.cursor.execute(select_query, (condition_id,))
            else:
                select_query = f"SELECT * FROM {table_name};"
                self.cursor.execute(select_query)

            result = self.cursor.fetchall()
            if result:
                return result
            else:
                print("[red]No data found in the table.[/red]")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")


    def get_data_history(self, table_name, user_table, condition_id=None):
        """Read data from a table, optionally filtered by user ID.

        Args:
            table_name (str): Name of the table.
            user_table (str): Name of the user table.
            condition_id (int, optional): User ID to use in the WHERE clause. Default is None.
        """
        try:
            # Construct the SQL query with an optional WHERE clause
            if condition_id is not None:
                select_query = f"SELECT {table_name}.id, {table_name}.commands " \
                            f"FROM {table_name} " \
                            f"LEFT JOIN {user_table} ON {table_name}.user_id = {user_table}.id " \
                            f"WHERE user_id = ?;"
                self.cursor.execute(select_query, (condition_id,))
            else:
                select_query = f"SELECT * FROM {table_name};"
                self.cursor.execute(select_query)

            result = self.cursor.fetchall()
            if result:
                return result
            else:
                print("[red]No data found in the table.[/red]")
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")