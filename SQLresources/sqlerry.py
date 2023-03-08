from arg_parse_module import argparse_config
tblName = ''
colName = ''
search = ''
meta = str("select * from INFORMATION_SCHEMA.TABLES")
get_all = "selecte * from *"

# test = "SELECT * FROM datamining"
table_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES " \
              "WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='dbName'"

# alles aus einer Tabelle ausgeben (-tb tabellenname) c
sql_tbl = f"SELECT * FROM {tblName}"

# Wort in einer Spalte suchen (-tb tabellenname -s spaltenname -w suchwert) c

sql_col = f"SELECT * FROM {tblName} WHERE {colName} = {search}"

# suche in spalte ob wort enthalten (-tb tabellenname -s spaltenname -l zeichenkette) c
sql_like = f"SELECT * FROM {tblName} WHERE {colName} LIKE %{search}%"

# suche ob eintrag mit gesuchtem wort endet (-tb tabellenname -s spaltenname -e wort/buchstabe) c
sql_end = f"SELECT * FROM {tblName} WHERE {colName} LIKE %{search}"

# suche ob eintrag mit gesuchtem wort anfängt ( -tb tabellenname -s spaltenname -b wort/buchstabe) c
sql_beg = f"SELECT * FROM {tblName} WHERE {colName} LIKE {search}%"

# einträge range zb alle datums,werte zwischen den beiden Werten
val1 = ''
val2 = ''
sql_range = f"SELECT * FROM {tblName} WHERE {colName} BETWEEN {val1} AND {val2}"

#ersten n Einttäge
val = ''
sql_head = f"SELECT TOP {val} FROM {tblName} WHERE {colName} = {search}"

# zeile range zb zeile 100-200
sql_range2 = f"SELECT * FROM {tblName} LIMIT {val1}, {val2}"

args = argparse_config.parse()


# input = {'table':"tablename",'column':"columnname, range:{'start':int, 'end':int}}

#postgres
def sql(input):
    right_sql = ''
    tblName = input['table']

    if 'table' in input \
            and 'column' in input \
            and input['begin']:
        colName = input['column']
        search = input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '^{search}'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '^{str(search)}'"

    elif 'table' in input \
            and 'column' in input \
            and input['end']:
        colName = input['column']
        search = input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '{search}$'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '{str(search)}$'"

    elif 'table' in input \
            and 'column' in input \
            and input['exact']:
        colName = input['column']
        search = input['search'][0]
        if search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" = {search}"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" = '{search}'"

    elif 'table' in input \
            and 'range' in input:
        colName = input['search']
        startval = input['range'][0]
        endval = input['range'][1]
        right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" BETWEEN {startval} AND {endval}"
    elif 'table' in input \
            and 'column' in input:
        colName = input['column']
        search = input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '^.*{search}.*$'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE \"{colName}\" ~ '^.*{str(search)}.*$'"
    else:
        #raise Exception('Invalid Combination or Input')
        print('Invalid combination of arguments, enter -h for help')
        exit()

    return right_sql

#mariadb
def base_search_maria(user_input):
    right_sql = ''
    tblName = user_input['table']
    if 'table' in user_input \
            and 'column' in user_input \
            and user_input['begin']:
        colName = user_input['column']
        search = user_input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '^{search}'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '^{str(search)}'"

    elif 'table' in user_input \
            and 'column' in user_input \
            and user_input['end']:
        colName = user_input['column']
        search = user_input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '{search}$'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '{str(search)}$'"

    elif 'table' in user_input \
            and 'column' in user_input \
            and user_input['exact']:
        colName = user_input['column']
        search = user_input['search'][0]
        if search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} = {search}"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} = '{search}'"

    elif 'table' in user_input \
            and 'range' in user_input:
        colName = user_input['search']
        startval = user_input['range'][0]
        endval = user_input['range'][1]
        right_sql = f"SELECT * FROM {tblName} WHERE {colName} BETWEEN {startval} AND {endval}"

    elif 'table' in user_input \
            and 'column' in user_input:
        colName = user_input['column']
        search = user_input['search'][0]
        right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '{str(search)}'"

    else:
        print('Invalid combination of arguments, enter -h for help')
        exit()

    return right_sql

#mySQL
def mySQL(input):
    right_sql = ''
    tblName = input['table']

    if 'table' in input \
            and 'column' in input \
            and input['begin']:
        colName = input['column']
        search = input['search'][0]
        if not search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} LIKE '{search}%'"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} LIKE '{str(search)}%'"

    elif 'table' in input \
            and 'column' in input \
            and input['end']:
        colName = input['column']
        search = input['search'][0]
        right_sql = f"SELECT * FROM {tblName} WHERE {colName} LIKE '%{str(search)}'"

    elif 'table' in input \
            and 'column' in input \
            and input['exact']:
        colName = input['column']
        search = input['search'][0]
        if search.isdigit():
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} = {search}"
        else:
            right_sql = f"SELECT * FROM {tblName} WHERE {colName} = '{search}'"


    elif 'table' in input \
            and 'range' in input:
        colName = input['search']
        startval = input['range'][0]
        endval = input['range'][1]
        right_sql = f"SELECT * FROM {tblName} WHERE {colName} BETWEEN {startval} AND {endval}"

    elif 'table' in input \
            and 'column' in input:
        colName = input['column']
        search = input['search'][0]
        right_sql = f"SELECT * FROM {tblName} WHERE {colName} LIKE '%{str(search)}%'"

    else:
        print('Invalid combination of arguments, enter -h for help')
        exit()

    return right_sql



#    if search.isdigit():
#        right_sql = f"SELECT * FROM {tblName} WHERE {colName} = {search}"
#    else:
#   right_sql = f"SELECT * FROM {tblName} WHERE {colName} REGEXP '{str(search)}'"
