import importlib.util
import sys
import inspect
import os
from types import ModuleType


def get_function_definitions(
        module: ModuleType,
        module_name: str,
        basedir_name: str) -> list[dict]:
    funcs = []

    module_attributes = dir(module)

    for attr_name in module_attributes:
        attr = getattr(module, attr_name)

        if (
            inspect.isfunction(attr) and
            attr.__module__ == module_name
        ):
            funcs.append(
                {
                    'name': attr.__name__,
                    'func_inst': attr,
                    'handler_type': basedir_name
                }
            )

    return funcs


def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def recursive_handler_loader(basedir: str) -> None:
    handlers = []

    for (root, dirs, files) in os.walk(basedir):
        if (
            '__pycache__' not in root and
            files
        ):
            for filename in files:
                joined = os.path.join(root, filename)
                fname_no_ext = joined.replace('.py', '')
                module_name = fname_no_ext.replace('/', '.')
                module = lazy_import(module_name)
                handlers.extend(
                    get_function_definitions(
                        module,
                        module_name,
                        module_name.split('.')[1]
                    )
                )
    return handlers
