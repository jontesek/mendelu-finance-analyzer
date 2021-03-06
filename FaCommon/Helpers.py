from contextlib import contextmanager
import sys, os


@contextmanager
def suppress_stdout():
    """Temporarily suppress console output.
    http://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python/#
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
