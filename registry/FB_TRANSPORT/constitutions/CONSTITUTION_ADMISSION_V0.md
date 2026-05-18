# CONSTITUTION_ADMISSION_V0

## Machine
```yaml
fqdn: fb.transport::CONSTITUTION_ADMISSION_V0
constitution_code: CONSTITUTION_ADMISSION_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs the pre-DAG admission gate declared within workflow artifacts
  scope: artifact
  governs:
    - WF
  enforcement_model: compiler_enforced

rules:
  - rule_id: ADMISSION_READ_ONLY
    applies_to: WF
    constraint: admission phase MUST NOT mutate payload or emit side effects
    enforced_by: TBD

  - rule_id: ADMISSION_PRECONDITION_ONLY
    applies_to: WF
    constraint: admission determines workflow admissibility only; it MUST NOT influence execution behavior
    enforced_by: TBD

  - rule_id: ADMISSION_DENIAL_IS_GOVERNED
    applies_to: WF
    constraint: admission denial MUST emit trace with error_code ADMISSION_DENIED and exit_reason_code ADMISSION_DENIED
    enforced_by: TBD
```

---

## §1. Purpose

Admission is the **pre-DAG enforcement gate** for workflow preconditions.

Admission determines whether a workflow MAY execute, not how it executes.

Admission is **read-only**. It SHALL NOT:
- Mutate payload
- Emit side effects
- Dispatch capabilities
- Invoke the node router

Admission scans existing event logs to verify that declared preconditions hold.

---

## §2. Rule Types

Admission supports exactly two rule types:

| Rule | Semantics |
|------|-----------|
| `requires` | Events that MUST exist in the event log before execution may proceed |
| `forbids` | Events that MUST NOT exist in the event log before execution may proceed |

Both rule types evaluate against the module's event log (JSONL files in the module data root).

---

## §3. Binding Semantics

Bindings map event fields to payload fields for filtered matching.

Declaration form:
```json
"bindings": {
  "EVENT_CODE": {
    "event_field": "payload_field"
  }
}
```

Resolution rules:
1. Each `payload_field` is looked up in the workflow payload
2. If a referenced payload field is absent, derivation MAY be attempted using declared deterministic functions (e.g., `actor_id` from `actor_record`)
3. Only successfully resolved bindings are applied as match filters
4. When a `forbids` event has no explicit binding, it inherits the identity context from all resolved bindings — forbids are scoped to the same entity

---

## §4. Execution Timing

Admission runs:
- AFTER protocol loading (workflow spec, intents, contracts are loaded)
- AFTER DAG construction and validation
- BEFORE DAG node dispatch

Admission is the ADMIT phase in the execution lifecycle (see fb.topology::CONSTITUTION_EXECUTION_V0 §2).

---

## §5. Failure Semantics

Admission denial is a **Governed Denial**, not an execution failure.

- Denial means preconditions are not met — the workflow is structurally valid but contextually inadmissible
- Denial emits an error trace with `error_code: ADMISSION_DENIED`
- Denial terminates execution with `exit_reason_code: ADMISSION_DENIED`
- Denial does not indicate a bug, schema violation, or system error

---

## §6. Declaration Site

Admission rules are declared in the workflow artifact under:

```
core.admission
```

The `admission` block contains:
- `requires`: list of event codes
- `forbids`: list of event codes
- `bindings`: map of event code to field bindings

Workflows without an `admission` block are unconditionally admitted.

---

## §7. Schema Authority (Documentation)

The admission block structure is governed by SCHEMA_WORKFLOW_V0.json, specifically the `admission` object within the `core` section.

---

## §8. Versioning

Changes to this constitution require:
- New version (CONSTITUTION_ADMISSION_V1)
- Migration path documented
- All dependent schemas updated

No backward compatibility assumed.
