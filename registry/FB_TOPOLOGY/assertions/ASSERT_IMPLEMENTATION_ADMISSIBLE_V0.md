# ASSERT_IMPLEMENTATION_ADMISSIBLE_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_IMPLEMENTATION_ADMISSIBLE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_IMPLEMENTATION_ADMISSIBLE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_implementation_admissible_v0
  callable: execute
```

## Summary

Validates that all executable capability artifacts have structurally complete implementation declarations. CT atoms must declare `machine.implementation` with non-empty `module` and `callable`. CS artifacts must declare `implementation` with non-empty `module` and `callable`. CT molecules are exempt (they compose atoms via `atom_stream`).

## Enforcement

- **Phase**: 4 (GOVERN)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CT (atom only) and CS artifacts

## Handler Behavior

### Context Relay Pattern

The compiler pre-computes implementation admissibility analysis for all CT atom and CS nodes and provides it as `compilation_context["implementation_admissibility"]`.

The handler:
1. Reads pre-computed analysis from compilation context
2. Iterates CT and CS artifacts, looks up per-FQDN result
3. Translates structural violations to standardized governance violations

### CT Molecule Exemption

CT molecules (`ct_kind: molecule`) do NOT require implementation declarations. They compose atoms via `atom_stream`, and the atoms provide the execution specification.

## Error Messages

### Missing Implementation (CT Atom)
```
ASSERT_IMPLEMENTATION_ADMISSIBLE_V0: atom CT missing implementation
   CT: capability_transforms::CT_EXAMPLE_V0
   Violation: atom CT must declare machine.implementation
   Fix: Add machine.implementation with module and callable
```

### Empty Module/Callable (CT Atom)
```
ASSERT_IMPLEMENTATION_ADMISSIBLE_V0: atom CT implementation incomplete
   CT: capability_transforms::CT_EXAMPLE_V0
   Violation: atom CT machine.implementation.module or callable is empty
   Fix: Provide non-empty module and callable in machine.implementation
```

### Missing Implementation (CS)
```
ASSERT_IMPLEMENTATION_ADMISSIBLE_V0: CS missing implementation
   CS: capability_side_effects::CS_EXAMPLE_V0
   Violation: CS must declare implementation
   Fix: Add implementation with module and callable
```

### Empty Module/Callable (CS)
```
ASSERT_IMPLEMENTATION_ADMISSIBLE_V0: CS implementation incomplete
   CS: capability_side_effects::CS_EXAMPLE_V0
   Violation: CS implementation.module or callable is empty
   Fix: Provide non-empty module and callable in implementation
```

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN CT/CS validation
