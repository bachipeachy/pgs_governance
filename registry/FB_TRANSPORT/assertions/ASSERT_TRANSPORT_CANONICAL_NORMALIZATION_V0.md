# ASSERT_TRANSPORT_CANONICAL_NORMALIZATION_V0

## Machine

```yaml
artifact_code: ASSERT_TRANSPORT_CANONICAL_NORMALIZATION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.transport::INVARIANT_TRANSPORT_CANONICAL_NORMALIZATION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_transport_canonical_normalization_v0
  callable: execute
```

---

## Purpose

Validates that TI_ artifacts declare an explicit admission schema (no passthrough
payloads) and that TE_ artifacts declare an explicit projection schema (no
passthrough execution results).

**Validates:**
- Every TI_ artifact declares an `admission_schema` with at least one field
- No TI_ artifact uses passthrough mode (forwarding raw payload without normalization)
- Every TE_ artifact declares a `response_schema` or equivalent projection declaration
- No TE_ artifact passes the raw execution result through without projection

**Does NOT validate:**
- Type compatibility between admission schema fields and workflow payload schema
- Completeness of projection (whether all execution output fields are projected)

---

## Enforcement

**Phase:** COMPILER_VALIDATION

**Severity:** HARD FAIL — build stops immediately on violation

**Trigger:** Every TI_ and TE_ artifact discovered during compilation

## Violation Examples

```yaml
# VIOLATION: no admission schema (passthrough)
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  route:
    method: POST
    path: /api/v0/transaction/submit
  passthrough: true  # Not permitted — schema must be declared
  workflow: blockchain::WF_HTTP_SUBMIT_TRANSACTION_V0
```

```yaml
# VIOLATION: no projection schema in TE
te_code: TE_HTTP_JSON_V0
core:
  description: Projects execution result as HTTP JSON
  # Missing: response_schema declaration
```

## Correct Form

```yaml
# TI with explicit admission schema
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  admission_schema:
    actor_record: {type: object, required: true}
    wallet_id: {type: string, required: true}
```

```yaml
# TE with explicit projection schema
te_code: TE_HTTP_JSON_V0
core:
  response_schema:
    status: {type: integer, required: true}
    body: {type: object, required: true}
```
