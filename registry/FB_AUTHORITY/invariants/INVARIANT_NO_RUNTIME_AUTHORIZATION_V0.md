# INVARIANT_NO_RUNTIME_AUTHORIZATION_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_NO_RUNTIME_AUTHORIZATION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: The runtime must never perform authorization evaluation; it consumes resolved authority state only
  rule: Runtime must consume pre-resolved authority state; dynamic authorization, role inference, policy evaluation, and permission negotiation at runtime are constitutional violations
  scope:
    - WF
    - CC
    - CT
    - CS
```

## Summary

Runtime dumbness is a core PGS architectural principle. The runtime is a graph traversal engine — it executes what is declared, without interpretation. This invariant extends that principle to authority: the runtime must never perform authorization evaluation. Authority is resolved before execution begins. The runtime reads the resolved state; it does not participate in producing it.

## Rule

For every runtime interaction with authority state:
1. The runtime MUST NOT evaluate permissions, resolve roles, or execute authorization logic
2. The runtime MUST NOT query authorization databases at execution time
3. The runtime MUST NOT negotiate permissions with external systems during execution
4. Authority state MUST be fully resolved before the runtime receives it
5. The runtime treats authority state as immutable input — not as a source to be re-evaluated

## Enforcement Scope

- **Artifact Types**: WF, CC, CT, CS (runtime boundary)
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_NO_RUNTIME_AUTHORIZATION_V0

## Rationale

If the runtime evaluates authorization, it becomes a policy engine. Policy engines are not graph traversal engines. They are dynamic, stateful, non-deterministic, and difficult to audit. PGS explicitly forbids this evolution. The authority state envelope is the output of pre-execution authority evaluation — the runtime consumes it without contributing to it.
