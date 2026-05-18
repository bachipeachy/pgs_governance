# ASSERT_TOPOLOGY_SURFACE_CANONICAL_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_SURFACE_CANONICAL_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_SURFACE_CANONICAL_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_surface_canonical_v0
  callable: execute
```

## Summary

Every CC pipeline step whose capability is governed by a SURFACE_CONTRACT must declare
a `result_surface` that exactly matches the contract's `canonical_surface`. The step is
matched to a contract by `{capability_id, op}` (exact match first) or by
`{capability_id_prefix, op}` (prefix match fallback). Steps whose capability has no
governing contract are silently skipped.

Steps with `on_ct_result` remapping are also skipped: such steps explicitly remap CT
native result codes to CC-level domain codes, so their `result_surface` represents
post-remapping domain semantics, not the CT's canonical surface.

## Rule

For every CC execution topology step where a SURFACE_CONTRACT governs the step's
`{capability_id, op}`:
1. The step MUST declare `result_surface`
2. The declared `result_surface` MUST exactly equal `canonical_surface` from the contract
3. Additional codes not in canonical_surface are violations
4. Missing codes that are in canonical_surface are violations

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_surface_canonical_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_SURFACE_CANONICAL_V0

## Rationale

SURFACE_CANONICAL is the semantic complement to ROUTING_COMPLETE. ROUTING_COMPLETE asks:
"is every declared surface code routed?" SURFACE_CANONICAL asks: "is the declared surface
semantically correct for this capability?" Together they provide complete topology governance:
structural correctness (routing) + semantic legitimacy (canonical surface).

Enforced at compile time: validates each step's `result_surface` against `canonical_surface` declared in SURFACE_CONTRACT artifacts.
