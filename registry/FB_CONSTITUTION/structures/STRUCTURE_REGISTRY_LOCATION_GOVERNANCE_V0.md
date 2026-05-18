# STRUCTURE_REGISTRY_LOCATION_GOVERNANCE_V0

Registry location declaration for GOVERNANCE layer.

## Header

- **Artifact Code:** STRUCTURE_REGISTRY_LOCATION_GOVERNANCE_V0
- **Artifact Kind:** structure
- **Governed By:** fb.constitution::CONSTITUTION_STRUCTURE_V0
- **Version:** V0
- **Status:** canonical
- **Authority:** foundational

---

## Purpose

Declares the physical registry module location for GOVERNANCE layer artifacts. This artifact enables federated ownership of registry locations while maintaining deterministic resolution.

**Constitutional Rule**: Each layer owns exactly one registry location artifact.

---

## Machine

```yaml
structure_code: STRUCTURE_REGISTRY_LOCATION_GOVERNANCE_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  layer_code: GOVERNANCE
  registry_module: pgs_governance.registry
  module_path_pattern: "{registry_module}"

  description: >
    Core platform governance artifacts (VOCAB, CONSTITUTION, STRUCTURE, SCHEMA).
    Sovereign authority layer for protocol governance.

  notes: >
    Pattern-based resolution: module_path_pattern defines how to compose registry path.
    No domain composition for platform governance layer.

output_configuration:
  artifacts_path:
    layer: GOVERNANCE
    subpath: compiled/artifacts

  conformance_path:
    layer: GOVERNANCE
    subpath: compiled/conformance

  vocabulary_path:
    layer: GOVERNANCE
    subpath: vocabulary/compiled
```

---

## Usage

Loaded by artifact discovery during build:

1. Discovery reads `STRUCTURE_LAYER_AUTHORITY_V0` → enumerates layers
2. For GOVERNANCE layer → loads this artifact
3. Extracts `registry_module: pgs_governance.governance`
4. Scans that module for protocol artifacts

---

## Version History

- **V0**: Initial federated registry location (2026-03-25)
  - Extracted from central STRUCTURE_LAYER_REGISTRY_LOCATIONS_V0
  - GOVERNANCE layer now owns its registry location
