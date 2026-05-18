# ASSERT_AUTHORITY_STATE_WELL_FORMED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_AUTHORITY_STATE_WELL_FORMED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_AUTHORITY_STATE_WELL_FORMED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_authority_state_well_formed_v0
  callable: execute
```

## Summary

A well-formed authority state is not merely present — it is structurally complete. An authority state envelope that satisfies the schema is admissible. One that is missing required fields, has absent execution authority, has absent observation authority, or lacks authority provenance is a structural violation. The compiler must reject it.

## Rule

For every authority state declaration:
1. The envelope MUST satisfy `SCHEMA_AUTHENTICATED_AUTHORITY_STATE_V0`: all required fields present and typed
2. `execution_authority.authorized_workflows` MUST be a non-empty explicit list — no wildcards
3. `observation_authority` MUST be declared — observation eligibility is not inferred
4. `authority_provenance` MUST be present — ungoverned authority has no provenance
5. The runtime MUST NOT infer or reconstruct missing authority state fields
6. Authority state MUST be fully resolved at the boundary — not assembled during execution

## Enforcement

- **Artifact Types**: WF (authority boundary declarations)
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_authority_state_well_formed_v0`
- **Paired Invariant**: INVARIANT_AUTHORITY_STATE_WELL_FORMED_V0

## Rationale

"Well-formed" captures the structural requirement precisely: the authority state envelope is either structurally valid according to its schema or it is not. "Complete" would suggest a content completeness check; "well-formed" signals a structural conformance check. The distinction matters: this assertion enforces schema conformance, not domain completeness.

Malformed authority state forces the runtime to fill gaps — either by rejecting execution (correct) or by inferring defaults (ambient authority). This assertion closes that gap at compile time.

This is a Phase 1 stub. Schema validation against SCHEMA_AUTHENTICATED_AUTHORITY_STATE_V0 is implemented in Phase 2.
