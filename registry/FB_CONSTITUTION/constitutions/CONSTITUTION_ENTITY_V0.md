# CONSTITUTION_ENTITY_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_ENTITY_V0
constitution_code: CONSTITUTION_ENTITY_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs ENTITY artifacts — the canonical protocol definition of a business object (identity, attributes, relationships, invariants)
  scope: artifact
  governs:
    - ENTITY
  enforcement_model: compiler_enforced

rules:
  - rule_id: ENTITY_IDENTITY_REQUIRED
    applies_to: ENTITY
    constraint: every entity MUST declare exactly one identity field with a name and type
    enforced_by: TBD

  - rule_id: ENTITY_ATTRIBUTES_TYPED
    applies_to: ENTITY
    constraint: every attribute MUST declare a name and a type; no untyped or implicit fields
    enforced_by: TBD

  - rule_id: ENTITY_NO_BEHAVIOR
    applies_to: ENTITY
    constraint: an entity declares structure only — no behavior, no side effects, no execution (an entity is not a capability)
    enforced_by: TBD

  - rule_id: ENTITY_RELATIONSHIPS_REFERENCE_ENTITIES
    applies_to: ENTITY
    constraint: every relationship MUST reference a governed ENTITY by FQDN; relationships never inline another entity's fields
    enforced_by: TBD

  - rule_id: ENTITY_RELATIONSHIPS_DEFERRABLE
    applies_to: ENTITY
    constraint: a relationship MAY declare status=deferred_resolution when its target entity is not yet compiled; the compiler MUST NOT resolve a deferred target, and MUST resolve a non-deferred target or fail
    enforced_by: TBD

  - rule_id: ENTITY_SEMANTICS_COMPLETE
    applies_to: ENTITY
    constraint: the identity field and every attribute MUST have a semantics entry; meaning is declared separately from structure so the two cannot drift
    enforced_by: TBD

  - rule_id: ENTITY_LIFECYCLE_DECLARED
    applies_to: ENTITY
    constraint: if an entity is stateful it MUST declare a lifecycle (field, stages, initial, terminal); the lifecycle field MUST be an enum attribute whose values equal the declared stages
    enforced_by: TBD

  - rule_id: ENTITY_AUTHORITY_DECLARED
    applies_to: ENTITY
    constraint: every entity MUST declare authority with primary=compiler; runtime is observational only and a Change Request is non_definitional. Runtime "truth by existence" is never authoritative over the compiled entity
    enforced_by: TBD

  - rule_id: ENTITY_PROJECTION_BOUNDED
    applies_to: ENTITY
    constraint: every entity MUST declare a projection whose source_of_truth is the compiler and whose forbidden_sources include markdown, change_requests, and runtime_snapshots. This is the semantic boundary ASSERT_PROJECTION_FIDELITY enforces
    enforced_by: TBD

  - rule_id: ENTITY_CANONICAL_SOURCE
    applies_to: ENTITY
    constraint: the compiled entity is the authoritative field vocabulary; STRUCTURE, RUNTIME_BINDING, CC, WF, Build Sheets and generators reference it and MUST NOT redefine or invent its fields
    enforced_by: TBD

  - rule_id: ENTITY_GOVERNED_RECONCILIATION
    applies_to: ENTITY
    constraint: an entity is a GOVERNED RECONCILIATION that defines the canonical protocol — derived by governance from all available evidence (runtime records, change requests, design intent, invariants), never copied from any single source. Neither runtime ("truth by existence") nor a change request ("truth by intent") is authoritative; only the compiled entity is. Where evidence diverges, the entity records the governed decision and rationale per field (the Reconciliation) using the four outcomes — ACCEPT (already belongs), ADOPT (governance promotes it; implementation converges later), DEFER (valid concept, no current protocol consumer), REJECT (does not belong) — and any non-conformant runtime data becomes a tracked migration. The system only ever migrates TOWARD the governed protocol
    enforced_by: TBD

  - rule_id: ENTITY_INTRINSIC_STATE_ONLY
    applies_to: ENTITY
    constraint: a field belongs in an ENTITY only if it represents INTRINSIC protocol state. Fields that are purely derived, observational, presentation-oriented, or implementation-specific MUST be projected (computed from the entity / events), never canonicalized. Strategic correctness drives the data model — a concept is included because it is fundamental to the protocol's semantics, not because it exists in today's runtime or appeared in an earlier CR

  - rule_id: ENTITY_SEMANTICS_OVER_LAYOUT
    applies_to: ENTITY
    constraint: canonical entities model PROTOCOL SEMANTICS, not implementation layout. (1) Relationships are PREFERRED over duplicated identifiers — reference a related entity once (e.g. included_in -> ENTITY_BLOCK_V0), never copy its several identifiers (block_id, height, hash) into this entity; the compiler projects them if needed. (2) A deterministic/derived value (e.g. a content hash) is canonical ONLY when it is INDEPENDENTLY GOVERNED protocol state — i.e. another protocol participant may legitimately reference, validate, or govern the object BY that value. Identity is the canonical *_id; a hash is canonical only when the protocol makes the hash itself the governed reference. (3) An abandoned or not-yet-adopted design direction (e.g. an EVM gas model the protocol has not adopted) is NOT a protocol concept and MUST be rejected, not deferred — it returns only via a fresh CR that adopts it with its own vocabulary
    enforced_by: TBD

  - rule_id: ENTITY_NOT_SCHEMA
    applies_to: ENTITY
    constraint: an entity is a protocol-level business object, not a storage schema; generated representations (JSON Schema, SQL DDL, Avro) are projections OF the entity, never its definition. The term "schema" MUST NOT be used for the entity's attribute declarations
    enforced_by: TBD

  - rule_id: ENTITY_FQDN_REFERENCES
    applies_to: ENTITY
    constraint: all artifact references in an ENTITY MUST use FQDN
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0
```

---

## 1. Purpose

This constitution governs ENTITY artifacts — the canonical, protocol-level definition of a domain
business object. An ENTITY answers one question and only one: **what *is* this object?** — its
identity, its attributes, its relationships to other entities, and its invariants.

It is the missing first-class layer that separates *what exists* from *where it is stored* (STRUCTURE),
*how it is persisted* (RUNTIME BINDING), and *what is done with it* (WORKFLOW/CC). Before ENTITY,
field definitions lived only in runtime data and in transient Change Requests, with no authoritative
protocol home — forcing downstream construction to invent field names.

---

## 2. Core Principles

- **Identity First:** every entity declares exactly one identity field. An entity without identity is
  inadmissible.
- **Typed Attributes:** every attribute is named and typed. Nothing is implicit.
- **No Behavior:** an entity is inert structure. It declares no execution, no side effects. Behavior
  belongs to capabilities (CC/CT/CS); storage belongs to STRUCTURE; access belongs to RUNTIME BINDING.
- **Compiled Is Truth:** the *compiled* entity is authoritative. Consumers ground field vocabulary from
  the compiled protocol (`pi entity <fqdn>`) — never from source markdown, YAML, or a Change Request.
  *The compiler defines protocol truth; source artifacts declare protocol intent.*
- **Entity ≠ Schema:** an entity is a protocol concept, not a database table. "Schema" is reserved for
  generated representations derived from the entity, never for the entity itself.

---

## 3. Relationship to Other Constitutions

- `CONSTITUTION_STRUCTURE_V0` — STRUCTURE declares *where* an entity is stored and references the entity
  by FQDN (`entity_stores[X].record_type`); it does not define the entity's fields.
- `CONSTITUTION_RUNTIME_BINDING_V0` — RUNTIME BINDING declares *how* an entity's store is accessed.
- `CONSTITUTION_CAPABILITY_CONTRACT_V0` — CCs reference entities for the objects they consume/produce.
- `CONSTITUTION_GOVERNANCE_V0` — governs this constitution.