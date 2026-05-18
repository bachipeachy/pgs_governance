# ASSERT_IN_WORKFLOW_BINDING_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_IN_WORKFLOW_BINDING_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_IN_WORKFLOW_BINDING_V0

implementation:
  module: pgs_governance.registry.handlers.assert_in_workflow_binding_v0
  callable: execute
```

## Summary

Validates that every IN artifact declares a resolvable workflow binding:
1. IN artifact must declare core.workflow pointing to a valid WF artifact
2. Each workflow may be bound by at most one IN artifact (one-to-one)

Note: The binding is declared on the IN side (IN.core.workflow = WF FQDN).
WF node names (e.g. "entry") are structural graph labels, not IN artifact references.

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All IN artifacts, all WF artifacts

## Handler Behavior

### 1. Check Workflow Declaration

For each IN artifact, verify core.workflow is declared.

Violation: core.workflow missing.

### 2. Check Workflow Resolution

Verify core.workflow resolves to a declared WF artifact (bare code or FQDN).

Violation: WF reference not found in compilation graph.

### 3. Check Uniqueness

Verify no two IN artifacts declare the same core.workflow target.

Violation: Multiple IN artifacts bound to same workflow.

## Error Messages

### Shared Entry Intent
```
❌ ASSERT_IN_WORKFLOW_BINDING_V0: Entry intent used by multiple workflows
   IN: IN_REGISTER_V0
   WFs: [WF_REGISTER_ACTOR_V0, WF_REGISTER_DEVICE_V0]
   Violation: IN artifact must be bound to exactly one workflow
   Fix: Create separate IN artifacts for each workflow
```

### Unresolvable IN Reference
```
❌ ASSERT_IN_WORKFLOW_BINDING_V0: Unresolvable entry intent
   WF: WF_EXAMPLE_V0
   IN: IN_MISSING_V0
   Violation: IN artifact not found in compilation graph
   Fix: Add IN artifact or fix reference
```

## Rationale

Intent artifacts are workflow-specific admission gates. Sharing a single intent
across multiple workflows creates ambiguous routing and weakens the admission
model. Each workflow requires its own dedicated entry intent.

## Version History

- **V0**: Initial implementation (2026-05-04)
