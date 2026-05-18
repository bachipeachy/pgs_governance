# ASSERT_FQDN_ONLY_REFERENCES_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_FQDN_ONLY_REFERENCES_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_FQDN_ONLY_REFERENCES_V0

implementation:
  module: pgs_governance.registry.handlers.assert_fqdn_only_references_v0
  callable: execute
```

## Summary

Validates that all artifact references use FQDN format (layer::artifact_code).

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All compiled artifacts

## Handler Behavior

For each compiled artifact:
1. Load Machine section
2. Extract reference fields: `governed_by`, `transform`, `structure`, `runtime_binding`
3. For each reference value:
   - Check if format matches `layer::artifact_code`
   - Fail if missing `::` separator
   - Fail if layer or artifact_code is empty

## Error Messages

```
❌ ASSERT_FQDN_ONLY_REFERENCES_V0: Short name reference detected
   Artifact: governance::CC_DISCOVER_ARTIFACTS_V0
   Field: pipeline[0].transform
   Value: "CT_SCAN_ARTIFACTS_V0"
   Required format: "transforms::CT_SCAN_ARTIFACTS_V0"
   Fix: Add layer prefix to all artifact references
```
