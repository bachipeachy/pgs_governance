# CONSTITUTION_EXECUTION_PLACEMENT_V0

## Machine

```yaml
constitution_code: CONSTITUTION_EXECUTION_PLACEMENT_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0
fqdn: fb.execution_placement::CONSTITUTION_EXECUTION_PLACEMENT_V0

core:
  summary: Governs execution substrate legality, locality, isolation, and placement admissibility
  description: |
    Declares which execution substrates are legal, how execution locality is
    constrained, and what placement modes a compiled snapshot may authorize.
    Placement is a compile-time governance declaration — not a runtime decision.
    The runtime executes the already-governed placement; it does not negotiate it.
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: PLACEMENT_MUST_BE_DECLARED
    applies_to: compiled_snapshot
    constraint: >
      Every compiled snapshot MUST declare exactly one active placement contract.
      A snapshot with no placement declaration is a compiler validation failure.
    enforced_by: compiler_validation

  - rule_id: PLACEMENT_IMMUTABLE_AFTER_COMPILE
    applies_to: compiled_snapshot
    constraint: >
      Placement mode is resolved at compile time and is immutable.
      Runtime MUST NOT select, override, or negotiate placement mode.
    enforced_by: compiler_validation

  - rule_id: REMOTE_EXECUTION_REQUIRES_CONTRACT
    applies_to: compiled_snapshot
    constraint: >
      Remote execution is not permitted unless an explicit placement contract
      authorizing a remote-capable placement mode is present.
      In V0, only LOCAL_SINGLE_NODE is authorized.
    enforced_by: compiler_validation

  - rule_id: PLACEMENT_IS_NOT_INFRASTRUCTURE
    applies_to: federation_boundary
    constraint: >
      FB_EXECUTION_PLACEMENT governs semantic placement legality only.
      It MUST NOT be bound to any infrastructure technology (Kubernetes, AWS,
      containers, FPGAs). Technology-specific placement is a future runtime
      concern, not a governance concern.
    enforced_by: process_enforced

  - rule_id: RUNTIME_READS_PLACEMENT_PASSIVELY
    applies_to: runtime
    constraint: >
      Runtime MAY read the active placement contract for trace metadata emission.
      Runtime MUST NOT branch on placement mode or alter execution behavior
      based on placement values.
    enforced_by: process_enforced
```

---

## Purpose

This constitution governs how and where PGS execution is permitted to run. It answers
the question: *on what substrate, in what configuration, is execution legal?*

Placement is a governance axis, not an infrastructure concern. The same canonical snapshot
may eventually be executed on a local process, a distributed worker pool, a secure appliance,
or silicon — placement governance ensures that each transition is authorized by declaration
rather than discovered at runtime.

## §1. V0 Placement Mode

The only authorized placement mode in V0 is `LOCAL_SINGLE_NODE`.

This means:
- Execution runs in a single process on the local machine
- No remote dispatch occurs
- No worker pool is consulted
- No distribution layer is involved

This is not a limitation — it is the correct starting declaration. Future placement modes
(multi-worker, remote pool, federated node) extend this axis additively.

## §2. Compiler Behavior

The compiler MUST:
- Discover the active placement contract in this boundary
- Validate that exactly one contract is active
- Materialize placement mode into the snapshot federation profile under:

```yaml
federation_profile:
  execution_placement: LOCAL_SINGLE_NODE
```

The compiler MUST NOT schedule, dispatch, or route execution.

## §3. Runtime Behavior

The runtime executes what the compiler governed. It MUST:
- Record `federation_profile.execution_placement` in trace metadata
- Execute the governed topology without consulting placement mode for branching

## §4. Future Expansion Path

```
LOCAL_SINGLE_NODE
  → LOCAL_MULTI_WORKER
  → REMOTE_WORKER_POOL
  → FEDERATED_NODE
  → SILICON_HOSTED
```

Each step requires a new placement contract authorized by this boundary.
No runtime changes are needed until the runtime evolution model is engaged (V3+).

## §5. Versioning

Changes to placement semantics require a new constitution version and migration rationale.