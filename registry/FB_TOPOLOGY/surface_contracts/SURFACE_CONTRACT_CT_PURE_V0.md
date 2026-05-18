# SURFACE_CONTRACT_CT_PURE_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_CT_PURE_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for pure capability transforms (CT_PURE_*).

A pure transform either succeeds or encounters a VIOLATION. Pure transforms are stateless,
have no backend dependency, and cannot produce BACKEND_ERROR or NOT_FOUND. The binary
success/violation surface is the semantic contract of the CT_PURE family.

This contract governs all capabilities whose identifier begins with `CT_PURE_`. It applies
to steps with a `transform:` binding (no `side_effect:`).

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_CT_PURE_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: CT_PURE
op: TRANSFORM

canonical_surface:
  - SUCCESS
  - VIOLATION

capability_id_prefix: CT_PURE_
governs: []
```
