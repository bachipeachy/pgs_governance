# INVARIANT_TOPOLOGY_STEP_ID_UNIQUE_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_STEP_ID_UNIQUE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: Step IDs must be unique within a CC execution topology; duplicate step IDs create ambiguous dataflow identity and are constitutional violations
  rule: Within a single CC pipeline, no two steps may share the same step identifier; the step identifier is the canonical dataflow address for downstream input bindings and must be unambiguous
  scope:
    - CC

```

---

## Summary

The step identifier (`step:`) is the canonical dataflow address. When a downstream step
binds `$.results.derive_master_key.*`, it is addressing the output surface of a specific
step by its declared identity. Duplicate step IDs make this address ambiguous — two steps
share the same identity, and the compiler and runtime cannot determine which one produced
the referenced output.

Step IDs are topology-addressable execution identity. Uniqueness is non-negotiable.

## Rule

For every CC execution topology:
1. Every step identifier MUST be unique within the pipeline (case-sensitive string comparison)
2. A pipeline with two or more steps sharing the same `step` value is a compile-time violation
3. Step identifiers MUST be stable strings — they are dataflow addresses, not display labels
4. Step identifiers SHOULD use snake_case for human readability, but the constraint is uniqueness, not naming style

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_STEP_ID_UNIQUE_V0

## Rationale

As graph analysis matures (topology fingerprints, execution provenance graphs, graph diffing),
step identity becomes increasingly load-bearing. A duplicate step ID is not just a naming
collision — it is an ambiguous execution graph that cannot be canonically addressed, traced,
or compared across builds.

Enforcing uniqueness at V0 ensures that future topology features can rely on step IDs as
stable, unambiguous canonical identifiers.

Full enforcement is implemented in Phase 3.
