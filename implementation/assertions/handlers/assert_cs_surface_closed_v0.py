"""
ASSERT_CS_SURFACE_CLOSED_V0 Handler

Validates CS surface closure:
1. All discovered CS are explicitly declared
2. All declared CS have runtime implementations
3. No excess declarations (declared but not discovered)
"""

from pathlib import Path
from typing import Any


def execute(artifacts: list[dict], compilation_context: dict) -> dict:
    """
    Verify CS surface is closed (declared == executable).

    Args:
        artifacts: All validated artifacts
        compilation_context: Contains artifacts_by_fqdn, layer_resolver, assert_artifact

    Returns:
        {
            "assert_count": int,
            "violations": list[dict],
            "status": "PASSED/FAILED"
        }
    """
    violations = []

    # Get allowed CS list from ASSERT artifact itself
    # The ASSERT artifact is passed via compilation_context during execution
    # We'll extract it from artifacts by finding the ASSERT_CS_SURFACE_CLOSED_V0 artifact

    assert_artifact = None
    for artifact in artifacts:
        frontmatter = artifact.get("frontmatter", {})
        artifact_code = frontmatter.get("artifact_code")
        if artifact_code == "ASSERT_CS_SURFACE_CLOSED_V0":
            assert_artifact = artifact
            break

    if not assert_artifact:
        # Fallback: empty allowed list (will flag all CS as violations)
        allowed_cs = set()
    else:
        frontmatter = assert_artifact.get("frontmatter", {})
        allowed_cs = set(frontmatter.get("allowed_capability_side_effects", []))

    # Extract all discovered CS artifacts
    # Note: CS artifacts may have artifact_kind="capability_side_effect" OR cs_code field
    discovered_cs = set()
    cs_artifacts = []

    for artifact in artifacts:
        frontmatter = artifact.get("frontmatter", {})

        # Check multiple patterns for CS identification:
        # 1. artifact_kind == "capability_side_effect"
        # 2. artifact_kind == "CS"
        # 3. Has cs_code field (CS artifact identifier)
        artifact_kind = frontmatter.get("artifact_kind")
        cs_code = frontmatter.get("cs_code")

        is_cs = (
            artifact_kind in ("capability_side_effect", "CS") or
            cs_code is not None
        )

        if is_cs:
            fqdn = artifact["fqdn_id"]
            discovered_cs.add(fqdn)
            cs_artifacts.append(artifact)

    # CHECK 1: No Undeclared CS (PLATFORM ONLY)
    # All discovered PLATFORM CS must be in allowed list
    # Domain CS are automatically valid if bound in RB
    for cs_fqdn in discovered_cs:
        # Find the artifact to check its layer
        cs_artifact = next((a for a in cs_artifacts if a["fqdn_id"] == cs_fqdn), None)

        if cs_artifact:
            # Skip domain artifacts - they're validated by RB binding check
            is_domain = cs_artifact.get("domain_name") is not None
            if is_domain:
                continue

        # Platform CS must be in allowed list
        if cs_fqdn not in allowed_cs:
            violations.append({
                "fqdn": cs_fqdn,
                "rule": "governance.layers::INVARIANT_CS_SURFACE_CLOSED_V0",
                "message": "Undeclared platform CS (exists in registry but not in allowed list)",
                "fix": f"Add '{cs_fqdn}' to allowed_capability_side_effects in ASSERT_CS_SURFACE_CLOSED_V0"
            })

    # CHECK 2: No Excess Declarations (SKIP FOR DOMAIN BUILDS)
    # All declared CS must be discovered (platform build only)
    # Domain builds may not discover all platform CS - this is expected
    # Skip this check if any domain artifacts are present
    has_domain_artifacts = any(a.get("domain_name") for a in artifacts)

    if not has_domain_artifacts:
        for allowed_fqdn in allowed_cs:
            if allowed_fqdn not in discovered_cs:
                violations.append({
                    "fqdn": allowed_fqdn,
                    "rule": "governance.layers::INVARIANT_CS_SURFACE_CLOSED_V0",
                    "message": "Declared CS not found (in allowed list but not discovered in registry)",
                    "fix": f"Remove '{allowed_fqdn}' from allowed_capability_side_effects (CS no longer exists)"
                })

    # CHECK 3: No Missing Implementations
    # All discovered CS must have runtime implementation (either RB binding or runtime.py)

    # Extract all CS bindings from RB artifacts
    rb_bound_cs = _extract_rb_bindings(artifacts)

    for artifact in cs_artifacts:
        fqdn = artifact["fqdn_id"]
        cs_code = artifact.get("frontmatter", {}).get("cs_code")

        if not cs_code:
            violations.append({
                "fqdn": fqdn,
                "rule": "governance.layers::INVARIANT_CS_SURFACE_CLOSED_V0",
                "message": "CS artifact missing cs_code field in frontmatter",
                "fix": f"Add cs_code field to {fqdn} artifact"
            })
            continue

        # Check if CS is bound in an RB artifact (domain CS pattern)
        if cs_code in rb_bound_cs:
            # CS is bound in RB - valid (no need to check runtime.py)
            continue

        # Check if runtime implementation exists (platform CS pattern)
        runtime_exists, runtime_path = _check_runtime_exists(cs_code)

        if not runtime_exists:
            violations.append({
                "fqdn": fqdn,
                "rule": "governance.layers::INVARIANT_CS_SURFACE_CLOSED_V0",
                "message": f"Missing runtime implementation (not bound in RB and no runtime.py at {runtime_path})",
                "fix": f"Either: (1) Bind CS in RB artifact, OR (2) Implement runtime.py at {runtime_path}"
            })

    # Return result
    if violations:
        # Add debug info about discovered CS
        debug_info = {
            "discovered_cs_count": len(discovered_cs),
            "discovered_cs_fqdns": sorted(list(discovered_cs)),
            "allowed_cs_count": len(allowed_cs),
            "allowed_cs_fqdns": sorted(list(allowed_cs)),
            "rb_bound_cs_count": len(rb_bound_cs),
            "violation_breakdown": {}
        }

        # Breakdown violations by type
        for v in violations:
            violation_type = v["message"].split("(")[0].strip()
            debug_info["violation_breakdown"].setdefault(violation_type, 0)
            debug_info["violation_breakdown"][violation_type] += 1

        return {
            "assert_count": len(cs_artifacts),
            "violations": violations,
            "status": "FAILED",
            "debug": debug_info
        }

    return {
        "assert_count": len(cs_artifacts),
        "violations": [],
        "status": "PASSED"
    }


def _extract_rb_bindings(artifacts: list[dict]) -> set[str]:
    """
    Extract all CS bindings from RB artifacts.

    Returns:
        Set of CS codes that are bound in RB artifacts
    """
    rb_bound_cs = set()

    for artifact in artifacts:
        # Check if this is an RB artifact
        # Use artifact_type (normalized) instead of artifact_kind
        artifact_type = artifact.get("artifact_type")

        if artifact_type != "RB":
            continue

        # Extract bindings from RB artifact
        frontmatter = artifact.get("frontmatter", {})
        core = frontmatter.get("core", {})
        bindings = core.get("bindings", {})

        # Add all bound CS codes
        # CS artifacts are identified by FQDN or code pattern: namespace::CS_*_V0 or CS_*_V0
        for bound_key in bindings.keys():
            if not isinstance(bound_key, str):
                continue

            # Extract CS code from FQDN (namespace::CS_X_V0 -> CS_X_V0)
            if "::" in bound_key:
                # FQDN format - extract the code part
                cs_code_part = bound_key.split("::")[-1]
                if cs_code_part.startswith("CS_"):
                    rb_bound_cs.add(cs_code_part)
            elif bound_key.startswith("CS_"):
                # Short code format
                rb_bound_cs.add(bound_key)

    return rb_bound_cs


def _find_project_root() -> Path:
    """
    Find project root by locating the installed pgs_governance package.

    Returns:
        Project root path (parent of the pgs_governance package directory)
    """
    import pgs_governance as _pg
    return Path(_pg.__file__).parent.parent


def _get_side_effects_implementation_root() -> Path:
    """
    Get side effects implementation root using LayerResolver (STRUCTURE_DISCOVERY_V0).

    REUSABLE_SIDE_EFFECTS registry_module resolves to pgs_side_effects/registry/.
    Implementation lives at the sibling path: pgs_side_effects/implementation/side_effects/.
    """
    from pgs_governance.implementation.structure.resolution.layer_resolver import LayerResolver
    resolver = LayerResolver()
    registry_root = resolver.resolve_layer_root("REUSABLE_SIDE_EFFECTS")
    # registry_root = .../pgs_side_effects/registry/
    # implementation root = .../pgs_side_effects/implementation/side_effects/
    return registry_root.parent / "implementation" / "side_effects"


def _check_runtime_exists(cs_code: str) -> tuple[bool, Path]:
    """
    Check if runtime implementation exists for CS.

    Expected pattern:
        CS_X_V0 → pgs_side_effects/implementation/side_effects/{persistent,internal,external}/CS_X_V0/runtime.py

    Returns:
        (exists: bool, expected_path: Path)
    """
    runtime_root = _get_side_effects_implementation_root()

    if not runtime_root.exists():
        return False, runtime_root / "persistent" / cs_code / "runtime.py"

    # Search in category subdirectories (persistent, internal, external)
    for category_dir in runtime_root.iterdir():
        if not category_dir.is_dir():
            continue
        runtime_path = category_dir / cs_code / "runtime.py"
        if runtime_path.exists():
            return True, runtime_path

    expected = runtime_root / "persistent" / cs_code / "runtime.py"
    return False, expected
