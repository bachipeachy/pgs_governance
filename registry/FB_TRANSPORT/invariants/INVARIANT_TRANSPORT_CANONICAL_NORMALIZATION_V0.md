# INVARIANT_TRANSPORT_CANONICAL_NORMALIZATION_V0

## Machine

```yaml
invariant_code: INVARIANT_TRANSPORT_CANONICAL_NORMALIZATION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Transport artifacts MUST declare explicit normalization schemas.
    No passthrough of raw payloads or raw execution results is permitted.

    (1) TI_ admission normalization: Every TI_ artifact must declare an explicit
    admission_schema that specifies which fields are accepted. Raw payload
    passthrough (forwarding the entire incoming payload without schema enforcement)
    is a boundary violation.

    (2) TE_ projection normalization: Every TE_ artifact must declare an explicit
    projection schema (response_schema, projection_schema, or projection) that
    specifies which execution result fields are emitted. Raw execution result
    passthrough leaks internal state through the boundary.

    Normalization is deterministic and pure: given the same input, the same
    canonical envelope is always produced.

  enforcement_stage:
    - compiler_validation

  scope:
    - TRANSPORT_INGRESS
    - TRANSPORT_EGRESS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - ti_passthrough_mode: >
        TI artifact declares passthrough: true instead of an admission schema
    - ti_no_admission_schema: >
        TI artifact missing core.admission_schema declaration
    - ti_empty_admission_schema: >
        TI core.admission_schema contains no fields
    - te_no_projection_schema: >
        TE artifact missing response_schema, projection_schema, or projection field
    - te_raw_result_passthrough: >
        TE artifact forwards raw execution result without projection
```

---

## Purpose

The system boundary is not transparent — it is a normalization membrane. Transport
ingress must normalize inbound payloads into a canonical admission envelope before
handing off to execution. Transport egress must project execution results into a
canonical response envelope before emitting to the caller.

This invariant enforces that both boundaries are explicit, governed, and closed.

---

## Scope

**Applies to:** All TI_ and TE_ artifacts

**Does NOT validate:**
- Type compatibility between admission schema fields and workflow payload schema
- Completeness of projection (whether all execution output fields are projected)
