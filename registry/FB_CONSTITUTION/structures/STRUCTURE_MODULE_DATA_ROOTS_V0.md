# STRUCTURE_MODULE_DATA_ROOTS_V0

## Machine

```yaml
structure_code: STRUCTURE_MODULE_DATA_ROOTS_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Module data roots and directory structure
  description: >
    Defines canonical directory names and module data roots aligned with
    current platform repository structure.

layer_directories:
  compiled_root: compiled
  compiled_artifacts: compiled/artifacts
  execution_machine_subdir: machine
  execution_host_subdir: host
  execution_conformance_subdir: conformance
  vocabulary_reserved_subdir: FB_VOCABULARY/reserved
  schemas_subdir: registry/FB_CONSTITUTION/schemas
  tooling_experimental_subdir: experimental

module_data_roots:
  governance:
    _type: path
    value: pgs_governance/registry
  compiler:
    _type: path
    value: pgs_compiler/compiler
  transforms:
    _type: path
    value: pgs_transforms/implementation/transforms
  side_effects:
    _type: path
    value: pgs_side_effects/implementation/side_effects
  execution:
    _type: path
    value: pgs_execution/execution
  structure:
    _type: path
    value: pgs_structure/structure
  tooling:
    _type: path
    value: pgs_tooling
  ingress:
    _type: path
    value: pgs_ingress/ingress
  egress:
    _type: path
    value: pgs_egress/egress

module_data_roots_lifecycle:
  governance:
    _type: lifecycle
    value: human
  compiler:
    _type: lifecycle
    value: compiler
  transforms:
    _type: lifecycle
    value: compiler
  side_effects:
    _type: lifecycle
    value: compiler
  execution:
    _type: lifecycle
    value: runtime
  structure:
    _type: lifecycle
    value: runtime
  tooling:
    _type: lifecycle
    value: human
  ingress:
    _type: lifecycle
    value: runtime
  egress:
    _type: lifecycle
    value: runtime

directory_lifecycle:
  compiled:
    _type: lifecycle
    value: compiler
  testbed:
    _type: lifecycle
    value: human
  conformance:
    _type: lifecycle
    value: compiler

output_configuration:
  _type: metadata
```
