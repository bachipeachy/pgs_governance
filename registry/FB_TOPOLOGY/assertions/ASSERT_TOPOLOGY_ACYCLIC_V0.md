# ASSERT_TOPOLOGY_ACYCLIC_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_ACYCLIC_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_ACYCLIC_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_acyclic_v0
  callable: execute
```

## Summary

Validates that the compiled semantic topology graph contains no dependency cycles. The compiler pre-computes cycle analysis on the dependency-edge-filtered subgraph; this handler translates the result into standardized governance violations.

## Enforcement

- **Phase**: 4 (GOVERN)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: Entire compiled graph (all artifacts, dependency edges only)

## Handler Behavior

### Context Relay Pattern

The compiler pre-computes cycle detection via `Query.has_cycle()` on the dependency edge subgraph and provides the result as `compilation_context["topology_cycle_analysis"]`.

The handler:
1. Reads pre-computed cycle analysis from compilation context
2. If cycle detected: emits violation with participating nodes
3. If no cycle: reports PASSED

### Dependency Edge Kinds

Only these edge kinds carry dependencies (and thus participate in cycle detection):
- WF_CONTAINS_NODE, WF_START, NODE_NEXT
- CC_BINDS_CT, CC_BINDS_CS
- RB_MAPS, WF_ADMITS_VIA_IN, WF_BINDS_RB
- MOLECULE_COMPOSES_ATOM

Governance edges (GOVERNED_BY, ASSERTED_BY) are excluded.

## Error Messages

### Cycle Detected
```
ASSERT_TOPOLOGY_ACYCLIC_V0: Circular dependency detected
   Graph contains cycle in dependency edges
   Violation: Governed topology must be acyclic (DAG)
   Fix: Remove circular dependency between artifacts
```

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN
