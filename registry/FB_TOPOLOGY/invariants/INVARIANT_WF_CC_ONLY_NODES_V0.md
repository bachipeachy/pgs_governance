# INVARIANT_WF_CC_ONLY_NODES_V0

## Machine

```yaml
invariant_code: INVARIANT_WF_CC_ONLY_NODES_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    All non-structural WF nodes must be of type CC. Structural nodes (IN, EXIT)
    are permitted. Direct CT or CS node references in a workflow are forbidden —
    they must be encapsulated inside a CC artifact.

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - ct_node_in_wf: "Workflow node of type CT — CT must be invoked from within a CC"
    - cs_node_in_wf: "Workflow node of type CS — CS must be invoked from within a CC"
    - unknown_node_type: "Workflow node with unrecognized type"

  clarification:
    structural_nodes: >
      IN and EXIT are structural nodes, not capability nodes. They are always
      permitted in a workflow regardless of this invariant.
    cc_encapsulation: >
      CTs and CSs are invoked by capability contracts (CCs). The workflow
      orchestrates CCs; it does not reach into implementation details.
```

---

## Purpose

Enforce the WF → CC → CT/CS layering. Workflows orchestrate; capability contracts implement.

---

## Validation Rules

### Rule: All Non-Structural Nodes Are CC

For each node in the WF nodes map, if type is not IN or EXIT, it must be CC.

**Violation**:
```yaml
nodes:
  entry:
    type: IN
  CT_TRANSFORM_V0:       # WRONG — CT cannot be a workflow node
    type: CT
  exit:
    type: EXIT
```

**Detection**: Check type field of every node. Reject CT, CS, or unknown types.

---

## Scope

**Applies to**: All WF artifacts (platform + domains)

**Does NOT restrict**: CC artifacts invoking CTs and CSs internally

---

## Version History

- **V0**: Initial implementation (2026-05-04)
