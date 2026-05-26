# ASSERT_BINDING_INTEGRITY_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_BINDING_INTEGRITY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_BINDING_INTEGRITY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_binding_integrity_v0
  callable: execute
```

## Summary

Validates that all RB (Runtime Binding) artifacts declare bindings only via FQDNs that resolve to existing artifacts in the compiled graph. Reads pre-computed binding analysis from the compiler.

## Enforcement

- **Phase**: 4 (GOVERN)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All RB artifacts

## Handler Behavior

The compiler pre-computes RB binding analysis and provides it as `compilation_context["rb_binding_integrity"]`. The handler translates structural violations to standardized governance violations.

## Error Messages

### Short Name Binding Key
```
ASSERT_BINDING_INTEGRITY_V0: Non-FQDN binding key
   RB: blockchain::RB_EXAMPLE_V0
   Key: CT_GENERATE_ID_V0
   Violation: RB binding key must be FQDN
   Fix: Use fully-qualified name (e.g. capability_transforms::CT_GENERATE_ID_V0)
```

### Dangling Binding
```
ASSERT_BINDING_INTEGRITY_V0: Binding target not found
   RB: blockchain::RB_EXAMPLE_V0
   Key: blockchain::CT_NONEXISTENT_V0
   Violation: RB references non-existent artifact
   Fix: Add artifact or fix binding reference
```

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN
