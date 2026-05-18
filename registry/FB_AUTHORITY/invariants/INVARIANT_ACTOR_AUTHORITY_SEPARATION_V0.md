# INVARIANT_ACTOR_AUTHORITY_SEPARATION_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_ACTOR_AUTHORITY_SEPARATION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0

core:
  summary: Identity governance and authority governance are orthogonal surfaces; neither may import semantics from the other
  rule: No actor artifact may carry authority semantics; no authority artifact may define identity semantics; the boundary between identity governance and authority governance is inviolable
  scope:
    - AC
```

## Summary

Identity governance and authority governance are two of the four orthogonal governance dimensions of PGS. Identity answers: *what is this entity?* Authority answers: *what may this entity do?* These questions have different answer surfaces, different lifecycle semantics, different downstream consumers, and different evolution trajectories.

The orthogonality invariant is the structural guarantee that these planes will never collapse. It is the architectural foundation that allows authority systems to evolve (from static JSON to cryptographic, federated, or distributed) without altering identity governance — and identity systems to evolve without altering authority semantics.

## Rule

The orthogonality boundary requires:
1. No AC_ artifact may carry authority semantics: no permissions, roles, workflow eligibility, admissibility rules, or execution rights
2. No authority artifact may define identity structure: actor types, identity attributes, or identity lifecycle are governed by CONSTITUTION_ACTOR_IDENTITY_V0
3. Authority evaluation MUST resolve from the authority registry — not from actor identity attributes
4. Actor type MUST NOT function as an implicit authority grant at any level of the stack

## Enforcement Scope

- **Artifact Types**: AC
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_ACTOR_AUTHORITY_SEPARATION_V0

## Relationship to INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0

`INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0` (governed by CONSTITUTION_ACTOR_IDENTITY_V0) enforces this boundary from the identity governance side — actor artifacts must not carry authority.

This invariant enforces the same boundary from the authority governance side — the authority plane must reject identity artifacts carrying authority payload.

Both invariants are required. Together they create a bilateral, cross-constitution enforcement of the same architectural law from each sovereign perspective.
