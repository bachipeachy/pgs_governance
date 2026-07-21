# INVARIANT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

## Machine

```yaml
invariant_code: INVARIANT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: execution topology MUST NOT be synthesized, generated, or inferred at runtime; all topology steps must be explicitly declared in the compiled artifact before execution begins
  rule: no runtime component may construct topology steps from dynamic inputs, environment state, payload content, authority grants, or any form of runtime inference; the complete topology graph must exist in the compiled artifact
  scope:
    - CC

```

---

## Summary

Runtime topology synthesis is the most dangerous form of topology violation: it produces
execution graphs that the compiler never saw, never validated, and cannot govern. A runtime
that generates steps from payload content, infers steps from authority grants, or constructs
topology from environment state is an ungovernatable orchestration engine — not a PGS runtime.

All topology exists in the compiled artifact. The runtime reads it. The runtime does not write it.

## Rule

Execution topology MUST NOT be:
1. Generated from payload content at runtime
2. Inferred from authority grants or actor type
3. Constructed from environment variables or configuration
4. Synthesized by the runtime based on execution state
5. Derived from prior execution traces or runtime observations

The topology that executes is identical to the topology in the compiled artifact — always.

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time (structural constraint)
- **Enforced By**: ASSERT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

## Rationale

The distinction between compilation and execution is fundamental to PGS governance. Compilation
is where topology is constructed, validated, and fixed. Execution is where it is traversed.
Any blurring of this boundary — any mechanism by which execution can create topology —
destroys the governance model. Runtime topology synthesis is not a performance concern or
a style concern: it is an architectural violation.

This is a Phase 1 stub. Full enforcement is implemented in Phase 3.
