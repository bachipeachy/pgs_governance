# INVARIANT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: each execution topology step MUST reference exactly one capability — exactly one of transform or side_effect, not both, not neither
  rule: each step must contain exactly one capability reference field (transform XOR side_effect); a step with both is an ambiguous execution unit; a step with neither is an empty execution unit; both are constitutional violations
  scope:
    - CC

```

---

## Summary

A step is the unit of capability execution in PGS topology. Its contract is one-to-one:
one step, one capability. Allowing multiple capability references per step would create
compound execution units with indeterminate ordering. Allowing zero capability references
would create phantom steps — declared topology entries that do nothing.

Both deviations violate the principle that topology is a deterministic execution graph.

## Rule

For every execution topology step:
1. Exactly one of `transform` or `side_effect` MUST be present
2. Both `transform` and `side_effect` MUST NOT be present in the same step
3. Neither `transform` nor `side_effect` absent from a step is a constitutional violation
4. The capability reference MUST be a valid FQDN to a registered CT or CS artifact

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

## Rationale

The step-to-capability one-to-one mapping is what makes topology statically analyzable.
With exactly one capability reference per step, the compiler knows precisely what executes,
in what order, and with what contract. This uniqueness constraint protects the compile-time
verifiability of the execution graph.

Full enforcement is implemented in Phase 3.
