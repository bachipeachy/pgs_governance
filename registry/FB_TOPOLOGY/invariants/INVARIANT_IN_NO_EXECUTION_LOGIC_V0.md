# INVARIANT_IN_NO_EXECUTION_LOGIC_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_IN_NO_EXECUTION_LOGIC_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_INTENT_V0

core:
  summary: IN artifacts must not contain execution logic fields
  rule: IN artifacts must not declare execute, callable, implementation, logic, transform, code, or handler fields
  scope:
    - IN
```

## Summary

Intent artifacts are admission gates. They declare the preconditions for workflow entry
and validate incoming payloads. They are not executors. An IN artifact that contains
execution logic fields has violated its constitutional role — execution belongs in CC
and CT artifacts.

## Rule

For every IN artifact, the frontmatter MUST NOT contain any of the following fields
at any nesting level:
- `execute`
- `callable`
- `implementation`
- `logic`
- `transform`
- `code`
- `handler`

## Enforcement Scope

- **Artifact Types**: IN
- **Validation Phase**: ASSERT (Phase 5, compile-time, hard fail)
- **Enforced By**: ASSERT_IN_NO_EXECUTION_LOGIC_V0

## Rationale

If an IN artifact contains execution logic fields, it has begun to absorb responsibilities
that belong in the execution layer. This violates separation of concerns and makes the
intent's role ambiguous. The compiler must reject any IN artifact that declares execution
fields so that this boundary remains crisp.
