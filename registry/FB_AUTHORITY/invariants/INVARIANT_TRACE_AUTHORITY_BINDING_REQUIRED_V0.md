# INVARIANT_TRACE_AUTHORITY_BINDING_REQUIRED_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_TRACE_AUTHORITY_BINDING_REQUIRED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: All execution traces must bind actor identity, workflow FQDN, authority provenance, and admissibility outcome — ungoverned execution has no audit chain
  rule: Execution without complete authority trace binding is ungoverned execution; actor_id, workflow_fqdn, authority_provenance, and admissibility_outcome are required trace fields
  scope:
    - WF
```

## Summary

Authority without trace is not accountable. Non-repudiation requires that every execution can be attributed to an actor, under a specific authority grant, at a specific time, with a recorded admissibility outcome. Authority trace binding is the accountability complement to authority evaluation: it closes the loop between the pre-execution authority decision and the post-execution audit record.

## Rule

For every execution trace:
1. MUST bind `actor_id` — the identity of the actor whose authority was evaluated
2. MUST bind `workflow_fqdn` — the fully qualified workflow that was authorized
3. MUST bind `authority_provenance` — the source, chain, and timestamp of authority that produced the admissibility decision
4. MUST bind `admissibility_outcome` — the resolved admissibility result (admitted / denied)
5. These fields are required, not optional — absent authority trace bindings constitute ungoverned execution

## Enforcement Scope

- **Artifact Types**: WF (trace output)
- **Validation Phase**: ASSERT (compile-time declaration check)
- **Enforced By**: ASSERT_TRACE_AUTHORITY_BINDING_REQUIRED_V0

## Rationale

Ambient authority has no trace. Implicit permissions produce no audit record. This invariant is the accountability complement to the no-ambient-authority rule: not only must authority be explicit, but its exercise must be recorded. The authority trace binding transforms authority governance from a pre-execution gate into a complete, deterministic accountability chain spanning execution and post-execution.

Full authority trace binding enforcement is implemented in Phase 5.
