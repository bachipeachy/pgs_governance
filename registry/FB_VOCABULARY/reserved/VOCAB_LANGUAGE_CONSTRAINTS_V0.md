# VOCAB_LANGUAGE_CONSTRAINTS_V0 — Authoring Law

**Governance Header**
- Vocabulary ID: fb.vocabulary::VOCAB_LANGUAGE_CONSTRAINTS_V0
- Version: v0
- Governed By: fb.vocabulary::CONSTITUTION_VOCABULARY_V0
- Status: Active

---

## Purpose

Defines words constrained during artifact authoring: structural keys, binding verbs, reserved words, and forbidden words.

## Allowed Usage

- `structural_keys`: As JSON object keys in protocol artifacts only
- `binding_verbs_cs`: Only within CS binding declarations
- `reserved_non_authorable`: May appear as semantic symbols but never as user-defined identifiers
- `forbidden_language`: Must NEVER appear anywhere in protocol artifacts

## Prohibited Usage

- Structural keys must NOT be used as protocol identifiers or parameter names
- Binding verbs must NOT be used in CT bindings or as identifiers
- Reserved words must NOT be used as codes, names, or keys
- Forbidden words trigger hard compiler errors in any context

## Governance Rules

- Each structural key has exactly one semantic role
- Binding verbs encode side-effect execution intent
- Reserved words are known to the compiler with explicit meaning
- Forbidden words represent deprecated or invalid language concepts
- Additions are conservative; removal requires protocol version break

---

## Machine

```yaml
vocabulary_id: fb.vocabulary::VOCAB_LANGUAGE_CONSTRAINTS_V0
version: v0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

structural_keys:
  casing: lower_snake
  entries:
    - bindings
    - capability_ref
    - cc_code
    - code
    - cs_code
    - ct_code
    - description
    - domain
    - guarantees
    - inputs
    - intent_code
    - kind
    - next
    - nodes
    - non_guarantees
    - on_result
    - op
    - operations
    - outputs
    - pipeline
    - properties
    - rb_code
    - runtime_binding
    - start_node
    - type
    - version
    - wf_code

binding_verbs_cs:
  casing: UPPER_SNAKE
  entries:
    - APPEND
    - COUNT
    - DELETE
    - DEREGISTER
    - EXISTS
    - FETCH
    - LIST_KEYS
    - READ
    - READ_ALL
    - REGISTER
    - RESOLVE
    - SEND
    - STORE
    - WRITE
    - EXECUTE

reserved_non_authorable:
  casing: UPPER_SNAKE
  entries:
    # Compiler / runtime concepts
    - COMPILER
    - ENGINE
    - INTERNAL
    - MACHINE
    - RUNTIME
    # Execution / control concepts
    - ABORT
    - END
    - START
    - STOP
    # Future-reserved language concepts
    - ASYNC
    - AWAIT
    - BRANCH
    - CONTEXT
    - LOOP
    - PARALLEL
    - STATE
    # Protocol meta nouns
    - ACTOR
    - CAPABILITY
    - EVENT
    - INTENT
    - OPERATION
    - PROTOCOL
    - WORKFLOW
    # Semantic guarantees / non-guarantees
    - CRYPTOGRAPHIC_STRENGTH
    - DETERMINISTIC_OUTPUT
    - FAIL_FAST
    - IDEMPOTENT
    - LOCALE_SPECIFIC_RULES
    - ORDERING_ENFORCEMENT
    - PURE_FUNCTION
    - SCHEMA_VALIDATION
    - SEMANTIC_VALIDATION
    - SINGLE_EXIT_OPERATION
    - TYPE_INFERENCE
    - UNICODE_NORMALIZATION
    # CT / capability error symbols
    - EMPTY_INPUT
    - INVALID_PATH
    - INVALID_TYPE
    - MISSING_VALUE
    - MULTIPLE_EMIT
    - MULTIPLE_VALUES
    - NOT_EXIT
    - PATH_NOT_FOUND

forbidden_language:
  casing: UPPER_SNAKE
  entries:
    - TERM
    - TERMINAL
    - TERMINATE
```
