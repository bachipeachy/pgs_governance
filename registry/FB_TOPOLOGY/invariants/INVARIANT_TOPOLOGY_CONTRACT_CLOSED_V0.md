# INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: the union of all codes that can exit a CC execution topology must exactly match result_status_contract.allowed; uncontracted exits and unreachable contract codes are compile-time violations
  rule: For every CC, the set of status codes that can actually exit the topology (via step exit routes, last-step continue routes, and evaluation outcomes) must equal exactly the set declared in result_status_contract.allowed — no uncontracted exits, no unreachable contract codes
  scope:
    - CC

```

---

## Summary

The CC-level result status contract is a promise to callers about what outcomes this CC can
produce. That promise is only valid if the execution topology can actually deliver every
declared outcome, and cannot deliver any undeclared one.

CONTRACT_CLOSED verifies that the topology fulfills the contract — not just that routing is
locally complete per step (ROUTING_COMPLETE), but that the full CC exit surface matches the
declared contract exactly.

## Rule

For every CC:

1. **No uncontracted exits**: every status code that can exit the CC topology (via `exit`,
   last-step `continue`, or evaluation `on_true`/`on_false`) MUST appear in
   `result_status_contract.allowed`
2. **No unreachable contract codes**: every code in `result_status_contract.allowed` MUST
   be reachable as a CC exit — there MUST exist at least one execution path that exits
   with that code
3. The contract is closed when `reachable_exits == allowed` exactly

## Exit Reachability

A status code is reachable as a CC exit when ANY of the following hold:

- A step routes that code as `exit` in `on_result` (and the code is in the step's `result_surface`)
- The LAST step in the pipeline routes that code as `continue` (last-step `continue` exits the CC)
- An `evaluation` block's `on_true` or `on_false` names that code as the evaluation outcome

Codes routed as `continue` in non-last steps remain in-pipeline — they do not exit the CC.
Codes routed to an evaluation target (e.g., `SUCCESS: evaluate_cap`) exit via evaluation
outcome — the evaluation's `on_true`/`on_false` codes are the actual exits.

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_CONTRACT_CLOSED_V0

## Relationship to ROUTING_COMPLETE

ROUTING_COMPLETE and CONTRACT_CLOSED are complementary, not redundant:

- **ROUTING_COMPLETE** (step-local): every code in a step's `result_surface` must have a
  routing declaration in that step's `on_result`. Scope: individual step.
- **CONTRACT_CLOSED** (CC-level): the union of all CC exits must equal `result_status_contract.allowed`.
  Scope: full CC topology.

ROUTING_COMPLETE ensures no step has a declared surface code without a routing decision.
CONTRACT_CLOSED ensures the full topology's exit surface matches the CC contract.

## Rationale

A CC's `result_status_contract.allowed` is a governance contract. Callers of the CC —
workflow nodes, orchestration logic, integration tests — rely on it to declare what outcomes
to handle. If a code can exit the topology but is not in the contract, callers cannot handle
it. If a code is in the contract but no path exits with it, the contract is overclaiming
and callers are writing dead routing branches.

Contract closure is the CC-level equivalent of exhaustive match. It cannot be inferred by
reading individual steps — it requires aggregating all exit paths across the full topology.
