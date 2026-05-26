# ASSERT_SCHEMA_CONFORMANCE_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_SCHEMA_CONFORMANCE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_SCHEMA_CONFORMANCE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_schema_conformance_v0
  callable: execute
```

## Summary

Validates that all governed artifact frontmatter conforms to the JSON schema declared for its artifact kind. The compiler pre-computes per-node schema validation using JSON Schema Draft 2020-12 and provides results via compilation context.

## Enforcement

- **Phase**: 4 (GOVERN)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All artifacts with declared schemas (CT, CS, CC, WF, RB, IN, EV, AC)

## Handler Behavior

### Context Relay Pattern

The compiler loads JSON schemas from `FB_CONSTITUTION/schemas/`, validates each node's frontmatter, and provides per-FQDN results as `compilation_context["schema_conformance"]`.

The handler:
1. Reads pre-computed schema validation from compilation context
2. Iterates all artifacts, looks up per-FQDN result
3. Translates jsonschema validation errors to standardized governance violations

### Schema Map

| Artifact Kind | Schema File |
|--------------|-------------|
| CT | SCHEMA_CAPABILITY_TRANSFORM_V0.json |
| CS | SCHEMA_CAPABILITY_SIDE_EFFECT_V0.json |
| CC | SCHEMA_CAPABILITY_CONTRACT_V0.json |
| WF | SCHEMA_WORKFLOW_V0.json |
| RB | SCHEMA_RUNTIME_BINDING_V0.json |

Artifact kinds without a declared schema are not validated.

## Error Messages

### Schema Violation
```
ASSERT_SCHEMA_CONFORMANCE_V0: Schema violation
   Artifact: blockchain::CC_EXAMPLE_V0
   Path: $.machine.implementation
   Violation: 'module' is a required property
   Fix: Add required field 'module' to machine.implementation
```

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN schema validation
