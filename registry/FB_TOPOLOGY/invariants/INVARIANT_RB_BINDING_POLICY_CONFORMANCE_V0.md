# INVARIANT_RB_BINDING_POLICY_CONFORMANCE_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_RB_BINDING_POLICY_CONFORMANCE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_RUNTIME_BINDING_V0

core:
  summary: RB bindings for file-path CS types must declare explicit policy.path
  rule: >
    For every CS binding in an RB artifact where the CS type is a file-path CS
    (CS_REGISTRY_V0 or CS_APPENDONLY_JSONL_V0), policy.path must be declared
    and non-empty. policy: {} causes a runtime KeyError crash for these types.
  scope:
    - RB
  file_path_cs_types:
    - CS_REGISTRY_V0
    - CS_APPENDONLY_JSONL_V0
```

## Summary

Runtime bindings map declared CS capabilities to concrete host implementations.
Most CS types (CS_REGISTRY_V0, CS_APPENDONLY_JSONL_V0, etc.) require an explicit
`policy.path` at runtime because their implementations call `policy['path']` directly.
Only `CS_MUTABLE_JSON_V0` resolves paths via a declared STRUCTURE artifact and is
permitted to declare `policy: {}`.

An RB compiled with `policy: {}` for a non-STRUCTURE-resolved CS type will cause
a runtime KeyError crash before any payload is processed — a compiler blind spot
that this invariant closes.

## Rule

For every RB artifact, for every key in `core.bindings`:
1. Extract the CS artifact code from the binding key FQDN
2. If the CS code is `CS_REGISTRY_V0` or `CS_APPENDONLY_JSONL_V0`:
   - The binding MUST declare `policy.path` as a non-empty string
   - `policy: {}` is a violation — it causes runtime KeyError before any payload is processed
3. Other CS types (CS_MUTABLE_JSON_V0, CS_SEND_EMAIL_V0, etc.) are not constrained by this rule

## Enforcement Scope

- **Artifact Types**: RB
- **Validation Phase**: ASSERT (Phase 5, compile-time, hard fail)
- **Enforced By**: ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0

## Rationale

The compiler must guarantee that any RB artifact admitted to the snapshot is
executable without runtime initialization failure. `policy: {}` for CS types
that require an explicit path is a structural defect: the runtime cannot proceed,
the trace is empty, and the error is unrelated to payload content. Catching this
at compile time preserves the PGS invariant that Compiler PASS → Runtime executable.
