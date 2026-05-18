"""
types.py — Vocabulary builder type definitions.

Dataclasses for vocabulary snapshots and results.

ARCHITECTURAL NOTE:
- VocabularyCategory and VocabularyEntry moved to structure layer (data types)
- Governance imports these from structure for validation
- Governance-specific types (VocabularyError, VocabularyResult, VocabularySnapshot) remain here
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Set, Any, Optional

# Import data types from structure layer
from pgs_governance.structure.structure.loading.vocabulary_loader import VocabularyCategory, VocabularyEntry


# ---------------------------------------------------------------------
# Result Types
# ---------------------------------------------------------------------

@dataclass
class VocabularyError:
    """Single vocabulary building error."""
    stage: str
    message: str
    file_path: Optional[Path] = None

    def __str__(self) -> str:
        if self.file_path:
            return f"[{self.stage}] {self.file_path}: {self.message}"
        return f"[{self.stage}] {self.message}"


@dataclass
class VocabularyResult:
    """Result of vocabulary building."""
    success: bool
    errors: List[VocabularyError] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: Optional[Dict[str, Any]] = None) -> "VocabularyResult":
        return cls(success=True, data=data or {})

    @classmethod
    def fail(cls, errors: List[VocabularyError]) -> "VocabularyResult":
        return cls(success=False, errors=errors)


# ---------------------------------------------------------------------
# Snapshot Types (from original vocabulary_builder.py)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class VocabularySnapshot:
    """Vocabulary symbols snapshot."""
    protocol_root: str

    # Protocol kinds (from VOCAB_PROTOCOL_KINDS_V0)
    node_types: List[str]
    artifact_kinds: List[str]

    # Execution states (from VOCAB_EXECUTION_STATES_V0)
    result_status: List[str]
    exit_reasons: List[str]

    # Language constraints (from VOCAB_LANGUAGE_CONSTRAINTS_V0)
    structural_keys: List[str]
    binding_verbs: Dict[str, List[str]]
    reserved_non_authorable: List[str]
    forbidden_language: List[str]

    # Protocol codes (scanned from artifacts)
    ct_codes: List[str]
    cs_codes: List[str]
    cc_codes: List[str]
    wf_codes: List[str]
    in_codes: List[str]

    stats: Dict[str, int]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    @classmethod
    def create(
        cls,
        protocol_root: Path,
        *,
        # Protocol kinds
        node_types: Set[str],
        artifact_kinds: Set[str],
        # Execution states
        result_status: Set[str],
        exit_reasons: Set[str],
        # Language constraints
        structural_keys: Set[str],
        binding_verbs_cs: Set[str],
        reserved_non_authorable: Set[str],
        forbidden_language: Set[str],
        # Protocol codes
        ct_codes: Set[str],
        cs_codes: Set[str],
        cc_codes: Set[str],
        wf_codes: Set[str],
        in_codes: Set[str],
    ) -> "VocabularySnapshot":
        """Factory to create snapshot with proper formatting."""
        # Phase 7: Use paths.roots.project (importlib-based, not marker walking)
        from pgs_governance.structure.structure.resolution import paths

        protocol_codes = ct_codes | cs_codes | cc_codes | wf_codes | in_codes

        # Store project-relative path, not absolute host path
        try:
            relative_root = str(protocol_root.relative_to(paths.roots.project))
        except ValueError:
            relative_root = str(protocol_root)

        return cls(
            protocol_root=relative_root,
            # Protocol kinds
            node_types=sorted(node_types),
            artifact_kinds=sorted(artifact_kinds),
            # Execution states
            result_status=sorted(result_status),
            exit_reasons=sorted(exit_reasons),
            # Language constraints
            structural_keys=sorted(structural_keys),
            binding_verbs={"CS": sorted(binding_verbs_cs)},
            reserved_non_authorable=sorted(reserved_non_authorable),
            forbidden_language=sorted(forbidden_language),
            # Protocol codes
            ct_codes=sorted(ct_codes),
            cs_codes=sorted(cs_codes),
            cc_codes=sorted(cc_codes),
            wf_codes=sorted(wf_codes),
            in_codes=sorted(in_codes),
            stats={
                "ct": len(ct_codes),
                "cs": len(cs_codes),
                "cc": len(cc_codes),
                "wf": len(wf_codes),
                "in": len(in_codes),
                "total": len(protocol_codes),
            },
        )


@dataclass(frozen=True)
class VocabularyIndexSnapshot:
    """Vocabulary semantic index snapshot."""
    workflows: Dict[str, dict]
    operations: Dict[str, dict]
    capabilities: Dict[str, dict]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)
