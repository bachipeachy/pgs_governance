# INVARIANT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: Execution may not proceed without a declared authority boundary requirement
  rule: Every WF_ artifact must declare an authority requirement; ungoverned execution entry points are a constitutional violation
  scope:
    - WF
```

## Summary

The invariant of execution requiring authority is the foundational constraint of the authority governance plane. If a workflow can be invoked without any authority declaration, the entire authority plane is optional rather than sovereign. This invariant makes authority mandatory for all workflows.

## Rule

For every WF_ artifact:
1. The workflow MUST have an associated authority declaration before execution may begin
2. No workflow may be invoked by the runtime without a resolved authority boundary
3. The compiler MUST reject WF_ artifacts that lack authority declarations

## Enforcement Scope

- **Artifact Types**: WF
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

## Rationale

Authority governance determines whether execution may exist. If that determination is optional, authority governance is advisory rather than constitutional. This invariant makes the determination mandatory at the architectural level: no authority declaration, no execution.
