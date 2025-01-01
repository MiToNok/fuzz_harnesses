import sys
import os
import signal
from contextlib import contextmanager
import atheris  # type: ignore

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "<PATH TO DJANGO SRC>")
    ),
)

# Import the vulnerable Django functions
from django.utils.html import urlize


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
        # Generate test string with brackets
        num_brackets = fdp.ConsumeIntInRange(100, 100000)
        str_length = fdp.ConsumeIntInRange(0, 1000000)
        test_input = "[" * num_brackets + "]" * num_brackets + fdp.ConsumeString(str_length)

        try:
            # Set seconds for timeout
            with timeout(6):
                urlize(test_input)

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
