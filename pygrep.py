"""Pygrep implements the grep function for databases.

Pygrep takes in flags which will be interpreted to select
the correct SQL query and prints out the results.
The results are formatted as prettyTables and can be
adjusted with flags, the default output has 5 columns
in a row but can be set to all columns with -u.
If -i is not set it will look in all databases
in the database.yaml, if column exist not implemented yet.
Throws error if -c contains nonexisting colum.
Pygrep is supported for Linux and Windows terminal if the
python environment is set up, in testing we used a
windows miniconda terminal and Linux terminal.
Important external packages in Python 3.9.12:

jaydebeapi                1.2.3
termcolor                 1.1.0
prettytable               3.4.0
pyyaml                    6.0
argparse                  1.4.0
mysqlclient               2.1.1
sqlalchemy                1.4.36 (only for the DatabaseSeed but not implemented in main code)
pandas                    1.4.2  (only for the DatabaseSeed but not implemented in main code)

Please add the jdk path in enviro.py, the reason in described in the documentation of enviro.py     !!!
could cause unecessary debugging issues in the jpype package, programm doesnt regocnize if jdk      !!!
is missing or has a wrong path and prevents connections from happening.                             !!!

Example csv and database drivers are in Database_basics, csv can be loaded into a database
with DatabaseSeed.auto_seed_csv(csv, table_name, connection_url), not implemented in the
final code, was used at the start for testing purposes.

jdbc drivers are preinstalled in the jdbc_driver folder and need to be put there if a certain
driver.jar is needed. We re currently supporting PostgreSQL, mariaDB, mysql driver

We got multiple subparsers their man pages can be called with:

python pygrep.py search/manage/docs -h

  Typical usage example:

  subparser search:
      python pygrep.py search en -t datamining
      python pygrep.py search en -t datamining -u -sr 15
      python pygrep.py search en -i Local_Postgres -t datamining -u -sr 15
      python pygrep.py search E6 -t datamining -c Schadstoffklasse -sc 10

      most of the flags in argparse_config.py group = parser_g1.add_mutually_exclusive_group()
      which are mainly for filter flags are not tested
      SQL queries are applicable in pgAdmin / postgress but there seem to be a bug
      also most test have been done on postgres database only connections with supported
      drivers have been tested

  subparser manage:
      python pygrep.py manage -l
      python pygrep.py manage -n
      python pygrep.py manage -del Example_ID

  subparser docs:
    python pygrep.py docs -l
    python pygrep.py docs pygrep
"""
import os
import enviro
from Control_Plane import pilot
from Database_classes import connector
from arg_parse_module import argparse_config

if __name__ == '__main__':
    # enviro.jdk is used to set the jdk path
    # put into external folder and .gitignore
    # missing jdk leads to wrong behaviour in code
    # because of jpype in Jaydebeapi
    # Connecting to Database with ID: Local_Postgres failed
    java_home = enviro.jdk
    os.environ["JAVA_HOME"] = java_home
    # os independent absolute paths
    project_home = os.path.dirname(os.path.abspath(__file__))
    databasePaths = os.path.join(project_home, "Database_basics", "databases.yaml")
    # csv variable would be needed to call the DatabaseSeed.auto_seed_csv(csv, table_name, connection_url)
    # csv = os.path.join("Database_basics", "Fahrzeuginformationen.csv")
    # conny is the connector class which holds all connections and information about it
    conny = connector.Connector(os.path.join("Database_basics", "databases.yaml"), project_home)
    try:
        # connects to all databases given in Database_basics.database.yaml
        conny.connect_all()
        args = argparse_config.parse()
        # Control_Plane.pilot calls the main routines depending on subparser being used
        pilot.search_manage(databasePaths, conny, args)
    finally:
        conny.disconnect_all()
