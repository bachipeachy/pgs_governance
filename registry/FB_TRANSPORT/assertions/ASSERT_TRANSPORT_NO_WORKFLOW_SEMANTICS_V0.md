# ASSERT_TRANSPORT_NO_WORKFLOW_SEMANTICS_V0

## Machine

```yaml
artifact_code: ASSERT_TRANSPORT_NO_WORKFLOW_SEMANTICS_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.transport::INVARIANT_TRANSPORT_NO_WORKFLOW_SEMANTICS_V0

implementation:
  module: pgs_governance.registry.handlers.assert_transport_no_workflow_semantics_v0
  callable: execute
```

---

## Purpose

Validates that transport artifacts do not participate in execution orchestration semantics.

**Validates:**
- No TI_ or TE_ artifact references CC_, CT_, or CS_ artifacts directly
- No TI_ or TE_ artifact declares pipeline steps or capability chains
- No TI_ or TE_ artifact declares side effects
- No TI_ or TE_ artifact declares retry or re-admission logic targeting execution

**Does NOT validate:**
- CC_ artifacts referenced within transport-domain workflows (those are execution)
- RB_ artifacts binding transport workflows (runtime binding is a separate concern)

---

## Enforcement

**Phase:** COMPILER_VALIDATION

**Severity:** HARD FAIL — build stops immediately on violation

**Trigger:** Every TI_ and TE_ artifact discovered during compilation

## Violation Examples

```yaml
# VIOLATION: CC reference inside TI
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  pre_validate: capability_contracts::CC_VALIDATE_HTTP_REQUEST_V0  # Not permitted
  workflow: blockchain::WF_HTTP_SUBMIT_TRANSACTION_V0
```

```yaml
# VIOLATION: pipeline step in TE
te_code: TE_HTTP_JSON_V0
core:
  pipeline:
    - step: transform
      ct: capability_transforms::CT_PURE_FORMAT_RESPONSE_V0  # Not permitted
```

## Correct Form

```yaml
# TI declares admission schema and target only — no capability references
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  route:
    method: POST
    path: /api/v0/transaction/submit
  admission_schema:
    actor_record: {type: object, required: true}
  workflow: blockchain::WF_HTTP_SUBMIT_TRANSACTION_V0
  outcomes:
    ACK: {description: Request valid, forwarded to workflow}
    NACK: {description: Request invalid, rejected at admission}
```
