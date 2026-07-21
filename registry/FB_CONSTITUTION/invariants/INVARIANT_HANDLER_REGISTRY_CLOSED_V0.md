# INVARIANT_HANDLER_REGISTRY_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_HANDLER_REGISTRY_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_COMPILER_V0

core:
  description: >
    Every ASSERT artifact present in the compiled artifact set MUST have its
    implementation handler registered in the static HANDLER_REGISTRY before the
    ASSERT phase executes. No ASSERT artifact may reference an unregistered handler.
    The registry is the sole authority for handler resolution — no dynamic discovery
    is permitted.

  enforcement_stage:
    - compiler_assert

  scope:
    - ALL_BUILD_CONTEXTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - unregistered_handler: "ASSERT artifact declares implementation.module not present in HANDLER_REGISTRY"
    - dynamic_resolution: "Handler resolved at runtime via importlib or filesystem discovery"
    - partial_registry: "Registry populated incrementally during assert phase execution"
```

---

## Purpose

Ensures the ASSERT phase is fully closed before it begins: every declared assertion
must have a registered implementation. An unregistered handler is a compiler
conformance violation — the build cannot proceed with incomplete enforcement surface.

This invariant makes the handler registry itself a governed, auditable artifact.
Any implementation that allows unregistered handlers to silently pass violates the
closed-world assumption that PGS compilation depends on.

## Relationship to CONSTITUTION_COMPILER_V0

Directly enforces `COMPILER_SURFACE_CLOSURE` (all references resolved at compile time)
and `COMPILER_NO_PARTIAL_RESOLUTION` (symbol resolution is all-or-nothing) as applied
to the ASSERT phase's handler surface.
