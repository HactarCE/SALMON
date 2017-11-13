from os import path
from glob import iglob


def import_all(init_filename):
    return [path.basename(f)[:-3]
            for f in iglob(path.dirname(init_filename) + r'/*.py')
            if path.isfile(f) and not f.endswith('__init__.py')]
