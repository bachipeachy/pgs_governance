# ASSERT_WF_ENTRY_INTENT_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_WF_ENTRY_INTENT_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_WF_ENTRY_INTENT_V0

implementation:
  module: pgs_governance.registry.handlers.assert_wf_entry_intent_v0
  callable: execute
```

## Summary

Validates that every WF declares exactly one entry intent:
1. Exactly one node of type IN exists in the nodes map
2. The start_node references that IN node
3. No workflow may have zero or multiple IN nodes

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All WF artifacts

## Handler Behavior

### 1. Count IN Nodes

Collect all nodes with type IN.

Violation: count != 1.

### 2. Check Start Node Type

Verify start_node references the single IN node.

Violation: start_node does not reference an IN node.

## Error Messages

### Missing Entry Intent
```
❌ ASSERT_WF_ENTRY_INTENT_V0: No entry intent declared
   WF: WF_EXAMPLE_V0
   Violation: Workflow must declare exactly one IN node
   Fix: Add an IN node and set start_node to reference it
```

### Multiple Entry Intents
```
❌ ASSERT_WF_ENTRY_INTENT_V0: Multiple entry intents declared
   WF: WF_EXAMPLE_V0
   IN nodes: [IN_GATE_V0, IN_ALT_V0]
   Violation: Workflow must declare exactly one IN node
   Fix: Consolidate into a single IN node
```

## Rationale

The entry intent is the admission gate for every workflow. Requiring exactly one
ensures a single, unambiguous entry point. Multiple intents would create ambiguous
admission semantics; zero intents would bypass admission entirely.

## Version History

- **V0**: Initial implementation (2026-05-04)
