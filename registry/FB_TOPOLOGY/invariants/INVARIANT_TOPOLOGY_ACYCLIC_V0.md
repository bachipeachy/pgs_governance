# INVARIANT_TOPOLOGY_ACYCLIC_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_ACYCLIC_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    The compiled semantic topology graph must be acyclic across all
    dependency-carrying edge kinds. Cycles in the dependency graph
    indicate structural contradictions — an artifact cannot depend
    on itself transitively. This is a constitutional property of
    governed topology: admissible graphs are always DAGs.

  enforcement_stage:
    - compiler_validation

  scope:
    - ALL_ARTIFACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - cyclic_dependency: "Artifact A depends on B depends on A (transitive cycle)"
    - self_referencing: "Artifact references itself through dependency chain"

  clarification:
    dependency_edges: >
      Only dependency-carrying edges participate in cycle detection:
      WF_CONTAINS_NODE, WF_START, NODE_NEXT, CC_BINDS_CT, CC_BINDS_CS,
      RB_MAPS, WF_ADMITS_VIA_IN, WF_BINDS_RB, MOLECULE_COMPOSES_ATOM.
      Governance edges (GOVERNED_BY, ASSERTED_BY) are not dependency edges.
    whole_graph: >
      Cycle detection operates on the entire compiled graph, not per-artifact.
      A cycle spanning multiple artifact types (WF → CC → CT → ... → WF)
      is still a violation.
```

---

## Purpose

Ensure the compiled topology graph has no circular dependencies. Cycles make compilation non-terminating and execution ordering undefined.

**Core Principle**: Governed topology is always a DAG. Cycles are structurally inadmissible.

---

## Validation Rules

### Rule 1: No Transitive Dependency Cycles

The dependency subgraph (filtered to dependency-carrying edge kinds) must admit a topological ordering.

**Violation**:
```
CC_A → CT_X → (via MOLECULE_COMPOSES_ATOM) → CT_Y → (via CC binding) → CC_A
```

**Detection**: Standard cycle detection (DFS-based or Kahn's algorithm) on the dependency-edge-filtered subgraph.

---

## Scope

**Applies to**: Entire compiled graph (all nodes, dependency edges only)

**Does NOT apply to**: Governance edges (GOVERNED_BY, ASSERTED_BY, INVARIANT_APPLIES) — these are metadata, not dependencies.

---

## Rationale

**Acyclic topology = well-ordered compilation and execution**

- Topological ordering guarantees deterministic stage processing
- No infinite loops in dependency resolution
- Foundation for deterministic semantic addressing

---

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN hardcoded cycle detection
