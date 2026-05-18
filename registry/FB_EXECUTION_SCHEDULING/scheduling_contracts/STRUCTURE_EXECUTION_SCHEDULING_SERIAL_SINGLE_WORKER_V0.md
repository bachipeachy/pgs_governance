# STRUCTURE_EXECUTION_SCHEDULING_SERIAL_SINGLE_WORKER_V0

## Machine

```yaml
artifact_code: STRUCTURE_EXECUTION_SCHEDULING_SERIAL_SINGLE_WORKER_V0
artifact_kind: STRUCTURE
version: V0
governed_by: fb.execution_scheduling::CONSTITUTION_EXECUTION_SCHEDULING_V0
fqdn: fb.execution_scheduling::STRUCTURE_EXECUTION_SCHEDULING_SERIAL_SINGLE_WORKER_V0
status: active

scheduling_mode: SERIAL_SINGLE_WORKER
parallel_branch_execution_allowed: false
non_blocking_dispatch_allowed: false
deterministic_join_required: false
```

---

## Purpose

Declares that this compiled snapshot authorizes serial single-worker scheduling only.
CC nodes execute one at a time in topological order. No parallel branches, no
non-blocking dispatch, no synchronization barriers.

This is the correct and complete description of V0 runtime execution scheduling.

## Active Declaration

This structure is the single active scheduling declaration for V0. The compiler validates
its presence via `INVARIANT_EXECUTION_SCHEDULING_DECLARED_V0` and materializes:

```yaml
federation_profile:
  execution_scheduling: SERIAL_SINGLE_WORKER
```

into every compiled snapshot.
