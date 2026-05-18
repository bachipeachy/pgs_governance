# ASSERT_TOPOLOGY_ROUTING_COMPLETE_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_ROUTING_COMPLETE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_routing_complete_v0
  callable: execute
```

## Summary

The `on_result` map of every execution topology step must cover all status codes declared
in that step's `result_surface`. An unrouted surface code is an ungoverned execution path
— the runtime has no declared action for a result that step's capability can actually produce.

Validation is step-local: each step's `on_result` is validated against that step's own
`result_surface`, not against the CC-level `result_status_contract.allowed`.

## Rule

For every CC execution topology step:
1. Every step MUST have a `result_surface` field — the set of codes that step's capability can produce
2. `on_result` MUST contain an entry for every code in that step's `result_surface`
3. Each routing value MUST be `continue`, `exit`, or an evaluation target name
4. Unknown status codes in `on_result` (not in step's `result_surface`) are governance noise violations
5. `on_result` is a finite map — no expressions or conditional logic

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_routing_complete_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0

## Rationale

Routing completeness guarantees that every possible execution outcome for a step has a
declared path. This is the topology equivalent of exhaustive pattern matching at step scope.
No result falls through to an undefined state. The compiler can verify this statically.

Step-local validation against `result_surface` is architecturally correct. Different
capabilities produce different result sets. ROUTING_COMPLETE governs step routing coverage.
CC-level contract closure (ensuring the union of exits matches the CC contract) is
governed by ASSERT_TOPOLOGY_CONTRACT_CLOSED_V0.

Enforced at compile time: validates that `on_result` covers all codes in `result_surface` and vice versa.
