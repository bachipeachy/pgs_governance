# SURFACE_CONTRACT_REGISTRY_DEREGISTER_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_REGISTRY_DEREGISTER_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for registry DEREGISTER operations.

A registry DEREGISTER operation can succeed, report that the key was not found, or fail
due to storage unavailability. Invalid input is caught upstream before reaching the DEREGISTER
operation. These three outcomes are exhaustive.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_REGISTRY_DEREGISTER_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: REGISTRY
op: DEREGISTER

canonical_surface:
  - SUCCESS
  - NOT_FOUND
  - BACKEND_ERROR

governs:
  - CS_REGISTRY_V0
```
