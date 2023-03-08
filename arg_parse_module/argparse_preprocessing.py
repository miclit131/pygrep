"""preprocess arguments.

def nonefilterconverttodict()         preprocess arguments to interface we agreed on
def choose_ids_or_default()           -i optional input and -i can be array or single value

"""

def nonefilterconverttodict(args):
    """ preprocess arguments to interface we agreed on.

    :param args:        contains None and is not iterable
    :return:            inputs iterable, None values removed boolean flags with
                        no input still got value False and get not filtered as expected
    """
    inputs = {}
    for arg in args.__dict__:
        if args.__dict__[arg] is None:
            continue
        else:
            inputs[arg] = args.__dict__[arg]
    return inputs


def choose_ids_or_default(inputs, connected_connector_class):
    """

    :param inputs:                          none filtered not iterable args needs to be called
                                            before def nonefilterconverttodict(args) or given args out of argparse
    :param connected_connector_class:       contains all connections
    :return:
    """
    if not inputs.__dict__["id_databases"]:
        return connected_connector_class.databases_list
    else:
        return inputs.__dict__["id_databases"]

