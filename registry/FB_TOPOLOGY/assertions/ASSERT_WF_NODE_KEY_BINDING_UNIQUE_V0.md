# ASSERT_WF_NODE_KEY_BINDING_UNIQUE_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_WF_NODE_KEY_BINDING_UNIQUE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_WF_NODE_KEY_BINDING_UNIQUE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_wf_node_key_binding_unique_v0
  callable: execute
```

## Summary

Within any WF, each CC node usage is uniquely identified by its `node_key` (the symbolic
name in `core.nodes`). When the same CC fqdn_id is used multiple times in a single WF,
each usage must have its own node_key and its own distinct binding context.

This assertion validates that the WF declarations are well-formed for dispatch projection:
the compiler must key all WF-level binding entries by node_key, not by CC address. Any
keying strategy that collapses multiple node_key bindings into one (e.g., keying by CC
integer address) violates this invariant and produces incorrect dispatch outputs.

## Rule

For every WF execution topology:
1. No two CC nodes in `core.nodes` may share both the same `fqdn_id` AND the same
   binding context (identical `inputs`). If same CC is used N times with N distinct
   input sets, all N must be preserved as N distinct binding entries in the dispatch.
2. Each CC node with inputs must have a unique `node_key` — this is inherent to the
   dict structure of `core.nodes` and is always satisfied at the source level.
3. The compiler dispatch projector MUST produce one binding entry per node_key, keyed
   BY node_key — not collapsed by CC address.

## Enforcement

- **Artifact Types**: WF
- **Validation Phase**: compile_time (S4 GOVERN)
- **Handler**: `pgs_governance.registry.handlers.assert_wf_node_key_binding_unique_v0`
- **Paired Invariant**: INVARIANT_WF_NODE_KEY_BINDING_UNIQUE_V0

## Rationale

This assertion exists to make the node_key binding requirement explicit and detectable
at compile time. Without it, a compiler implementation that keys dispatch bindings by
CC address instead of node_key would produce a structurally valid-looking dispatch.json
that silently delivers wrong inputs to all but one of the duplicated CC nodes.

The assertion checks WF source declarations for structural ambiguity — if two CC nodes
use the same CC fqdn_id with the same inputs, one is undetectable from the other under
address-based keying. If inputs differ, they are distinguishable and must be preserved.
