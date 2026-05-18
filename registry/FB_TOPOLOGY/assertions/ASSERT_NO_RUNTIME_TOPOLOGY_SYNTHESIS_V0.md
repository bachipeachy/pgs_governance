# ASSERT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

implementation:
  module: pgs_governance.registry.handlers.assert_no_runtime_topology_synthesis_v0
  callable: execute
```

## Summary

Execution topology MUST NOT be synthesized, generated, or inferred at runtime. All topology
steps must be explicitly declared in the compiled artifact before execution begins. A runtime
that constructs steps from payload content, infers steps from authority grants, or derives
topology from environment state is producing execution graphs the compiler never validated.

## Rule

Execution topology MUST NOT be:
1. Generated from payload content at runtime
2. Inferred from authority grants or actor type
3. Constructed from environment variables or configuration
4. Synthesized by the runtime based on execution state or observations
5. Derived from prior execution traces

The topology that executes must be identical to the topology in the compiled artifact.

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_no_runtime_topology_synthesis_v0`
- **Paired Invariant**: INVARIANT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

## Rationale

The compilation/execution boundary is fundamental to PGS governance. Compilation constructs,
validates, and fixes topology. Execution traverses it. Any mechanism that allows execution
to create topology collapses this boundary and destroys the governance model. Runtime
topology synthesis is an architectural violation, not a style concern.

This is a Phase 1 stub. Full enforcement is implemented in Phase 3.
