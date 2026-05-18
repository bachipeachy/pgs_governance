# SURFACE_CONTRACT_STORAGE_WRITE_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_STORAGE_WRITE_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for mutable storage WRITE operations.

A storage WRITE can succeed, encounter invalid input, or fail due to storage unavailability.
WRITE does not produce NOT_FOUND — a write operation creates or overwrites the document.
These three outcomes are exhaustive across all mutable storage capabilities.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_STORAGE_WRITE_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: STORAGE
op: WRITE

canonical_surface:
  - SUCCESS
  - VIOLATION
  - BACKEND_ERROR

governs:
  - CS_MUTABLE_JSON_V0
  - CS_NAME_REGISTRY_V0
```
