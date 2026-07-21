# INVARIANT_RUNTIME_INVARIANT_WIRED_V0

## Machine

```yaml
invariant_code: INVARIANT_RUNTIME_INVARIANT_WIRED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Every runtime-enforced business invariant must be wired to a real
    enforcement point. A runtime invariant (core.enforcement_stage contains
    "runtime_outcome") is enforced through the existing capability-contract
    outcome-routing mechanism: an enforcing CC emits a non-SUCCESS violation
    outcome which the enforcing workflow routes to a terminal node, and the
    trace is classified as a BUSINESS_VIOLATION. This invariant requires that
    each such declaration is authoritative — bound to a CC that declares the
    violation outcome and a workflow that routes it to the declared terminal —
    so that no runtime invariant is decorative.

  enforcement_stage:
    - compiler_assertion

  scope:
    - TOPOLOGY

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - unbound_invariant: "runtime invariant missing runtime_binding fields"
    - missing_outcome: "enforcing CC does not declare the violation outcome in result_surface"
    - missing_route: "enforcing workflow does not route the violation outcome to the declared terminal node"
    - decorative_governance: "invariant artifact exists but no enforcement point upholds it"

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  scope:
    applies_to:
    - PLATFORM
```

## Summary

Constitutional rule that runtime business invariants must be bound to the
capability-contract outcome-routing mechanism that enforces them. The runtime is
unchanged; this is verified at compile time by `ASSERT_RUNTIME_INVARIANT_WIRED_V0`.

## Version History

- **V0**: Initial runtime-invariant wiring rule (2026-06-14)
