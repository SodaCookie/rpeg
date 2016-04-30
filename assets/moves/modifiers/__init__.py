"""Detects and imports all objects in effects folder"""
from os.path import dirname, basename, isfile, relpath
from importlib import import_module
import glob
import inspect

_modules = glob.glob(dirname(__file__)+"/*.py")
_relmodule = dirname(relpath(__file__)).replace("\\", ".") + "."

_imports = [import_module(_relmodule + basename(f)[:-3])
    for f in _modules if isfile(f) and basename(f) != "__init__.py"]
# Bring to global scope
imported_names = []
for module in _imports:
    members = inspect.getmembers(module)
    for name, value in members:
        if inspect.isclass(value):
            locals()[name] = value
            imported_names.append(name)

__all__ = imported_names