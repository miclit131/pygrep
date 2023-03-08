
# Pygrep 

implements the grep function for databases

Pygrep takes in flags which will be interpreted to select
the correct SQL query and prints out the results.
The results are formatted as prettyTables and can be
adjusted with flags, the default output has 5 columns
in a row but can be set to all columns with -u.
If -i is not set it will look in all databases
in the database.yaml, if column exist not implemented yet.
Throws error if -c contains nonexisting colum.

# OS Integration

Pygrep is supported for Linux and Windows terminal if the
python environment is set up, in testing we used a
windows miniconda terminal and Linux terminal.
No #! because of cross OS support.

# Important external packages 

in Python 3.9.12 and JDK version 17 or higher:

* jaydebeapi                1.2.3
* termcolor                 1.1.0
* prettytable               3.4.0
* pyyaml                    6.0
* argparse                  1.4.0
* mysqlclient               2.1.1
* sqlalchemy                1.4.36 (only for the DatabaseSeed but not implemented in main code)
* pandas                    1.4.2  (only for the DatabaseSeed but not implemented in main code)

Example csv and database drivers are in Database_basics, csv can be loaded into a database
with DatabaseSeed.auto_seed_csv(csv, table_name, connection_url), not implemented in the
final code, was used at the start for testing purposes.

jdbc drivers are preinstalled in the jdbc_driver folder and need to be put there if a certain
driver.jar is needed. We re currently supporting PostgreSQL, mariaDB, mysql driver

We got multiple subparsers their man pages can be called with:

python pygrep.py search/manage/docs -h

# Typical usage example:

## subparser search:

* python pygrep.py search en -t datamining
* python pygrep.py search en -t datamining -u -sr 15
* python pygrep.py search en -i Local_Postgres -t datamining -u -sr 15
* python pygrep.py search E6 -t datamining -c Schadstoffklasse -sc 10

most of the flags in argparse_config.py group = parser_g1.add_mutually_exclusive_group()
which are mainly for filter flags are not tested
SQL queries are applicable in pgAdmin / postgress but there seem to be a bug
also most test have been done on postgres database only connections with supported
drivers have been tested

## subparser manage:

* python pygrep.py manage -l
* python pygrep.py manage -n
* python pygrep.py manage -del Example_ID

## subparser docs:

* python pygrep.py docs -l
* python pygrep.py docs pygrep
