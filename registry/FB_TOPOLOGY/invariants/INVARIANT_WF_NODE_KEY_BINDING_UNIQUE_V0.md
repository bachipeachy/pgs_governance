# INVARIANT_WF_NODE_KEY_BINDING_UNIQUE_V0

## Machine

```yaml
invariant_code: INVARIANT_WF_NODE_KEY_BINDING_UNIQUE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: >
    Within any WF, each CC node usage is identified by a unique node_key.
    When two or more CC nodes in a WF reference the same CC fqdn_id (same capability,
    used multiple times), each usage MUST declare its input bindings under its own
    node_key — never collapsed into a single shared binding context.

  rule: >
    For every WF in the compiled graph: the set of node_keys with non-empty input
    bindings must be injective with respect to (CC_fqdn_id, binding_context).
    A compiler that keys WF-level bindings by CC address instead of node_key silently
    collapses N distinct binding contexts into 1. This is a structural information loss
    and a dispatch correctness violation. The compiler MUST key all WF binding entries
    by node_key (the WF-level symbolic identifier), not by CC address.

  scope:
    - WF

```

---

## Summary

The `node_key` is the WF-level symbolic identifier for a CC node usage. It is what
makes four uses of `CC_RECORD_DENIED_ACTION_V0` distinct within a single WF —
`CC_AUDIT_PARAMETER_VIOLATION`, `CC_AUDIT_UNAUTHORIZED_ACTOR`,
`CC_AUDIT_UNAUTHORIZED_TOOL`, `CC_AUDIT_UNDECLARED_TOOL` are four separate execution
contexts, each with different input bindings, all bound to the same underlying CC.

The dispatch projection binds WF-level inputs per node_key, not per CC address.
If a compiler implementation keys by CC address, all four contexts collapse to the
last-writer's bindings — three denial paths silently receive the wrong inputs.

## Rule

For every WF execution topology:

1. Each CC node usage is identified by `node_key` (the dict key in `core.nodes`).
2. When the same CC fqdn_id appears N times in a WF's `core.nodes`, there are N
   distinct node_keys and N distinct binding contexts.
3. The compiler dispatch projector MUST produce exactly N binding entries for that WF
   (one per node_key), even when all N nodes share the same CC integer address.
4. Keying dispatch bindings by CC address is a violation of this invariant.
5. Routing values in the dispatch projection MUST carry the target node_key alongside
   the target CC address so the scheduler can select the correct binding context.

## Enforcement Scope

- **Artifact Types**: WF
- **Validation Phase**: compile_time (S4 GOVERN)
- **Enforced By**: ASSERT_WF_NODE_KEY_BINDING_UNIQUE_V0

## Rationale

This invariant exists because binding collapse is a silent bug. The compiler builds
successfully; the runtime loads the snapshot without error; all routing decisions are
correct; only the inputs at the collapsed nodes are wrong. Without this invariant,
the bug is undetectable until runtime produces incorrect results that are difficult
to trace back to a projection defect.

The invariant exposes the rule that makes node_key the mandatory binding discriminator.
Any compiler implementation that introduces address-based binding keying will be caught
at compile time rather than discovered through incorrect execution traces.

## Version History

- **V0**: Initial invariant establishing node_key as mandatory WF binding discriminator (2026-06-03)
