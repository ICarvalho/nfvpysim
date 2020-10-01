from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python version 2.7 or later is required for Icarus (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys


# Import release information
import nfvpysim.release as release

__author__ = release.author
__version__ = release.version
__license__ = release.license_short


# List of all modules (even outside Icarus) that contain classes or function
# needed to be registered with the registry (via a register decorator)
# This code ensures that the modules are imported and hence the decorators are
# executed and the classes/functions registered.
__modules_to_register = [
     'nfvpysim.model.cache',
     'nfvpysim.model.policy',
     'nfvpysim.results.readwrite',
     'nfvpysim.execution.collectors',
     'nfvpysim.scenarios.topology',
     'nfvpysim.scenarios.vnfplacement',
     'nfvpysim.scenarios.vnfallocation',
     'nfvpysim.scenarios.workload',
                         ]

for m in __modules_to_register:
    # This try/catch is needed to support reload(icarus)
    try:
        exec('import %s' % m)
        exec('del %s' % m)
    except AttributeError:
        pass
del m

# Imports
from nfvpysim.model import *
from nfvpysim.tools import *
from nfvpysim.runner import run


