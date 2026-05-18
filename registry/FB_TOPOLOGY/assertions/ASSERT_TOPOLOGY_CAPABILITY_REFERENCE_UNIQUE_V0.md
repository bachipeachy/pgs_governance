# ASSERT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_capability_reference_unique_v0
  callable: execute
```

## Summary

Each execution topology step MUST reference exactly one capability — exactly one of
`transform` (CT) or `side_effect` (CS), not both, not neither. A step with both capability
references is ambiguous; a step with no capability reference is empty. Both are constitutional
violations.

## Rule

For every execution topology step:
1. Exactly one of `transform` or `side_effect` MUST be present
2. Both present in the same step is a violation
3. Neither present in a step is a violation
4. The capability reference MUST be a valid FQDN to a registered artifact

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_capability_reference_unique_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

## Rationale

The one-to-one step-to-capability mapping is what makes topology statically analyzable.
With exactly one capability reference per step, the compiler knows precisely what executes
at each node in the graph without ambiguity.

Enforced at compile time: each pipeline step must declare exactly one capability (`transform` or `side_effect`), not both and not neither.
