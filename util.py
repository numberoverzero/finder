import os

_root = None


def set_root(file):
    '''
Pass in __file__ from a script to set that script's directory as the root for
determining absolute paths to resources
'''
    global _root
    _root = os.path.dirname(os.path.realpath(file))


def abs_path(filename):
    '''Absolute path from _root '''
    if not _root:
        raise ValueError("Unknown root. Use set_root(__file__) from a script in the root directory first.")
    return os.path.join(_root, filename)


def load_file(filename):
    '''Returns the contents of the given file in the data folder.'''
    path = abs_path(filename)
    with open(path) as f:
        data = f.read()
        return _sanitize(data)


def load_config(config, filename):
    '''key = value in filename becomes config[key] = value'''
    config_lines = load_file(filename).split(u'\n')
    for line in config_lines:
        line = _until(line, u'#')
        if not line or u'=' not in line:
            continue
        key, value = line.split(u'=', 1)
        key, value = key.strip(), value.strip()
        config[key] = value


def _until(string, suffix):
    '''Returns the string until the first occurance of suffix'''
    if not suffix:
        return string
    return string.split(suffix)[0]


def _sanitize(string):
    '''Returns the string as unicode, with \n line endings'''
    try:
        string = unicode(string, encoding='utf-8')
    except UnicodeEncodeError:
        # Already unicode
        pass
    string = string.replace(u'\r\n', u'\n')
    return string
