"""sqlDataProcessing is used manipulate result prettyTable.

    the main function of this package is to is used to partition, color and print results:

    def partition_pretty_table_array        partition tables to control the numbers of
                                            columns being printed in each row of outputs

    def print_pretty_results                takes in partitioned prettyTable, and prints
                                            result partitions with keyword / signal colored

"""

from SQLresources import sqlerry
from termcolor import colored
from prettytable import PrettyTable
import os

# Color highlighting tested on Ubuntu 20, Fedora 37 and Windows 10
if os.name != "posix":
    print(f"Running command on '{os.name}', which is a non-posix shell, trying to run 'color' to enable colors in the terminal.")
    # activate color in terminal for termcolor to work
    os.system('color')


def partition_pretty_table_array(column_names, records,
                                 partition_size):
    """partitions columns and records for formatted output.
    
    :param column_names:                        part of the return of generated search parameters in pilot.py
                                                generate_simple_search_parameters
                                                generate_advanced_search_parameters
    :param records:
                                                generated in:
                                                pilot.py
                                                def generate_simple_search_parameters():
                                                def generate_advanced_search_parameters():
                                                cursor.execute(sqlStatement->type:string)
                                                records = cursor.fetchall()
    :param partition_size:                      amount of columns printed in a terminal row
    :return: columnSection, recordSections      needed for print_pretty_results()
    """

    columnSection = []
    recordSections = [] * len(column_names)

    # columnSection is built up in sections of partition_size ["column_name_1", "column_name_2", "column_name_3"]
    #           [column1.size=partition_size,column1.size=partition_size,column1.size=total_amount_column % partition_size]
    # recordSections is built up in sections of partition_size
    # each section of recordSection is multidimensional array because of the row count
    #               [record_section_1, record_section_2, record_section_3,]
    # record_section_1= [[Entry_0,...,Entry_last_table_row],...,[Entry_0,...,Entry_last_table_row]]
    # partition_size = amount of arrays in each record_section_1
    # last record_section got total_amount_column % partition_size
    for i in range(0, len(column_names), partition_size):
        columnSection.append(column_names[i:i + partition_size])
        recordSections.append([r[i:i + partition_size] for r in records])

    return columnSection, recordSections


def print_pretty_results(column_partitioned, record_partitioned, signal, bottom_bound):
    """

    :param column_partitioned:
    :param record_partitioned:
    :param signal:
    :param bottom_bound:
    """
    for idx, (column_partition, record_partition) in enumerate(zip(column_partitioned, record_partitioned)):
        table = PrettyTable(column_partition)
        for r in record_partition:
            table.add_row(
                [str(elem).replace(signal, colored(signal, "green", attrs=['reverse', 'blink'])) for elem in r])
        # needed a numeric value which can also represent a false boolean
        # unintended bug no validation on some input flags
        # :TODO input validation on bottom_bound to be positive and not -1
        if bottom_bound == -1:
            print(table)
        else:
            print(table[:bottom_bound])


def get_table_names(connection_dictionary):
    """ get table names for a new argparse flag.

    Not in use.
    Could be used to have -t optional and search
    all tables of a database and even all columns
    if -c is not set, but we didnt implement this
    flag. The idea was to return list of table names
    and then iterate through all table like we do
    with -t set

    :param connection_dictionary:
    :return: Array of table names
    """

    connection = connection_dictionary['Conn']
    cursor = connection.cursor()
    print("execute command on database from get_table_names:" + sqlerry.table_names)
    cursor.execute(sqlerry.table_names)
    tables = cursor.fetchall()
    fetchToArray = []
    for table in tables:
        fetchToArray.append(table)

    return fetchToArray
