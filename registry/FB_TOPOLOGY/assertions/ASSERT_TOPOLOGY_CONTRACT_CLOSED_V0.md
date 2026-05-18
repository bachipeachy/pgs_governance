# ASSERT_TOPOLOGY_CONTRACT_CLOSED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_CONTRACT_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_contract_closed_v0
  callable: execute
```

## Summary

The union of all status codes that can exit a CC execution topology must exactly match
`result_status_contract.allowed`. An uncontracted exit is an undeclared outcome. An
unreachable contract code is an overclaimed outcome. Both are compile-time violations.

## Rule

For every CC execution topology:

1. **No uncontracted exits**: every code reachable as a CC exit MUST appear in
   `result_status_contract.allowed`
2. **No unreachable contract codes**: every code in `result_status_contract.allowed` MUST
   be reachable as a CC exit
3. Exit reachability includes: step `exit` routes (when code is in step `result_surface`),
   last-step `continue` routes, and evaluation `on_true`/`on_false` outcomes
4. `continue` in non-last steps is in-pipeline routing — does not exit the CC

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_contract_closed_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0

## Rationale

CONTRACT_CLOSED operates at CC scope. It aggregates exit surfaces across all steps and
evaluation blocks to compute the full set of codes that can exit the CC. It then compares
this against the declared contract. Both directions of mismatch (uncontracted exits,
unreachable codes) are violations — the contract is only valid when it matches reality exactly.

This is a Phase 3 assertion — it requires the full compiled pipeline with `result_surface`
fields populated on every step.
