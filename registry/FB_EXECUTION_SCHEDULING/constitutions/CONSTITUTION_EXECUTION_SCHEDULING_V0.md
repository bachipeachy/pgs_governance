# CONSTITUTION_EXECUTION_SCHEDULING_V0

## Machine

```yaml
constitution_code: CONSTITUTION_EXECUTION_SCHEDULING_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0
fqdn: fb.execution_scheduling::CONSTITUTION_EXECUTION_SCHEDULING_V0

core:
  summary: >
    Governs runtime execution scheduling legality — serial execution,
    parallel branch authorization, non-blocking dispatch legality,
    and deterministic synchronization behavior.
  description: |
    Declares which execution scheduling model is legally active for a compiled
    snapshot. Governs how execution units within a topology are permitted to
    coordinate: serially, in parallel branches, with non-blocking dispatch,
    or with deterministic joins.

    This boundary governs scheduling legality only. It does NOT govern
    global PGS admissibility semantics (intent admission, payload validation,
    or workflow entry-gate logic). Those concerns belong to FB_TRANSPORT and
    the intent admission layer.
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: SCHEDULING_MUST_BE_DECLARED
    applies_to: compiled_snapshot
    constraint: >
      Every compiled snapshot MUST declare exactly one active scheduling contract.
      A snapshot with no scheduling declaration is a compiler validation failure.
    enforced_by: compiler_validation

  - rule_id: PARALLEL_REQUIRES_EXPLICIT_AUTHORIZATION
    applies_to: compiled_snapshot
    constraint: >
      Parallel branch execution is not permitted unless the active scheduling
      contract explicitly sets parallel_branch_execution_allowed: true.
      In V0, only SERIAL_SINGLE_WORKER is authorized.
    enforced_by: compiler_validation

  - rule_id: NON_BLOCKING_REQUIRES_EXPLICIT_AUTHORIZATION
    applies_to: compiled_snapshot
    constraint: >
      Non-blocking dispatch is not permitted unless the active scheduling
      contract explicitly sets non_blocking_dispatch_allowed: true.
      In V0 SERIAL_SINGLE_WORKER mode, this is false.
    enforced_by: compiler_validation

  - rule_id: SCHEDULING_SCOPE_IS_COORDINATION_ONLY
    applies_to: federation_boundary
    constraint: >
      FB_EXECUTION_SCHEDULING governs execution scheduling legality only.
      It MUST NOT be confused with intent admission or payload validation.
      Admission gate logic remains in FB_TRANSPORT and intent artifacts.
    enforced_by: process_enforced

  - rule_id: RUNTIME_READS_SCHEDULING_PASSIVELY
    applies_to: runtime
    constraint: >
      Runtime MAY read the active scheduling contract for trace metadata emission.
      Runtime MUST NOT branch on scheduling mode or alter execution behavior
      based on scheduling values. In V0, the runtime is always serial.
    enforced_by: process_enforced
```

---

## Purpose

This constitution governs execution scheduling legality. It answers the question:
*how are execution units within a workflow topology permitted to be scheduled
and coordinated with each other?*

This is distinct from whether a workflow is admissible at the entry gate (intent/transport
concern) or where it runs (placement concern). Scheduling governs: is this coordination
pattern — serial, parallel, non-blocking — legally authorized for this snapshot?

## §1. V0 Scheduling Mode

The only authorized scheduling mode in V0 is `SERIAL_SINGLE_WORKER`.

This means:
- CC nodes execute one at a time, in topological order
- No parallel branch execution occurs
- No non-blocking dispatch occurs
- No deterministic join synchronization is required

This is the correct and complete description of V0 runtime scheduling behavior.

## §2. Compiler Behavior

The compiler MUST:
- Discover the active scheduling contract in this boundary
- Validate that exactly one contract is active
- Materialize scheduling mode into the snapshot federation profile under:

```yaml
federation_profile:
  execution_scheduling: SERIAL_SINGLE_WORKER
```

## §3. Runtime Behavior

The runtime MUST:
- Record `federation_profile.execution_scheduling` in trace metadata
- Execute serially as the current topology requires
- NOT consult scheduling mode for any execution branching

## §4. Future Expansion Path

```
SERIAL_SINGLE_WORKER
  → PARALLEL_SAFE_DAG
  → NON_BLOCKING_DISPATCH
  → DETERMINISTIC_JOIN
```

Each step requires a new scheduling contract and corresponding runtime evolution
(Runtime V2+). No runtime changes are needed in V0.

## §5. Versioning

Changes to scheduling semantics require a new constitution version and migration rationale.
