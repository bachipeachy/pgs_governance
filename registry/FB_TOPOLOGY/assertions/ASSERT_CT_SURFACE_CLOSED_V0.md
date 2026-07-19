# ASSERT_CT_SURFACE_CLOSED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CT_SURFACE_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CT_SURFACE_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_ct_surface_closed_v0
  callable: execute

scope:
  applies_to:
    - PLATFORM

allowed_capability_transforms:
  - capability_transforms::CT_EXEC_EMIT_V0
  - capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0
  - capability_transforms::CT_PURE_CHECK_QUOTA_AVAILABLE_V0
  - capability_transforms::CT_PURE_CHECK_TRAINING_STATUS_V0
  - capability_transforms::CT_PURE_COMPARE_EQUAL_V0
  - capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
  - capability_transforms::CT_PURE_DERIVE_MASTER_KEY_V0
  - capability_transforms::CT_PURE_ECDSA_SIGN_V0
  - capability_transforms::CT_PURE_ENTROPY_TO_MNEMONIC_V0
  - capability_transforms::CT_PURE_EVALUATE_INACTIVITY_V0
  - capability_transforms::CT_PURE_EXTRACT_V0
  - capability_transforms::CT_PURE_FILTER_RECORDS_V0
  - capability_transforms::CT_PURE_GENERATE_ENTROPY_V0
  - capability_transforms::CT_PURE_GENERATE_ID_V0
  - capability_transforms::CT_PURE_KECCAK256_HASH_V0
  - capability_transforms::CT_PURE_LOOKUP_V0
  - capability_transforms::CT_PURE_MAP_RESULT_TO_HTTP_V0
  - capability_transforms::CT_PURE_MNEMONIC_TO_SEED_V0
  - capability_transforms::CT_PURE_PASSTHROUGH_V0
  - capability_transforms::CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
  - capability_transforms::CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
  - capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0
  - capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
  - capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
```

## Summary

Validates that all executable capability transforms are explicitly declared and all declared CT have runtime implementations.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CT artifacts

## Closure Definition

```
Declared_CT_set == Executable_CT_set

No more, no less.
```

## Handler Behavior

The assertion validates three invariants:

### 1. No Undeclared CT
**All discovered CT must be in allowed list**

Scans compiled artifacts for CT artifacts and verifies each CT FQDN is in `allowed_capability_transforms`.

Violation: CT exists in registry but not declared in allowed list.

### 2. No Missing Implementations
**All declared CT must have runtime implementation**

For each CT in `allowed_capability_transforms`, verifies runtime implementation exists at expected path:

```
CT_X_V0 → pgs_transforms/implementation/transforms/.../ct_x_v0.py
```

Violation: CT declared but runtime implementation missing.

### 3. No Excess Declarations
**All declared CT must be discovered**

Violation: CT in allowed list but not discovered during compilation.

## Error Messages

### Undeclared CT
```
❌ ASSERT_CT_SURFACE_CLOSED_V0: Undeclared CT detected
   FQDN: capability_transforms::CT_UNDECLARED_V0
   Location: pgs_transforms/registry/capability_transforms/CT_UNDECLARED_V0.md
   Violation: CT exists in registry but not in allowed list
   Fix: Add to allowed_capability_transforms in ASSERT_CT_SURFACE_CLOSED_V0
```

### Missing Implementation
```
❌ ASSERT_CT_SURFACE_CLOSED_V0: Missing runtime implementation
   FQDN: capability_transforms::CT_DECLARED_V0
   Expected: pgs_transforms/implementation/transforms/atoms/ct_declared_v0.py
   Violation: CT declared in allowed list but runtime missing
   Fix: Implement runtime or remove from allowed list
```

### Excess Declaration
```
❌ ASSERT_CT_SURFACE_CLOSED_V0: Declared CT not found
   FQDN: capability_transforms::CT_REMOVED_V0
   Violation: CT in allowed list but not discovered during compilation
   Fix: Remove from allowed_capability_transforms (CT no longer exists)
```

## Rationale

**Closed CT surface = bounded, auditable computation**

### Security Model
- Finite enumeration of all transforms
- No dynamic CT discovery at runtime
- Logic surface is explicit and complete

### Architectural Purity
- Code executes only declared computation
- No heuristic resolution, no fallbacks
- System logic = declared protocol

### Operational Clarity
"What can this system compute?" → Read one file

## Version History

- **V0**: Initial implementation (2026-04-05) - CT Surface Closure enforcement
