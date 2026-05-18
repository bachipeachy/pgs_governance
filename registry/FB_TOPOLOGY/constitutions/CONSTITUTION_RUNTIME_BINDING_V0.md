# CONSTITUTION_RUNTIME_BINDING_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0
constitution_code: CONSTITUTION_RUNTIME_BINDING_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs mapping of CS capabilities to concrete host implementations
  scope: artifact
  governs:
    - RB
  enforcement_model: compiler_enforced

rules:
  - rule_id: RB_DETERMINISTIC_BINDING
    applies_to: RB
    constraint: bindings MUST be deterministic and explicit; no dynamic resolution
    enforced_by: ASSERT_RB_NO_LOGIC_V0

  - rule_id: RB_CS_ONLY
    applies_to: RB
    constraint: RB MUST bind CS artifacts only; never CT or WF
    enforced_by: ASSERT_RB_CS_ONLY_V0

  - rule_id: RB_NO_BEHAVIOR_EXTENSION
    applies_to: RB
    constraint: binding MUST NOT alter capability semantics
    enforced_by: ASSERT_RB_NO_LOGIC_V0

  - rule_id: RB_NO_LOGIC
    applies_to: RB
    constraint: RB MUST NOT contain execution logic; it is a mapping declaration only
    enforced_by: ASSERT_RB_NO_LOGIC_V0

  - rule_id: RB_FQDN_KEYS
    applies_to: RB
    constraint: all binding keys MUST be FQDN
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Runtime Binding (RB) artifacts.

Runtime bindings map declared CS capability artifacts to their concrete host implementations. They supply the configuration that connects protocol-declared capabilities to physical storage and I/O resources at runtime.

---

## 2. Core Principles

- **Deterministic Binding:** Every binding MUST be explicit and produce the same resolution given the same input. No dynamic discovery or late binding.
- **CS-Only:** Runtime bindings bind CS artifacts exclusively. CT and WF artifacts are never bound — they resolve through different mechanisms.
- **No Behavior Extension:** A binding configures a CS capability; it MUST NOT add, remove, or alter the semantics declared in the CS artifact.
- **No Logic:** RB artifacts are mapping declarations. They MUST NOT contain conditional logic, transformations, or execution expressions.
- **FQDN Keys:** All capability references used as binding keys MUST use fully-qualified names.

---

## 3. Required Fields

- `rb_code`: Unique identifier for the runtime binding.
- `version`: Version of the runtime binding artifact.
- `governed_by`: The constitution governing this runtime binding.
- `core`: Metadata including summary and bindings map.
- `bindings`: Map of CS FQDN to implementation type and configuration.

---

## 4. Validation Rules

- Every binding key MUST be a valid CS FQDN that resolves to a declared CS artifact.
- Binding configuration MUST supply all required fields declared in the CS configuration schema.
- RB MUST NOT reference CT, WF, CC, or IN artifacts as binding targets.

---

## End of Constitution
