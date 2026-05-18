# STRUCTURE_ARTIFACT_IDENTITY_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Governed By**: fb.constitution::CONSTITUTION_STRUCTURE_V0

---

## Purpose

Defines the canonical artifact identity system for Protocol-Governed Systems (PGS). Establishes **FQDN-scoped identity** as the internal system identity while preserving clean, short names in human-authored artifacts.

**Core Principle**: Human identity (local + readable) is separate from system identity (global + deterministic). Compilation is the resolution boundary.

**Scope**: All artifact discovery, compilation, and runtime resolution.

---

## Identity Model

### Human Identity (Authoring Layer)
Human-authored source artifacts (.md files) use **short artifact codes**:
```yaml
artifact_code: CT_VALIDATE_SCHEMA_V0
```

This preserves:
- Readability
- Speed of authoring
- Cognitive clarity

### System Identity (Compilation + Runtime)
Compiled artifacts (.json files) use **FQDN-scoped identity**:
```json
{
  "artifact_code": "CT_VALIDATE_SCHEMA_V0",
  "fqdn_id": "blockchain.testbed.CT_VALIDATE_SCHEMA_V0"
}
```

This ensures:
- No namespace collisions
- Deterministic resolution
- Explicit debugging (traces show full FQDN)
- True federation (same code in multiple scopes)

---

## FQDN Schema

### Format

```
fqdn_id = <fqdn> + "." + <artifact_code>

where:
  fqdn = <scope>
  scope = <package>[.<domain>][.<subscope>]
```

### Examples

**Platform artifacts (single-level scope)**:
- `governance.STRUCTURE_LAYER_AUTHORITY_V0`
- `transforms.CT_PURE_HASH_V0`
- `side_effects.CS_FILE_WRITE_V0`
- `compiler.WF_BUILD_PLATFORM_V0`

**Domain artifacts (multi-level scope)**:
- `blockchain.identity.WF_CREATE_IDENTITY_V0`
- `blockchain.wallet.CT_VALIDATE_SIGNATURE_V0`
- `blockchain.transaction.IN_SUBMIT_TRANSACTION_V0`
- `ai_licensing.CC_LICENSE_VALIDATION_V0`
- `agent_governance.WF_REGISTER_AGENT_V0`

**Reusable capabilities (platform)**:
- `transforms.CT_NORMALIZE_ARTIFACT_V0`
- `side_effects.CS_COMPILER_ARTIFACT_REGISTRY_V0`

---

## Scope Computation Rules

### Platform Artifacts
```python
# For platform layers (GOVERNANCE, COMPILER, etc.)
fqdn = package_name

# Examples:
# registry/registry/compiler/CT_SCAN_V0.md
#   → fqdn = "registry"
#   → fqdn_id = "registry.CT_SCAN_V0"

# transforms/registry/CT_HASH_V0.md
#   → fqdn = "transforms"
#   → fqdn_id = "transforms.CT_HASH_V0"
```

### Domain Artifacts
```python
# For DOMAINS layer
fqdn = f"{domain_name}.{subscope}"

# Examples:
# domains/blockchain/registry/wallet/CT_VALIDATE_V0.md
#   → fqdn = "blockchain.wallet"
#   → fqdn_id = "blockchain.wallet.CT_VALIDATE_V0"

# domains/ai_licensing/registry/WF_LICENSE_V0.md
#   → fqdn = "ai_licensing"
#   → fqdn_id = "ai_licensing.WF_LICENSE_V0"
```

### Scope Extraction Algorithm
```python
def compute_fqdn_scope(artifact_path: Path, layer_code: str) -> str:
    """
    Compute FQDN scope from artifact path and layer.

    This is the ONLY way scope is determined.
    No filesystem heuristics. No guessing.
    """
    if layer_code == "DOMAINS":
        # Extract: domains/{domain}/registry/{subscope}/...
        parts = artifact_path.parts
        domain_idx = parts.index("domains") + 1
        domain = parts[domain_idx]

        # Check for subscope (e.g., wallet, identity, transaction)
        registry_idx = parts.index("registry", domain_idx) + 1
        if registry_idx < len(parts) - 1:  # Has subscope
            subscope = parts[registry_idx]
            return f"{domain}.{subscope}"
        else:
            return domain

    elif layer_code in ["GOVERNANCE", "COMPILER", "EXECUTION",
                        "REUSABLE_TRANSFORMS", "REUSABLE_SIDE_EFFECTS",
                        "AUTHORING", "TRANSPORT", "INGRESS", "EGRESS"]:
        # Platform artifacts: scope = package name
        return layer_code_to_package_name(layer_code)

    else:
        raise RuntimeError(f"Unknown layer for FQDN scope: {layer_code}")

def layer_code_to_package_name(layer_code: str) -> str:
    """Map layer code to package name for platform artifacts."""
    mapping = {
        "GOVERNANCE": "registry",
        "COMPILER": "compiler",
        "EXECUTION": "execution",
        "REUSABLE_TRANSFORMS": "transforms",
        "REUSABLE_SIDE_EFFECTS": "side_effects",
        "AUTHORING": "authoring",
        "TRANSPORT": "transport",
        "INGRESS": "ingress",
        "EGRESS": "egress",
    }
    return mapping.get(layer_code, layer_code.lower())
```

---

## Reference Resolution

### Compile-Time Resolution

When compiling an artifact that references other artifacts:

```yaml
# Source .md file (human-authored)
pipeline:
  - step: validate
    transform: CT_VALIDATE_SCHEMA_V0  # Short name

# Compiled .json file (machine-generated)
{
  "pipeline": [{
    "step": "validate",
    "transform": "registry.CT_VALIDATE_SCHEMA_V0"  // Resolved FQDN
  }]
}
```

**Resolution algorithm**:
1. Extract short name from reference: `CT_VALIDATE_SCHEMA_V0`
2. Determine search scope from STRUCTURE artifact
3. Scan search roots for matching artifact_code
4. Resolve to fqdn_id
5. Write resolved FQDN to compiled artifact

### Search Scope Rules

**Same-scope references** (common case):
```yaml
# blockchain.wallet.WF_CREATE_WALLET_V0 references CT_VALIDATE_SIGNATURE_V0
# Search order:
1. blockchain.wallet.*  # Local scope first
2. blockchain.*         # Parent domain scope
3. transforms.*         # Platform capabilities
4. registry.*         # Platform registry
```

**Cross-scope references** (explicit):
```yaml
# Domain artifact referencing platform registry
# blockchain.wallet.CC_WALLET_CONTRACT_V0 references registry.SCHEMA_CONTRACT_V0
# Must be resolved via STRUCTURE search_roots
```

**Search roots** are declared in STRUCTURE artifacts:
- Platform build: `STRUCTURE_BUILD_PLATFORM_CONFIG_V0`
- Domain build: `STRUCTURE_BUILD_DOMAINS_CONFIG_V0`
- Runtime execution: `STRUCTURE_RUNTIME_EXECUTION_V0`

---

## Bootstrap Exception

**STRUCTURE artifacts themselves** require special handling to avoid chicken-egg problem:

```python
# Bootstrap STRUCTURE artifacts use hardcoded path
def bootstrap_discover_structure_artifact(structure_code: str):
    """
    Bootstrap exception: STRUCTURE artifacts resolved from canonical location.

    This is the ONLY hardcoded path in the system.
    All other artifacts use STRUCTURE-driven resolution.
    """
    bootstrap_root = Path("pgs_governance/registry/structures")
    artifact_path = bootstrap_root / f"{structure_code}.md"

    artifact = parse_artifact(artifact_path)

    # Bootstrap artifacts get special FQDN
    artifact["fqdn"] = "registry"
    artifact["fqdn_id"] = f"registry.{structure_code}"

    return artifact
```

**Bootstrap-eligible STRUCTURE codes**:
- `STRUCTURE_RUNTIME_EXECUTION_V0`
- `STRUCTURE_BUILD_PLATFORM_CONFIG_V0`
- `STRUCTURE_BUILD_DOMAINS_CONFIG_V0`
- `STRUCTURE_ARTIFACT_IDENTITY_V0` (this artifact)

---

## Uniqueness Enforcement

### FQDN Uniqueness (STRICT)

```python
duplicate fqdn_id → HARD ERROR

# Example violation:
blockchain.wallet.CT_VALIDATE_V0  # First occurrence
blockchain.wallet.CT_VALIDATE_V0  # Second occurrence
# → ERROR: Duplicate fqdn_id detected
```

### Artifact Code Uniqueness (RELAXED)

```python
duplicate artifact_code across scopes → ALLOWED

# Example allowed:
blockchain.wallet.CT_VALIDATE_V0
ai_licensing.CT_VALIDATE_V0
# → OK: Same code, different scopes
```

This enables artifact reuse patterns across domains while maintaining global uniqueness.

---

## Runtime Resolution

### Strict FQDN-Only Resolution

Runtime MUST use fqdn_id for all artifact lookups:

```python
# ✅ CORRECT - Runtime resolution
def resolve_artifact(fqdn_id: str) -> Artifact:
    """Resolve artifact by FQDN only."""
    return artifact_registry[fqdn_id]

# ❌ FORBIDDEN - Short name resolution
def bad_resolve(artifact_code: str) -> Artifact:
    """This pattern is FORBIDDEN at runtime."""
    # No guessing, no fallback, no heuristics
    raise RuntimeError("Runtime must use fqdn_id, not artifact_code")
```

### No Fallback Logic

```python
# ❌ FORBIDDEN - Fallback resolution
artifact = registry.get(fqdn_id) or registry.get(f"*.{artifact_code}")

# ✅ CORRECT - Hard failure
artifact = registry.get(fqdn_id)
if artifact is None:
    raise ArtifactNotFoundError(
        f"Artifact not found: {fqdn_id}\n"
        f"No fallback resolution permitted."
    )
```

---

## Enforcement Rules

### Rule 1: Source Artifacts Never Change
Human-authored .md files continue using short artifact_code. FQDN is internal system identity only.

### Rule 2: Discovery Computes FQDN
During discovery phase (`ct_scan_artifacts.py`), compute fqdn and fqdn_id for every artifact based on path + layer.

### Rule 3: Compilation Resolves References
During compilation phase (`ct_normalize_artifact.py`), resolve all short-name references to FQDN using STRUCTURE search scope.

### Rule 4: Runtime Uses FQDN Only
Runtime resolution APIs accept fqdn_id only. No short-name lookups permitted.

### Rule 5: Uniqueness Validation
Build MUST validate fqdn_id uniqueness. Duplicate fqdn_id → hard build failure.

### Rule 6: Bootstrap Exception
STRUCTURE artifacts (and only STRUCTURE artifacts) may use hardcoded bootstrap resolution.

---

## Migration Path

### Phase 1: Add fqdn_id to Discovery
Modify `ct_scan_artifacts.py` to compute fqdn and fqdn_id.

### Phase 2: Store in Compiled Artifacts
Update compiled JSON schema to include fqdn_id field.

### Phase 3: Resolve References at Compile Time
Update `ct_normalize_artifact.py` to resolve short names → FQDN.

### Phase 4: Switch Runtime to FQDN
Update all runtime indexes and resolution APIs to use fqdn_id.

### Phase 5: Remove Legacy Resolution
Delete all fallback and short-name resolution code paths.

### Phase 6: Enforce Uniqueness
Add validation to fail build on duplicate fqdn_id.

---

## Machine

```yaml
structure_code: STRUCTURE_ARTIFACT_IDENTITY_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Canonical artifact identity system (FQDN-scoped)
  description: >
    Defines FQDN-scoped identity as internal system identity while preserving
    clean, short names in human-authored artifacts. Compilation is the
    resolution boundary between human identity and system identity.

  identity_model:
    human_identity:
      layer: authoring
      format: artifact_code
      example: "CT_VALIDATE_SCHEMA_V0"

    system_identity:
      layer: compilation_runtime
      format: fqdn_id
      example: "blockchain.wallet.CT_VALIDATE_SCHEMA_V0"

  fqdn_schema:
    format: "<fqdn>.<artifact_code>"

    scope_format:
      platform: "<package>"
      domain: "<domain>[.<subscope>]"

    examples:
      platform:
        - "registry.STRUCTURE_LAYER_AUTHORITY_V0"
        - "transforms.CT_PURE_HASH_V0"
        - "compiler.WF_BUILD_PLATFORM_V0"

      domain:
        - "blockchain.wallet.CT_VALIDATE_SIGNATURE_V0"
        - "blockchain.identity.WF_CREATE_IDENTITY_V0"
        - "ai_licensing.CC_LICENSE_VALIDATION_V0"

  resolution:
    bootstrap_exception:
      - STRUCTURE_RUNTIME_EXECUTION_V0
      - STRUCTURE_BUILD_PLATFORM_CONFIG_V0
      - STRUCTURE_BUILD_DOMAINS_CONFIG_V0
      - STRUCTURE_ARTIFACT_IDENTITY_V0

    search_scope_source: STRUCTURE_*_CONFIG_V0

    resolution_boundary: compilation

    runtime_resolution: fqdn_id_only

  uniqueness:
    fqdn_id:
      rule: strict
      violation: hard_error

    artifact_code:
      rule: relaxed_across_scopes
      violation: allowed

  enforcement:
    - source_artifacts_unchanged
    - discovery_computes_fqdn
    - compilation_resolves_references
    - runtime_uses_fqdn_only
    - no_fallback_resolution
    - bootstrap_exception_only_for_structure

output_configuration:
  _type: metadata  # This artifact defines identity schema, not output paths
```

---

## Version History

- **V0**: Initial canonical artifact identity definition (2026-03-27)
