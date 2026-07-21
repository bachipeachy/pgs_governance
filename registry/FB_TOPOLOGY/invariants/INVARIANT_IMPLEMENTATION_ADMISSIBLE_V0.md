# INVARIANT_IMPLEMENTATION_ADMISSIBLE_V0

## Machine

```yaml
invariant_code: INVARIANT_IMPLEMENTATION_ADMISSIBLE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    All capability artifacts (CT atoms and CS side effects) must declare
    structurally complete implementation specifications. An atom CT must
    have machine.implementation with non-empty module and callable. A CS
    must have implementation with non-empty module and callable. Without
    these declarations, the runtime binding surface is incomplete and
    execution cannot be resolved.

  enforcement_stage:
    - compiler_validation

  scope:
    - CAPABILITY_TRANSFORMS
    - CAPABILITY_SIDE_EFFECTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_implementation: "CT atom or CS with no implementation block"
    - empty_module: "Implementation declared but module field empty"
    - empty_callable: "Implementation declared but callable field empty"

  clarification:
    ct_molecule_exemption: >
      CT molecules (ct_kind: molecule) do NOT require direct implementation
      declarations — they compose atoms, and the atom_stream provides the
      execution specification. Only ct_kind: atom requires implementation.
    cs_always_required: >
      All CS artifacts require implementation declarations. CS artifacts
      interact with external state and must always have concrete handlers.
```

---

## Purpose

Ensure every executable capability artifact has a structurally complete implementation declaration. This is the compile-time guarantee that the runtime binding surface can resolve all execution targets.

**Core Principle**: Implementation admissibility is a compile-time invariant, not a runtime discovery.

---

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN hardcoded CT/CS validation
