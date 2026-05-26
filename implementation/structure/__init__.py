"""
structure — PGS Structure Layer (Foundational)

The structure layer provides foundational runtime services for all other layers:
- Discovery: Artifact discovery and scanning
- Loading: Protocol file loading and parsing
- Resolution: Path and layer resolution

Public API organized by concern:
- structure.discovery.*
- structure.loading.*
- structure.resolution.*

Quick imports for common use:
- from pgs_governance.implementation.structure.resolution import bootstrap, paths, LayerResolver
- from pgs_governance.implementation.structure.loading import load_trace, parse_yaml_simple
- from pgs_governance.implementation.structure.discovery import extract_codes, scan_artifacts_by_type
"""

# Re-export commonly used items for convenience
from pgs_governance.implementation.structure.resolution import bootstrap, paths, LayerResolver
from pgs_governance.implementation.structure.loading import (
    ProtocolFSReader,
    ProtocolLoader,
    load_trace,
    TestCase,
    load_test_cases,
    parse_yaml_simple,
    load_vocabulary_md,
)
from pgs_governance.implementation.structure.discovery import (
    extract_codes,
    extract_wf_codes,
    extract_in_codes,
    scan_artifacts_by_type,
)

__all__ = [
    # Resolution (most commonly used)
    "bootstrap",
    "paths",
    "LayerResolver",
    # Loading (commonly used)
    "ProtocolFSReader",
    "ProtocolLoader",
    "load_trace",
    "TestCase",
    "load_test_cases",
    "parse_yaml_simple",
    "load_vocabulary_md",
    # Discovery (commonly used)
    "extract_codes",
    "extract_wf_codes",
    "extract_in_codes",
    "scan_artifacts_by_type",
]
