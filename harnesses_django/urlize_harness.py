import sys
import os
import inspect
import atheris  # type: ignore

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "<PATH TO DJANGO SRC>")
    ),
)

# Import the vulnerable Django functions
from django.utils.html import urlize


@atheris.instrument_func
def TestOneInput(data):
    """Fuzz Target"""
    fdp = atheris.FuzzedDataProvider(data)

    try:
        # Get a fuzzed string that might contain URLs or email addresses
        fdp_string = fdp.ComsumeString(sys.maxsize)

        # Feed fdp string to target function
        result = urlize(fdp_string, trim_url_limit=None)
        print(result)

    except Exception as e:
        # Catch any other unexpected exceptions
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
