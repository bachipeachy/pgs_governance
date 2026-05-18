"""
contract.py — Vocabulary builder contract.

Immutable contract with all paths as explicit fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pgs_governance.structure.structure.resolution import PathRegistry


@dataclass(frozen=True)
class VocabularyContract:
    """
    Immutable vocabulary builder contract.

    All paths are explicit fields — no host discovery.

    Scan dirs are tuples to support multi-source aggregation (Phase Type B).
    For platform-only builds (Phase Type A), each tuple contains a single path.
    For federated aggregation, tuples contain one path per contributing layer.
    """

    # Artifacts root — used only as protocol_root metadata in snapshot output
    artifacts_root: Path

    # Vocabulary output paths
    vocabulary_dir: Path
    vocabulary_reserved_dir: Path
    vocabulary_symbols_path: Path
    vocabulary_semantic_index_path: Path

    # Artifact scan dirs (tuples: single entry for per-structure, multi for aggregation)
    capability_transforms_dirs: tuple
    capability_side_effects_dirs: tuple
    capability_contracts_dirs: tuple
    workflows_dirs: tuple
    intents_dirs: tuple

    @classmethod
    def from_paths(cls, paths: "PathRegistry", structure_artifact: dict) -> "VocabularyContract":
        """
        Factory from path registry — per-structure (Phase Type A) build.

        STRUCTURE sovereignty: Uses resolve_output_path() for vocabulary outputs.
        Raises ValueError if structure does not declare vocabulary_artifacts_path.

        Args:
            paths: PathRegistry instance (after bootstrap)
            structure_artifact: STRUCTURE artifact (e.g., STRUCTURE_BUILD_PLATFORM_CONFIG_V0)
        """
        # For platform build, compiled artifacts are centralized at project root
        # per STRUCTURE_BUILD_PLATFORM_CONFIG_V0 layer_outputs configuration
        project_root = paths.protocol._roots.project
        compiled_artifacts_root = project_root / "compiled" / "artifacts"

        # Resolve vocabulary output path via STRUCTURE (raises if not declared)
        vocabulary_dir = paths.resolve_output_path("vocabulary_artifacts_path", structure_artifact)

        return cls(
            artifacts_root=compiled_artifacts_root,
            vocabulary_dir=vocabulary_dir,
            vocabulary_reserved_dir=paths.governance.vocabulary_reserved_dir(),
            vocabulary_symbols_path=vocabulary_dir / "vocabulary_symbols.json",
            vocabulary_semantic_index_path=vocabulary_dir / "vocabulary_semantic_index.json",
            # Wrap single dirs in tuples (consistent with aggregation interface)
            capability_transforms_dirs=(compiled_artifacts_root / "capability_transforms",),
            capability_side_effects_dirs=(compiled_artifacts_root / "capability_side_effects",),
            capability_contracts_dirs=(compiled_artifacts_root / "capability_contracts",),
            workflows_dirs=(compiled_artifacts_root / "workflows",),
            intents_dirs=(compiled_artifacts_root / "intents",),
        )

    @classmethod
    def from_aggregate_structure(
        cls, paths: "PathRegistry", aggregate_structure: dict
    ) -> "VocabularyContract":
        """
        Factory from aggregation STRUCTURE (Phase Type B) — federated vocabulary build.

        Resolves source dirs from declared artifact_source_dirs in the aggregation
        STRUCTURE artifact. No hardcoded filesystem paths.

        Args:
            paths: PathRegistry instance (after bootstrap)
            aggregate_structure: STRUCTURE_BUILD_VOCABULARY_AGGREGATE_V0 artifact dict
        """
        structure_code = aggregate_structure.get("structure_code", "UNKNOWN")

        source_dirs_config = aggregate_structure.get("artifact_source_dirs")
        if not source_dirs_config:
            raise ValueError(
                f"PROTOCOL_INCOMPLETE: '{structure_code}' missing 'artifact_source_dirs'. "
                "Aggregation STRUCTURE must declare all contributing artifact directories."
            )

        from pgs_governance.structure.structure.resolution.path_registry import _layer_resolver
        resolver = _layer_resolver()

        def _resolve_repo_path(layer: str, subpath: str) -> Path:
            """
            Resolve layer-relative path using repo root (not module root).

            Uses the layer resolver's resolve_output_path with a synthesized
            layer_outputs structure — same mechanism as the materializer — so
            paths land correctly regardless of where the module root sits within
            the repo (e.g., 'registry/', 'compiler/', etc.).
            """
            fake_structure = {
                "output_configuration": {
                    "layer_outputs": {
                        layer: {"layer": layer, "subpath": subpath}
                    }
                }
            }
            return resolver.resolve_output_path("layer_outputs", layer, fake_structure)

        def resolve_dir_list(kind: str) -> tuple:
            entries = source_dirs_config.get(kind, [])
            if not entries:
                return ()
            resolved = []
            for entry in entries:
                layer = entry.get("layer")
                subpath = entry.get("subpath", "")
                if not layer:
                    raise ValueError(
                        f"PROTOCOL_INCOMPLETE: artifact_source_dirs.{kind} entry missing 'layer' in '{structure_code}'"
                    )
                resolved.append(_resolve_repo_path(layer, subpath))
            return tuple(resolved)

        ct_dirs = resolve_dir_list("capability_transforms")
        cs_dirs = resolve_dir_list("capability_side_effects")
        cc_dirs = resolve_dir_list("capability_contracts")
        wf_dirs = resolve_dir_list("workflows")
        in_dirs = resolve_dir_list("intents")

        # Resolve vocabulary output path
        vocabulary_dir = paths.resolve_output_path("vocabulary_artifacts_path", aggregate_structure)

        # artifacts_root is metadata-only in aggregation mode; use governance repo root
        artifacts_root = _resolve_repo_path("GOVERNANCE", "")

        return cls(
            artifacts_root=artifacts_root,
            vocabulary_dir=vocabulary_dir,
            vocabulary_reserved_dir=paths.governance.vocabulary_reserved_dir(),
            vocabulary_symbols_path=vocabulary_dir / "vocabulary_symbols.json",
            vocabulary_semantic_index_path=vocabulary_dir / "vocabulary_semantic_index.json",
            capability_transforms_dirs=ct_dirs,
            capability_side_effects_dirs=cs_dirs,
            capability_contracts_dirs=cc_dirs,
            workflows_dirs=wf_dirs,
            intents_dirs=in_dirs,
        )
