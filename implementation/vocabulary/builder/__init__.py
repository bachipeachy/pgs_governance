"""
builder/ — Vocabulary Builder Module.

Headless, deterministic vocabulary building.

Public API:
    - VocabularyOrchestrator: Main orchestrator class
    - VocabularyContract: Immutable contract
    - VocabularyResult: Build result
    - VocabularySnapshot: Vocabulary symbols snapshot
    - VocabularyIndexSnapshot: Semantic index snapshot

Usage:
    from pgs_governance.registry.vocabulary.builder import (
        VocabularyOrchestrator,
        VocabularyContract,
    )
    from pgs_governance.structure.structure.loading.protocol_loader import load_bootstrap_artifact

    structure = load_bootstrap_artifact("fb.constitution::STRUCTURE_BUILD_PLATFORM_CONFIG_V0")
    contract = VocabularyContract.from_paths(paths, structure)
    orchestrator = VocabularyOrchestrator(
        contract=contract,
        read_file=lambda p: p.read_text(encoding="utf-8"),
        write_file=lambda p, c: p.write_text(c, encoding="utf-8"),
        logger=lambda msg: print(msg),
    )
    result = orchestrator.run()
"""

from pgs_governance.implementation.vocabulary.builder.types import (
    VocabularyCategory,
    VocabularyEntry,
    VocabularyError,
    VocabularyResult,
    VocabularySnapshot,
    VocabularyIndexSnapshot,
)
from pgs_governance.implementation.vocabulary.builder.contract import VocabularyContract
from pgs_governance.implementation.vocabulary.builder.orchestrator import VocabularyOrchestrator
from pgs_governance.implementation.vocabulary.builder.reserved import load_reserved_vocabulary, load_reserved_vocabulary_with_deprecated

# Import artifact discovery from structure layer
from pgs_governance.structure.structure.discovery import (
    extract_codes,
    extract_wf_codes,
    extract_in_codes,
)
from pgs_governance.structure.structure.loading import VocabularyLoadResult

from pgs_governance.implementation.vocabulary.builder.snapshot import (
    build_vocabulary_symbols,
    build_vocabulary_semantic_index,
)

__all__ = [
    # Types
    "VocabularyCategory",
    "VocabularyEntry",
    "VocabularyError",
    "VocabularyResult",
    "VocabularySnapshot",
    "VocabularyIndexSnapshot",
    # Contract
    "VocabularyContract",
    # Orchestrator
    "VocabularyOrchestrator",
    # Functions
    "load_reserved_vocabulary",
    "load_reserved_vocabulary_with_deprecated",
    "VocabularyLoadResult",
    "extract_codes",
    "extract_wf_codes",
    "extract_in_codes",
    "build_vocabulary_symbols",
    "build_vocabulary_semantic_index",
]
