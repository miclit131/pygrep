"""all argparse flags, groups and subparser

mutually exclusive groups :             only one of each group can be set as input at the same time

                column_group            column manipulation that
                group                   filter flags
                database_yaml_group     database manager flags
subparser:
                search                  main functionality of the program
                manage                  edit configuration of databases.yaml
                docs                    show internal documentation files

"""

import argparse


def parse():
    parser = argparse.ArgumentParser(description='Pygrep Manpage')

    subparsers = parser.add_subparsers(help="subparsers")
    parser_g1 = subparsers.add_parser("search")
    parser_g1.add_argument("search", nargs=1)
    #parser_g1.add_argument('-p', '--paint', help='get all tables or use all table_names, is an [OBJECT]')
    parser_g1.add_argument('-i', '--id-databases', nargs='+', help='the database that is searched in (id)')
    parser_g1.add_argument('-t', '--table', help='name of the table that is searched in')
    parser_g1.add_argument('-c', '--column', help='name of the column that is searched in')

    column_group = parser_g1.add_mutually_exclusive_group()
    column_group.add_argument('-k', '--keep-selected', nargs='+', help='Table_Name of the Database, use this function only during simple search (which is activated with the --column flag), do not use \'index\' (meta column).')
    column_group.add_argument('-sc', '--shortened-column', default=5, help='borders for the output for larger results [COLUMNS], default is 5 columns')
    column_group.add_argument('-u', '--unlimited-column', action='store_true',
                              help=' use -u to remove column border, default is 5 columns')
    parser_g1.add_argument('-sr', '--shortened-rows', default=-1, help='borders for the output for larger results [ROWS], no default if not set it is unlimited')

    group = parser_g1.add_mutually_exclusive_group()
    # group.add_argument('-to', '--top', help='get top n values')
    group.add_argument('-b', '--begin', action='store_true',
                       help='get all rows of a column that contain values, that begin with the searched string')
    group.add_argument('-e', '--end', action='store_true',
                       help='get all rows of a column, that contain exact the input value')
    group.add_argument('-ex', '--exact', action='store_true',
                       help='get all rows of a column, that contain the searched string')
    group.add_argument('-r', '--range', nargs=2, metavar=('start', 'end'),
                       help='get all data between two values, has to be used with search as column')


    #group.add_argument('-d', '--date', help='get all tables or use all table_names, is an [OBJECT]')
    parser_g1.set_defaults(group=1)

    parser_g2 = subparsers.add_parser("manage")
    database_yaml_group = parser_g2.add_mutually_exclusive_group()
    database_yaml_group.add_argument('-l', '--list', action='store_true',
                                     help='list all existing database entries')
    database_yaml_group.add_argument('-n', '--new-entry', action='store_true',
                                     help='add new database connection entry')
    database_yaml_group.add_argument('-del', '--delete', help='remove existing database entry by given name')
    parser_g2.set_defaults(group=2)

    parser_g3 = subparsers.add_parser("docs")
    document_group = parser_g3.add_mutually_exclusive_group()
    document_group.add_argument("search", nargs='?', help='filename to search for')
    document_group.add_argument('-l', '--list', action='store_true',
                                help='list all documented files')

    parser_g3.set_defaults(group=3)


    args = parser.parse_args()

    # special case (see docs)
    if args.__dict__["group"] == 1:
        if not args.column and args.keep_selected:
            print("Don't use -k without -c, terminating pgre. Call pygrep --help to view user docs.")
            exit(1)

        # if args.keep_selected and "index" in args.keep_selected:
        #     print("Index is not allowed to be a column for \"--keep-selected\".")
        #     exit(1)

    return args
