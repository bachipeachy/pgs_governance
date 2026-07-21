# INVARIANT_WF_EXECUTION_PATH_VALID_V0

## Machine

```yaml
invariant_code: INVARIANT_WF_EXECUTION_PATH_VALID_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    WF execution graph must be valid: start_node exists and is type IN or TI,
    all nodes reachable from start_node, no cycles (DAG constraint),
    all node.next references point to existing nodes, all EXIT nodes
    are terminal, all CC nodes reference valid CC codes (FQDN resolution).

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - unreachable_node: "Node exists but not reachable from start_node"
    - cyclic_graph: "Graph contains cycle (violates DAG constraint)"
    - invalid_next_reference: "node.next references non-existent node"
    - invalid_start_node: "start_node does not exist or is not type IN/TI"
    - non_terminal_exit: "EXIT node has outbound edges"
    - invalid_cc_reference: "CC node references non-existent CC (FQDN not found)"

  clarification:
    dag_model: >
      WF defines execution as DAG (Directed Acyclic Graph) via nodes structure.
      This is the authoritative execution model. Compiler derives linear paths
      from DAG for validation purposes.
    branching_allowed: >
      Branching is valid and expected (SUCCESS/VIOLATION/etc paths).
      Each branch is validated independently.
    execution_paths: >
      Execution paths are derived projections, not declared fields.
      Compiler extracts all possible paths from IN → EXIT for validation.
```

---

## Purpose

Ensure WF execution graph is structurally valid and all references resolve.

**Core Principle**: WF nodes structure is single source of truth for execution flow.

---

## Validation Rules

### Rule 1: Valid Start Node

WF must have `start_node` field referencing existing node of type IN or TI.

**Rationale**: Domain workflows start with IN (Intent), transport workflows start with TI (Transport Ingress).

**Violation**:
```yaml
core:
  start_node: IN_MISSING_V0  # Does not exist in nodes
  nodes:
    IN_OTHER_V0:
      type: IN
```

**Detection**: Check `start_node` exists in `nodes` map and has `type: IN` or `type: TI`.

---

### Rule 2: Graph Connectivity

All nodes must be reachable from `start_node`.

**Violation**:
```yaml
core:
  start_node: IN_START_V0
  nodes:
    IN_START_V0:
      type: IN
      next:
        ACK: EXIT
    CC_ORPHAN_V0:  # Unreachable!
      type: CC
```

**Detection**: Traverse graph from start_node, collect reachable nodes, compare with all nodes.

---

### Rule 3: Acyclic Graph (DAG)

Graph must not contain cycles.

**Violation**:
```yaml
nodes:
  CC_A_V0:
    next:
      SUCCESS: CC_B_V0
  CC_B_V0:
    next:
      SUCCESS: CC_A_V0  # Cycle!
```

**Detection**: Topological sort must succeed (no cycles).

---

### Rule 4: Valid Next References

All `node.next` values must reference existing nodes.

**Violation**:
```yaml
nodes:
  CC_EXAMPLE_V0:
    type: CC
    next:
      SUCCESS: CC_MISSING_V0  # Does not exist!
```

**Detection**: For each node, validate all `next` values exist in `nodes` map.

---

### Rule 5: Terminal EXIT Nodes

EXIT nodes must have no outbound edges.

**Violation**:
```yaml
nodes:
  EXIT:
    type: EXIT
    next:
      CONTINUE: CC_INVALID_V0  # EXIT cannot have next!
```

**Detection**: EXIT nodes must not have `next` field.

---

### Rule 6: Valid CC References

CC nodes must reference existing CC artifacts (FQDN resolution).

**Violation**:
```yaml
nodes:
  CC_GENERATE_ID_V0:
    type: CC
    code: CC_NONEXISTENT_V0  # CC not found in compilation graph
```

**Detection**: Resolve CC FQDN via existing `INVARIANT_FQDN_ONLY_REFERENCES_V0`.

---

## Scope

**Applies to**:
- All WF artifacts (platform + domains)
- All node types (IN, CC, EXIT)
- All transition conditions (ACK, SUCCESS, VIOLATION, etc.)

**Does NOT validate**:
- Data availability (Phase 5)
- Type safety (out of scope)
- Mapping correctness (out of scope)

---

## Execution Path Model (Critical)

**WF = DAG (authoritative)**

Compiler MUST:
1. Treat WF `nodes` graph as single source of truth
2. Derive ALL linear execution paths from DAG (IN → ... → EXIT)
3. Use derived paths for validation (not declared paths)

**Prohibited**:
- ❌ No replacement of DAG with linear `execution_path` field
- ❌ No dual source of truth
- ❌ No global topological order (validate per-path)

**Per-Path Validation**:
- A dependency valid in Path A may be invalid in Path B
- Each branch validated independently
- No false positives from unreachable branches

---

## Rationale

**Closed WF surface = bounded, predictable execution**

### Architectural Purity
- Execution graph is explicit (no implicit behavior)
- No runtime discovery of nodes
- All transitions declared in protocol

### Compile-Time Safety
- Structure errors caught before runtime
- No "node not found" failures during execution
- Fast feedback for protocol authors

### Debugging Support
- Graph visualization available (Phase 8)
- Trace correlation with validated graph
- Clear error messages with location

---

## Version History

- **V0**: Initial implementation (2026-04-12) - WF Execution Path Validation
