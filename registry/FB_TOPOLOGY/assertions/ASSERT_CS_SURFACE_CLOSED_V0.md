# ASSERT_CS_SURFACE_CLOSED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CS_SURFACE_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CS_SURFACE_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cs_surface_closed_v0
  callable: execute

allowed_capability_side_effects:
  - capability_side_effects::CS_APPENDONLY_JSONL_V0
  - capability_side_effects::CS_MUTABLE_JSON_V0
  - capability_side_effects::CS_REGISTRY_V0
  - capability_side_effects::CS_SEND_EMAIL_V0
  - capability_side_effects::CS_WORKFLOW_GATEWAY_V0
  - pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0
```

## Summary

Validates that all executable capability side effects are explicitly declared and all declared CS have runtime implementations.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CS artifacts

## Closure Definition

```
Declared_CS_set == Executable_CS_set

No more, no less.
```

## Handler Behavior

The assertion validates two invariants:

### 1. No Undeclared CS
**All discovered CS must be in allowed list**

Scans compiled artifacts for CS artifacts and verifies each CS FQDN is in `allowed_capability_side_effects`.

Violation: CS exists in registry but not declared in allowed list.

### 2. No Missing Implementations
**All declared CS must have runtime implementation**

For each CS in `allowed_capability_side_effects`, verifies runtime implementation exists at expected path:

```
CS_X_V0 → pgs_side_effects/implementation/side_effects/.../CS_X_V0/runtime.py
```

Violation: CS declared but runtime implementation missing.

## Error Messages

### Undeclared CS
```
❌ ASSERT_CS_SURFACE_CLOSED_V0: Undeclared CS detected
   FQDN: capability_side_effects::CS_UNDECLARED_V0
   Location: pgs_side_effects/registry/capability_side_effects/CS_UNDECLARED_V0.md
   Violation: CS exists in registry but not in allowed list
   Fix: Add to allowed_capability_side_effects in ASSERT_CS_SURFACE_CLOSED_V0
```

### Missing Implementation
```
❌ ASSERT_CS_SURFACE_CLOSED_V0: Missing runtime implementation
   FQDN: capability_side_effects::CS_DECLARED_V0
   Expected: pgs_side_effects/implementation/side_effects/.../CS_DECLARED_V0/runtime.py
   Violation: CS declared in allowed list but runtime missing
   Fix: Implement runtime or remove from allowed list
```

### Excess Declaration
```
❌ ASSERT_CS_SURFACE_CLOSED_V0: Declared CS not found
   FQDN: capability_side_effects::CS_REMOVED_V0
   Violation: CS in allowed list but not discovered during compilation
   Fix: Remove from allowed_capability_side_effects (CS no longer exists)
```

## Rationale

**Closed CS surface = bounded, auditable system behavior**

### Security Model
- Finite enumeration of all side effects
- No dynamic CS discovery at runtime
- Audit surface is explicit and complete

### Architectural Purity
- Code executes only declared behavior
- No heuristic resolution, no fallbacks
- System behavior = declared protocol

### Operational Clarity
"What can this system do?" → Read one file

## Version History

- **V0**: Initial implementation (2026-04-05) - CS Surface Closure enforcement
