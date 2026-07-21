# INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: execution topology is fixed at compile time and MUST NOT be modified, extended, or overridden at runtime; topology is a read-only graph structure after compilation
  rule: no runtime component, workflow engine, or execution agent may alter, extend, patch, or override a compiled execution topology; the compiled step sequence and routing declarations are immutable for the lifetime of the compiled artifact
  scope:
    - CC

```

---

## Summary

The governance guarantee of PGS topology rests on compilation being the terminal authority
over execution structure. If any runtime component could modify the step sequence, add
steps, remove steps, or override routing after compilation, the compiler's validation
would be invalidated by changes it never saw.

Topology immutability after compilation is what makes compiler-enforced governance meaningful.

## Rule

Compiled execution topology MUST NOT be:
1. Modified by any runtime component (workflow engine, executor, host environment)
2. Extended with runtime-injected steps not present in the compiled artifact
3. Patched via configuration, environment variable, or feature flag
4. Overridden by caller-supplied topology modifications

The compiled artifact is the topology. The runtime traverses it. No other authority exists.

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time (structural) + runtime (behavioral constraint)
- **Enforced By**: ASSERT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

## Rationale

If topology can be changed at runtime, compilation is advisory, not authoritative. The
entire governance model — invariant checks, routing completeness, dataflow closure —
collapses if any of those properties can be overridden after the fact. Immutability
after compilation is the property that makes compile-time governance load-bearing.

This is a Phase 1 stub. Full enforcement is implemented in Phase 3.
