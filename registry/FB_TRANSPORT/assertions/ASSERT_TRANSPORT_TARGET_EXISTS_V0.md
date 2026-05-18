# ASSERT_TRANSPORT_TARGET_EXISTS_V0

## Machine

```yaml
artifact_code: ASSERT_TRANSPORT_TARGET_EXISTS_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.transport::INVARIANT_TRANSPORT_TARGET_EXISTS_V0

implementation:
  module: pgs_governance.registry.handlers.assert_transport_target_exists_v0
  callable: execute
```

---

## Purpose

Validates at compile time that every TI_ artifact declares an explicit workflow
target and that the target workflow exists in the protocol snapshot.

**Validates:**
- Every TI_ artifact has a `workflow` field in its `core` block
- The declared workflow FQDN resolves to an artifact in the compiled snapshot
- No TI_ artifact declares a null, empty, or wildcard target

**Does NOT validate:**
- Whether the workflow is currently enabled or reachable at runtime
- Whether the workflow accepts the TI admission schema fields

---

## Enforcement

**Phase:** COMPILER_VALIDATION

**Severity:** HARD FAIL — build stops immediately on violation

**Trigger:** Every TI_ artifact discovered during compilation

## Violation Examples

```yaml
# VIOLATION: missing workflow binding
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  route:
    method: POST
    path: /api/v0/transaction/submit
  # Missing: workflow field
```

```yaml
# VIOLATION: workflow not in snapshot
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  workflow: blockchain::WF_NONEXISTENT_V0  # Does not exist in snapshot
```

## Correct Form

```yaml
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  workflow: blockchain::WF_HTTP_SUBMIT_TRANSACTION_V0  # Exists in snapshot
```
