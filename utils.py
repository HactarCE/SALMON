from os import path
from glob import iglob
import signal


def import_all(init_filename):
    return [path.basename(f)[:-3]
            for f in iglob(path.dirname(init_filename) + r'/*.py')
            if path.isfile(f) and not f.endswith('__init__.py')]


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
