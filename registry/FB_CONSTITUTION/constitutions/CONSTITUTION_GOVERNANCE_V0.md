# CONSTITUTION_GOVERNANCE_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_GOVERNANCE_V0
constitution_code: CONSTITUTION_GOVERNANCE_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Root authority for the OmniBachi governance system — governs all constitutions and the governance hierarchy
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: GOVERNANCE_SUPREMACY
    applies_to: system
    constraint: this constitution takes precedence over all other constitutions in any conflict
    enforced_by: PROCESS_ENFORCED

  - rule_id: GOVERNANCE_VERSION_IMMUTABILITY
    applies_to: system
    constraint: ratified constitutions MUST NOT be mutated; any change requires a new version
    enforced_by: PROCESS_ENFORCED

  - rule_id: GOVERNANCE_EXPLICIT_AUTHORITY
    applies_to: system
    constraint: all governance authority MUST be explicitly declared; no implicit authority
    enforced_by: ASSERT_PROTOCOL_SURFACE_CLOSED_V0

  - rule_id: GOVERNANCE_NO_SILENT_EVOLUTION
    applies_to: system
    constraint: all changes MUST be versioned and visible; undocumented changes are constitutional violations
    enforced_by: PROCESS_ENFORCED
```

---

**Header Block (Documentation)**
- **Constitution ID:** CONSTITUTION_GOVERNANCE_V0
- **Tier:** Sovereign Authority
- **Applies To:** All OmniBachi governance artifacts and constitutions
- **Status:** Active — Foundational
- **Supersedes:** NONE
- **Ratified By:** [AUTHORITY]
- **Ratification Date:** [ISO-8601]
- **Audience:** All protocol authors, implementers, and reviewers
- **Dependencies:** NONE (this is the root)

---

## 1. Scope & Authority

### 1.1 What This Constitution Governs

This constitution is the root authority for the OmniBachi governance system. It governs:
- The existence and hierarchy of all other constitutions
- The rules for creating, amending, and deprecating governance artifacts
- The authority model for protocol governance
- The relationship between governance tiers

### 1.2 Constitutional Supremacy

This constitution is supreme. All other constitutions derive authority from this document.
In the event of conflict between this constitution and any other, this constitution prevails.

### 1.3 What This Constitution Does NOT Govern

This constitution does not govern:
- Implementation details of any system component
- Domain-specific business logic
- Runtime behavior (delegated to fb.topology::CONSTITUTION_EXECUTION_V0)
- Authoring-time behavior (governed by fb.constitution::CONSTITUTION_COMPILER_V0)

---

## 2. Canonical Definitions

### 2.1 Governance Terminology

- **MUST:** An absolute requirement. Violations are constitutional failures.
- **MUST NOT:** An absolute prohibition. Violations are constitutional failures.
- **SHOULD:** A strong recommendation. Deviations require documented justification.
- **MAY:** An optional action. No justification required.
- **Constitution:** A versioned governance document declaring authority, constraints, and semantics.
- **Schema:** A versioned structural definition. Governs shape, not behavior.
- **Artifact:** A versioned, declarative document conforming to a schema and governed by a constitution.
- **Registry:** A declared collection of governance artifacts at a specific FQDN path.

### 2.2 Authority Levels

| Level | Description | Example |
|-------|-------------|---------|
| Sovereign | Root authority, defines protocol semantics | This constitution |
| Delegated | Authority derived from sovereign, must comply | Domain constitutions |

### 2.3 Governance Tiers

| Tier | Scope | Documents |
|------|-------|-----------|
| Sovereign Authority | Protocol-wide rules | CONSTITUTION_GOVERNANCE_V0, GOVERNANCE_FQDN_TREE_V0, CONSTITUTION_VOCABULARY_V0 |
| System Authority | Specific system concerns | CONSTITUTION_COMPILER_V0, CONSTITUTION_EXECUTION_V0, CONSTITUTION_EXECUTION_POLICY_V0, CONSTITUTION_TRACE_EXECUTION_V0 |
| Artifact Authority | Artifact type rules | CONSTITUTION_WORKFLOW_V0, CONSTITUTION_INTENT_V0, CONSTITUTION_RUNTIME_BINDING_V0, CONSTITUTION_CAPABILITY_TRANSFORMS_V0, CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0, CONSTITUTION_EVENT_V0 |
| Schema Definition | Structural specifications | TRACE_SCHEMA_V0 |
| Domain Authority | Domain-specific rules | Per FQDN tree declaration |

---

## 3. Constitution Structure

### 3.1 Required Elements

Every constitution MUST include:
- **Header Block:** ID, Tier, Applies To, Status, Supersedes, Dependencies
- **Scope & Authority:** What it governs and does not govern
- **Canonical Definitions:** Terms used within the document
- **Substantive Sections:** The actual governance rules
- **Amendment Policy:** How the constitution may be changed

### 3.2 Versioning

- Constitutions MUST be versioned (V0, V1, V2, ...)
- A new version MUST be created for any semantic change
- Versions are immutable once ratified
- Version numbers are monotonically increasing integers

### 3.3 Immutability

Ratified constitutions are immutable.
Any change, including corrections, MUST result in a new version.
The previous version remains valid until explicitly superseded.

---

## 4. Authority Hierarchy

### 4.1 Hierarchy Rules

- Parent constitutions take precedence over child constitutions
- Sovereign tier takes precedence over all other tiers
- Within a tier, explicit dependencies determine precedence
- Circular dependencies are forbidden

### 4.2 Conflict Resolution

When constitutions conflict:
1. Apply the higher-tier constitution
2. If same tier, apply the constitution with explicit authority over the matter
3. If ambiguous, apply fb.constitution::CONSTITUTION_GOVERNANCE_V0 (this document)

### 4.3 Delegation

A constitution MAY delegate authority to a child constitution.
Delegation MUST be explicit.
Delegated authority cannot exceed the delegating constitution's authority.

---

## 5. Amendment Policy

### 5.1 Amendment Requirements

Amendments to any constitution MUST:
- Create a new version (V1, V2, ...)
- Explicitly state what is superseded
- Be ratified by the appropriate authority
- Include a ratification date

### 5.2 Silent Evolution Prohibition

Silent evolution is prohibited.
All changes MUST be versioned and visible.
Undocumented changes are constitutional violations.

### 5.3 Deprecation

Deprecated constitutions MUST:
- Be marked with Status: Deprecated
- Reference the superseding document
- Remain available for historical reference

---

## 6. Registry Governance

### 6.1 Registry Authority

GOVERNANCE_FQDN_TREE_V0 is the sole authority for:
- Which registries exist
- What artifact types each registry contains
- The build order of packages
- Physical path mappings

### 6.2 Registry Invariants

- Only declared registries participate in governance
- Undeclared registries are invisible to the protocol
- Registry contents MUST conform to their governing constitution

---

## 7. Artifact Governance

### 7.1 Artifact Identity

Every governance artifact MUST have:
- A unique code (e.g., WF_CREATE_WALLET_V0)
- A version
- A governing constitution reference

### 7.2 Artifact Immutability

Ratified artifacts are immutable.
Changes require a new version.
This rule has no exceptions.

### 7.3 Artifact Conformance

Artifacts MUST conform to:
- Their governing constitution's structural requirements
- Their schema's type constraints
- Vocabulary admissibility rules per fb.vocabulary::CONSTITUTION_VOCABULARY_V0

---

## 8. Enforcement

### 8.1 Build-Time Enforcement

fb.constitution::CONSTITUTION_COMPILER_V0 governs build-time enforcement.
The compiler MUST reject artifacts that violate their governing constitution.

### 8.2 Runtime Enforcement

fb.topology::CONSTITUTION_EXECUTION_V0 governs runtime enforcement.
The execution engine MUST halt on constitutional violations.

### 8.3 Violation Reporting

All constitutional violations MUST be:
- Explicit (no silent failures)
- Traceable (reference the violated rule)
- Actionable (clear remediation path)

---

## 9. Closing Principle

Protocol governs behavior.
Constitutions govern protocol.
This constitution governs constitutions.

The chain of authority is explicit, versioned, and immutable.

---

## End of Constitution
