import os
import glob

__all__ = []

for fn in glob.glob(os.path.dirname(__file__) + "/*.py"):
    m = os.path.basename(fn)[:-3]
    if m == '__init__':
        continue

    globals()[m] = getattr(__import__(m, globals(), locals(), [], -1), m)
    __all__.append(m)
