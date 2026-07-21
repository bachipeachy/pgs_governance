# INVARIANT_SCHEMA_CONFORMANCE_V0

## Machine

```yaml
invariant_code: INVARIANT_SCHEMA_CONFORMANCE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    All governed artifacts with a declared JSON schema must have frontmatter
    that validates against that schema. Schema conformance is a compile-time
    structural guarantee — no artifact with invalid frontmatter may enter the
    compiled topology. Schemas are loaded from FB_CONSTITUTION and mapped by
    artifact kind (CT, CS, CC, WF, RB, IN, EV, AC).

  enforcement_stage:
    - compiler_validation

  scope:
    - CAPABILITY_TRANSFORMS
    - CAPABILITY_SIDE_EFFECTS
    - CAPABILITY_CONTRACTS
    - WORKFLOWS
    - RUNTIME_BINDINGS
    - INTENTS
    - EVENTS
    - ACTORS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_required_field: "Frontmatter missing a schema-required field"
    - wrong_type: "Frontmatter field has wrong type (e.g. string where object expected)"
    - extra_unconstrained: "Frontmatter contains fields not permitted by schema"

  clarification:
    schema_source: >
      Schemas are authoritative artifacts in FB_CONSTITUTION/schemas/.
      The schema_file_map in the compiler maps NodeKind to schema filename.
      Only artifact kinds with a declared schema are validated — artifact
      kinds without schemas pass through without validation.
```

---

## Purpose

Ensure every governed artifact's frontmatter is structurally valid against its declared JSON schema. This is the compile-time guarantee that all artifacts entering the topology have well-formed declarations.

**Core Principle**: Schema conformance is a compile-time invariant, not a runtime discovery.

---

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN schema validation
