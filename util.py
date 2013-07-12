import os

_root = None


def set_root(file):
    '''
Pass in __file__ from a script to set that script's directory as the root for
determining absolute paths to resources
'''
    global _root
    _root = os.path.dirname(os.path.realpath(file))


def get_root():
    return _root


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
        return sanitize(data)


def load_file_config(config, filename):
    '''key = value in filename becomes config[key] = value'''
    config_lines = load_file(filename).split(u'\n')
    for line in config_lines:
        line = _until(line, u'#')
        if not line or u'=' not in line:
            continue
        key, value = line.split(u'=', 1)
        key, value = key.strip(), value.strip()
        config[key] = value


def load_env_config(config, keys, overwrite_null=False):
    '''
    Load environment variables into config, where keys is an iterable of env keys to look up.
    overwrite_null=True means keys not found in env vars are set in config as None.  Otherwise, those values aren't set.
    '''
    for key in keys:
        value = os.getenv(key, None)
        if (value is not None) or overwrite_null:
            config[key] = value


def _until(string, suffix):
    '''Returns the string until the first occurance of suffix'''
    if not suffix:
        return string
    return string.split(suffix)[0]


def sanitize(string):
    '''Returns the string as unicode, with \n line endings'''
    if string is None:
        return u''
    try:
        string = unicode(string, encoding='utf-8')
    except UnicodeEncodeError:
        # Already unicode
        pass
    except TypeError:
        # Already unicode
        pass
    string = string.replace(u'\r\n', u'\n')
    return string


def touch(fname, times=None, overwrite=False):
    mode = 'w' if overwrite else 'a'
    with file(fname, mode):
        os.utime(fname, times)


def format_scaled_value(value, scale, precision=1):
    '''
    Returns an int or string.

    Returns an int when value is evenly divisible by scale,
    otherwise returns a string with the given number of decimal places.
    '''
    if value % scale == 0:
        return int(value / scale)
    return "{0:0.{p}f}".format(value / scale, p=precision)
