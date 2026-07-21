# INVARIANT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

## Machine

```yaml
invariant_code: INVARIANT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: Execution topology must not encode transport semantics — no HTTP routing, endpoint dispatch, transport conditions, or TE projection rules inside steps
  rule: Execution topology steps must not declare fields that carry transport semantics (http_method, endpoint, transport_target, response_code, content_type, headers, projection_rules); transport governs boundaries and topology governs traversal; these are orthogonal planes
  scope:
    - CC

```

---

## Summary

Transport governance controls how execution surfaces are exposed at boundaries — HTTP methods,
endpoints, projection visibility, response codes, and TE semantics. Execution topology
controls how capabilities are traversed inside a workflow. These are distinct governance
planes with separate lifecycles and separate consumers.

When topology steps encode transport semantics — routing based on HTTP method, dispatching
to endpoints, declaring response codes per step — the execution topology becomes coupled to
transport infrastructure. Changes to transport governance require topology changes, and
changes to topology potentially alter transport behavior.

## Rule

For every execution topology step in a CC pipeline:
1. Steps MUST NOT declare fields named to signal transport semantics:
   - `http_method`, `endpoint`, `transport_target`, `url`, `route`
   - `response_code`, `status_code`, `content_type`, `headers`
   - `projection_rules`, `visibility`, `te_binding`
2. Steps MUST NOT perform HTTP dispatch, transport routing, or endpoint resolution
3. Steps MUST NOT declare TE boundary conditions or projection visibility rules
4. Transport-conditional execution paths (e.g., "route differently for POST vs GET") are constitutional violations

## Enforcement Scope

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Enforced By**: ASSERT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

## Rationale

Transport orthogonality is one of the core architectural properties of PGS. The runtime
is transport-agnostic: the same workflow executes identically regardless of whether it was
invoked via HTTP, CLI, SDK, or another transport mechanism.

Embedding transport semantics inside execution topology steps destroys this property.
Once a step knows its transport context, the execution graph is no longer pure — it carries
transport state through the governance surface. This invariant prevents that collapse.

This is a Phase 1 stub. Field name detection is implemented in Phase 3.
