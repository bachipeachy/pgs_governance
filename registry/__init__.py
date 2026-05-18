"""
registry/ — Namespace Package

This is an explicit namespace package shared across multiple PGS repositories.

Contributing repositories:
- pgs_governance (primary registry layer)
- pgs_transforms (registry/registry/capability_transforms/)
- pgs_side_effects (registry/registry/capability_side_effects/)

CONSTITUTIONAL NOTE:
This uses pkgutil.extend_path for legitimate namespace package merging.
This is the ONLY allowed import magic in the registry layer.
All other sys.path manipulation is FORBIDDEN.
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
