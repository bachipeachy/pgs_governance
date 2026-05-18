# STRUCTURE_EXECUTION_PLACEMENT_LOCAL_SINGLE_NODE_V0

## Machine

```yaml
artifact_code: STRUCTURE_EXECUTION_PLACEMENT_LOCAL_SINGLE_NODE_V0
artifact_kind: STRUCTURE
version: V0
governed_by: fb.execution_placement::CONSTITUTION_EXECUTION_PLACEMENT_V0
fqdn: fb.execution_placement::STRUCTURE_EXECUTION_PLACEMENT_LOCAL_SINGLE_NODE_V0
status: active

placement_mode: LOCAL_SINGLE_NODE
remote_execution_allowed: false
cross_node_dispatch_allowed: false
placement_target: local_process
```

---

## Purpose

Declares that this compiled snapshot authorizes local single-node placement only.
All execution units run in the same process on the same host. No remote dispatch,
no cross-node coordination.

This is the correct and complete description of V0 runtime placement.

## Active Declaration

This structure is the single active placement declaration for V0. The compiler validates
its presence via `INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0` and materializes:

```yaml
federation_profile:
  execution_placement: LOCAL_SINGLE_NODE
```

into every compiled snapshot.
