'''
connector.py contains a class where the connections and database values are stored.
It has functions to set up connections if inputs are correct and database is accessible,
also functions to disconnect all connections.
Additionally, there are some functions to check if id, host, port, type are valid
and a function who returns all active connections.

following values are stored for one database:

    ID: User given ID for the database connection. it's impotent to identifier the correct connection ID's are unique
    Host: IP address or localhost. dns names are not supported
    Port: Port-number of the Database connection
    Database: name of the database to be accessed
    User: Username to login into the database
    Password: Users password to login into the database
    Connection_URL: complete url for the connection with information about host, port database,
                    username, password and database type in it example: 'postgresql://postgres:pwd1234@localhost:5432/DatabaseName'
    Conn: the actual connection information are stored here
    Connected: flag if database is connected and used for the current user request


'''

import os
from yaml import Loader
import yaml
import Database_classes.DatabaseManager


class Connector:
    databases_list = {}

    id = ""
    host = ""
    port = ""
    database = ""
    user = ""
    pwd = ""
    connection_url = ""
    conn = ""
    type = ""


    def __init__(self, path, project_home):
        '''
        Description
        -----------
        constructor of the class Connector.
        loads the data from the databases.yaml file, where all connections are stored and saves them into the
        list as dictionaries

        Parameters
        ----------
            path: str
                path to the databases.yaml file
            project_home: str
                path to the project root folder
        '''
        self.project_home = project_home
        self.databasePaths = os.path.join(self.project_home, path)

        stream = open(self.databasePaths, 'r')
        databases_dict = yaml.load(stream, Loader=Loader)

        # select the right url in relation to the type
        def choose_url(conn):
            try:
                return {
                    'postgresql': f'postgresql://{conn["User"]}:{conn["Password"]}@{conn["Host"]}:{conn["Port"]}/{conn["Database"]}',
                    'mysql': f'mysql://{conn["User"]}:{conn["Password"]}@{conn["Host"]}:{conn["Port"]}/{conn["Database"]}',
                    'mariadb': f'jdbc:mariadb://{conn["User"]}:{conn["Password"]}@{conn["Host"]}:{conn["Port"]}/{conn["Database"]}'
                }[conn['Type'].lower()]
            except:
                exit("Database type not found")

        if databases_dict == None:
            tmp_list = []
        else:
            tmp_list = list(databases_dict)
            for index in range(len(list(databases_dict))):
                try:
                    self.check_id(tmp_list[index]['ID'])
                    self.check_host(tmp_list[index]['Host'], tmp_list[index]['ID'])
                    self.check_port(tmp_list[index]['Port'], tmp_list[index]['ID'])
                    self.check_type(tmp_list[index]['Type'], tmp_list[index]['ID'])

                    database_values = {"Type": tmp_list[index]['Type'],
                                       "Host": tmp_list[index]['Host'],
                                       "Port": tmp_list[index]['Port'],
                                       "Database": tmp_list[index]['Database'],
                                       "User": tmp_list[index]['User'],
                                       "Password": tmp_list[index]['Password'],
                                       "Connection_URL": choose_url(tmp_list[index]),
                                       "Conn": "",
                                       "ID": tmp_list[index]['ID'],
                                       "Connected": False
                                       }
                    self.databases_list[tmp_list[index]['ID']] = database_values
                except:
                    pass

    def connect_all(self):
        '''
        Description
        -----------
        this function sets the connection and filters out connections which are not valid or reachable.

        '''
        for database in list(self.databases_list.values()):
            try:
                database['Conn'] = Database_classes.DatabaseManager.create_connection_url(database, self.project_home)
                database['Connected'] = True

            except:
                del self.databases_list[database['ID']]
                print('\033[91m' + f'Connecting to Database with ID: {database["ID"]} failed' + '\033[0m')
                pass

        return self

    def select_database_by_id(self, connection_id):
        '''
        Description
        -----------
        this function searches for the database dictionaries based on the given id list and returns them as a list.

        Parameters
        ----------
            connection_id: [str]
                list of ID's to be searched for
        '''
        tmp_list = []

        try:
            for id in connection_id:
                tmp_list.append(self.databases_list[id])
        except:
            exit(f"No database with ID: {connection_id} exists.")
        return tmp_list

    def check_host(self, host, id):
        '''
        Description
        -----------
        This function checks if the host is valid.
        only IP addresses and localhost are allowed.
        DNS-Names are not supported.

        Parameters
        ----------
            host: str
                IP address to be checked
            id: str
                id of the host to be checked for
        '''
        import ipaddress

        if host.lower() == "localhost":
            pass
        else:
            try:
                ip = ipaddress.ip_address(host)
            except ValueError:
                print('\033[91m' + f'{host} invalide IP-Adress in Database with ID: {id}' + '\033[0m')
            except:
                print('\033[91m' + f'{host} invalide IP-Adress in Database with ID: {id}' + '\033[0m')
        return None

    def check_port(self, port, id):
        '''
        Description
        -----------
        This function checks if the port is valid.
        only port in a range of 1 to 65535 are allowed.

        Parameters
        ----------
            port: str
                database port
            id: str
                id of the port to be checked for
        '''
        try:
            port = int(port)
            if 1 <= port <= 65535:
                return None
            else:
                raise ValueError
        except ValueError:
            print('\033[91m' + f"Port: {port} in Database with ID: {id} is not a valide portnumber" + '\033[0m')
            return next()

    def check_id(self, id):
        '''
        Description
        -----------
        This function checks if the database id is unique.

        Parameters
        ----------
            id: str
                id to be checked for uniqueness
        '''
        try:
            for database in self.databases_list.values():
                if database['ID'] == id:
                    raise ValueError
                else:
                    pass
            return None
        except ValueError:
            print('\033[91m' + f"Database ID: {id} already exists" + '\033[0m')
            return next()

    def check_type(self, type, id):
        '''
        Description
        -----------
        This function checks if the database type is supported.
        Supported types are: PostgreSQL, MySQL and MariaDB

        Parameters
        ----------
            type: str
                type of database
            id: str
                id of the type to be checked for
        '''
        try:
            if type.lower() == 'mariadb' or type.lower() == 'mysql' or type.lower() == 'postgresql':
                return None
            else:
                raise ValueError
        except ValueError:
            print(
                '\033[91m' + f"Type: {type} in Database with ID: {id} is not supported.\nSupported types are: PostgreSQL, MySQL, MariaDB " + '\033[0m')
            return next()

    def disconnect_all(self):
        '''
        Description
        -----------
        This function disconnect all active connections.
        '''
        for database in self.databases_list.values():
            if database['Connected']:
                database['Conn'].close()
        return None
