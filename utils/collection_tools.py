import itertools


class NoFieldsError(Exception):
    pass

class FormatError(Exception):
    pass

def recursive_hierarchy(elements, fields):
    if not fields:
        return elements

    nodes = []

    # Clone fields and remove first element
    fields = fields[:]
    field = fields.pop(0)
    # Sort elements by current field to allow grouping
    ordered_elements = sorted(elements, key=lambda k: k[field])

    for k, g in itertools.groupby(ordered_elements, lambda el: el[field]):
        node = {
            'title': k,
            'nodes': recursive_hierarchy(list(g), fields)
        }

        nodes.append(node)

    return nodes

def build_hierarchy(elements, fields):
    """Takes a list of dicts and groups them in an hierarchical way
    respecting the order provied by "fields".
    First field is used to group the first layer.
    
    :param elements: list of JSON objects
    :param fields: list of fields to use as grouping keys. Order matters
    :return: a JSON list with the format [
        {title: "something1", nodes:[{title: "something2", nodes:[...]}]}] 
    """
    if not fields:
        raise NoFieldsError('Please provide an iterable of key strings')
    elif not isinstance(fields, list):
        raise FormatError("The 'fields' parameter must be of type <list>")

    return recursive_hierarchy(elements, fields)
