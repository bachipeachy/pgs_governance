# ASSERT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_authority_required_for_execution_v0
  callable: execute
```

## Summary

Execution authority is not optional. Every workflow that may be invoked by an actor must declare an authority requirement. Workflows without authority declarations represent ungoverned execution entry points — a constitutional violation of the authority governance plane.

## Rule

For every WF_ artifact:
1. The artifact MUST reference an authority requirement (via `governed_authority` or equivalent authority binding field)
2. The absence of an authority declaration is a compile-time violation
3. Placeholders, inline authority logic, and self-authorization patterns are all violations

## Enforcement

- **Artifact Types**: WF
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_authority_required_for_execution_v0`
- **Paired Invariant**: INVARIANT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

## Rationale

If execution can begin without an authority declaration, the authority governance plane is bypassed. This assertion closes that gap at compile time: workflows that do not declare authority requirements cannot compile, and therefore cannot be invoked.

This is a Phase 1 stub. Full enforcement against authority boundary resolution is implemented in Phase 4.
