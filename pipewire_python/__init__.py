import sys


if sys.platform=='linux':
    from pipewire_python import *
else:
    raise Exception('By now, Pipewire only runs on linux.')