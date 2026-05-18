# INVARIANT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: Authorization semantics belong exclusively to the authority boundary; execution artifacts must not contain authorization logic
  rule: WF, CC, CT, CS artifacts must assume admissibility has succeeded; authorization logic, role checks, and permission branching inside execution artifacts are a constitutional violation
  scope:
    - WF
    - CC
    - CT
    - CS
```

## Summary

The boundary between authority governance and execution governance is inviolable. Authority evaluation happens before the Intent gate. Once execution traversal begins, authority is settled — the runtime consumes resolved authority state. It does not evaluate authority. Execution artifacts that contain authorization logic violate this invariant by extending the authority plane into the execution plane.

## Rule

For every WF_, CC_, CT_, and CS_ artifact:
1. Authorization logic, role checks, and permission branching MUST NOT appear in execution artifacts
2. The authority evaluation MUST be completed before IN (intent) is reached
3. Execution MAY consume authority state but MUST NOT evaluate, re-evaluate, or re-interpret it
4. Execution topology MUST NOT vary based on authority state after admissibility succeeds

## Enforcement Scope

- **Artifact Types**: WF, CC, CT, CS
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

## Rationale

When authorization logic creeps into execution artifacts, two things happen: the authority plane becomes distributed and inconsistent (different parts of the execution graph can grant different permissions), and the execution plane becomes non-deterministic (topology varies based on authority evaluation outcomes). Both are catastrophic. This invariant enforces the boundary: authorization logic belongs to the authority boundary, not to workflow execution.
