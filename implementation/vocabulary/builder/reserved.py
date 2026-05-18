"""
reserved.py — Reserved vocabulary validation (registry layer)

This module provides vocabulary validation using structure layer for loading.

ARCHITECTURAL BOUNDARY:
- Structure: Implements file loading and parsing
- Governance: Implements validation and schema enforcement (this file)

Refactored to use structure.protocol_loading for all file operations.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Set, Callable, Tuple

# Import data types and loading from structure
from pgs_governance.structure.structure.loading.vocabulary_loader import (
    VocabularyLoadResult,
    load_vocabulary_md,
)

# Import local types (registry-specific)
from .types import VocabularyEntry


# Validation patterns
LOWER_SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")
UPPER_SNAKE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# Type alias for file reader
FileReader = Callable[[Path], str]


def _validate_casing(entries: Set[str], casing: str, category: str) -> None:
    """
    Validate that all entries match the declared casing.

    Governance validation: Ensures vocabulary entries conform to schema.

    Args:
        entries: Set of vocabulary entries.
        casing: Expected casing ("UPPER_SNAKE" or "lower_snake").
        category: Category name for error messages.

    Raises:
        ValueError: If any entry doesn't match expected casing.
    """
    pattern = UPPER_SNAKE if casing == "UPPER_SNAKE" else LOWER_SNAKE

    for entry in entries:
        if not pattern.match(entry):
            raise ValueError(f"Invalid casing for '{entry}' in {category} (expected {casing})")


def load_reserved_vocabulary(
    reserved_dir: Path,
    read_file: FileReader,
) -> Dict[str, Set[str]]:
    """
    Load all reserved vocabulary from canonical .md files.

    Uses structure layer for file loading, adds registry validation.

    Args:
        reserved_dir: Path to reserved vocabulary directory.
        read_file: File reader function.

    Returns:
        Dictionary mapping category name to set of active words.

    Raises:
        ValueError: If any vocabulary file is invalid or fails validation.
    """
    vocab, _ = load_reserved_vocabulary_with_deprecated(reserved_dir, read_file)
    return vocab


def load_reserved_vocabulary_with_deprecated(
    reserved_dir: Path,
    read_file: FileReader,
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Load all reserved vocabulary from canonical .md files, including deprecated terms.

    Uses structure layer for file loading, adds registry validation.

    Args:
        reserved_dir: Path to reserved vocabulary directory.
        read_file: File reader function.

    Returns:
        Tuple of (active_vocabulary, deprecated_vocabulary), each mapping
        category name to set of words.

    Raises:
        ValueError: If any vocabulary file is invalid or fails validation.
    """
    # Load the 3 canonical vocabulary files using structure layer
    protocol_kinds = load_vocabulary_md(
        reserved_dir / "VOCAB_PROTOCOL_KINDS_V0.md", read_file
    )
    execution_states = load_vocabulary_md(
        reserved_dir / "VOCAB_EXECUTION_STATES_V0.md", read_file
    )
    language_constraints = load_vocabulary_md(
        reserved_dir / "VOCAB_LANGUAGE_CONSTRAINTS_V0.md", read_file
    )

    # Helper to get entries from a VocabularyLoadResult
    def _entries(lr: VocabularyLoadResult, cat: str) -> Set[str]:
        return lr.entry.get_entries(cat)

    def _deprecated(lr: VocabularyLoadResult, cat: str) -> Set[str]:
        dep_cat = lr.deprecated_categories.get(cat)
        return set(dep_cat.entries) if dep_cat else set()

    # Build active vocabulary dictionary
    vocab: Dict[str, Set[str]] = {
        "node_types": _entries(protocol_kinds, "node_types"),
        "artifact_kinds": _entries(protocol_kinds, "artifact_kinds"),
        "result_status": _entries(execution_states, "result_status"),
        "exit_reasons": _entries(execution_states, "exit_reasons"),
        "structural_keys": _entries(language_constraints, "structural_keys"),
        "binding_verbs_cs": _entries(language_constraints, "binding_verbs_cs"),
        "reserved_non_authorable": _entries(language_constraints, "reserved_non_authorable"),
        "forbidden_language": _entries(language_constraints, "forbidden_language"),
    }

    # Build deprecated vocabulary dictionary
    deprecated: Dict[str, Set[str]] = {}
    for lr, categories in [
        (protocol_kinds, ["node_types", "artifact_kinds"]),
        (execution_states, ["result_status", "exit_reasons"]),
        (language_constraints, ["structural_keys", "binding_verbs_cs", "reserved_non_authorable", "forbidden_language"]),
    ]:
        for cat in categories:
            dep = _deprecated(lr, cat)
            if dep:
                deprecated[cat] = dep

    # GOVERNANCE VALIDATION: Validate casing for each category
    _validate_casing(vocab["node_types"], "UPPER_SNAKE", "node_types")
    _validate_casing(vocab["artifact_kinds"], "lower_snake", "artifact_kinds")
    _validate_casing(vocab["result_status"], "UPPER_SNAKE", "result_status")
    _validate_casing(vocab["exit_reasons"], "UPPER_SNAKE", "exit_reasons")
    _validate_casing(vocab["structural_keys"], "lower_snake", "structural_keys")
    _validate_casing(vocab["binding_verbs_cs"], "UPPER_SNAKE", "binding_verbs_cs")
    _validate_casing(vocab["reserved_non_authorable"], "UPPER_SNAKE", "reserved_non_authorable")
    _validate_casing(vocab["forbidden_language"], "UPPER_SNAKE", "forbidden_language")

    # GOVERNANCE VALIDATION: Check for duplicates across incompatible groups
    collision_groups = [
        {"node_types", "artifact_kinds"},
        {"structural_keys", "binding_verbs_cs", "reserved_non_authorable", "forbidden_language"},
    ]

    for groups in collision_groups:
        seen: Dict[str, str] = {}
        for group in groups:
            if group not in vocab:
                continue
            for w in vocab[group]:
                if w in seen:
                    raise ValueError(f"Reserved word duplicated: '{w}' in {seen[w]} and {group}")
                seen[w] = group

    return vocab, deprecated
