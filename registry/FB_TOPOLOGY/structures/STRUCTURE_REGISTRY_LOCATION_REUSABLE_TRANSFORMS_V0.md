# STRUCTURE_REGISTRY_LOCATION_REUSABLE_TRANSFORMS_V0

Registry location declaration for REUSABLE_TRANSFORMS layer.

## Header

- **Artifact Code:** STRUCTURE_REGISTRY_LOCATION_REUSABLE_TRANSFORMS_V0
- **Artifact Kind:** structure
- **Governed By:** fb.constitution::CONSTITUTION_STRUCTURE_V0
- **Version:** V0
- **Status:** canonical
- **Authority:** foundational

---

## Purpose

Declares the physical registry module location for REUSABLE_TRANSFORMS layer artifacts. This artifact enables federated ownership of registry locations while maintaining deterministic resolution.

**Constitutional Rule**: Each layer owns exactly one registry location artifact.

---

## Machine

```yaml
structure_code: STRUCTURE_REGISTRY_LOCATION_REUSABLE_TRANSFORMS_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  layer_code: REUSABLE_TRANSFORMS
  registry_module: pgs_transforms.registry
  module_path_pattern: "{registry_module}"

  description: >
    Platform capability transforms (CT artifacts).
    Pure, deterministic, side-effect-free functions.

  notes: >
    Pattern-based resolution: module_path_pattern defines how to compose registry path.
    No domain composition for platform transforms layer.

output_configuration:
  artifacts_path:
    layer: REUSABLE_TRANSFORMS
    subpath: compiled/artifacts

  molecules_path:
    layer: REUSABLE_TRANSFORMS
    subpath: compiled/molecules
```

---

## Usage

Loaded by artifact discovery during build:

1. Discovery reads `STRUCTURE_LAYER_AUTHORITY_V0` → enumerates layers
2. For REUSABLE_TRANSFORMS layer → loads this artifact
3. Extracts `registry_module: pgs_transforms.registry`
4. Scans that module for protocol artifacts

---

## Version History

- **V0**: Initial federated registry location (2026-03-25)
  - Extracted from central STRUCTURE_LAYER_REGISTRY_LOCATIONS_V0
  - REUSABLE_TRANSFORMS layer now owns its registry location
  - Moved to central pgs_governance namespace (2026-03-26)
