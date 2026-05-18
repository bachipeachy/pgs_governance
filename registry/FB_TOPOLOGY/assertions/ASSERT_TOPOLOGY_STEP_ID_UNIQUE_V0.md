# ASSERT_TOPOLOGY_STEP_ID_UNIQUE_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_STEP_ID_UNIQUE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_STEP_ID_UNIQUE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_step_id_unique_v0
  callable: execute
```

## Summary

Step identifiers must be unique within a CC execution topology. The step ID is the canonical
dataflow address — `$.results.<step_id>.*` bindings in downstream steps address a specific
step by this identifier. Duplicate step IDs create ambiguous dataflow identity that cannot
be resolved at compile time or traced at runtime.

## Rule

For every CC execution topology (pipeline):
1. No two steps within the same pipeline may share the same `step` identifier
2. Comparison is case-sensitive
3. Duplicate step IDs are compile-time violations

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_step_id_unique_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_STEP_ID_UNIQUE_V0

## Rationale

Step IDs are topology-addressable execution identity. As graph analysis matures, step IDs
become the stable canonical identifiers for topology fingerprinting, execution provenance,
and graph diffing. Enforcing uniqueness now ensures future topology features have a sound
identity foundation.

Enforced at compile time: detects duplicate step IDs within each CC pipeline.
