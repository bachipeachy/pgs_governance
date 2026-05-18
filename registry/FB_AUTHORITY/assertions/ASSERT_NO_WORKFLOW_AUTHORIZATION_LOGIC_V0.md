# ASSERT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

implementation:
  module: pgs_governance.registry.handlers.assert_no_workflow_authorization_logic_v0
  callable: execute
```

## Summary

Authorization logic embedded inside execution artifacts is a constitutional violation. Workflows, capability contracts, transforms, and side effects must assume admissibility has already succeeded. They may not inspect roles, check permissions, branch on authority semantics, or perform any authorization evaluation.

## Rule

For every WF_, CC_, CT_, and CS_ artifact:
1. The artifact MUST NOT contain fields or declarations that perform role checks (e.g., `if actor == "admin"`, `required_role`, `permission_check`)
2. The artifact MUST NOT declare inline ACL logic, permission gates, or authorization branching
3. The artifact MUST NOT reference authorization databases, permission tables, or runtime role resolution
4. Authorization semantics belong exclusively to the authority governance plane — not inside execution

## Enforcement

- **Artifact Types**: WF, CC, CT, CS
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_no_workflow_authorization_logic_v0`
- **Paired Invariant**: INVARIANT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

## Rationale

This is one of the highest-value assertions in authority governance. Authorization logic inside execution artifacts is the most common form of authority/execution conflation. Once introduced, it grows: role checks proliferate, permission branching creates undeclared topology variation, and authority semantics become embedded in domain logic.

The architectural remedy is constitutional: detect authorization logic at compile time and prevent it from entering the artifact surface. Execution assumes admissibility. It does not perform admissibility.

This is a Phase 1 stub. Pattern-matching for authorization field names and inline permission logic is implemented in Phase 4.
