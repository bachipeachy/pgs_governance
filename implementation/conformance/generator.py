"""
generator.py — Conformance Test Generator.

Generates conformance test descriptors from discovered artifacts.
No runtime_loader. No env_facts. Pure structural derivation from FQDN tree.

Governed by: CONSTITUTION_COMPILER_V0
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Callable

from pgs_compiler.tooling.builder.structure_tree import StructureTree, Package, PackageRoots


@dataclass(frozen=True)
class GeneratedTest:
    """A generated conformance test descriptor."""
    artifact_code: str
    artifact_kind: str
    module: str
    test_path: Path
    descriptor: Dict[str, Any]


@dataclass
class GeneratorResult:
    """Result of conformance test generation."""
    tests: List[GeneratedTest] = field(default_factory=list)
    package_stats: Dict[str, int] = field(default_factory=dict)
    skipped: List[str] = field(default_factory=list)


def _workflow_test_descriptor(artifact_code: str, module: str) -> Dict[str, Any]:
    """Generate a minimal workflow test descriptor."""
    return {
        "artifact": artifact_code,
        "module": module,
        "kind": "workflow",
        "expected_exit": "EXIT:SUCCESS",
        "trace_required": True,
    }


def _capability_contract_test_descriptor(artifact_code: str, module: str) -> Dict[str, Any]:
    """Generate a minimal capability contract test descriptor."""
    return {
        "artifact": artifact_code,
        "module": module,
        "kind": "capability_contract",
        "expected_result_status": "OK",
    }


def _clean_generated_dir(test_root: Path) -> int:
    """
    Remove all .test.json files from generated directory.

    Returns count of removed files.
    """
    removed = 0
    if test_root.exists():
        for test_file in test_root.glob("*.test.json"):
            test_file.unlink()
            removed += 1
    return removed


def generate_conformance_tests(
    artifacts: List[Any],  # DiscoveredArtifact from discover phase
    structure: StructureTree,
    roots: PackageRoots,
    write_file: Callable[[Path, str], None],
) -> GeneratorResult:
    """
    Generate conformance test descriptors from discovered artifacts.

    Cleanup: Removes stale .test.json files before generation to ensure
    deterministic output and prevent orphaned tests from accumulating.

    Args:
        artifacts: List of discovered artifacts (from validation phase)
        structure: Loaded structure tree
        roots: Dual roots for role-aware path resolution
        write_file: File writer function

    Returns:
        GeneratorResult with all generated tests
    """
    result = GeneratorResult()

    # Group artifacts by package
    artifacts_by_package: Dict[str, List[Any]] = {}
    for artifact in artifacts:
        pkg_name = artifact.package
        if pkg_name not in artifacts_by_package:
            artifacts_by_package[pkg_name] = []
        artifacts_by_package[pkg_name].append(artifact)

    # Process each package
    for pkg in structure.packages_by_order():
        pkg_artifacts = artifacts_by_package.get(pkg.package, [])
        if not pkg_artifacts:
            continue

        root = structure.resolve_root(pkg, roots)

        # Skip packages that opt out of conformance generation
        if not pkg.conformance_generation:
            test_root = root / pkg.physical_root.lstrip("./") / "testbed" / "generated"
            _clean_generated_dir(test_root)
            result.skipped.append(
                f"'{pkg.package}': conformance_generation disabled "
                f"({len(pkg_artifacts)} artifacts)"
            )
            continue

        # Filter to testable artifacts
        workflows = [a for a in pkg_artifacts if a.kind == "workflows"]
        contracts = [a for a in pkg_artifacts if a.kind == "capability_contracts"]

        if not workflows and not contracts:
            result.skipped.append(
                f"'{pkg.package}': no testable artifacts "
                f"({len(pkg_artifacts)} non-workflow/non-CC artifacts)"
            )
            continue

        # Derive test output directory from package structure
        output_dir = root / "testbed" / "generated"

        # CONTRACT: Path must be absolute (no relative hacks)
        if not output_dir.is_absolute():
            raise ValueError("STRUCTURE VIOLATION: conformance output path must be absolute")

        if ".." in output_dir.parts:
            raise ValueError("STRUCTURE VIOLATION: path traversal detected ('..')")

        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean stale tests before generation
        _clean_generated_dir(output_dir)

        generated_count = 0

        # Generate workflow tests
        for wf in workflows:
            descriptor = _workflow_test_descriptor(wf.code, pkg.package)
            test_path = output_dir / f"{wf.code.lower()}.test.json"

            # Write as single-item list to match oracle format
            test_content = json.dumps([{
                "title": f"Generated conformance test for {wf.code}",
                "target": wf.code,
                "payload": {},
                "trace": [
                    {"event": "workflow_start", "workflow_code": wf.code},
                    {"event": "workflow_complete", "result_status": "SUCCESS"},
                ],
                "_meta": descriptor,
            }], indent=2)

            write_file(test_path, test_content)

            result.tests.append(GeneratedTest(
                artifact_code=wf.code,
                artifact_kind="workflow",
                module=pkg.package,
                test_path=test_path,
                descriptor=descriptor,
            ))
            generated_count += 1

        # Generate capability contract tests
        for cc in contracts:
            descriptor = _capability_contract_test_descriptor(cc.code, pkg.package)
            test_path = output_dir / f"{cc.code.lower()}.test.json"

            # Write as single-item list to match oracle format
            test_content = json.dumps([{
                "title": f"Generated conformance test for {cc.code}",
                "target": cc.code,
                "payload": {},
                "trace": [
                    {"event": "capability_start", "capability_code": cc.code},
                    {"event": "capability_end", "capability_code": cc.code, "result_status": "SUCCESS"},
                ],
                "_meta": descriptor,
            }], indent=2)

            write_file(test_path, test_content)

            result.tests.append(GeneratedTest(
                artifact_code=cc.code,
                artifact_kind="capability_contract",
                module=pkg.package,
                test_path=test_path,
                descriptor=descriptor,
            ))
            generated_count += 1

        if generated_count > 0:
            result.package_stats[pkg.package] = generated_count

    return result
