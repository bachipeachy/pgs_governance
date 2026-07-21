# INVARIANT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: Execution topology must not encode authority semantics — no role branching, permission routing, actor-dependent topology, or authorization field names inside steps
  rule: Execution topology steps must not declare fields that carry authority semantics (role, permissions, authorized_by, on_role, required_role, authorization, execution_rights); authority is evaluated before topology traversal begins and topology must not reproduce or replicate that surface
  scope:
    - CC

```

---

## Summary

Authority governance determines whether execution may exist. Execution topology governs
how execution proceeds once admitted. These are orthogonal planes. When topology steps
encode authority semantics — routing based on roles, branching on permissions, declaring
authorization requirements per step — the topology plane colonizes the authority plane,
collapsing two sovereign governance dimensions.

This is the topology-side complement of `ASSERT_IDENTITY_AUTHORITY_SEPARATION_V0` and
`ASSERT_ACTOR_AUTHORITY_SEPARATION_V0`. All three enforce orthogonality from their
respective surfaces.

## Rule

For every execution topology step in a CC pipeline:
1. Steps MUST NOT declare fields named to signal authority semantics:
   - `role`, `required_role`, `permissions`, `authorization`, `authorized_by`
   - `on_role`, `execution_rights`, `actor_type_gate`, `permission_check`
2. Steps MUST NOT declare routing that branches on actor identity or permission state
3. Steps MUST NOT reference authority registries, permission tables, or role databases
4. Topology variation based on actor type, role, or permission state is a constitutional violation

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

## Rationale

Authority semantics inside topology steps is the execution-plane equivalent of authorization
logic inside workflow steps. Both violate the orthogonality law by embedding authority
evaluation inside execution traversal. The pattern is seductive: "route this step differently
for admin actors." The consequence is a collapsed governance surface that cannot be evolved,
audited, or governed independently.

Authority is resolved before topology begins. Topology receives a binary: admitted or not.
It does not receive authority state for consumption.

This is a Phase 1 stub. Field name detection is implemented in Phase 3.
