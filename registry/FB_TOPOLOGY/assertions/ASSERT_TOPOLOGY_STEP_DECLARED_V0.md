# ASSERT_TOPOLOGY_STEP_DECLARED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_STEP_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_STEP_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_step_declared_v0
  callable: execute
```

## Summary

Every execution topology step in a CC pipeline MUST be fully and explicitly declared.
Implicit steps, wildcard step references, and ambient dataflow coupling are constitutional
violations. The compiler must be able to enumerate every step from the declared topology
before execution begins.

## Rule

For every CC execution topology:
1. Every step MUST appear as an explicit named entry with a `step` field
2. Step identity is the `step` field — not position, not key name, not co-location with other fields
3. Wildcard input references (`$.results.*` without a step_id) are violations
4. Ambient dataflow (state shared without explicit binding) is a violation

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_step_declared_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_STEP_DECLARED_V0

## Rationale

Explicit declaration is what makes compile-time topology governance possible. If steps
can be implied, the compiler cannot enumerate the execution graph or validate dataflow
closure. Every step must exist as a named, declared entry before compilation completes.

Enforced at compile time: every pipeline step must carry an explicit `step` field; wildcard `$.results.*` references are violations.
