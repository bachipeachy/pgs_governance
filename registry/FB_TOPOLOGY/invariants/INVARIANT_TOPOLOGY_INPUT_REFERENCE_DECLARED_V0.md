# INVARIANT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: all step input references to prior step outputs MUST resolve to a declared step ID within the same pipeline; forward references and dangling references are constitutional violations
  rule: every $.results.<step_id>.* reference in step inputs MUST name a step_id that is explicitly declared earlier in the same pipeline; references to undeclared or future steps are compile-time violations
  scope:
    - CC

```

---

## Summary

Input references are the dataflow edges of the execution graph. If a step references the
output of a step that does not exist, the execution graph has a dangling edge — a reference
into empty space. If it references a step that appears later in the pipeline, the runtime
would need to execute out of declared order to satisfy it.

Both dangling references and forward references are compile-time violations. The compiler
must be able to validate every input reference before the runtime executes a single step.

## Rule

For every execution topology step:
1. All `$.results.<step_id>.*` input references MUST name a `step_id` declared in the same pipeline
2. Referenced step IDs MUST be declared before the referencing step (no forward references)
3. `$.inputs.*` references (CC-level inputs) are always valid and require no step resolution
4. Dangling references (step_id not found in any declared step) are constitutional violations
5. Circular references are constitutional violations

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

## Rationale

Dataflow closure is the property that makes topology statically verifiable. When every
input reference resolves to a declared, earlier step, the compiler can trace every value
from its origin to its consumption without executing the graph. This is the mechanism
that eliminates runtime surprises about missing or unexpected data shapes.

Full enforcement is implemented in Phase 3.
