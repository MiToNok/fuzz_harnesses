import atheris
import sys
import random
with atheris.instrument_imports():
     from decorator import *

def TestInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    @decorator
    def dummy_decorator(func, dummy=1, *args, **kw):
        result = func(*args, **kw)

    @decoratorx
    def dummy_decoratorx(func, *args, **kw):
        result = func(*args, **kw)

    def dummy_decorate(func, dummy=1, *args, **kw):
        result = func(*args, **kw)

    @dummy_decorator(dummy=fdp.ConsumeInt(8))
    def func1(dummy):
        pass

    @dummy_decoratorx
    def func2(dummy):
        pass

    def func3(dummy):
        pass

    choice = fdp.ConsumeIntInRange(1,3)
	
    if choice == 1:
        func1(fdp.ConsumeBytes(fdp.ConsumeIntInRange(1,1000)))
    if choice == 2:
        func2(fdp.ConsumeBytes(fdp.ConsumeIntInRange(1,1000)))
    if choice == 3:
        decorate(func3,dummy_decorate,fdp.ConsumeInt(fdp.ConsumeIntInRange(1,1000)))
        func3(fdp.ConsumeBytes(10))

def main():
    atheris.Setup(sys.argv, TestInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()