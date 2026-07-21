# INVARIANT_TRANSPORT_NO_DYNAMIC_ROUTING_V0

## Machine

```yaml
invariant_code: INVARIANT_TRANSPORT_NO_DYNAMIC_ROUTING_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Transport routing MUST be static and explicit. No conditional routing logic,
    dynamic target resolution, or runtime dispatch declarations are permitted
    in TI_ or TE_ artifacts.

    Transport is a static binding layer. Routing decisions are made at compile time,
    not at runtime. Any routing that requires inspection of runtime context,
    payload values, or dynamic references collapses the transport/execution
    separation and is forbidden.

  enforcement_stage:
    - compiler_validation

  scope:
    - TRANSPORT_INGRESS
    - TRANSPORT_EGRESS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - conditional_workflow_selection: >
        TI declares if/else or match routing to select between workflows
    - dynamic_workflow_reference: >
        TI core.workflow uses a $ prefix (runtime-computed reference)
    - wildcard_routing: >
        Transport artifact uses * or ? in routing declarations
    - runtime_dispatch_key: >
        Transport artifact declares route_by, dispatch, switch, or when keys
    - payload_dependent_routing: >
        Routing target is determined by inspecting payload field values at runtime
```

---

## Purpose

Transport artifacts are compile-time declarations. The routing from transport
ingress to execution workflow is fully resolved at compile time and stored in
the snapshot. Runtime has no routing decisions to make — it reads the static
binding and executes it.

This invariant ensures that transport remains a pure static membrane, not a
routing engine.

---

## Scope

**Applies to:** All TI_ and TE_ artifacts

**Does NOT apply to:**
- Outcome routing within a CC node (that is execution semantics)
- Workflow-internal DAG branching (governed by WF assertions)
