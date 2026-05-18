# CONSTITUTION_EXECUTION_TOPOLOGY_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
constitution_code: CONSTITUTION_EXECUTION_TOPOLOGY_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  description: Governs the execution topology surface of Capability Contract artifacts — explicit step declaration, deterministic routing, dataflow closure, and governance plane orthogonality
  scope: artifact
  governs:
    - CC
  enforcement_model: compiler_enforced

doctrine: Execution topology governs traversal structure only. Execution topology validation is structural, not semantic. Workflow authors MAY route surfaces. Workflow authors MAY NOT define capability semantics.

rules:
  - rule_id: TOPOLOGY_STEP_DECLARED
    applies_to: CC
    constraint: every execution topology step MUST be fully and explicitly declared; implicit steps, wildcard references, and ambient dataflow are constitutional violations
    enforced_by: ASSERT_TOPOLOGY_STEP_DECLARED_V0

  - rule_id: TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE
    applies_to: CC
    constraint: each execution topology step MUST reference exactly one capability — exactly one of transform or side_effect, not both, not neither
    enforced_by: ASSERT_TOPOLOGY_CAPABILITY_REFERENCE_UNIQUE_V0

  - rule_id: TOPOLOGY_INPUT_REFERENCE_DECLARED
    applies_to: CC
    constraint: all step input references to prior step outputs MUST resolve to a declared step ID within the same pipeline; forward references and dangling references are constitutional violations
    enforced_by: ASSERT_TOPOLOGY_INPUT_REFERENCE_DECLARED_V0

  - rule_id: TOPOLOGY_ROUTING_COMPLETE
    applies_to: CC
    constraint: every step MUST declare a result_surface and on_result MUST declare routing for every status code in that step's result_surface; unrouted surface codes constitute ungoverned execution paths
    enforced_by: ASSERT_TOPOLOGY_ROUTING_COMPLETE_V0

  - rule_id: TOPOLOGY_CONTRACT_CLOSED
    applies_to: CC
    constraint: the union of all status codes that can exit the CC execution topology (via step exit routes, last-step continue routes, and evaluation outcomes) MUST exactly match result_status_contract.allowed; uncontracted exits and unreachable contract codes are constitutional violations
    enforced_by: ASSERT_TOPOLOGY_CONTRACT_CLOSED_V0

  - rule_id: TOPOLOGY_STEP_ID_UNIQUE
    applies_to: CC
    constraint: step IDs MUST be unique within a CC execution topology; duplicate step IDs create ambiguous dataflow identity and are constitutional violations
    enforced_by: ASSERT_TOPOLOGY_STEP_ID_UNIQUE_V0

  - rule_id: TOPOLOGY_AUTHORITY_ORTHOGONAL
    applies_to: CC
    constraint: execution topology MUST NOT encode authority semantics — no role branching, permission routing, actor-dependent topology, or authorization field names inside steps
    enforced_by: ASSERT_TOPOLOGY_AUTHORITY_ORTHOGONAL_V0

  - rule_id: TOPOLOGY_TRANSPORT_ORTHOGONAL
    applies_to: CC
    constraint: execution topology MUST NOT encode transport semantics — no HTTP routing, endpoint dispatch, transport conditions, or TE projection rules inside steps
    enforced_by: ASSERT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0

  - rule_id: TOPOLOGY_IMMUTABLE_AFTER_COMPILATION
    applies_to: CC
    constraint: compiled execution topology MUST NOT be modified, extended, or overridden at runtime; the compiled step sequence and routing declarations are immutable for the lifetime of the compiled artifact
    enforced_by: ASSERT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0

  - rule_id: NO_RUNTIME_TOPOLOGY_SYNTHESIS
    applies_to: CC
    constraint: execution topology MUST NOT be synthesized, generated, or inferred at runtime from payload content, authority grants, environment state, or any form of runtime inference
    enforced_by: ASSERT_NO_RUNTIME_TOPOLOGY_SYNTHESIS_V0

  - rule_id: TOPOLOGY_SURFACE_CANONICAL
    applies_to: CC
    constraint: every step's result_surface MUST exactly match the canonical_surface declared by the governing SURFACE_CONTRACT for that step's capability and operation; workflow authors MAY route surfaces, workflow authors MAY NOT define capability semantics
    enforced_by: ASSERT_TOPOLOGY_SURFACE_CANONICAL_V0
```

---

## Foundational Doctrine

**Execution topology is compile-time governed graph structure, not runtime orchestration intelligence.**

Execution topology governs:
- Admissible traversal: which capabilities execute in what declared sequence
- Deterministic step sequencing: order and dataflow are fully declared before runtime begins
- Explicit dependency closure: all step inputs resolve to declared sources at compile time

Execution topology does NOT govern:
- Authority evaluation (authority governance plane)
- Transport boundary admission (transport governance plane)
- Identity declaration (identity governance plane)
- Trace accountability (post-execution trace plane)

The four governance planes remain orthogonal. Topology is execution-only.

**Capability semantics are governed by protocol, not by workflow authors.**
Workflow authors declare routing (`on_result`). They do not define what result codes a
capability can produce. The canonical surface of each capability family is declared once
in a SURFACE_CONTRACT and enforced at compile time across all CCs that bind that capability.

---

## §1. Canonical Step Structure

Every execution topology step must conform to the following canonical shape:

```yaml
- step: <step_id>           # unique string identifier within this CC
  transform: <CT_FQDN>      # exactly one of: transform (CT) or side_effect (CS)
  op: <OPERATION>           # operation name bound to the CT or CS
  inputs: {...}             # explicit JSONPath bindings ($.inputs.* or $.results.<step_id>.*)
  outputs: {...}            # explicit output field bindings from capability result
  on_ct_result:             # capability-level result mapping
    on_success: <STATUS>
    on_failure: <STATUS>
  result_surface: [SUCCESS, VIOLATION]   # codes this step's capability can produce
  on_result:                # step routing — must cover all codes in result_surface
    SUCCESS: continue | exit
    VIOLATION: continue | exit
```

Step structure is self-describing. Each step declares:
1. **Identity** — unique `step` identifier (becomes dataflow address for downstream steps)
2. **Capability binding** — exactly one CT or CS
3. **Input contracts** — all inputs explicitly bound to CC inputs or prior step outputs
4. **Output contracts** — all outputs explicitly mapped from capability result
5. **Capability surface** — `result_surface` declares the codes this step's capability can produce
6. **Routing** — all surface codes explicitly routed (continue, exit, or evaluation target)

---

## §2. Step-Local Semantics

Bindings are step-local. There is no global binding registry, no centralized orchestration
map, and no hidden routing table.

Each step's inputs reference only:
- `$.inputs.*` — CC-level input fields
- `$.results.<step_id>.*` — outputs of a previously declared step

No ambient state. No implicit variable scope. No context injection from outside the step.

This is the canonical architecture. Do not regress toward centralized binding maps.

---

## §3. Compile-Time Graph Closure

All execution paths must exist before runtime begins. This means:

- All step IDs referenced in `$.results.*` bindings must resolve to declared steps
- All status codes in a step's `result_surface` must appear in that step's `on_result`
- The union of all CC exit codes (step exits, last-step continues, evaluation outcomes) must equal `result_status_contract.allowed`
- No step may reference a step declared after it in sequence (no forward references to results)
- No step may be unreachable (all topology closure validated at compile time)

Runtime must receive a fully closed topology graph. Runtime is a traversal engine.
It does not discover, repair, or extend topology.

---

## §4. Routing Semantics

`on_result` is declarative and finite. It maps result status codes to exactly two routing
outcomes: `continue` (next step) or `exit` (terminate CC with that status).

`on_result` MUST NOT:
- Use nested evaluation logic
- Reference arbitrary conditions or expressions
- Introduce recursive routing
- Use dynamic predicates or runtime-evaluated values

Routing is bounded. It is a lookup table, not an expression evaluator.

---

## §5. Orthogonality Constraints

### Authority Orthogonality

Execution topology may consume the outcome of authority evaluation (admissibility result)
but may not:
- Branch on role, permission, or actor type
- Reference authorization databases or permission registries
- Declare execution paths that vary by authority state
- Encode authorization logic in step fields

Authority is evaluated before topology traversal begins. Topology assumes admissibility
has already been resolved.

### Transport Orthogonality

Execution topology may not encode:
- HTTP methods, endpoints, or transport targets
- TE boundary conditions or projection rules
- Transport-level routing or dispatch logic

Transport governs boundaries. Topology governs traversal. These are orthogonal planes.

---

## §6. Forbidden Patterns

The following constitute execution topology violations:

- Implicit step chaining (step order inferred from field names, not explicit sequence)
- Wildcard input bindings (`$.results.*` without step ID)
- Missing `result_surface` declaration on any pipeline step
- Missing `on_result` coverage (surface codes without routing)
- CC exit surface that does not match `result_status_contract.allowed`
- Duplicate `step` identifiers within a pipeline
- Multiple capability bindings per step (`transform` and `side_effect` both present)
- Authority-semantic field names inside steps (`role`, `permissions`, `authorized_by`, `on_role`)
- Transport-semantic field names inside steps (`http_method`, `endpoint`, `transport_target`)
- Expression evaluators or scripting constructs inside `on_result`
- `result_surface` that differs from the canonical_surface declared by the governing SURFACE_CONTRACT

---

## §7. V0 Scope

V0 topology governance formalizes existing practice. It does not introduce new topology
primitives. Current execution topology features (single-capability steps, explicit JSONPath
bindings, declarative on_result routing) are the complete V0 surface.

Future topology evolution (molecules as step primitives, loop steps, parallel step groups,
topology fingerprints) is explicitly deferred to future versions. V0 governs current reality.

---

## End of Constitution
