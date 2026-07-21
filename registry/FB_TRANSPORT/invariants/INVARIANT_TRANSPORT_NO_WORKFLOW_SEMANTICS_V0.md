# INVARIANT_TRANSPORT_NO_WORKFLOW_SEMANTICS_V0

## Machine

```yaml
invariant_code: INVARIANT_TRANSPORT_NO_WORKFLOW_SEMANTICS_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    TI_ and TE_ artifacts MUST NOT participate in execution orchestration semantics.

    This invariant covers three related sub-constraints:

    (1) No execution logic: TI_ and TE_ artifacts must not contain execution steps,
    capability references (CC_, CT_, CS_), or side-effect declarations.

    (2) Execution orthogonality: Transport must not alter execution state.
    Transport is a membrane — it delivers payloads and projects results without
    modifying the execution graph or its intermediate state.

    (3) No execution retry semantics: Transport may retry delivery (network-level),
    but must not declare retry or re-admission logic that targets execution.
    Re-execution is an execution concern, not a transport concern.

  enforcement_stage:
    - compiler_validation

  scope:
    - TRANSPORT_INGRESS
    - TRANSPORT_EGRESS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - execution_step_in_ti: >
        TI artifact declares a pipeline or step sequence
    - cc_reference_in_transport: >
        TI or TE artifact references a CC_, CT_, or CS_ artifact directly
    - side_effect_in_te: >
        TE artifact declares storage writes or external calls
    - execution_retry_in_transport: >
        TI or TE artifact declares retry, re-admission, or backoff targeting execution
    - transport_alters_execution_state: >
        Transport artifact writes to or reads from execution intermediate state
```

---

## Purpose

Transport artifacts are membranes — they declare boundaries, not behavior.
Any execution logic, execution state access, or execution retry semantics inside
a transport artifact collapses the transport/execution firewall and must be
stopped at compile time.

---

## Scope

**Applies to:** All TI_ and TE_ artifacts

**Does NOT apply to:**
- CC_ artifacts within transport workflows (those are execution, not transport)
- RB_ artifacts binding transport workflows (runtime binding is a separate concern)
- Network-level retry (e.g., HTTP retries at the gateway) — transport-layer delivery
