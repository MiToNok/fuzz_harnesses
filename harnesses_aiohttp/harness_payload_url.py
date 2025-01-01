import sys
import atheris

# aiohttp specific
with atheris.instrument_imports():
    from aiohttp import http_exceptions, payload
    from yarl import URL

@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    original = fdp.ConsumeString(sys.maxsize)

    try:
        p = payload.StringPayload(original)
    except UnicodeEncodeError:
        None
    try:
        u = URL(original)
    except ValueError:
        None

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()