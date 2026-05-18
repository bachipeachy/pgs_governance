# INVARIANT_AUTHORITY_STATE_WELL_FORMED_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_AUTHORITY_STATE_WELL_FORMED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: Authority state crossing the execution boundary must be structurally well-formed; malformed authority state is inadmissible
  rule: Authority state must satisfy SCHEMA_AUTHENTICATED_AUTHORITY_STATE_V0; absent, partial, or structurally invalid authority state may not cross the execution boundary
  scope:
    - WF
```

## Summary

This invariant governs the **structural validity** of authority state at the execution boundary — a distinct concern from runtime authorization behavior (`INVARIANT_NO_RUNTIME_AUTHORIZATION_V0`). An authority state that is structurally valid satisfies the schema: all required fields present, execution authority declared, observation authority declared, provenance recorded. Structural validity is a pre-condition for admissibility evaluation.

Malformed authority state is distinct from absent authority state, but both are inadmissible. Partial state that satisfies some schema fields but not others forces the runtime to infer defaults — which is ambient authority by another name.

## Rule

For every authority state presented at the execution boundary:
1. MUST satisfy `SCHEMA_AUTHENTICATED_AUTHORITY_STATE_V0` — all required fields present and typed
2. `execution_authority.authorized_workflows` MUST be a non-empty explicit list
3. `observation_authority` MUST be structurally present — observation scope is not inferred
4. `authority_provenance` MUST be structurally present — ungoverned authority has no provenance
5. Structural validity is a necessary but not sufficient condition for admissibility

## Enforcement Scope

- **Artifact Types**: WF (authority boundary declarations)
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_AUTHORITY_STATE_WELL_FORMED_V0

## Rationale

Structural validity is the most concrete and checkable form of authority governance. Schema conformance can be verified at compile time without executing any authorization logic. This invariant makes structural conformance mandatory at the boundary: authority state that does not satisfy the schema cannot compile, and therefore cannot be presented to the runtime.

This is distinct from `INVARIANT_NO_RUNTIME_AUTHORIZATION_V0`, which governs runtime behavior. This invariant governs shape. Both are required.
