"""
In Django 3.2 before 3.2.21, 4.1 before 4.1.11, and 4.2 before 4.2.5,
django.utils.encoding.uri_to_iri() is subject to a potential DoS
(denial of service) attack via certain inputs with a very large number of Unicode characters.
"""

import sys
import os
import signal
from contextlib import contextmanager
from urllib.parse import quote
import atheris  # type: ignore

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "<PATH TO DJANGO SRC>")
    ),
)

# Import the vulnerable Django functions
from django.utils.encoding import uri_to_iri


class TimeoutException(Exception):
    """
    Timeout Exception
    """
    pass

@contextmanager
def timeout(seconds):
    """
    Timeout handler using signal
    """
    def timeout_handler(signum, frame):
        raise TimeoutException("Function call timed out")

    # Set the timeout handler
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Restore the original handler
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)



@atheris.instrument_func
def TestOneInput(data):
    """Fuzz Target"""
    fdp = atheris.FuzzedDataProvider(data)

    try:
        # Perform a percent enconding on input data
        test_input = quote(fdp, safe='')

        try:
            # Set 3 seconds for timeout
            with timeout(6):
                uri_to_iri(test_input)

        except TimeoutException:
            # Function took too long - potential DoS vulnerability
            sys.stderr.write(f"Timeout detected with input length: {len(test_input)}\n")
            sys.stderr.write(f"First 100 chars of problematic input: {test_input[:100]}\n")
            
    except Exception as e:
        pass


def main():
    """Main to execute atheris"""
    # Initialize atheris
    atheris.Setup(sys.argv, TestOneInput)

    # Add coverage hooks
    atheris.instrument_all()

    # Start fuzzing
    atheris.Fuzz()


if __name__ == "__main__":
    main()
