# CONSTITUTION_EXECUTION_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_EXECUTION_V0
constitution_code: CONSTITUTION_EXECUTION_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs workflow execution semantics — phases, dispatch, determinism, and error propagation
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: EXECUTION_PHASE_ORDER
    applies_to: system
    constraint: execution MUST proceed through phases INTERPRET→ADMIT→DISPATCH→EVALUATE→EXIT in order; no phase may be skipped
    enforced_by: TBD

  - rule_id: EXECUTION_NO_BUSINESS_LOGIC
    applies_to: system
    constraint: execution MUST NOT encode business rules or domain logic
    enforced_by: TBD

  - rule_id: EXECUTION_NO_SILENT_FAILURE
    applies_to: system
    constraint: all violations MUST emit explicit trace; no silent failures or swallowed exceptions
    enforced_by: TBD

  - rule_id: EXECUTION_DECLARED_SIDE_EFFECTS_ONLY
    applies_to: system
    constraint: side effects MUST only occur through declared CS artifacts
    enforced_by: TBD

  - rule_id: EXECUTION_DETERMINISM
    applies_to: system
    constraint: given identical inputs and policy, execution MUST produce identical trace
    enforced_by: TBD
```

---

## §1. Purpose

Define the execution semantics for OmniBachi protocol interpretation.

Execution is a **protocol interpreter**, not a behavior author.

Execution code SHALL:
- Interpret constitutions
- Enforce schemas
- Dispatch capabilities
- Emit mandated trace

Execution code SHALL NOT:
- Encode business rules
- Make policy decisions
- Implement domain logic
- Define trace structure

---

## §2. Execution Phases

All workflow execution proceeds through exactly five phases:

| Phase | Responsibility | Governance |
|-------|---------------|------------|
| INTERPRET | Parse DAG from workflow artifact | SCHEMA_EXECUTION_DAG_V0 |
| ADMIT | Enforce pre-DAG preconditions | fb.transport::CONSTITUTION_ADMISSION_V0 |
| DISPATCH | Route nodes to capability executors | fb.topology::CONSTITUTION_EXECUTION_V0 |
| EVALUATE | Execute capability and collect result | Capability Contract |
| EXIT | Terminate with success/failure + trace | CONSTITUTION_TRACE_EXECUTION_V0 |

No phase may be skipped. No phase may execute out of order.

---

## §3. Determinism Guarantees

| Property | Requirement |
|----------|-------------|
| Replay | Given identical inputs and policy, execution produces identical trace |
| Ordering | DAG dependencies determine execution order; no implicit parallelism |
| Side Effects | Only through declared Capability Side Effects (CS_*) |
| Randomness | Forbidden unless capability explicitly declares non-determinism |

---

## §4. Policy Enforcement Boundary

Execution behavior varies only by loaded policy profile.

Policy profiles are defined in CONSTITUTION_EXECUTION_POLICY_V0.

Policy is loaded at execution start. Policy cannot change mid-execution.

---

## §5. Machine Classes

### §5.1 Basic Machine (OSS)

- Deterministic execution
- DAG enforcement
- Capability dispatch
- Minimal trace
- No replay guarantees

### §5.2 Advanced Machine (Licensed)

- All Basic Machine capabilities
- Full trace with hash chain
- Guaranteed replay
- Audit trail
- Encrypted execution option
- AOT compilation hooks

Same codebase. Different policy profile.

---

## §6. Capability Dispatch Rules

1. Node type determines dispatcher (Intent vs Capability Contract)
2. Capability Contract specifies transforms (CT_*) and side effects (CS_*)
3. Transforms execute in declared order
4. Side effects execute after all transforms complete
5. Results propagate via execution context

---

## §7. Error and Violation Propagation

| Condition | Action |
|-----------|--------|
| Schema violation | ABORT execution, emit violation trace |
| Capability failure | Mark node FAILED, propagate to dependents |
| Policy violation | ABORT execution, emit violation trace |
| Unhandled exception | ABORT execution, emit error trace |

No silent failures. No swallowed exceptions.

---

## §8. Exit Conditions

Execution terminates when:
- All terminal nodes complete (SUCCESS)
- Any node fails with no recovery path (FAILURE)
- Policy violation detected (ABORT)
- Timeout exceeded (TIMEOUT)

Exit MUST emit terminal trace event with:
- Exit condition
- Final execution context hash
- Duration

---

## §9. Trace Obligations

Trace is not optional. Trace is **obligated**.

Minimum required events (BASIC):
- `execution_start`
- `node_start` (each node)
- `node_end` (each node)
- `workflow_complete`

Full events (ADVANCED): See CONSTITUTION_TRACE_EXECUTION_V0.

---

## §10. Forbidden Patterns

The following are constitutional violations:

- Hardcoded policy in Python
- Implicit feature flags
- Trace events defined in code (not schema)
- Business logic in executor
- Dynamic capability discovery
- Undeclared side effects
- Silent error handling

---

## §11. Implementation Constraints

| Metric | Target |
|--------|--------|
| Total SLOC | ≤1,000 |
| Files | ≤10 |
| Circular imports | 0 |
| Policy in Python | 0 lines |

Execution is a thin interpreter. Governance is the authority.

---

## §12. Versioning

Changes to this constitution require:
- New version (CONSTITUTION_EXECUTION_V1)
- Migration path documented
- All dependent schemas updated

No backward compatibility assumed.
