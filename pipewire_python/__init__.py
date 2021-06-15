"""pipewire_python:
Python controller, player and recorder via pipewire's commands"""

__version__ = "0.0.4"

import sys

if sys.platform == "linux":
    from pipewire_python.pipewirecontroller import *
else:
    raise NotImplementedError("By now, Pipewire only runs on linux.")
