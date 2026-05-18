# ASSERT_NO_AMBIENT_AUTHORITY_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_NO_AMBIENT_AUTHORITY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_NO_AMBIENT_AUTHORITY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_no_ambient_authority_v0
  callable: execute
```

## Summary

Ambient authority arises when authority is assumed rather than declared — implicit admin state, default permissions, catch-all roles, or authority inferred from actor type. All of these are constitutional violations. Authority must be explicit: every actor, every workflow, every execution right must be declared and resolvable from governed artifacts.

## Rule

For every execution artifact and authority declaration:
1. MUST NOT rely on implicit permissions, default authority grants, or assumed execution rights
2. MUST NOT infer authority from actor type, actor attributes, or structural position
3. MUST NOT use wildcard authority grants (e.g., `allowed_workflows: "*"`)
4. MUST NOT use catch-all roles that implicitly grant execution rights
5. All authority references MUST resolve to explicit entries in the governed authority database
6. Authority not explicitly granted is implicitly denied

## Enforcement

- **Artifact Types**: WF, CC, CT, CS
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_no_ambient_authority_v0`
- **Paired Invariant**: INVARIANT_NO_AMBIENT_AUTHORITY_V0

## Rationale

Ambient authority is the root cause of privilege escalation at the architectural level. When authority is inferred from context rather than declared explicitly, the system has no way to audit what was authorized, by whom, and why. Every implicit permission is a gap in the non-repudiation chain.

The PGS authority model is: authority not granted is denied. Explicit grants only. No wildcards. No inference. No ambient state. This assertion enforces that constraint at compile time.

This is a Phase 1 stub. Wildcard detection and implicit grant analysis are implemented in Phase 3.
