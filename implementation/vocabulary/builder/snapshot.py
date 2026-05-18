"""
snapshot.py — Vocabulary snapshot building.

Pure functions for building vocabulary symbols and semantic index.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Callable

from pgs_governance.implementation.vocabulary.builder.types import VocabularySnapshot, VocabularyIndexSnapshot
from pgs_governance.implementation.vocabulary.builder.contract import VocabularyContract
from pgs_governance.implementation.vocabulary.builder.reserved import load_reserved_vocabulary

# Import artifact discovery from structure layer
from pgs_governance.structure.structure.discovery import (
    extract_codes,
    extract_wf_codes,
    extract_in_codes,
    iter_protocol_jsons,
    load_json_strict,
)


# Type alias for file reader
FileReader = Callable[[Path], str]


def extract_codes_from_compiled(
    artifacts_dir: Path,
    read_file: FileReader,
    prefix: str,
) -> set[str]:
    """
    Extract artifact codes from compiled JSON artifacts.

    Compiled artifacts have structure:
    {
      "artifact_code": "CT_PURE_FOO_V0",
      "artifact_type": "CT",
      ...
    }

    Args:
        artifacts_dir: Directory containing compiled JSON artifacts.
        read_file: File reader function.
        prefix: Required prefix for codes (e.g., "CT_", "CS_").

    Returns:
        Set of extracted artifact codes.
    """
    codes: set[str] = set()

    for path in iter_protocol_jsons(artifacts_dir):
        try:
            data = load_json_strict(path, read_file)
            code = data.get("artifact_code")
            if isinstance(code, str) and code.startswith(prefix):
                codes.add(code)
        except ValueError:
            # Skip malformed files
            continue

    return codes


def build_vocabulary_symbols(
    config: VocabularyContract,
    read_file: FileReader,
) -> VocabularySnapshot:
    """
    Build vocabulary symbols snapshot.

    Args:
        config: Vocabulary configuration.
        read_file: File reader function.

    Returns:
        VocabularySnapshot with all symbols.

    Raises:
        ValueError: If vocabulary building fails.
    """
    # Load reserved vocabulary from canonical .md files
    reserved = load_reserved_vocabulary(config.vocabulary_reserved_dir, read_file)

    # Extract codes from compiled artifacts (scan all declared source dirs per type)
    ct_codes: set[str] = set()
    for d in config.capability_transforms_dirs:
        ct_codes |= extract_codes_from_compiled(d, read_file, "CT_")

    cs_codes: set[str] = set()
    for d in config.capability_side_effects_dirs:
        cs_codes |= extract_codes_from_compiled(d, read_file, "CS_")

    cc_codes: set[str] = set()
    for d in config.capability_contracts_dirs:
        cc_codes |= extract_codes_from_compiled(d, read_file, "CC_")

    wf_codes: set[str] = set()
    for d in config.workflows_dirs:
        wf_codes |= extract_codes_from_compiled(d, read_file, "WF_")

    in_codes: set[str] = set()
    for d in config.intents_dirs:
        in_codes |= extract_codes_from_compiled(d, read_file, "IN_")

    # Validate at least some artifacts exist
    if not (ct_codes or cs_codes or cc_codes or wf_codes or in_codes):
        raise ValueError("No protocol artifacts discovered")

    # Check for collisions with reserved words
    protocol_codes = ct_codes | cs_codes | cc_codes | wf_codes | in_codes
    all_reserved = set().union(*reserved.values())

    collisions = protocol_codes & all_reserved
    if collisions:
        raise ValueError(
            f"Protocol identifiers collide with reserved words: {sorted(collisions)}"
        )

    # Create snapshot with all vocabulary categories
    return VocabularySnapshot.create(
        protocol_root=config.artifacts_root,
        # Protocol kinds
        node_types=reserved["node_types"],
        artifact_kinds=reserved["artifact_kinds"],
        # Execution states
        result_status=reserved["result_status"],
        exit_reasons=reserved["exit_reasons"],
        # Language constraints
        structural_keys=reserved["structural_keys"],
        binding_verbs_cs=reserved["binding_verbs_cs"],
        reserved_non_authorable=reserved["reserved_non_authorable"],
        forbidden_language=reserved["forbidden_language"],
        # Protocol codes
        ct_codes=ct_codes,
        cs_codes=cs_codes,
        cc_codes=cc_codes,
        wf_codes=wf_codes,
        in_codes=in_codes,
    )


def build_vocabulary_semantic_index(
    config: VocabularyContract,
    read_file: FileReader,
) -> VocabularyIndexSnapshot:
    """
    Build vocabulary semantic index.

    Args:
        config: Vocabulary configuration.
        read_file: File reader function.

    Returns:
        VocabularyIndexSnapshot with all indexed artifacts.
    """
    # Index workflows (from all declared workflow source dirs)
    workflows: Dict[str, dict] = {}
    for source_dir in config.workflows_dirs:
        for path in iter_protocol_jsons(source_dir):
            try:
                data = load_json_strict(path, read_file)
                code = data.get("artifact_code")
                if code and code.startswith("WF_"):
                    workflows[code] = data
            except ValueError:
                continue

    # Index operations (capability contracts from all declared source dirs)
    operations: Dict[str, dict] = {}
    for source_dir in config.capability_contracts_dirs:
        for path in iter_protocol_jsons(source_dir):
            try:
                data = load_json_strict(path, read_file)
                code = data.get("artifact_code")
                if code and code.startswith("CC_"):
                    operations[code] = data
            except ValueError:
                continue

    # Index capabilities (transforms and side effects from all declared source dirs)
    capabilities: Dict[str, dict] = {}

    for dirs, prefix in [
        (config.capability_transforms_dirs, "CT_"),
        (config.capability_side_effects_dirs, "CS_"),
    ]:
        for root in dirs:
            for path in iter_protocol_jsons(root):
                try:
                    data = load_json_strict(path, read_file)
                    code = data.get("artifact_code")
                    if code and code.startswith(prefix):
                        capabilities[code] = data
                except ValueError:
                    continue

    return VocabularyIndexSnapshot(
        workflows=workflows,
        operations=operations,
        capabilities=capabilities,
    )
