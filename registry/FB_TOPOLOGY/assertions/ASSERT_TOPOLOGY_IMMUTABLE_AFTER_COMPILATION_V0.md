# ASSERT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_immutable_after_compilation_v0
  callable: execute
```

## Summary

Execution topology is fixed at compile time and MUST NOT be modified, extended, or
overridden at runtime. The compiled step sequence and routing declarations are immutable
for the lifetime of the compiled artifact. Any mechanism that allows runtime topology
modification invalidates the compiler's governance guarantees.

## Rule

Compiled execution topology MUST NOT be:
1. Modified by any runtime component (workflow engine, executor, host environment)
2. Extended with runtime-injected steps not present in the compiled artifact
3. Patched via configuration, environment variable, or feature flag
4. Overridden by caller-supplied topology modifications at any execution boundary

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_immutable_after_compilation_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

## Rationale

Topology immutability after compilation is what makes compile-time governance load-bearing.
If the topology can be changed at runtime, compilation becomes advisory rather than
authoritative — all invariant checks, routing completeness validation, and dataflow closure
analysis are rendered meaningless by changes the compiler never saw.

This is a Phase 1 stub. Full enforcement is implemented in Phase 3.
