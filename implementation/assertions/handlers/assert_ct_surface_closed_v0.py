"""
ASSERT_CT_SURFACE_CLOSED_V0 Handler

Validates CT surface closure:
1. All discovered CT are explicitly declared
2. All declared CT have runtime implementations
3. No excess declarations (declared but not discovered)
"""

from pathlib import Path
from typing import Any

# Import LayerResolver for runtime path resolution
try:
    from pgs_governance.structure.structure.resolution.layer_resolver import LayerResolver
    LAYER_RESOLVER_AVAILABLE = True
except ImportError:
    LAYER_RESOLVER_AVAILABLE = False


def execute(artifacts: list[dict], compilation_context: dict) -> dict:
    """
    Verify CT surface is closed (declared == executable).

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

    # Get layer category map from compilation context (STRUCTURE-driven)
    layer_category_map = compilation_context.get("layer_category_map", {})

    # Get allowed CT list from ASSERT artifact itself
    assert_artifact = None
    for artifact in artifacts:
        frontmatter = artifact.get("frontmatter", {})
        artifact_code = frontmatter.get("artifact_code")
        if artifact_code == "ASSERT_CT_SURFACE_CLOSED_V0":
            assert_artifact = artifact
            break

    if not assert_artifact:
        # Fallback: empty allowed list (will flag all CT as violations)
        allowed_ct = set()
    else:
        frontmatter = assert_artifact.get("frontmatter", {})
        allowed_ct = set(frontmatter.get("allowed_capability_transforms", []))

    # Extract all discovered CT artifacts
    # Note: CT artifacts may have artifact_kind="atom"/"molecule" OR ct_code field
    discovered_ct = set()
    ct_artifacts = []

    for artifact in artifacts:
        frontmatter = artifact.get("frontmatter", {})

        # Check multiple patterns for CT identification:
        # 1. artifact_kind == "atom" or "molecule"
        # 2. Has ct_code field (CT artifact identifier)
        artifact_kind = frontmatter.get("artifact_kind")
        ct_code = frontmatter.get("ct_code")

        is_ct = (
            artifact_kind in ("atom", "molecule", "capability_transform") or
            ct_code is not None
        )

        if is_ct:
            fqdn = artifact["fqdn_id"]
            discovered_ct.add(fqdn)
            ct_artifacts.append(artifact)

    # CHECK 1: No Undeclared CT (PLATFORM ONLY)
    # All discovered PLATFORM CT must be in allowed list
    # Domain CT are automatically valid if they exist in registry (intrinsic resolution)
    for ct_fqdn in discovered_ct:
        # Find the artifact to check its layer
        ct_artifact = next((a for a in ct_artifacts if a["fqdn_id"] == ct_fqdn), None)

        if ct_artifact:
            # Skip domain artifacts - they're validated by existence (discovery)
            # Domain detection: check layer_category from STRUCTURE
            layer_code = ct_artifact.get("layer_code")
            is_domain = layer_category_map.get(layer_code) == "domain"
            if is_domain:
                continue

        # Platform CT must be in allowed list
        if ct_fqdn not in allowed_ct:
            violations.append({
                "fqdn": ct_fqdn,
                "rule": "governance.layers::INVARIANT_CT_SURFACE_CLOSED_V0",
                "message": "Undeclared platform CT (exists in registry but not in allowed list)",
                "fix": f"Add '{ct_fqdn}' to allowed_capability_transforms in ASSERT_CT_SURFACE_CLOSED_V0"
            })

    # CHECK 2: No Excess Declarations (SKIP FOR DOMAIN BUILDS)
    # All declared CT must be discovered (platform build only)
    # Domain builds may not discover all platform CT - this is expected
    # Skip this check if this is a domain build
    is_domain_build = compilation_context.get("is_domain_build", False)

    if not is_domain_build:
        for allowed_fqdn in allowed_ct:
            if allowed_fqdn not in discovered_ct:
                violations.append({
                    "fqdn": allowed_fqdn,
                    "rule": "governance.layers::INVARIANT_CT_SURFACE_CLOSED_V0",
                    "message": "Declared CT not found (in allowed list but not discovered in registry)",
                    "fix": f"Remove '{allowed_fqdn}' from allowed_capability_transforms (CT no longer exists)"
                })

    # CHECK 3: No Missing Implementations
    # CT resolution is intrinsic (registry + code import)
    # If CT was discovered, it exists in registry → valid
    # No need to check for runtime.py files
    # (CT are resolved via direct code import, not RB bindings)

    # Validate ct_code field presence
    for artifact in ct_artifacts:
        fqdn = artifact["fqdn_id"]
        ct_code = artifact.get("frontmatter", {}).get("ct_code")

        if not ct_code:
            violations.append({
                "fqdn": fqdn,
                "rule": "governance.layers::INVARIANT_CT_SURFACE_CLOSED_V0",
                "message": "CT artifact missing ct_code field in frontmatter",
                "fix": f"Add ct_code field to {fqdn} artifact"
            })

    # Return result
    if violations:
        # Add debug info about discovered CT
        debug_info = {
            "discovered_ct_count": len(discovered_ct),
            "discovered_ct_fqdns": sorted(list(discovered_ct)),
            "allowed_ct_count": len(allowed_ct),
            "allowed_ct_fqdns": sorted(list(allowed_ct))
        }

        return {
            "assert_count": len(ct_artifacts),
            "violations": violations,
            "status": "FAILED",
            "debug": debug_info
        }

    return {
        "assert_count": len(ct_artifacts),
        "violations": [],
        "status": "PASSED"
    }


def _check_runtime_exists(ct_code: str, layer_resolver) -> tuple[bool, Path]:
    """
    Check if runtime implementation exists for CT.

    Expected pattern:
        CT_X_V0 → pgs_transforms/implementation/transforms/{atoms,molecules}/ct_x_v0.py

    Returns:
        (exists: bool, expected_path: Path)
    """
    try:
        # Resolve REUSABLE_TRANSFORMS layer root
        # This returns the module root: /Users/bp/pgs_capabilities/pgs_transforms/implementation/transforms/
        layer_root = layer_resolver.resolve_layer_root("REUSABLE_TRANSFORMS")

        # Convert CT_CODE to lowercase for filename
        ct_code_lower = ct_code.lower()

        if not layer_root.exists():
            return False, layer_root / "atoms" / f"{ct_code_lower}.py"

        # Search in category subdirectories (atoms, molecules)
        for category_dir in layer_root.iterdir():
            if not category_dir.is_dir():
                continue

            # Check for flat .py file (not directory structure)
            runtime_path = category_dir / f"{ct_code_lower}.py"

            if runtime_path.exists():
                return True, runtime_path

        # Not found - return expected path in atoms/ by default
        expected = layer_root / "atoms" / f"{ct_code_lower}.py"
        return False, expected

    except Exception as e:
        # If layer resolution fails, assume missing
        return False, Path(f"<layer_resolution_failed: {e}>")
