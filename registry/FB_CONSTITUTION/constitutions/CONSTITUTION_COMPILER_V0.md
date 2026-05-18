# CONSTITUTION_COMPILER_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_COMPILER_V0
constitution_code: CONSTITUTION_COMPILER_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs the OmniBachi compiler pipeline — phases, surface closure, determinism, and validation obligations
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: COMPILER_DETERMINISM
    applies_to: system
    constraint: identical inputs MUST produce identical outputs
    enforced_by: ASSERT_ARTIFACT_CONTENT_HASH_DECLARED_V0

  - rule_id: COMPILER_SURFACE_CLOSURE
    applies_to: system
    constraint: all references MUST be resolved at compile time; no partial resolution permitted
    enforced_by: ASSERT_HANDLER_REGISTRY_CLOSED_V0

  - rule_id: COMPILER_NO_HEURISTICS
    applies_to: system
    constraint: compiler MUST NOT use heuristic resolution or implicit defaults
    enforced_by: TBD

  - rule_id: COMPILER_FQDN_ONLY
    applies_to: system
    constraint: all artifact references MUST use FQDN after NORMALIZE phase
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0

  - rule_id: COMPILER_FQDN_TREE_AUTHORITY
    applies_to: system
    constraint: FQDN tree is the sole discovery authority; compiler MUST NOT perform filesystem heuristics
    enforced_by: TBD

  - rule_id: COMPILER_RULE_DRIVEN_VALIDATION
    applies_to: system
    constraint: validation MUST be rule-driven; MUST NOT depend on execution order or side effects
    enforced_by: TBD

  - rule_id: COMPILER_NO_PARTIAL_RESOLUTION
    applies_to: system
    constraint: symbol resolution is all-or-nothing; partial resolution is forbidden
    enforced_by: ASSERT_HANDLER_REGISTRY_CLOSED_V0

  - rule_id: COMPILER_LOSSLESS_EMISSION
    applies_to: system
    constraint: materialized artifacts MUST preserve all declared semantics; no new semantics may be introduced
    enforced_by: ASSERT_ARTIFACT_CONTENT_HASH_DECLARED_V0

  - rule_id: COMPILER_SELF_APPLICABLE
    applies_to: system
    constraint: compiler MUST be capable of validating its own governance artifacts
    enforced_by: ASSERT_COMPILER_GOVERNANCE_DECLARED_V0
```

---

## Header (Documentation)

| Field         | Value                      |
| ------------- | -------------------------- |
| Artifact Code | CONSTITUTION_COMPILER_V0   |
| Artifact Kind | constitution               |
| Tier          | Concern Authority          |
| Governed By   | fb.constitution::CONSTITUTION_GOVERNANCE_V0 |
| Applies To    | Builder, Compiler          |
| Version       | v0                         |
| Status        | active                     |

---

## §1. Purpose

This constitution defines the authoritative behavior of the OmniBachi compiler layer.

The compiler is responsible for:

* Discovering protocol artifacts
* Validating structural and semantic correctness
* Enforcing protocol surface closure
* Producing deterministic, canonical build outputs

**The compiler is a deterministic builder that enforces protocol declarations.**

---

## §2. Role of the Compiler

The compiler SHALL:

1. Discover protocol artifacts via STRUCTURE
2. Parse artifacts into canonical machine form
3. Normalize all references to fully-qualified identifiers (FQDN)
4. Validate artifacts against schemas and governance rules
5. Enforce surface closure across all artifacts
6. Emit deterministic, materialized artifacts

The compiler SHALL NOT:

1. Invent behavior
2. Apply heuristics or fallback logic
3. Encode business logic
4. Depend on runtime, policy, or execution context
5. Execute workflows, capabilities, or side effects

---

## §3. Compiler Pipeline

The compiler SHALL implement the following deterministic pipeline:

```
DISCOVER
→ PARSE
→ NORMALIZE
→ VALIDATE
→ ASSERT
→ ENFORCE
→ MATERIALIZE
```

### Phase Definitions

* **DISCOVER**: Locate artifacts using STRUCTURE declarations only
* **PARSE**: Extract canonical machine sections from artifacts
* **NORMALIZE**: Resolves all references to FQDN and guarantees unambiguous binding while preserving short-name authoring
* **VALIDATE**: Enforce schema correctness using compiler validation rules
* **ASSERT**: Evaluate system-level invariants and cross-artifact constraints
* **ENFORCE**: Fail build if any violation exists
* **MATERIALIZE**: Emit deterministic output artifacts

Each phase SHALL be:

* Stateless
* Deterministic
* Independent of runtime context

---

## §4. Surface Closure

The compiler SHALL enforce protocol surface closure.

Surface closure requires:

1. All references MUST be resolved at compile time
2. All references MUST be unambiguous (FQDN)
3. All referenced artifacts MUST exist
4. No implicit dependencies SHALL be permitted

Violation of surface closure SHALL result in build failure.

Surface closure SHALL be enforced prior to materialization.

---

## §5. Validation Obligations

The compiler SHALL reject any artifact that:

1. Violates schema definitions
2. References undefined artifacts
3. Contains implicit bindings or defaults
4. Introduces cycles in dependency graphs
5. Depends on runtime data
6. Violates vocabulary constraints

Validation SHALL occur before ASSERT evaluation.

---

## §6. ASSERT Evaluation

The compiler SHALL evaluate system-level invariants through ASSERT mechanisms.

ASSERT evaluation:

1. Occurs after schema validation
2. Evaluates cross-artifact relationships
3. Produces deterministic results
4. Does not modify artifacts

ASSERT SHALL NOT:

1. Perform schema validation
2. Introduce new data
3. Depend on runtime state

All ASSERT results SHALL be aggregated prior to enforcement.

---

## §7. Determinism Guarantees

Given identical:

* Input artifacts
* STRUCTURE declarations
* Compiler version

The compiler SHALL:

* Produce identical outputs
* Preserve ordering deterministically
* Resolve all references consistently

Non-determinism is forbidden.

---

## §8. STRUCTURE Authority

All artifact discovery and resolution SHALL be governed by STRUCTURE.

The compiler SHALL:

* Use STRUCTURE as the sole source of truth
* Not perform filesystem heuristics
* Not infer missing paths

Any missing STRUCTURE declaration SHALL result in failure.

---

## §9. Forbidden Patterns

The following are constitutional violations:

1. Heuristic resolution
2. Implicit defaults or fallback behavior
3. Runtime-dependent compilation
4. Partial resolution of references
5. Use of global mutable state
6. Execution of protocol behavior during compilation

---

## §10. Relationship to Other Constitutions

| Constitution               | Relationship                      |
| -------------------------- | --------------------------------- |
| fb.topology::CONSTITUTION_EXECUTION_V0  | Execution is compiler-independent |
| fb.vocabulary::CONSTITUTION_VOCABULARY_V0 | Naming and symbols enforced       |
| fb.constitution::CONSTITUTION_GOVERNANCE_V0 | Amendment authority               |

This constitution does not override other constitutions.

---

## §11. Versioning

Any change to:

* Compiler pipeline phases
* Surface closure semantics
* Determinism guarantees

REQUIRES:

* New version
* Updated schemas or ASSERT definitions
* Explicit migration guidance

Backward compatibility is not assumed.

---

## §12. Design Principle (Non-Normative)

> **Artifacts declare intent.**
> **Compiler enforces correctness.**
> **Execution consumes validated output.**

---

*End of CONSTITUTION_COMPILER_V0*
