# INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_IDENTITY_AUTHORITY_SEPARATION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.identity::CONSTITUTION_ACTOR_IDENTITY_V0

core:
  summary: Identity declaration and execution authority must remain orthogonal governance surfaces
  rule: AC_ artifacts must not conflate identity with authority; no actor artifact may declare permissions, execution rights, admissibility rules, or authorization semantics
  scope:
    - AC
```

## Summary

Actor identity governance and execution authority governance are orthogonal surfaces. An actor artifact that conflates identity with authority collapses two sovereign governance dimensions into one, destroying the separation that makes authority governance composable and transport-independent.

## Rule

For every AC_ artifact:
1. `core.attributes` MUST NOT contain fields named to signal permissions, roles, capabilities, or execution rights (e.g., `allowed_workflows`, `permissions`, `roles`, `authorization`, `execution_rights`)
2. The artifact MUST NOT declare admissibility rules, projection visibility constraints, or workflow authorization grants
3. The artifact MUST NOT reference authorization databases, authority stores, or runtime permission tables
4. Identity attributes (type, email, agent_id, etc.) MUST carry no implicit authority semantics

## Enforcement Scope

- **Artifact Types**: AC
- **Validation Phase**: ASSERT (compile-time)
- **Enforced By**: ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0

## Rationale

Identity answers: *what is this entity?*
Authority answers: *what may this entity do?*

These are orthogonal governance questions with different answer surfaces, different lifecycle semantics, and different downstream consumers. Identity is stable and structural; authority is dynamic, workflow-scoped, and policy-driven.

Collapsing them into a single artifact conflates identity declaration with execution eligibility, introduces hidden authority semantics into the compiled snapshot, and makes authority governance dependent on identity artifact structure. This is the same class of error as embedding routing logic in transport artifacts or embedding domain logic in the runtime.

The separation is not a convention — it is a structural invariant enforced at compile time. Future authority systems (cryptographic, federated, distributed) may evolve independently of actor identity governance precisely because this boundary is invariant.
