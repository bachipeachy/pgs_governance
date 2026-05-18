# SURFACE_CONTRACT_STORAGE_APPENDONLY_APPEND_V0

## Header

- **Artifact Code:** SURFACE_CONTRACT_STORAGE_APPENDONLY_APPEND_V0
- **Artifact Kind:** surface_contract
- **Governed By:** fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
- **Version:** V0
- **Status:** canonical

---

## Purpose

Canonical result surface for append-only storage APPEND operations.

An append-only APPEND can succeed, encounter invalid input (malformed record), or fail
due to storage unavailability. APPEND does not produce NOT_FOUND or ALREADY_EXISTS —
append-only storage grows monotonically. These three outcomes are exhaustive.

---

## Machine

```yaml
surface_contract_code: SURFACE_CONTRACT_STORAGE_APPENDONLY_APPEND_V0
artifact_kind: SURFACE_CONTRACT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

capability_family: STORAGE_APPENDONLY
op: APPEND

canonical_surface:
  - SUCCESS
  - VIOLATION
  - BACKEND_ERROR

governs:
  - CS_APPENDONLY_JSONL_V0
```
