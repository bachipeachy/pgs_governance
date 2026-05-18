# INVARIANT_CS_TRACEABLE_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_CS_TRACEABLE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: Every CS execution must be recorded in the execution trace
  rule: CS executors must emit a trace entry for every side-effect execution
  scope:
    - CS
```

## Summary

Every execution of a Capability Side Effect must leave an observable record in the execution
trace. Traceability is what makes the system auditable, replayable, and debuggable. A CS
execution that does not appear in the trace is an invisible side effect — a constitutional
violation.

## Rule

For every CS artifact execution:
1. The executor MUST emit a trace entry recording the CS invocation
2. The trace entry MUST include the CS code, inputs, output result, and timestamp

This invariant is enforced at runtime by the execution engine. Compile-time static
analysis cannot verify executor behavior.

## Enforcement Scope

- **Artifact Types**: CS
- **Validation Phase**: Runtime (execution engine)
- **Compile-Time**: ASSERT_CS_TRACEABLE_V0 (parity stub — runtime enforcement)
- **Enforced By**: ASSERT_CS_TRACEABLE_V0

## Rationale

Without traceability, the system cannot provide a complete audit trail. Side effects that
occur outside the trace are indistinguishable from unrecorded mutations, undermining the
guarantee that the trace is the definitive record of what happened.
