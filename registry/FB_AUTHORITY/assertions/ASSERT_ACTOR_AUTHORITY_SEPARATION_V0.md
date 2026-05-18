# ASSERT_ACTOR_AUTHORITY_SEPARATION_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_ACTOR_AUTHORITY_SEPARATION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.authority::INVARIANT_ACTOR_AUTHORITY_SEPARATION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_actor_authority_separation_v0
  callable: execute
```

## Summary

Actor identity artifacts declare what an entity is. Authority governance declares what an entity may do. These are orthogonal governance surfaces with different lifecycles, different answer surfaces, and different downstream consumers. An actor artifact that imports authority semantics — by declaring permissions, workflow eligibility, or admissibility rules — collapses two sovereign governance dimensions into one.

This assertion enforces the separation from the authority governance side: the authority plane must never allow identity artifacts to carry authority payload.

## Rule

For every AC_ artifact:
1. `core.attributes` MUST NOT contain fields named to signal permissions, roles, capabilities, or execution rights (e.g., `allowed_workflows`, `permissions`, `roles`, `authorization`, `execution_rights`)
2. The artifact MUST NOT declare admissibility rules, projection visibility constraints, or workflow authorization grants
3. The artifact MUST NOT reference the authority registry, authorization databases, or runtime permission tables
4. Identity attributes (type, email, agent_id, etc.) MUST carry no implicit authority semantics
5. Actor type MUST NOT function as an implicit authority grant (e.g., `type: admin` granting permissions)

## Enforcement

- **Artifact Types**: AC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_actor_authority_separation_v0`
- **Paired Invariant**: INVARIANT_ACTOR_AUTHORITY_SEPARATION_V0

## Rationale

This is a high-value assertion because identity/authority conflation is the most seductive architectural mistake. When identity and authority are separate, future authority systems (cryptographic, federated, distributed) may evolve independently of actor identity governance. When they collapse, all authority evolution requires identity changes — and all identity changes potentially alter authority semantics.

The assertion pair (ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0 from actor identity governance + this assertion from authority governance) ensures the separation is enforced from both sides: identity artifacts cannot carry authority, and authority governance rejects identity artifacts that do.
