# ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.identity::INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_identity_authority_separation_v0
  callable: execute
```

## Summary

Identity declaration and execution authority must remain orthogonal governance surfaces. This assertion detects conflation from the identity governance side: actor artifacts that carry authority semantics (permissions, workflow eligibility, admissibility rules, execution rights) are a constitutional violation.

## Rule

For every AC_ artifact:
1. `core.attributes` MUST NOT contain fields named to signal permissions, roles, capabilities, or execution rights (e.g., `allowed_workflows`, `permissions`, `roles`, `authorization`, `execution_rights`)
2. The artifact MUST NOT declare admissibility rules, projection visibility constraints, or workflow authorization grants
3. The artifact MUST NOT reference the authority registry, authorization databases, or runtime permission tables
4. Identity attributes (type, email, agent_id, etc.) MUST carry no implicit authority semantics

## Enforcement

- **Artifact Types**: AC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_identity_authority_separation_v0`
- **Paired Invariant**: INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0

## Rationale

This assertion enforces the boundary from the identity governance side. `ASSERT_ACTOR_AUTHORITY_SEPARATION_V0` enforces the same boundary from the authority governance side. Both are required for complete bilateral enforcement of the identity/authority orthogonality law.

This is a Phase 1 stub. Attribute field name detection is implemented in Phase 4.
