# INVARIANT_NO_AMBIENT_AUTHORITY_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_NO_AMBIENT_AUTHORITY_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: All authority must be explicit and fully declared; implicit permissions, default authority, and inferred execution rights are forbidden
  rule: No execution artifact, authority declaration, or schema may rely on implicit permissions, default authority grants, role inference, or undeclared execution rights; authority not explicitly granted is denied
  scope:
    - WF
    - CC
    - CT
    - CS
```

## Summary

Ambient authority arises when authority is assumed rather than declared — implicit admin state, default permissions, catch-all roles, or authority inferred from actor type or context. This invariant closes that class of vulnerability: authority must be explicit at every level. Authority not explicitly granted is denied. There are no defaults, no wildcards, no inferred rights.

This invariant governs **authority declaration completeness** — a distinct concern from `INVARIANT_TRACE_AUTHORITY_BINDING_REQUIRED_V0`, which governs authority provenance recording. You can have explicit declarations without a complete trace record; you can have a trace record without having had explicit declarations. Both invariants are required.

## Rule

For every execution artifact and authority declaration:
1. MUST NOT rely on implicit permissions, default authority grants, or assumed execution rights
2. MUST NOT infer authority from actor type, actor attributes, or structural position
3. MUST NOT use wildcard authority grants (e.g., `allowed_workflows: "*"`)
4. MUST NOT use catch-all roles that implicitly grant execution rights
5. All authority references MUST resolve to explicit entries in the governed authority registry
6. Authority not explicitly granted is implicitly denied — there is no default allow

## Enforcement Scope

- **Artifact Types**: WF, CC, CT, CS
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_NO_AMBIENT_AUTHORITY_V0

## Rationale

Ambient authority is the root cause of privilege escalation at the architectural level. When authority is inferred from context rather than declared explicitly, the system has no way to audit what was authorized, by whom, and why. Every implicit permission is a gap in the admissibility record and the non-repudiation chain.

The PGS authority model is: authority not granted is denied. Explicit grants only. This invariant enforces that constraint structurally.
