import atheris
import sys
import random
with atheris.instrument_imports():
     from decorator import *

def base_func(*args, **kw):
    pass

def TestInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    try:
        FunctionMaker.create(
            "f%s(%s)"%(fdp.ConsumeString(20),fdp.ConsumeString(20)),
            "base_func()",
            dict(f=base_func),
            addsource=fdp.ConsumeBool()
        )
    except Exception as e:
        if "Error in generated code" not in str(e):
             raise e

def main():
    atheris.Setup(sys.argv, TestInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()