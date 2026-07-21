# INVARIANT_TOPOLOGY_STEP_DECLARED_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_STEP_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: every execution topology step MUST be fully and explicitly declared; implicit steps, wildcard bindings, and ambient dataflow are constitutional violations
  rule: each step in a CC pipeline MUST appear as an explicit named entry in the pipeline array; no step may be implied by position, naming convention, field co-location, or runtime inference
  scope:
    - CC

```

---

## Summary

An undeclared step is an ungoverned execution unit. If a CC's execution topology contains
steps that are implied rather than declared — by field naming patterns, positional convention,
or ambient coupling — the compiler cannot validate them, and the runtime cannot traverse them
deterministically.

Every step that executes must exist by name in the topology before compilation completes.

## Rule

For every CC execution topology:
1. Every step MUST be an explicit named entry in the pipeline array
2. Step identity is the `step` field — not position, not key name, not inference
3. No step may be implied by proximity to another step
4. Wildcard bindings (`$.results.*` without a step ID) are constitutional violations
5. Ambient dataflow (state shared across steps without explicit binding) is a constitutional violation

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_STEP_DECLARED_V0

## Rationale

Explicit declaration is the foundation of compile-time governance. If steps can be implied,
the compiler cannot enumerate the execution graph, cannot validate dataflow closure, and
cannot verify routing completeness. Declared steps are the compiler's unit of analysis.

Full enforcement is implemented in Phase 3.
