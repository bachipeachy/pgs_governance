# INVARIANT_FQDN_ONLY_REFERENCES_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_FQDN_ONLY_REFERENCES_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  summary: All artifact references must use FQDN (layer::code), never short names
  rule: All cross-artifact references must use fully qualified domain names in format layer::artifact_code
  scope:
    - CC
    - CT
    - CS
    - WF
    - IN
    - RB
    - STRUCTURE
    - TEST_DATA
```

## Summary

All artifacts must reference other artifacts using fully qualified domain names (FQDN) in the format `layer::artifact_code`. Short names (bare artifact_code) are forbidden.

## Rule

For all artifact types:
1. References to CT must use: `transforms::CT_*_V0`
2. References to CS must use: `side_effects::CS_*_V0`
3. References to CC must use: `governance::CC_*_V0`
4. References to WF must use: `governance::WF_*_V0`
5. References to VOCAB must use: `governance::VOCAB_*_V0`
6. References to STRUCTURE must use: `governance::STRUCTURE_*_V0`
7. NO bare artifact codes (e.g., `CT_HASH_V0` without layer prefix)

## Enforcement Scope

- **Artifact Types**: ALL
- **Validation Phase**: Phase 5 (ASSERT)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID

**CC Pipeline:**
```yaml
pipeline:
  - step: hash_data
    transform: transforms::CT_HASH_DATA_V0  # ✅ FQDN
```

**WF Reference:**
```yaml
structure: registry::STRUCTURE_BUILD_CONFIG_V0  # ✅ FQDN
runtime_binding: registry::RB_BUILD_PLATFORM_V0  # ✅ FQDN
```

**CT governed_by:**
```yaml
governed_by:
  - registry::CC_HASH_DATA_V0  # ✅ FQDN
```

### ❌ INVALID

**Short name:**
```yaml
pipeline:
  - step: hash_data
    transform: CT_HASH_DATA_V0  # ❌ No layer prefix
```

**Partial FQDN:**
```yaml
structure: STRUCTURE_BUILD_CONFIG_V0  # ❌ Missing layer
```

## Rationale

FQDN-only references ensure:
- Unambiguous artifact resolution
- No namespace collisions
- Explicit layer boundaries
- Traceable dependencies
- No implicit search paths

## Detection Strategy

Scan all artifact Machine sections for:
- `governed_by` field values without `::`
- `transform` field values without `::`
- `structure` field values without `::`
- `runtime_binding` field values without `::`
- Any artifact_code reference pattern without layer prefix

## Related Artifacts

- `governance::STRUCTURE_FQDN_TREE_V0` - Defines FQDN format
- `fb.constitution::CONSTITUTION_ARTIFACT_SCHEMA_V0` - Defines reference fields
