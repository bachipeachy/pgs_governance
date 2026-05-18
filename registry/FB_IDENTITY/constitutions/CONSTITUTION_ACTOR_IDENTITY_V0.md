# CONSTITUTION_ACTOR_IDENTITY_V0

## One-Line Doctrine

Actors are declarative identity authorities, not behavioral or execution authorities.

## Machine
```yaml
fqdn: fb.identity::CONSTITUTION_ACTOR_IDENTITY_V0
constitution_code: CONSTITUTION_ACTOR_IDENTITY_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Constitution governing declarative actor identity semantics
  scope: artifact
  governs:
    - AC
  enforcement_model: compiler_enforced

rules:
  - rule_id: AC_TYPE_REQUIRED
    applies_to: AC
    constraint: every actor MUST declare a type field from the governed actor type vocabulary
    enforced_by: ASSERT_AC_TYPE_REQUIRED_V0

  - rule_id: AC_ATTRIBUTES_TYPED
    applies_to: AC
    constraint: all declared attributes MUST specify an explicit type; schemaless attributes are a constitutional violation
    enforced_by: ASSERT_AC_ATTRIBUTES_TYPED_V0

  - rule_id: AC_IDENTITY_GOVERNED
    applies_to: AC
    constraint: actor identity is a compile-time governed declaration; runtime inference, dynamic assembly, and ambient identity are prohibited
    enforced_by: ASSERT_AC_IDENTITY_GOVERNED_V0

  - rule_id: AC_IDENTITY_ONLY
    applies_to: AC
    constraint: actor artifacts declare identity and attributes only; execution logic, routing semantics, and side-effect declarations are prohibited
    enforced_by: ASSERT_AC_IDENTITY_ONLY_V0

  - rule_id: AC_NO_AUTHORITY_SEMANTICS
    applies_to: AC
    constraint: actors may not declare permissions, workflow authority, admissibility rules, projection visibility, or execution rights
    enforced_by: ASSERT_AC_NO_AUTHORITY_SEMANTICS_V0

  - rule_id: IDENTITY_AUTHORITY_SEPARATION
    applies_to: AC
    constraint: identity declaration and execution authority must remain orthogonal governance surfaces; no actor artifact may conflate identity with authority
    enforced_by: ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0
```

---

## Scope Boundary

This constitution governs:
- actor identity
- actor typing
- declarative actor attributes

This constitution does NOT govern:
- authority
- authorization
- execution eligibility
- projection visibility
- workflow admissibility

Those concerns belong to authority governance and transport governance.

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Actor (AC_) artifacts.

Actors are the pre-execution governed identity subjects of the protocol. They declare what kinds of principals may participate in governed execution — not what those principals may do (that is the domain of authority governance) or how execution proceeds (that is the domain of workflows).

Actor identity is a **pre-execution governed concern**. Actors are declared, compiled, and resolved before any execution begins. The runtime never infers, assembles, or negotiates actor identity. If an actor is not declared in the protocol, it does not exist from the system's perspective.

---

## 2. Core Principles

- **Pre-Execution Governance:** Actors are governed at compile time. Actor identity is declared, not inferred, discovered, or assembled at runtime.
- **Type Required:** Every actor MUST declare a type from the governed actor type vocabulary. An absent or empty type field is a constitutional violation.
- **Explicit Attribute Schema:** Every attribute declared by an actor MUST carry an explicit type. Schemaless or implicitly typed attributes are prohibited.
- **Identity Only:** Actors declare identity and structural attributes only. An actor artifact may not declare execution logic, routing conditions, or side-effect bindings.
- **No Authority Semantics:** Actors may not declare permissions, workflow authority, admissibility rules, projection visibility, or execution rights. Those concerns belong exclusively to authority governance.
- **AC_ Prefix Reserved:** The `AC_` prefix is reserved exclusively for actor concern artifacts. No other artifact family may use this prefix.

---

## 3. Required Fields

- `ac_code`: Unique identifier for the actor artifact.
- `version`: Version of the actor artifact.
- `governed_by`: Must reference `fb.identity::CONSTITUTION_ACTOR_IDENTITY_V0`.
- `core.type`: Declared actor type (e.g., `person`, `agent`, `system`).
- `core.summary`: One-line description of the actor's role.
- `core.description`: Extended description of the actor's purpose in the governed system.
- `core.attributes`: Attribute declarations, each with an explicit `type`.

---

## 4. Validation Rules

- Actor MUST declare a `type` field. An absent or empty `type` is a compile-time violation.
- Every field in `core.attributes` MUST declare an explicit `type`. Attribute type inference is prohibited.
- Actor artifact MUST NOT contain: execution logic, routing conditions, policy rules, side-effect bindings, or authorization assertions.
- Actor artifact MUST NOT declare: permissions, workflow authority, admissibility rules, projection visibility, or execution rights.
- Actor identity MUST be resolvable entirely from the compiled snapshot. No runtime identity discovery or ambient authority is permitted.
- All artifact references from an actor MUST use FQDN.

---

## 5. Identity Orthogonality

Actor identity is orthogonal to:
- authority governance
- execution semantics
- transport semantics
- workflow admissibility

Actors declare identity only. Authority governance determines what actors may do.

Future authority systems may authenticate or authorize actors without altering actor identity governance semantics.

---

## 6. Relationship to Authority Governance

`CONSTITUTION_ACTOR_IDENTITY_V0` governs **what an actor is** — its identity structure, type, and declared attributes.

`CONSTITUTION_AUTHORITY_GOVERNANCE_V0` (Phase 1) governs **what an actor may do** — its admissibility for execution, workflow authorization, and observation rights.

This separation is foundational. Actors are identity subjects. Authority governance is the sovereign domain that evaluates their admissibility. These two constitutions are orthogonal and must not collapse into each other.

---

## End of Constitution
