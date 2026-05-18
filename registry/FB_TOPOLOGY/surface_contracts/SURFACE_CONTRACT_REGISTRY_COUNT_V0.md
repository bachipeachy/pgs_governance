# SURFACE_CONTRACT_REGISTRY_COUNT_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_REGISTRY_COUNT_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for registry COUNT operations.

A registry COUNT operation either succeeds with a count or fails due to storage unavailability.
COUNT does not produce NOT_FOUND (the count of a missing key is 0, not an error) and does not
produce VIOLATION (COUNT takes no input that can be invalid). These two outcomes are exhaustive.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_REGISTRY_COUNT_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: REGISTRY
op: COUNT

canonical_surface:
  - SUCCESS
  - BACKEND_ERROR

governs:
  - CS_REGISTRY_V0
```
