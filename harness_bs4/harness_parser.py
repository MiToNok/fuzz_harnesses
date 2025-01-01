import sys
import atheris
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "<PATH TO BS4 SOURCE>")
    ),
)

with atheris.instrument_imports():
    import logging
    import warnings
    import soupsieve
    from bs4 import BeautifulSoup
    from soupsieve.util import SelectorSyntaxError


try:
    import HTMLParser
    HTMLParseError = HTMLParser.HTMLParseError
except ImportError:
  # HTMLParseError is removed in Python 3.5. Since it can never be
  # thrown in 3.5, we can just define our own class as a placeholder.

    class HTMLParseError(Exception):
        pass


@atheris.instrument_func
def TestOneInput(data):
    """TestOneInput gets random data from the fuzzer, and throws it at bs4."""
    if len(data) < 12:
        return

    parsers = ['lxml-xml', 'html5lib', 'html.parser', 'lxml']
    try:
        idx = int(data[0]) % len(parsers)
    except ValueError:
        return

    css_selector, data = data[1:10], data[10:]

    try:
        soup = BeautifulSoup(data[1:], features=parsers[idx])
    except HTMLParseError:
        return
    except ValueError:
        return

    list(soup.find_all(True))
    if soup.css:
        try:
            soup.css.select(css_selector.decode('utf-8', 'replace'))
        except SelectorSyntaxError:
            return
        except NotImplementedError:
            return
    soup.prettify()    


def main():
    """Main Function to execute Atheris"""
    logging.disable(logging.CRITICAL)
    warnings.filterwarnings('ignore')
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
