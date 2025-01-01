###################### UNPROOFED ######################

import os
AIOHTTP_VAL=0
if AIOHTTP_VAL == 0:
  os.environ["AIOHTTP_NO_EXTENSIONS"] = ""
else:
  os.environ["AIOHTTP_NO_EXTENSIONS"] = "1"

import sys
import atheris

# aiohttp imports
import asyncio
with atheris.instrument_imports():
    import aiohttp
    from aiohttp.base_protocol import BaseProtocol
    from aiohttp import http_exceptions, streams

@atheris.instrument_func
def TestOneInput(data):
    loop = asyncio.get_event_loop()
    pr = BaseProtocol(loop)
    h_p = aiohttp.http_parser.HttpRequestParser(pr, loop, 32768)
    try:
        h_p.feed_data(data)
        h_p.feed_eof()
    except aiohttp.http_exceptions.HttpProcessingError:
        None

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    atheris.Fuzz()

if __name__ == "__main__":
    main()