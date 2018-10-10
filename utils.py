from os import path
from glob import iglob
import signal


def import_all(init_filename):
    return [path.basename(f)[:-3]
            for f in iglob(path.dirname(init_filename) + r'/*.py')
            if path.isfile(f) and not f.endswith('__init__.py')]


def find_all_in_string(query, search_string):
    i = 0
    indices = []
    while i >= 0:
        i = search_string.find(query)
        if i > 0:
            indices.append(i)
        i += 1
    return indices


# from https://stackoverflow.com/a/28676904/4958484
def np_blit(dest, src, loc):
    pos = [i if i >= 0 else None for i in loc]
    neg = [-i if i < 0 else None for i in loc]
    target = dest[tuple(slice(i,None) for i in pos)]
    src = src[tuple(slice(i, j) for i,j in zip(neg, target.shape))]
    target[tuple(slice(None, i) for i in src.shape)] = src
    return dest


# from https://stackoverflow.com/a/22348885/4958484
class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
