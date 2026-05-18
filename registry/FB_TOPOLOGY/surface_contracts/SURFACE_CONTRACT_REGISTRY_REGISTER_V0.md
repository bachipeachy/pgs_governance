# SURFACE_CONTRACT_REGISTRY_REGISTER_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_REGISTRY_REGISTER_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for registry REGISTER operations.

A registry REGISTER operation can succeed, find the key already registered, encounter an
invalid input, or fail due to storage unavailability. These four outcomes are exhaustive —
no other result codes may be declared in a step's result_surface when the step binds a
registry capability with REGISTER operation.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_REGISTRY_REGISTER_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: REGISTRY
op: REGISTER

canonical_surface:
  - SUCCESS
  - ALREADY_EXISTS
  - VIOLATION
  - BACKEND_ERROR

governs:
  - CS_REGISTRY_V0
```
