def is_empty(object):
    if not isinstance(object, (list, tuple, dict, set, str)):
        return True
    if object is None:
        return True
    if len(object) == 0:
        return True
    if isinstance(object, str):
        if object.isspace() or object == '':
            return True
    return False
