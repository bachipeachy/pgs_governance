# ASSERT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_authority_orthogonal_v0
  callable: execute
```

## Summary

Execution topology steps must not encode authority semantics. This assertion detects
authority-semantic field names inside CC pipeline steps — role declarations, permission
checks, authorization branching, actor-type gating. Topology that encodes authority
semantics collapses two orthogonal governance planes.

This is the topology-side complement of `ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0` (identity
plane) and `ASSERT_ACTOR_AUTHORITY_SEPARATION_V0` (authority plane). All three enforce the
identity/authority/topology orthogonality law from their respective governance surfaces.

## Rule

For every CC execution topology step:
1. Steps MUST NOT declare authority-semantic fields:
   - `role`, `required_role`, `permissions`, `authorization`, `authorized_by`
   - `on_role`, `execution_rights`, `actor_type_gate`, `permission_check`
2. Steps MUST NOT route based on actor identity or permission state
3. Steps MUST NOT reference authority registries or permission tables

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_authority_orthogonal_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

## Rationale

Authority is evaluated before topology traversal begins. The topology surface receives
a binary admissibility outcome — admitted or not. It does not receive authority state to
consume, route on, or re-evaluate. Topology that encodes authority semantics has bypassed
the authority governance plane and embedded authorization logic in execution traversal.

Enforced at compile time: detects authority-semantic field names (`role`, `permissions`, `authorized_by`, etc.) inside CC pipeline steps.
