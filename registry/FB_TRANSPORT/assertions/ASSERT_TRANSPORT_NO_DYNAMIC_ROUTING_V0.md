# ASSERT_TRANSPORT_NO_DYNAMIC_ROUTING_V0

## Machine

```yaml
artifact_code: ASSERT_TRANSPORT_NO_DYNAMIC_ROUTING_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.transport::INVARIANT_TRANSPORT_NO_DYNAMIC_ROUTING_V0

implementation:
  module: pgs_governance.registry.handlers.assert_transport_no_dynamic_routing_v0
  callable: execute
```

---

## Purpose

Validates that no TI_ or TE_ artifact contains conditional routing logic,
dynamic target resolution, or runtime dispatch declarations.

**Validates:**
- No TI_ artifact contains conditional workflow selection (if/else routing)
- No TI_ artifact contains runtime-resolved target references
- No TE_ artifact contains conditional rendering branches based on runtime context
- No transport artifact uses pattern matching or wildcard targeting

**Does NOT validate:**
- Outcome routing within a CC node (that is execution semantics)
- Workflow-internal DAG branching (governed by WF assertions)

---

## Enforcement

**Phase:** COMPILER_VALIDATION

**Severity:** HARD FAIL — build stops immediately on violation

**Trigger:** Every TI_ and TE_ artifact discovered during compilation

## Violation Examples

```yaml
# VIOLATION: conditional routing in TI
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  workflow:
    if_field: actor_type
    equals: enterprise
    then: blockchain::WF_ENTERPRISE_SUBMIT_V0
    else: blockchain::WF_STANDARD_SUBMIT_V0
```

```yaml
# VIOLATION: runtime-resolved target
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  workflow: "$.payload.target_workflow"  # Dynamic — not permitted
```

## Correct Form

```yaml
ti_code: TI_HTTP_SUBMIT_TRANSACTION_V0
core:
  workflow: blockchain::WF_HTTP_SUBMIT_TRANSACTION_V0  # Static, explicit
```
