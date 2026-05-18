# SURFACE_CONTRACT_REGISTRY_RESOLVE_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_REGISTRY_RESOLVE_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for registry READ (resolve/lookup) operations.

A registry READ operation can succeed with the resolved record, report that the key is not
registered, encounter an invalid input, or fail due to storage unavailability. These four
outcomes are exhaustive.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_REGISTRY_RESOLVE_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: REGISTRY
op: READ

canonical_surface:
  - SUCCESS
  - NOT_FOUND
  - VIOLATION
  - BACKEND_ERROR

governs:
  - CS_REGISTRY_V0
```
