import functools
import importlib
import os
import sys
from typing import List, Optional, Union
import types

@functools.cache
def module_type(module: types.ModuleType):
    """ Uses heuristics to classify input module

    Returns one of #{"built_in", "third_party", "stdlib", "user_defined"}

    >>> import puddypeak as pp # installed as editable
    >>> import numpy as np
    >>> pp.module_type(pp)
    "user_defined"
    >>> pp.module_type(np)
    "third_party"
    """
    # 1. Exclude built-ins
    if not hasattr(module, '__file__'):
        return "built_in"
    # 2. Check for third-party common directories
    third_party_fps = [os.path.normcase(i) for i in sys.path if 'site-packages' in i]
    module_fp = os.path.normcase(module.__file__)
    for fp in third_party_fps:
        if module_fp.startswith(fp):
            return "third_party"
    # 3. Exclude standard library
    stdlib_fp = os.path.dirname(os.path.normcase(os.__file__))
    if stdlib_fp in module_fp:
        return "stdlib"
    return "user_defined"

def reload_all(
    gs: {},
    user_defined: bool = True,
    third_party: bool = False,
    modules: List[str] = [],
):
    """Reloads all modules using importlib

    Need to pass in `globals()` as positional argument because globals()
    returns the vars in this file, need to get them from the caller.

    By default, only reloads user defined modules.

    >>> import puddypeak as pp
    >>> import numpy as np
    >>> pp.reload_all(globals())
    {'reloaded': ['puddypeak'], 'not_reloaded': ['builtins(built_in)', 'numpy(third_party)']}
    """
    mods_loaded = {module for name, module in gs.items() if isinstance(module, types.ModuleType)}
    mods_loaded.update(set(modules))
    reload_info = {"reloaded": [], "not_reloaded": []}
    for mod in mods_loaded:
        mod_type = module_type(mod)
        mod_name = mod.__name__
        if (user_defined and mod_type == "user_defined") \
                or (third_party and mod_type == "third_party") \
                or mod in modules:
            importlib.reload(mod)
            reload_info["reloaded"].append(mod_name)
        else:
            reload_info["not_reloaded"].append(f"{mod_name}({mod_type})")
    reload_info["reloaded"].sort()
    reload_info["not_reloaded"].sort()
    return reload_info
