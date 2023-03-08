'''
In DatabaseManager.py are all functions stored to manage the database.yaml file where all database values are stored.
Entries can be added, removed and all entries can be listed.
Additionally, there is a function to create the connection URL based of the database values.

'''
import os
from pathlib import Path
import yaml
from yaml import Loader
import jaydebeapi as jay


# -n / -new-entry adds database by userinput in databases.yaml
def add_new_database(databasePaths):
    '''
        Description
        -----------
        poll the user for all needed data of the database and then writes them into the databases.yaml file in the correct format.
        After the input, the connection to the database is tested, if the test fails, the program exits without saving the data.

        Parameters
        ----------
            databasePaths: str
                path to databases.yaml file
    '''
    ID = input("Enter ID: ")  # User given Database ID
    Type = input("Enter Type: ")  # Database type e.g postgres, mysql, mariadb ...
    Host = input("Enter Host: ")  # Host/ IP-Adress
    Port = input("Enter Port: ")  # Port
    Database = input("Enter Database: ")  # Name of Database
    User = input("Enter User: ")  # Username
    Password = input("Enter Password: ")  # User password

    new_yaml_dict = {
        'ID': ID,
        'Type': Type,
        'Host': Host,
        'Port': Port,
        'Database': Database,
        'User': User,
        'Password': Password
    }

    try:
        project_home = Path(__file__).parent.parent
        create_connection_url(new_yaml_dict, project_home)
    except:
        exit("creating new entry failed, can't reach database")

    with open(databasePaths, 'r') as yamlfile:
        cur_yaml = yaml.safe_load(yamlfile)

    if cur_yaml:
        for yaml_obj in list(cur_yaml):
            if yaml_obj['ID'] == ID:
                exit('ID must be unique')
        with open(databasePaths, 'w') as yamlfile:
            tmp_list = list(cur_yaml)
            tmp_list.append(new_yaml_dict)
            for yaml_obj in tmp_list:
                yamlfile.write(yaml.safe_dump([yaml_obj], sort_keys=False))
                yamlfile.write("\n")
    else:
        with open(databasePaths, 'w') as yamlfile:
            tmp_list = []
            tmp_list.append(new_yaml_dict)
            yaml.safe_dump(tmp_list, yamlfile, sort_keys=False)


# -del / -delete remove database by given id in databases.yaml
def remove_database_by_id(databasePaths, id):
    '''
    Description
    -----------
    Check whether the specified database id is included in the established connections and delete it.
    If the ID is not found, a message is displayed that the id was not found.
    If there is no database entry, a message is displayed, that there is no entry in databaseses.yaml file.

    Parameters
    ----------
        databasePaths: str
            path to databases.yaml file
        id: str
            id given by the user to be searched for
    '''
    try:
        with open(databasePaths, 'r') as yamlfile_read:
            databases_dict = yaml.safe_load(yamlfile_read)
            id_deleted = False
            for index in range(len(list(databases_dict))):
                if databases_dict[index]['ID'] == id:
                    del databases_dict[index]
                    if databases_dict:
                        with open(databasePaths, 'w') as yamlfile_write:
                            yaml.safe_dump(databases_dict, yamlfile_write, sort_keys=False)
                    print(f'Database with ID: {id} removed')
                    id_deleted = True
                    break
            if id_deleted == False:
                print(f'No Database with ID: {id} found')

    except TypeError:
        print("No database entry in databases.yaml file.")


# -l / -list displays all existing databases in databases.yaml
def list_database_by_id(databasePaths):
    '''
    Description
    -----------
    Loads all entries in the databases.yaml file and displays their ID's.
    If there is no database entry, a message is displayed, that there is no entry in databasese.yaml file.

    Parameters
    ----------
        databasePaths: str
            path to databases.yaml file
    '''
    try:
        with open(databasePaths, 'r') as yamlfile_read:
            databases_dict = yaml.safe_load(yamlfile_read)

            for index in range(len(list(databases_dict))):
                print(databases_dict[index]['ID'])
    except TypeError:
        print("No database entry in databases.yaml file.")


# If there is a new .jar file, it has to be added here into the jay connect
def create_connection_url(database, project_home):
    '''
        Description
        -----------
        This function returns the correct connection URL based of the database type.
        Supported database types are: PostgreSQL, MySQL and Mariadb

        Parameters
        ----------
            database: dict
                database with all its values stored in it, for which the connection URL is to be created
            project_home: str
                path to the project root folder
    '''
    drivers_path = os.path.join(project_home, "jdbc_driver")
    stream = open(os.path.join(project_home, 'Database_basics', '../Database_basics/driver.yaml'), 'r')
    driver_dict = yaml.load(stream, Loader=Loader)

    if database['Type'].lower() == 'postgresql':
        return jay.connect("org.postgresql.Driver",
                           f'jdbc:postgresql://{database["Host"]}:{database["Port"]}/{database["Database"]}',
                           {'user': database["User"], 'password': database["Password"], },
                           [os.path.join(drivers_path, driver_dict['MySQL']),
                            os.path.join(drivers_path, driver_dict['PostgreSQL']),
                            os.path.join(drivers_path, driver_dict['MariaDB'])])

    elif database['Type'].lower() == 'mysql':
        return jay.connect("com.mysql.cj.jdbc.Driver",
                           f'jdbc:mysql://{database["Host"]}:{database["Port"]}/{database["Database"]}',
                           {'user': database["User"], 'password': database["Password"], },
                           [os.path.join(drivers_path, driver_dict['MySQL']),
                            os.path.join(drivers_path, driver_dict['PostgreSQL']),
                            os.path.join(drivers_path, driver_dict['MariaDB'])])

    elif database['Type'].lower() == 'mariadb':
        return jay.connect("com.mysql.cj.jdbc.Driver",
                           f'jdbc:mariadb://{database["Host"]}:{database["Port"]}/{database["Database"]}',
                           {'user': database["User"], 'password': database["Password"], },
                           [os.path.join(drivers_path, driver_dict['MySQL']),
                            os.path.join(drivers_path, driver_dict['PostgreSQL']),
                            os.path.join(drivers_path, driver_dict['MariaDB'])])
    else:
        exit("No DB type found")