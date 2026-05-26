# VOCAB_PROTOCOL_KINDS_V0 — Protocol Ontology

**Governance Header**
- Vocabulary ID: fb.vocabulary::VOCAB_PROTOCOL_KINDS_V0
- Version: v0
- Governed By: fb.vocabulary::CONSTITUTION_VOCABULARY_V0
- Status: Active

---

## Purpose

Defines what things ARE in the protocol: node type prefixes and artifact kind names.

## Allowed Usage

- `node_types`: As node type values in workflow DAG definitions
- `artifact_kinds`: In artifact header `Artifact Kind` field and schema routing

## Prohibited Usage

- Must NOT be used as protocol identifiers (WF_*, CC_*, etc.)
- Must NOT be used as parameter names or free-form identifiers
- Node types and artifact kinds must not appear in other vocabulary files

## Governance Rules

- Node types are globally unique 2-letter UPPER_SNAKE prefixes
- Artifact kinds are globally unique lower_snake names
- Each artifact kind maps to exactly one JSON Schema
- Not all node types have corresponding artifact kinds (EXIT, OP are structural)
- TE and TI are authorable via existing artifact_kinds (event, intent respectively)

---

## Machine

```yaml
vocabulary_id: fb.vocabulary::VOCAB_PROTOCOL_KINDS_V0
version: v0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

node_types:
  casing: UPPER_SNAKE
  entries:
    - AC
    - CC
    - CS
    - CT
    - EV
    - EXIT
    - IN
    - OP
    - RB
    - TE
    - TI
    - WF

artifact_kinds:
  casing: lower_snake
  entries:
    - actor
    - capability_contract
    - capability_side_effect
    - capability_transform
    - event
    - governance
    - intent
    - runtime_binding
    - workflow
```
