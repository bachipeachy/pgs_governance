# ASSERT_WF_CC_ONLY_NODES_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_WF_CC_ONLY_NODES_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_WF_CC_ONLY_NODES_V0

implementation:
  module: pgs_governance.registry.handlers.assert_wf_cc_only_nodes_v0
  callable: execute
```

## Summary

Validates that all non-structural WF nodes reference CC artifacts only:
1. IN (entry intent) nodes are permitted structural nodes
2. EXIT nodes are permitted structural nodes
3. All other nodes MUST be of type CC
4. No direct CT or CS node references are permitted

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All WF artifacts

## Handler Behavior

### 1. Identify Non-Structural Nodes

Collect all nodes with type other than IN and EXIT.

### 2. Check Node Types

For each non-structural node, verify type is CC.

Violation: Node type is CT, CS, or any unrecognized type.

## Error Messages

### Non-CC Node
```
❌ ASSERT_WF_CC_ONLY_NODES_V0: Non-CC node in workflow
   WF: WF_EXAMPLE_V0
   Node: CT_TRANSFORM_V0
   Type: CT
   Violation: Workflow nodes must be CC only; CT and CS are not permitted
   Fix: Move CT invocation inside a CC artifact
```

## Rationale

Workflows are execution graphs of CC nodes. CTs and CSs are invoked from within CCs,
never directly from workflows. This constraint enforces a clean separation between
orchestration (WF) and implementation (CC → CT/CS).

## Version History

- **V0**: Initial implementation (2026-05-04)
