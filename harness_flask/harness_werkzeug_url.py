### Die URL Methoden sind vom Jahr 2013 und wurden großflächlich durch urllib ersetzt ###
import sys
import atheris
import werkzeug.urls

with atheris.instrument_imports():
    import werkzeug


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    original = fdp.ConsumeUnicode(100)
    try:
        werkzeug.urls.url_fix(original)
    except UnicodeEncodeError as e2:
        return
    except ValueError as e:
        if not "IPv6" in str(e):
            raise e

    try:
        werkzeug.urls.url_join(
            fdp.ConsumeUnicode(30),
            fdp.ConsumeUnicode(30)
        )
    except UnicodeEncodeError as e2:
        return
    except ValueError as e:
        if not "IPv6" in str(e):
            raise e

    try:
        werkzeug.urls.url_parse(fdp.ConsumeUnicode(30))
    except UnicodeEncodeError as e2:
        return
    except ValueError as e:
        if not "IPv6" in str(e):
            raise e

    try:
        werkzeug.urls.iri_to_uri(fdp.ConsumeUnicode(30))
    except UnicodeEncodeError as e2:
        return
    except ValueError as e:
        if not "IPv6" in str(e):
            raise e

    try:
        werkzeug.urls.url_decode(fdp.ConsumeUnicode(30))
    except UnicodeEncodeError as e2:
        return
    except ValueError as e:
        if not "IPv6" in str(e):
            raise e
    return


def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()