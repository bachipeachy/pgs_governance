# CONSTITUTION_INTENT_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_INTENT_V0
constitution_code: CONSTITUTION_INTENT_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs system entry points and payload schema validation
  scope: artifact
  governs:
    - IN
  enforcement_model: compiler_enforced

rules:
  - rule_id: IN_SCHEMA_REQUIRED
    applies_to: IN
    constraint: intent MUST define an input schema
    enforced_by: ASSERT_IN_SCHEMA_REQUIRED_V0

  - rule_id: IN_NO_EXECUTION_LOGIC
    applies_to: IN
    constraint: intent MUST NOT contain execution logic; it is an admission gate only
    enforced_by: ASSERT_IN_NO_EXECUTION_LOGIC_V0

  - rule_id: IN_WORKFLOW_BINDING
    applies_to: IN
    constraint: intent MUST map to exactly one workflow
    enforced_by: ASSERT_IN_WORKFLOW_BINDING_V0

  - rule_id: IN_FQDN_REFERENCES
    applies_to: IN
    constraint: all artifact references in intent MUST use FQDN
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Intent (IN) artifacts.

Intents are the declared entry points of the protocol. They define the input schema for a workflow invocation and act as the admission gate — validating that incoming payloads meet the declared preconditions before execution begins.

---

## 2. Core Principles

- **Schema Required:** Every intent MUST define a schema that incoming payloads must conform to.
- **No Execution Logic:** Intents declare admission conditions only. They MUST NOT encode routing, transformation, or side-effect logic.
- **Single Workflow Binding:** Each intent maps to exactly one workflow. One-to-one binding is required.
- **FQDN References:** All artifact references within an intent MUST use fully-qualified names.

---

## 3. Required Fields

- `in_code`: Unique identifier for the intent.
- `version`: Version of the intent artifact.
- `governed_by`: The constitution governing this intent.
- `core`: Metadata including summary and input schema declaration.

---

## 4. Validation Rules

- Intent MUST declare an input schema with at least one field.
- Intent MUST reference its target workflow via FQDN.
- Intent MUST NOT contain conditional logic or transformation expressions.

---

## End of Constitution
