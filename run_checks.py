"""Run all supplementary proof checks, failing on any error."""
from pathlib import Path
import os
import sys
import unittest

if not __debug__:
    raise RuntimeError('Run without -O')
root=Path(__file__).resolve().parent
os.chdir(root)
suite=unittest.defaultTestLoader.discover('tests')
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
