# ASSERT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

implementation:
  module: pgs_governance.registry.handlers.assert_topology_transport_orthogonal_v0
  callable: execute
```

## Summary

Execution topology steps must not encode transport semantics. This assertion detects
transport-semantic field names inside CC pipeline steps — HTTP methods, endpoints, response
codes, headers, projection rules. Topology that encodes transport semantics couples
execution traversal to transport infrastructure, destroying transport orthogonality.

## Rule

For every CC execution topology step:
1. Steps MUST NOT declare transport-semantic fields:
   - `http_method`, `endpoint`, `transport_target`, `url`, `route`
   - `response_code`, `status_code`, `content_type`, `headers`
   - `projection_rules`, `visibility`, `te_binding`
2. Steps MUST NOT dispatch to HTTP endpoints or perform transport routing
3. Steps MUST NOT declare TE boundary conditions or projection visibility rules

## Enforcement

- **Artifact Types**: CC
- **Validation Phase**: compile_time
- **Handler**: `pgs_governance.registry.handlers.assert_topology_transport_orthogonal_v0`
- **Paired Invariant**: INVARIANT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

## Rationale

Transport orthogonality is a core PGS architectural property: the same workflow executes
identically regardless of transport mechanism. Topology steps that reference transport
semantics break this property — the execution graph becomes coupled to the transport
context, and the runtime can no longer be transport-agnostic.

Transport governance controls boundaries. Execution topology controls traversal.
These are orthogonal planes with separate lifecycles.

Enforced at compile time: detects transport-semantic field names (`http_method`, `endpoint`, `response_code`, `headers`, etc.) inside CC pipeline steps.
