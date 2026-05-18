# INVARIANT_EV_SCHEMA_REQUIRED_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_EV_SCHEMA_REQUIRED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: Every EV artifact must declare a non-empty schema
  rule: All EV artifacts must define core.schema with at least one field declaration
  scope:
    - EV
```

## Summary

Every Event (EV) artifact must declare a schema describing the data it carries.
A schema-less event is a constitutional violation — it cannot be replayed, audited,
or consumed by downstream systems without a declared data contract.

## Rule

For every EV artifact:
1. `core.schema` MUST be present
2. `core.schema` MUST be a non-empty mapping containing at least one field

## Enforcement Scope

- **Artifact Types**: EV
- **Validation Phase**: ASSERT (Phase 5, compile-time, hard fail)
- **Enforced By**: ASSERT_EV_SCHEMA_REQUIRED_V0

## Rationale

Events are the audit record of the system. Without a declared schema, event replay is
impossible and cross-domain consumers cannot interpret the payload. The schema declaration
is the binding contract between the event emitter and all downstream consumers.
