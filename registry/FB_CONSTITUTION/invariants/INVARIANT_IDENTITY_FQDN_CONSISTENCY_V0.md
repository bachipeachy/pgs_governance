# INVARIANT_IDENTITY_FQDN_CONSISTENCY_V0

## Machine

```yaml
invariant_code: INVARIANT_IDENTITY_FQDN_CONSISTENCY_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Artifact FQDN must match namespace and artifact_code consistently.

    FQDN format: {namespace}::{artifact_code}

    This ensures identity resolution is deterministic and unambiguous.

  enforcement_stage:
    - compiler_discovery
    - compiler_validation

  scope:
    - ALL_ARTIFACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - fqdn_namespace_mismatch: "FQDN namespace doesn't match artifact's actual namespace"
    - fqdn_code_mismatch: "FQDN artifact_code doesn't match artifact's declared code"
    - malformed_fqdn: "FQDN doesn't follow {namespace}::{code} pattern"

  clarification:
    deterministic_identity: >
      Every artifact has exactly one FQDN.
      FQDN is derived from namespace + artifact_code (never manually set).
      Resolution must be unambiguous and reproducible.

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  handler: pgs_governance.registry.handlers.assert_identity_fqdn_consistency
  enforcement:
    phase: validation
    order: 5
    failure_mode: HARD_FAIL
    scope: ALL_ARTIFACTS
```

---

## Purpose

Ensure artifact identity (FQDN) is consistent with namespace and artifact_code.

**Core Principle**: Identity derives from structure, never invented.

---

## Validation Rules

### Rule 1: FQDN Structure

FQDN must follow pattern: `{namespace}::{artifact_code}`

**Violation**:
```yaml
# ❌ WRONG
namespace: capability_transforms
artifact_code: CT_PURE_VALIDATE_V0
fqdn_id: transforms::CT_PURE_VALIDATE_V0  # Namespace mismatch!
```

**Correct**:
```yaml
# ✅ CORRECT
namespace: capability_transforms
artifact_code: CT_PURE_VALIDATE_V0
fqdn_id: capability_transforms::CT_PURE_VALIDATE_V0
```

### Rule 2: Namespace Consistency

FQDN namespace part must match artifact's actual namespace.

**Detection**:
```python
namespace, code = fqdn_id.split("::")
assert namespace == artifact["namespace"]
```

### Rule 3: Code Consistency

FQDN code part must match artifact's declared artifact_code.

**Detection**:
```python
namespace, code = fqdn_id.split("::")
assert code == artifact["artifact_code"]
```

---

## Scope

**Applies to**: All artifacts (CT, CS, WF, IN, CC, EV, RB, STRUCTURE, etc.)

**Does NOT validate**:
- Namespace validity (different concern)
- Artifact code naming conventions (different concern)
- FQDN uniqueness (different concern)

---

## Rationale

### Identity Integrity

**Problem without consistency**:
- Artifact declares `CT_FOO_V0` but FQDN says `CT_BAR_V0`
- Resolution fails or resolves wrong artifact
- Debugging becomes impossible

**Solution with consistency**:
- FQDN deterministically derived from namespace + code
- Resolution always unambiguous
- Identity matches reality

### Build-Time Detection

FQDN inconsistency is structural defect, must be caught during discovery/parsing.

**Validation order**:
1. Discovery: Parse artifact, extract namespace, artifact_code
2. Validation: Verify FQDN matches namespace::artifact_code
3. Materialization: Write artifact with validated FQDN

---

## Implementation Note

**FQDN is derived, not authored**:

```python
# Compiler/discovery phase
artifact_code = frontmatter["artifact_code"]
namespace = derive_namespace(source_path, layer)

# FQDN is constructed (not read from file)
fqdn_id = f"{namespace}::{artifact_code}"

# Validation: If FQDN was manually set in file, verify it matches
if "fqdn_id" in frontmatter:
    assert frontmatter["fqdn_id"] == fqdn_id, "FQDN inconsistency"
```

---

## Version History

- **V0**: Initial implementation (2026-04-12) - Identity Consistency Enforcement
