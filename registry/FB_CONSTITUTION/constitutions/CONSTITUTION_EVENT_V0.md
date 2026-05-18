# CONSTITUTION_EVENT_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_EVENT_V0
constitution_code: CONSTITUTION_EVENT_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs event emission and audit integrity
  scope: artifact
  governs:
    - EV
  enforcement_model: compiler_enforced

rules:
  - rule_id: EV_APPEND_ONLY
    applies_to: EV
    constraint: event stores MUST be append-only; records MUST NOT be mutated
    enforced_by: ASSERT_EV_APPEND_ONLY_V0

  - rule_id: EV_SCHEMA_REQUIRED
    applies_to: EV
    constraint: every event MUST define a schema
    enforced_by: ASSERT_EV_SCHEMA_REQUIRED_V0

  - rule_id: EV_IMMUTABLE_RECORDS
    applies_to: EV
    constraint: emitted event records MUST be immutable
    enforced_by: ASSERT_EV_APPEND_ONLY_V0
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Event (EV) artifacts.

Events are the protocol's mechanism for recording state transitions and observable outcomes. They form the audit trail of the system — what happened, in what order, and with what data — and are the basis for replay, observability, and cross-domain notification.

---

## 2. Core Principles

- **Append-Only:** Event stores are append-only. Once written, event records cannot be modified or deleted.
- **Schema Required:** Every event declaration MUST define the schema of the data it carries. Schemaless events are constitutional violations.
- **Immutable Records:** Individual emitted event records are immutable from the moment they are written.

---

## 3. Required Fields

- `ev_code`: Unique identifier for the event.
- `version`: Version of the event artifact.
- `governed_by`: The constitution governing this event.
- `core`: Metadata including summary and schema declaration.

---

## 4. Validation Rules

- Event MUST declare a schema with at least one field.
- Event stores referenced by EV artifacts MUST enforce append-only semantics.
- No mutation operation (update, delete, patch) is permitted on an event store.

---

## End of Constitution
