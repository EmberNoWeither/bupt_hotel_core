




def list_attr_Add(property : dict, attr : str, element : any, *args, **kwds):
    property[attr].append(element)
    return property[attr]


def dict_attr_change(property : dict, attr : str, key : str, value : any, *args, **kwds):
    property[attr][key] = value
    return property[attr]