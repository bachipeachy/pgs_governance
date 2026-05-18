# ASSERT_CC_CAPABILITY_BINDING_VALID_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CC_CAPABILITY_BINDING_VALID_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CC_CAPABILITY_BINDING_VALID_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cc_capability_binding_valid_v0
  callable: execute
```

## Summary

Validates CC pipeline step capability bindings:
1. Each step has exactly one binding (never zero, never dual)
2. Binding is either `transform` (CT) or `side_effect` (CS)
3. FQDN validation delegated to existing FQDN invariant

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CC artifacts, all pipeline steps

## Handler Behavior

### 1. Validate Step Bindings

For each pipeline step:
- Count `transform` bindings
- Count `side_effect` bindings
- Assert total == 1

Violations:
- Zero bindings: No capability specified
- Dual bindings: Both CT and CS present

### 2. Delegate FQDN Validation

FQDN resolution validated by existing `INVARIANT_FQDN_ONLY_REFERENCES_V0`.

This assertion validates cardinality only (exactly one binding).

### 3. Aggregate Violations

Collect violations across all CC artifacts.

Return result with violation details.

## Error Messages

### Zero Bindings
```
❌ ASSERT_CC_CAPABILITY_BINDING_VALID_V0: Missing capability binding
   CC: CC_EXAMPLE_V0
   Step: validate_input
   Violation: Pipeline step has no capability binding (neither transform nor side_effect)
   Fix: Add either transform (for CT) or side_effect (for CS)
```

### Dual Bindings
```
❌ ASSERT_CC_CAPABILITY_BINDING_VALID_V0: Dual capability binding
   CC: CC_EXAMPLE_V0
   Step: process_and_save
   Transform: CT_PROCESS_V0
   Side Effect: CS_SAVE_V0
   Violation: Pipeline step binds both CT and CS (violates single responsibility)
   Fix: Split into two steps - one for transform, one for side_effect
```

### Invalid Binding Type
```
❌ ASSERT_CC_CAPABILITY_BINDING_VALID_V0: Invalid binding field
   CC: CC_EXAMPLE_V0
   Step: custom_step
   Field: custom_capability
   Violation: Unknown binding field (expected transform or side_effect)
   Fix: Use transform (for CT) or side_effect (for CS)
```

## Rationale

**Single responsibility enforcement**

### Architectural Clarity
- One step = one capability
- No ambiguity about what executes
- Clear execution model

### Foundation for Data Flow
- Phase 5 validates inputs/outputs
- Requires knowing which capability executes
- Single binding = deterministic data flow

### Type Safety Preparation
- CT always pure (outputs deterministic)
- CS may have side effects (outputs + effects)
- Different contracts enforced by binding type

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Capability Binding Validation
