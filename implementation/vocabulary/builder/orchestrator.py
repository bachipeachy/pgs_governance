"""
orchestrator.py — Vocabulary builder orchestrator.

Coordinates vocabulary building with dependency injection for I/O.

Can be run directly: python orchestrator.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable

from pgs_governance.implementation.vocabulary.builder.types import VocabularyResult, VocabularyError
from pgs_governance.implementation.vocabulary.builder.contract import VocabularyContract
from pgs_governance.implementation.vocabulary.builder.snapshot import build_vocabulary_symbols, build_vocabulary_semantic_index


# Type aliases
FileReader = Callable[[Path], str]
FileWriter = Callable[[Path, str], None]
Logger = Callable[[str], None]


def _noop_logger(msg: str) -> None:
    """Default no-op logger."""
    pass


@dataclass
class VocabularyOrchestrator:
    """
    Vocabulary builder orchestrator.

    Constructor injection for testability:
    - contract: Paths and options
    - read_file: File reading function
    - write_file: File writing function
    - logger: Logging function
    """

    contract: VocabularyContract
    read_file: FileReader
    write_file: FileWriter
    logger: Logger = field(default=_noop_logger)

    def run(self) -> VocabularyResult:
        """
        Execute vocabulary build pipeline.

        Returns:
            VocabularyResult with symbols_path, index_path, and snapshots.
        """
        errors = []

        # Build vocabulary symbols
        self.logger("Building vocabulary symbols")
        try:
            symbols = build_vocabulary_symbols(self.contract, self.read_file)
        except ValueError as e:
            return VocabularyResult.fail([
                VocabularyError(stage="symbols", message=str(e))
            ])
        except Exception as e:
            return VocabularyResult.fail([
                VocabularyError(stage="symbols", message=f"Unexpected error: {e}")
            ])

        # Write symbols
        try:
            self.contract.vocabulary_dir.mkdir(parents=True, exist_ok=True)
            self.write_file(self.contract.vocabulary_symbols_path, symbols.to_json())
        except Exception as e:
            return VocabularyResult.fail([
                VocabularyError(
                    stage="write_symbols",
                    message=f"Failed to write symbols: {e}",
                    file_path=self.contract.vocabulary_symbols_path,
                )
            ])

        # Build semantic index
        self.logger("Building vocabulary semantic index")
        try:
            semantic_index = build_vocabulary_semantic_index(self.contract, self.read_file)
        except ValueError as e:
            return VocabularyResult.fail([
                VocabularyError(stage="index", message=str(e))
            ])
        except Exception as e:
            return VocabularyResult.fail([
                VocabularyError(stage="index", message=f"Unexpected error: {e}")
            ])

        # Write index
        try:
            self.write_file(self.contract.vocabulary_semantic_index_path, semantic_index.to_json())
        except Exception as e:
            return VocabularyResult.fail([
                VocabularyError(
                    stage="write_index",
                    message=f"Failed to write index: {e}",
                    file_path=self.contract.vocabulary_semantic_index_path,
                )
            ])

        return VocabularyResult.ok({
            "symbols_path": self.contract.vocabulary_symbols_path,
            "index_path": self.contract.vocabulary_semantic_index_path,
            "symbols": symbols,
            "semantic_index": semantic_index,
            "artifacts": {
                "symbols": str(self.contract.vocabulary_symbols_path),
                "semantic_index": str(self.contract.vocabulary_semantic_index_path),
            },
        })

    def build_symbols_only(self) -> VocabularyResult:
        """
        Build only vocabulary symbols (not semantic index).

        Useful for validation or partial builds.
        """
        self.logger("Building vocabulary symbols")
        try:
            symbols = build_vocabulary_symbols(self.contract, self.read_file)
            return VocabularyResult.ok({
                "symbols": symbols,
            })
        except ValueError as e:
            return VocabularyResult.fail([
                VocabularyError(stage="symbols", message=str(e))
            ])

    def build_index_only(self) -> VocabularyResult:
        """
        Build only semantic index (not symbols).

        Useful for partial rebuilds.
        """
        self.logger("Building vocabulary semantic index")
        try:
            semantic_index = build_vocabulary_semantic_index(self.contract, self.read_file)
            return VocabularyResult.ok({
                "semantic_index": semantic_index,
            })
        except ValueError as e:
            return VocabularyResult.fail([
                VocabularyError(stage="index", message=str(e))
            ])


# ---------------------------------------------------------------------
# CLI Entry Point (for direct execution)
# ---------------------------------------------------------------------

def main() -> None:
    """
    CLI entry point for direct execution.

    Enables running: python orchestrator.py
    """
    import json

    from pgs_governance.structure.structure.resolution import bootstrap, paths
    from pgs_governance.structure.structure.loading.protocol_loader import load_bootstrap_artifact

    # Bootstrap path registry
    bootstrap()

    # Load STRUCTURE configuration (vocabulary builder uses platform config)
    structure = load_bootstrap_artifact("fb.constitution::STRUCTURE_BUILD_PLATFORM_CONFIG_V0")

    # Create contract from paths (STRUCTURE sovereignty)
    contract = VocabularyContract.from_paths(paths, structure)

    # Create I/O functions
    def read_file(p: Path) -> str:
        return p.read_text(encoding="utf-8")

    def write_file(p: Path, content: str) -> None:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def logger(msg: str) -> None:
        print(f"[vocab_builder] {msg}", file=sys.stderr)

    # Create and run orchestrator
    logger("Vocabulary Builder started")

    orchestrator = VocabularyOrchestrator(
        contract=contract,
        read_file=read_file,
        write_file=write_file,
        logger=logger,
    )

    result = orchestrator.run()

    # Report errors
    if not result.success:
        for error in result.errors:
            print(f"[vocab_builder] FATAL: {error}", file=sys.stderr)
        sys.exit(1)

    # Output manifest
    manifest = {
        "status": "SUCCESS",
        "artifacts": result.data.get("artifacts", {}),
    }
    print(json.dumps(manifest, indent=2))

    logger("Vocabulary build completed successfully")


if __name__ == "__main__":
    main()
