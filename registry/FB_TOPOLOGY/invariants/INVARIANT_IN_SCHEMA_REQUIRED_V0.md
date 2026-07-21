# INVARIANT_IN_SCHEMA_REQUIRED_V0

## Machine

```yaml
invariant_code: INVARIANT_IN_SCHEMA_REQUIRED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Every IN artifact must declare a non-empty schema. Schema must contain at
    least one field, and each field must declare a non-empty type. Schema-less
    intents cannot validate admission payloads.

  enforcement_stage:
    - compiler_validation

  scope:
    - INTENTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_schema: "IN artifact has no schema field"
    - empty_schema: "IN schema declares no fields"
    - untyped_field: "Schema field present but type missing or empty"

  clarification:
    purpose: >
      The schema is the admission contract. Without it, the intent is a pass-through
      gate that cannot reject malformed payloads.
    minimal_schema: >
      At minimum one field with a declared type is required. The schema need not
      be exhaustive but must be non-empty.
```

---

## Purpose

Ensure every admission gate declares what it expects from incoming payloads.

---

## Validation Rules

### Rule: Schema Field Required

IN artifact must have a top-level schema field.

**Violation**:
```yaml
in_code: IN_EXAMPLE_V0
core:
  summary: Entry intent
# No schema field
```

### Rule: Non-Empty Schema

Schema must declare at least one field.

**Violation**:
```yaml
schema: {}  # Empty
```

### Rule: Typed Fields

Each field in schema must declare a non-empty type.

**Violation**:
```yaml
schema:
  name:
    # No type declared
```

---

## Scope

**Applies to**: All IN artifacts

**Does NOT validate**: Type correctness or field semantics (out of scope for this invariant)

---

## Version History

- **V0**: Initial implementation (2026-05-04)
