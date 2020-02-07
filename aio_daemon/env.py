import os


def getenv_path(name, default=None):
    value = os.getenv(name, default)
    if value and value.startswith('./'):
        return os.path.join(os.getcwd(), value[2:])
    return value
