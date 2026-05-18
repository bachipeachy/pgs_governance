# ASSERT_WF_EXECUTION_PATH_VALID_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_WF_EXECUTION_PATH_VALID_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_WF_EXECUTION_PATH_VALID_V0

implementation:
  module: pgs_governance.registry.handlers.assert_wf_execution_path_valid_v0
  callable: execute
```

## Summary

Validates WF execution graph structural correctness:
1. Valid start node (exists and is type IN)
2. All nodes reachable from start_node
3. No cycles (DAG constraint)
4. All node.next references valid
5. EXIT nodes are terminal
6. All CC nodes reference existing CC artifacts

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All WF artifacts

## Graph Model

**WF = DAG (Directed Acyclic Graph)**

```
start_node: IN_XXX
  ↓
nodes:
  IN_XXX → [ACK: CC_A, NACK: EXIT]
  CC_A → [SUCCESS: CC_B, VIOLATION: EXIT]
  CC_B → [SUCCESS: EXIT]
  EXIT (terminal)
```

**Derived Paths**:
- Path 1: IN_XXX [ACK] → CC_A [SUCCESS] → CC_B [SUCCESS] → EXIT
- Path 2: IN_XXX [ACK] → CC_A [VIOLATION] → EXIT
- Path 3: IN_XXX [NACK] → EXIT

Each path validated independently.

## Handler Behavior

### 1. Validate Start Node

Check `start_node` exists in `nodes` map and has `type: IN`.

Violation: start_node missing or wrong type.

### 2. Check Connectivity

Traverse graph from start_node, collect reachable nodes.

Violation: Nodes exist but not reachable (deadcode).

### 3. Detect Cycles

Perform topological sort (Kahn's algorithm or DFS).

Violation: Cycle detected (violates DAG constraint).

### 4. Validate Next References

For each node, check all `next` values point to existing nodes.

Violation: Reference to non-existent node.

### 5. Check EXIT Terminals

Ensure EXIT nodes have no outbound edges (`next` field absent or empty).

Violation: EXIT node has `next` field.

### 6. Validate CC References

For each CC node, resolve CC FQDN via compilation graph.

Violation: CC not found (delegates to `INVARIANT_FQDN_ONLY_REFERENCES_V0`).

## Error Messages

### Unreachable Node
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Unreachable node
   WF: WF_EXAMPLE_V0
   Node: CC_ORPHAN_V0
   Violation: Node exists but not reachable from start_node
   Fix: Either connect to graph or remove node
```

### Cyclic Graph
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Cycle detected
   WF: WF_EXAMPLE_V0
   Cycle: CC_A_V0 → CC_B_V0 → CC_A_V0
   Violation: Graph contains cycle (violates DAG constraint)
   Fix: Remove cycle-causing edge
```

### Invalid Next Reference
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Invalid next reference
   WF: WF_EXAMPLE_V0
   Node: CC_EXAMPLE_V0
   Reference: CC_MISSING_V0
   Violation: next points to non-existent node
   Fix: Add CC_MISSING_V0 node or fix reference
```

### Invalid Start Node
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Invalid start_node
   WF: WF_EXAMPLE_V0
   start_node: IN_MISSING_V0
   Violation: start_node does not exist in nodes map
   Fix: Add IN_MISSING_V0 to nodes or fix start_node reference
```

### Non-Terminal EXIT
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Non-terminal EXIT
   WF: WF_EXAMPLE_V0
   Node: EXIT
   Violation: EXIT node has outbound edges (next field present)
   Fix: Remove next field from EXIT node
```

### Invalid CC Reference
```
❌ ASSERT_WF_EXECUTION_PATH_VALID_V0: Invalid CC reference
   WF: WF_EXAMPLE_V0
   Node: CC_GENERATE_ID_V0
   CC Code: CC_NONEXISTENT_V0
   Violation: CC not found in compilation graph
   Fix: Add CC artifact or fix code reference
```

## Rationale

**Structural validation prevents runtime failures**

### Early Detection
- Structure errors caught at compile time
- No "node not found" during execution
- Fast feedback loop

### Explicit Execution Model
- All transitions declared
- No implicit behavior
- Graph = single source of truth

### Foundation for Data Validation
- Phase 5 (data availability) requires valid graph
- Cannot validate data flow without valid structure
- Layered validation (structure → data → types)

## Version History

- **V0**: Initial implementation (2026-04-12) - WF Execution Path Validation
