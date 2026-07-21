# INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: on_result must declare routing for every status code in the step's result_surface; unrouted surface codes constitute ungoverned execution paths
  rule: The on_result map of every step must contain an entry for every code in that step's result_surface; a status code declared in result_surface but absent from on_result is an unrouted execution path and a compile-time violation
  scope:
    - CC

```

---

## Summary

An unrouted status code is an ungoverned execution path. If a step declares that its
capability may produce `VIOLATION` (via `result_surface`) but its `on_result` has no entry
for `VIOLATION`, the runtime has no declared path — it must guess, default, or crash.
All three outcomes violate deterministic execution topology.

Routing completeness is validated step-locally against `result_surface`, not against the
CC-level `result_status_contract.allowed`. Different steps bind different capabilities with
different reachable outcome sets. A pure transform step cannot produce BACKEND_ERROR; a
registry side-effect step cannot produce custom domain status codes. Forcing every step to
route the full CC contract would require ghost routes for codes the step's capability cannot
produce — governance noise, not governance.

## Rule

For every execution topology step in a CC pipeline:
1. Every step MUST declare a `result_surface` — the set of status codes that step's specific
   capability can actually produce
2. `on_result` MUST contain an entry for every code in that step's `result_surface`
3. Each routing value MUST be exactly one of: `continue`, `exit`, or an evaluation target
   name declared in the CC's `evaluation` block
4. `on_result` MUST NOT contain status codes not declared in that step's `result_surface`
   (unknown routes are governance noise)
5. `on_result` is a finite lookup map — no expressions, no conditions, no dynamic predicates

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_ROUTING_COMPLETE_V0

## Rationale

Routing completeness is the topology equivalent of exhaustive pattern matching. When every
result code in a step's declared surface has a routing outcome, the step is deterministic:
given any result the capability can actually produce, the runtime knows exactly what to do
next. No defaults. No implicit fallbacks. No runtime inference.

Step-local validation against `result_surface` is correct because the capability surface is
per-step, not per-CC. A CC contract declares what the full topology can surface to callers.
A step's `result_surface` declares what that step's specific capability can produce. These
are different scopes. ROUTING_COMPLETE governs the step scope.
CC-level contract closure is governed by INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0.

Full enforcement is implemented in Phase 3.
