# ASSERT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_input_reference_declared_v0
  callable: execute
```

## Summary

All step input references to prior step outputs MUST resolve to a declared step ID within
the same pipeline. Forward references (referencing a step not yet declared) and dangling
references (referencing a step that does not exist) are compile-time violations that break
dataflow closure.

## Rule

For every execution topology step:
1. All `$.results.<step_id>.*` references MUST name a step_id declared in the same pipeline
2. Referenced step IDs MUST be declared before the referencing step (no forward references)
3. Dangling references (step_id not found in any declared step) are violations
4. Circular references are violations
5. `$.inputs.*` references are always valid — they resolve to CC-level inputs, not steps

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_input_reference_declared_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

## Rationale

Dataflow closure — every input reference resolving to a declared earlier step — is the
property that makes topology statically verifiable. Without it, the compiler cannot trace
values from origin to consumption, and runtime data surprises become possible.

Enforced at compile time: all `$.results.<step_id>.*` references must resolve to a declared prior step in the same pipeline.
