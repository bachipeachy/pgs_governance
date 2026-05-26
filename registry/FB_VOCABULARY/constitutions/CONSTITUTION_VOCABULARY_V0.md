# CONSTITUTION_VOCABULARY_V0

## Machine
```yaml
fqdn: fb.vocabulary::CONSTITUTION_VOCABULARY_V0
constitution_code: CONSTITUTION_VOCABULARY_V0
artifact_kind: CONSTITUTION
version: V0

core:
  description: Naming authority for OmniBachi — governs reserved words, symbol admissibility, and FQDN conformance
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: VOCAB_FQDN_CONFORMANCE
    applies_to: system
    constraint: all FQDNs MUST conform to vocabulary naming rules
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0

  - rule_id: VOCAB_UNKNOWN_SYMBOL_FORBIDDEN
    applies_to: system
    constraint: unknown symbols are constitutional violations; no implicit symbol creation
    enforced_by: TBD

  - rule_id: VOCAB_APPEND_ONLY
    applies_to: system
    constraint: vocabulary is append-only; symbols MUST NOT be removed or redefined
    enforced_by: TBD

  - rule_id: VOCAB_UPPER_SNAKE_CASE
    applies_to: system
    constraint: all artifact symbols MUST use UPPER_SNAKE_CASE with version suffix
    enforced_by: TBD
```

---

## 1. Scope & Authority

### 1.1 What This Constitution Governs

This constitution governs:
- Reserved word definitions and namespaces
- Symbol admissibility rules
- Vocabulary versioning and deprecation
- Semantic stability guarantees

### 1.2 What This Constitution Does NOT Govern

This constitution does not govern:
- The mechanical enforcement of vocabulary rules (delegated to fb.constitution::CONSTITUTION_COMPILER_V0)
- Domain-specific terminology (delegated to domain constitutions)
- Runtime interpretation of symbols (delegated to CONSTITUTION_EXECUTION_V0)

### 1.3 Constitutional Hierarchy

- **Parent Constitution:** CONSTITUTION_GOVERNANCE_V0
- **Enforcement Delegate:** fb.constitution::CONSTITUTION_COMPILER_V0

---

## 2. Canonical Definitions

### 2.1 Vocabulary Terminology

- **Symbol:** A named identifier used in protocol artifacts (e.g., `CT_PURE_PROJECT_V0`)
- **Reserved Word:** A symbol with fixed, protocol-defined meaning
- **Vocabulary:** A declared set of admissible symbols for a given context
- **Namespace:** A logical grouping of symbols sharing a common prefix
- **Admissibility:** Whether a symbol is valid in a given context

### 2.2 Symbol Categories

| Category | Prefix | Example | Authority |
|----------|--------|---------|-----------|
| Workflow | WF_ | WF_CREATE_WALLET_V0 | Domain constitution |
| Intent | IN_ | IN_WALLET_CREATED_V0 | Domain constitution |
| Capability Contract | CC_ | CC_WALLET_CREATE_V0 | Domain constitution |
| Capability Transform | CT_ | CT_PURE_PROJECT_V0 | CONSTITUTION_CAPABILITY_TRANSFORMS_V0 |
| Capability Side-Effect | CS_ | CS_MUTABLE_JSON_V0 | CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0 |
| Event | EV_ | EV_WALLET_CREATED_V0 | Domain constitution |
| Actor | AC_ | AC_WALLET_HOLDER_V0 | Domain constitution |
| Runtime Binding | RB_ | RB_CAPABILITY_BINDINGS_V0 | Domain constitution |

---

## 3. Reserved Word Governance

### 3.1 Reserved Word Authority

Reserved words are declared in:
```
pgs_governance/governance/vocabulary/reserved/{namespace}.txt
```

### 3.2 Reserved Word Immutability

Once a reserved word is ratified:
- Its meaning MUST NOT change
- Its spelling MUST NOT change
- It MAY be deprecated but MUST NOT be removed

### 3.3 Reserved Word Registration

New reserved words MUST:
- Be added to the appropriate namespace file
- Follow the naming conventions of their category
- Have a corresponding implementation or artifact
- Be documented with a one-line definition

---

## 4. Symbol Admissibility

### 4.1 Admissibility Rules

A symbol is admissible if:
1. It belongs to a declared namespace (prefix match)
2. It follows the naming pattern for its category
3. It is either reserved OR declared in a governing artifact
4. It is not deprecated (unless in a deprecated context)

### 4.2 Admissibility Enforcement

The builder MUST reject artifacts containing:
- Symbols with unknown prefixes
- Symbols violating naming patterns
- References to deprecated symbols in new artifacts
- Undeclared symbols in contexts requiring declaration

### 4.3 Unknown Symbol Policy

Unknown symbols are constitutional violations.
There is no implicit symbol creation.
All symbols MUST be explicitly declared or reserved.

---

## 5. Naming Conventions

### 5.1 General Rules

- Symbols MUST use UPPER_SNAKE_CASE
- Symbols MUST include a version suffix (_V0, _V1, ...)
- Symbols MUST start with their category prefix
- Symbols MUST NOT contain ambiguous abbreviations

### 5.2 Version Suffix

The version suffix (_V0, _V1, ...) is:
- Required for all artifact symbols
- Monotonically increasing
- Immutable once assigned

### 5.3 Naming Patterns by Category

| Category | Pattern | Example |
|----------|---------|---------|
| Workflow | WF_{DOMAIN}_{ACTION}_V{N} | WF_CREATE_WALLET_V0 |
| Intent | IN_{OUTCOME}_V{N} | IN_WALLET_CREATED_V0 |
| Capability Contract | CC_{DOMAIN}_{ACTION}_V{N} | CC_WALLET_CREATE_V0 |
| Capability Transform | CT_{PURITY}_{VERB}_V{N} | CT_PURE_PROJECT_V0 |
| Capability Side-Effect | CS_{MUTABILITY}_{STORE}_V{N} | CS_MUTABLE_JSON_V0 |

---

## 6. Vocabulary Versioning

### 6.1 Vocabulary Files

Vocabulary files are located at:
```
pgs_governance/governance/vocabulary/reserved/{namespace}.txt
```

### 6.2 Vocabulary Changes

Adding a new symbol: Permitted, no version bump required
Changing a symbol's meaning: Forbidden (create new symbol)
Deprecating a symbol: Permitted, requires deprecation annotation
Removing a symbol: Forbidden

### 6.3 Vocabulary Stability

Vocabulary is append-only.
Backward compatibility is guaranteed.
Old symbols remain valid indefinitely.

---

## 7. Deprecation

### 7.1 Deprecation Process

To deprecate a symbol:
1. Add deprecation annotation to vocabulary file
2. Reference the superseding symbol (if any)
3. Document deprecation in changelog
4. Builder MUST warn on deprecated symbol usage

### 7.2 Deprecation Annotation

```
# DEPRECATED: CT_OLD_TRANSFORM_V0 -> CT_NEW_TRANSFORM_V0
CT_OLD_TRANSFORM_V0
```

### 7.3 Deprecated Symbol Usage

- Deprecated symbols MAY be used in existing artifacts
- Deprecated symbols MUST NOT be used in new artifacts
- Builder MUST emit warnings for deprecated symbol usage
- Deprecated symbols are never removed from vocabulary

---

## 8. Semantic Index

### 8.1 Index Location

The semantic index is located at:
```
pgs_governance/governance/vocabulary/vocabulary_semantic_index.json
```

### 8.2 Index Purpose

The semantic index provides:
- Human-readable definitions for all symbols
- Category and namespace mappings
- Deprecation status
- Cross-references

### 8.3 Index Maintenance

The semantic index MUST be kept in sync with vocabulary files.
The builder MAY validate index consistency.

---

## 9. Domain Vocabulary

### 9.1 Domain Authority

Each domain MAY define domain-specific symbols.
Domain symbols MUST:
- Use a category prefix from Section 2.2
- Be declared in the domain's registry
- Not conflict with reserved words

### 9.2 Domain Isolation

Domain vocabularies are scoped to their domain.
A symbol declared in domain A is not automatically visible in domain B.
Cross-domain references MUST use fully-qualified names.

---

## 10. Amendment Policy

### 10.1 Vocabulary Amendments

New vocabulary entries: No constitutional amendment required
New namespaces: Requires constitutional amendment
Changed admissibility rules: Requires constitutional amendment

### 10.2 Constitutional Amendments

Changes to this constitution require a new version (V1, V2, ...).
Silent evolution is prohibited.

---

## 11. Closing Principle

Symbols are the atoms of protocol semantics.
Vocabulary governance ensures semantic stability.
What is named is governed. What is unnamed does not exist.

---

## End of Constitution
