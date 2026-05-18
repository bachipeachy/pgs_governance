# ASSERT_TRACE_AUTHORITY_BINDING_REQUIRED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TRACE_AUTHORITY_BINDING_REQUIRED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_TRACE_AUTHORITY_BINDING_REQUIRED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_trace_authority_binding_required_v0
  callable: execute
```

## Summary

All execution traces must bind authority provenance. This assertion enforces the accountability complement of authority governance: not only must authority be evaluated before execution, but its exercise must be recorded in the trace. Authority without a trace binding is ungoverned authority — it happened, but there is no audit record.

## Rule

For every execution trace declaration:
1. MUST declare a binding for `actor_id` — the identity of the actor whose authority was evaluated
2. MUST declare a binding for `workflow_fqdn` — the fully qualified workflow that was authorized
3. MUST declare a binding for `authority_provenance` — the source, chain, and evaluation timestamp of authority
4. MUST declare a binding for `admissibility_outcome` — the resolved admissibility result
5. These bindings are required, not optional — absent authority trace bindings constitute ungoverned execution

## Enforcement

- **Artifact Types**: WF (trace output declarations)
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_trace_authority_binding_required_v0`
- **Paired Invariant**: INVARIANT_TRACE_AUTHORITY_BINDING_REQUIRED_V0

## Rationale

Trace authority binding is a governance surface distinct from no-ambient-authority. Ambient authority governs what is declared before execution. Trace binding governs what is recorded after execution. You can have explicit authority declarations with incomplete trace records (provenance surface violation), or complete trace records that masked ambient authority (admissibility surface violation). Both must be independently enforced.

Full trace binding enforcement is implemented in Phase 5.
