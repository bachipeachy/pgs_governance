# INVARIANT_TOPOLOGY_SURFACE_CANONICAL_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_SURFACE_CANONICAL_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: every step's result_surface must match the canonical surface declared by the governing SURFACE_CONTRACT for that step's capability and operation
  rule: For every CC pipeline step whose capability (transform or side_effect) is governed by a SURFACE_CONTRACT artifact, the step's declared result_surface MUST exactly equal the canonical_surface declared in that contract; additions, omissions, aliases, and substitutions are constitutional violations
  scope:
    - CC

```

---

## Summary

A step's `result_surface` declares what result codes its capability can produce. The
SURFACE_CONTRACT for that capability declares what result codes that capability MUST produce —
no more, no fewer. When a contract exists for a `{capability_id, op}` pair, the step's
`result_surface` must be an exact match.

This invariant separates two distinct governance concerns:

- **ROUTING_COMPLETE** — structural: does the step route every code it declares?
- **SURFACE_CANONICAL** — semantic: does the step declare the correct codes for its capability?

A step can be routing-complete and still be wrong: if it declares `[SUCCESS, VIOLATION]` for a
registry REGISTER operation, every code is routed but ALREADY_EXISTS and BACKEND_ERROR are
missing. SURFACE_CANONICAL catches this.

## Rule

For every CC pipeline step where a SURFACE_CONTRACT governs the step's capability and op:
1. The step MUST declare `result_surface`
2. The declared `result_surface` MUST exactly equal the contract's `canonical_surface`
3. Extra codes (additions) are violations — they claim the capability can produce codes it cannot
4. Missing codes (omissions) are violations — they hide reachable outcomes from routing
5. Aliased codes (e.g. `FAILED` instead of `BACKEND_ERROR`) are violations — they invent private semantics

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_SURFACE_CANONICAL_V0

## Doctrine

Workflow authors MAY route surfaces. Workflow authors MAY NOT define capability semantics.

The canonical surface of a capability is governed by protocol, not by the CC author. A CC
author who changes a step's result_surface relative to its canonical contract is not routing
— they are redefining what the capability produces. That authority belongs to the capability
family's surface contract, not to the CC.

## Rationale

Without canonical surface governance, result_surface becomes author-defined. Two CCs binding
the same registry capability could declare different surfaces. One says ALREADY_EXISTS is
reachable; another omits it. Both can pass ROUTING_COMPLETE. Neither is provably correct.
The runtime cannot make guarantees about reachability.

SURFACE_CANONICAL closes this gap. When the canonical surface is declared once in a
SURFACE_CONTRACT and enforced across all CCs that bind that capability, the result_surface
field stops being a claim and becomes a verified fact.

Full enforcement is implemented in Phase 3.
