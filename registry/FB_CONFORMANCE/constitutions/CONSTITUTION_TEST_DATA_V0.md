# CONSTITUTION_TEST_DATA_V0

## Machine
```yaml
fqdn: fb.conformance::CONSTITUTION_TEST_DATA_V0
constitution_code: CONSTITUTION_TEST_DATA_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs Test Data (TEST_DATA) artifacts — declarative test specifications for CT conformance
  scope: artifact
  governs:
    - TEST_DATA
  enforcement_model: compiler_enforced

rules:
  - rule_id: TD_CT_OUTPUT_MATCH
    applies_to: TEST_DATA
    constraint: test case expected outputs MUST match the actual CT output contract
    enforced_by: ASSERT_TEST_DATA_MATCH_CT_OUTPUT_V0

  - rule_id: TD_FQDN_REFERENCES
    applies_to: TEST_DATA
    constraint: target artifact references in TEST_DATA MUST use FQDN
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Test Data (TEST_DATA) artifacts.

Test Data artifacts provide declarative test specifications for validating Capability Transforms (CTs). They are the conformance surface for CT behavior — each test case declares input bindings and expected outputs that the CT must produce deterministically.

---

## 2. Core Principles

- **CT Output Match:** Expected outputs in test cases MUST match the actual output contract declared by the target CT. Mismatches are constitutional violations.
- **FQDN References:** All references to target artifacts MUST use fully-qualified names.

---

## 3. Required Fields

- `test_data_code`: Unique identifier for the test data artifact.
- `version`: Version of the test data artifact.
- `governed_by`: The constitution governing this test data.
- `core`: Metadata including summary, target artifact reference, and test cases.

---

## 4. Validation Rules

- Each test case MUST declare input bindings that satisfy the target CT's input schema.
- Each test case MUST declare expected outputs that match the target CT's output contract.
- The target artifact reference MUST use FQDN and resolve to a declared CT artifact.

---

## End of Constitution
