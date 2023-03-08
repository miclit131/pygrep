""" pilot is the main logic of pygrep connecting argparse, database and SQL requests.

    the whole package is built up on inputs initialized in search_manage()
                                        inputs = argparse_preprocessing.nonefilterconverttodict(args)
    which itself is a none filtered and to list converted args created with argparse

    def search_manage()                 selects action based on used subparser
    def supervise_output()              prepare and search parameters
                                        call print function with results of
                                        sqlDataProcessing.print_pretty_results()
    def generate_simple_search_parameters()
                                        fetches results with a single sql
                                        request string generated with sqlerry.sql() -> returns right_sql : String
    def generate_advance_search_parameters()
                                        builds sql request which searches all columns in -t -> inputs["table"]
                                        for any match with signal / inputs["search"][0] in it

"""
from SQLresources import sqlDataProcessing, sqlerry
from Database_classes import DatabaseManager, connector
from termcolor import colored
from arg_parse_module import argparse_preprocessing
import DocsParser.DocHub as DocHub


def search_manage(databasePaths, conny, args):
    """ choose between subparser and starts the correct routine.

    :param databasePaths:       path to databases.yaml to build all connections needed in pilot
    :param conny:               Database_classes.connector.Connector class:
                                                                            builds up connections
                                                                            holds connection details
                                                                            closes connections
    :param args:                argparse arguments to be converted to inputs
    :return: None
    """
    if args.group == 1:
        ids = argparse_preprocessing.choose_ids_or_default(args, conny)
        inputs = argparse_preprocessing.nonefilterconverttodict(args)
        databases_list = connector.Connector.select_database_by_id(conny, ids)

        print(inputs)
        rowcount = int(inputs["shortened_rows"])
        columncount = int(inputs["shortened_column"])
        print(inputs["unlimited_column"])
        if inputs["unlimited_column"]:
            supervise_output(databases_list, inputs, -1, rowcount)
        else:
            supervise_output(databases_list, inputs, columncount, rowcount)
    if args.group == 2:
        if args.__dict__['list'] == True:
            DatabaseManager.list_database_by_id(databasePaths)
        elif args.__dict__['delete'] != None:
            DatabaseManager.remove_database_by_id(databasePaths, args.__dict__['delete'])
        elif args.__dict__['new_entry'] == True:
            DatabaseManager.add_new_database(databasePaths)
    if args.group == 3:
        DocHub.DocHub(args)


def supervise_output(connections, inputs, right_bound, bottom_bound):
    """ supervise_output prepare, call print function.

        prepare and search parameters
        call print function with results of
        sqlDataProcessing.print_pretty_results()

    :param connections:     [jaydebeapi_connections]
    :param inputs:          filtered args
    :param right_bound:     number of
    :param bottom_bound:
    :return:
    """
    signal = inputs["search"][0]
    for i, connection in enumerate(range(len(list(connections)))):
        print(colored("this results of ID: " + connections[connection]["ID"], 'red', attrs=['reverse', 'blink']))
        cursor = connections[connection]["Conn"].cursor()
        connection_type = connections[connection]['Type']
        # choose between if:
        #                   generate_advanced_search_parameters()
        #                       ->search all columns with only -t given and only print columns with found si
        #                else:
        #                    generate_simple_search_parameters()
        #                       ->simple execute with one sql command
        #                both cases got the same return structure
        if 'table' in inputs \
                and 'column' not in inputs \
                and 'top' not in inputs \
                and 'range' not in inputs \
                and not inputs['exact'] \
                and not inputs['end'] \
                and not inputs['begin']:
            print(connections[i]['Database'])
            records, column_names = generate_advanced_search_parameters(inputs, cursor, connection_type, connections[i]['Database'])
        else:
            records, column_names = generate_simple_search_parameters(inputs, cursor, connection_type)

        # if right_bound was not set -> default value 5
        # if inputs["unlimited_column"] -> right_bound = -1
        #                               -> partition_pretty_table_array will print all columns at once
        # else:
        #   if right_bound was not set      -> default value 5          print(table[:bottom_bound])
        #   if bottom_bound = -1 = not set  -> default no limitations   print(table)
        #   the -1 in bottom_bound is given in search_manage if inputs["unlimited_column"]:
        #                                                        supervise_output(databases_list, inputs, -1, rowcount)
        # unintended bug no validation on some input flags
        # :TODO input validation on right_bound to be positive and not 0

        if right_bound == -1:
            columnSections, recordSections = sqlDataProcessing.partition_pretty_table_array(column_names, records,
                                                                                            len(column_names))
            sqlDataProcessing.print_pretty_results(columnSections, recordSections, signal, bottom_bound)
        else:
            columnSections, recordSections = sqlDataProcessing.partition_pretty_table_array(column_names, records,
                                                                                            right_bound)
            sqlDataProcessing.print_pretty_results(columnSections, recordSections, signal, bottom_bound)


def generate_simple_search_parameters(inputs, cursor, connection_type):
    """ execute single SQL statement selected with sqlerry.sql().

    :param inputs:      none filtered iterable args
    :param cursor:      jaydebeapi cursor
    :return:            parameters for partitioning and printing
    """
    if connection_type == "MariaDB":
        sql_stmt = sqlerry.base_search_maria(inputs)
    elif connection_type == "MySQL":
        sql_stmt = sqlerry.mySQL(inputs)
    else:
        sql_stmt = sqlerry.sql(inputs)

    records, description = run_sql(cursor, sql_stmt)

    selected_cols = []
    column_names = [column[0] for column in description]
    # TODO: Inputvalidierung SELECT selected_cols

    if 'keep_selected' in inputs:
        keep_only_selected = True
        selected_cols.append(inputs["column"])
        for keep in inputs["keep_selected"]:
            selected_cols.append(keep)
    else:
        keep_only_selected = False
    selected_cols_full = selected_cols
    # selected_cols_full = ["index", "HT Benennung", "UT Benennung", inputs["column"]]
    # inputs["keep_selected"] -> for example ["HT Benennung", "UT Benennung"]
    # if "index" or inputs["column"] is in inputs["keep_selected"] program crashes
    # because of duplicate column names in pretty table -> unique columns condition internal
    # TODO input validation for -k and -c to be unique and -k"

    if not keep_only_selected:
        new_cols = [column[0] for column in description]
    else:
        new_cols = selected_cols_full

    new_col_idx = [column_names.index(c) for c in new_cols]
    reshuffled_cols = [column_names[i] for i in new_col_idx]
    reshuffled_rows = [tuple([r[i] for i in new_col_idx]) for r in records]
    column_names = reshuffled_cols
    records = reshuffled_rows
    return records, column_names


def run_sql(cursor, sql_stmt):
    print("Running SQL command: " + sql_stmt)
    cursor.execute(sql_stmt)
    records = cursor.fetchall()
    desc = cursor.description
    return records, desc


def generate_advanced_search_parameters(inputs, cursor, connection_type, schema):
    """ build SQL and search all columns.

    :param inputs:      none filtered iterable args
    :param cursor:      jaydebeapi cursor
    :return:            parameters for partitioning and printing
    """
    # Get all columns from table
    tblName = inputs["table"]
    search = inputs['search'][0]

    # Construct query to search each column (collected above) for regex match
    # SELECT * FROM datamining WHERE ("Antrieb" LIKE '%en%' OR "KSTA Motor" LIKE '%en%' OR "HST-HT Benennung" ...)
    # 1. Construct regex match
    if connection_type == "MariaDB":
        get_col_names_sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{tblName}'"
        records, description = run_sql(cursor, get_col_names_sql)
        column_names = [record[0] for record in records]
        column_filter = " OR ".join([f"{c} REGEXP '{search}'" for c in column_names])
    else:
        # postgres SQL
        get_col_names_sql = f"SELECT * FROM information_schema.columns WHERE table_name = '{tblName}'"
        records, description = run_sql(cursor, get_col_names_sql)
        column_names = [(r[3], r[7], i) for i, r in enumerate(records)]
        column_filter = " OR ".join([f"\"{c[0]}\" LIKE '%{search}%'" for c in column_names if c[1] == 'text'])

    # 2. plugin regex match to SQL query
    sql_search_all_cols = f"SELECT * FROM {tblName} WHERE ({column_filter})"

    # 3. Run and collect results
    records, description = run_sql(cursor, sql_search_all_cols)
    column_names = [c[0] for c in description] if connection_type == "MariaDB" else description

    # Collect columns where there is at least one record containing a matching cell
    selected_cols = []
    for col_idx, col_name in enumerate(column_names):
        #if col_idx in text_col_ids:
        for r in records:
            if search in str(r[col_idx]):
                selected_cols.append(col_name)
                break

    selected_cols = [c if connection_type == "MariaDB" else c[0] for c in selected_cols]
    column_names = [c if connection_type == "MariaDB" else c[0] for c in column_names]
    selected_cols_idx = [column_names.index(c) for c in selected_cols]
    records = [tuple([r[i] for i in selected_cols_idx]) for r in records]

    return records, selected_cols
