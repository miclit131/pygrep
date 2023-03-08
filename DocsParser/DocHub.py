
def DocHub(args):

    if args.__dict__["list"]:

        files = ["pygrep", "enviro", "sqlDataProcessing", "databaseManager", "connector", "argparse_config", "argparse_preprocessing", "pilot" ]

        for file in files:
            print(file)
    elif args.__dict__["search"]:
        choose_file(args.__dict__["search"])
    else:
        exit("No params set")

def choose_file(file):

    if file == "pygrep":
        help('pygrep')
    elif file == "enviro":
        help('enviro')
    elif file == "sqlDataProcessing":
        help('SQLresources.sqlDataProcessing')
    elif file == "databaseManager":
        help('Database_classes.DatabaseManager')
    elif file == "connector":
        help('Database_classes.connector')
    elif file == "argparse_config":
        help('arg_parse_module.argparse_config')
    elif file == "argparse_preprocessing":
        help('arg_parse_module.argparse_preprocessing')
    elif file == "pilot":
        help('Control_Plane.pilot')

    else:
        exit(f"{file} not found")
