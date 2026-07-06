"""
SentinelAI - MCP Complete Namespace Proxy
Resolves the collision between our frozen 'mcp' folder and the official 'mcp' SDK.
Proxies both submodule paths AND base variables without renaming directories.
"""

import sys
import os
import importlib.util

# 1. Identify local paths to temporarily exclude
_local_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
_original_sys_path = list(sys.path)

# 2. Strip local paths so Python is forced to look at site-packages for the official 'mcp'
sys.path = [p for p in sys.path if p not in (_local_dir, os.getcwd(), "")]

try:
    # 3. Locate and load the official 'mcp' SDK
    _official_spec = importlib.util.find_spec("mcp")
    if _official_spec and _official_spec.origin:
        _official_module = importlib.util.module_from_spec(_official_spec)
        _official_spec.loader.exec_module(_official_module)

        # 4. Proxy all base variables (like SamplingCapability) into this local namespace
        for _key, _value in _official_module.__dict__.items():
            if not _key.startswith("__"):
                globals()[_key] = _value

        # 5. Merge __path__ so submodules (mcp.server and mcp.weather) both resolve cleanly
        if hasattr(_official_module, "__path__"):
            __path__ = list(__path__) + list(_official_module.__path__)
except ImportError:
    pass
finally:
    # 6. Restore the execution environment variables
    sys.path = _original_sys_path