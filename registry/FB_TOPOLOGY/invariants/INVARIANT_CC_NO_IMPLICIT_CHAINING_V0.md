# INVARIANT_CC_NO_IMPLICIT_CHAINING_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_NO_IMPLICIT_CHAINING_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    CC must not contain orchestration logic or flow control.
    CCs define ONLY capability pipelines (CT/CS bindings).
    Workflow orchestration belongs in WF artifacts, not CC.

    Forbidden fields:
    - next_step (implicit chaining)
    - next (state transitions)
    - transitions (workflow logic)
    - flow (control flow)
    - conditional (branching logic)
    - loop (iteration control)

    CC defines WHAT capability to invoke, WF defines WHEN and in what ORDER.

  enforcement_stage:
    - compiler_validation

  scope:
    - CAPABILITY_CONTRACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - next_step_field: "CC contains next_step field (implicit chaining)"
    - next_field: "CC contains next field (state transitions)"
    - transitions_field: "CC contains transitions field (workflow logic)"
    - flow_field: "CC contains flow field (control flow)"
    - conditional_field: "CC contains conditional field (branching logic)"
    - loop_field: "CC contains loop field (iteration control)"

  clarification:
    cc_responsibility: >
      CC is a capability wrapper, not a workflow fragment.
      It binds inputs to CT/CS, produces outputs, and stops.
      No knowledge of what happens next, no control flow.
    wf_responsibility: >
      WF controls execution flow via nodes graph.
      CC nodes reference CCs, WF decides transitions.
      Clean separation: WF = orchestration, CC = capability.
```

---

## Purpose

Enforce architectural separation: CC defines capability, WF defines execution flow.

**Core Principle**: CC has zero knowledge of execution context or next steps.

---

## Validation Rules

### Rule 1: No Explicit Chaining

CC must not contain `next_step` field.

**Violation**:
```yaml
# ❌ FORBIDDEN
pipeline:
  - step: validate
    transform: CT_VALIDATE_V0
next_step: CC_PROCESS_V0  # ❌ Implicit chaining
```

**Correct**:
```yaml
# ✅ CC defines capability only
pipeline:
  - step: validate
    transform: CT_VALIDATE_V0
    # No next_step - WF controls flow
```

**Detection**: Check for `next_step` field in CC frontmatter.

---

### Rule 2: No State Transitions

CC must not contain `next` field (workflow construct).

**Violation**:
```yaml
# ❌ FORBIDDEN
pipeline:
  - step: process
    transform: CT_PROCESS_V0
next:  # ❌ State transitions
  SUCCESS: CC_FINALIZE_V0
  VIOLATION: CC_ERROR_V0
```

**Detection**: Check for `next` field in CC frontmatter or pipeline steps.

---

### Rule 3: No Transition Logic

CC must not contain `transitions` field.

**Violation**:
```yaml
# ❌ FORBIDDEN
transitions:  # ❌ Workflow logic
  - from: validate
    to: process
    condition: valid
```

**Detection**: Check for `transitions` field in CC frontmatter.

---

### Rule 4: No Control Flow

CC must not contain `flow`, `conditional`, or `loop` fields.

**Violation**:
```yaml
# ❌ FORBIDDEN
flow:  # ❌ Control flow
  type: conditional
  condition: $.inputs.flag
  true_path: CC_A_V0
  false_path: CC_B_V0
```

**Detection**: Check for `flow`, `conditional`, `loop` fields.

---

## Scope

**Applies to**:
- All CC artifacts (platform + domains)
- CC frontmatter section
- CC pipeline steps

**Does NOT validate**:
- Pipeline correctness (Phase 3)
- Input/output availability (Phase 5)
- CT/CS binding validity (Phase 3)

---

## Rationale

**Clean architectural boundaries**

### Separation of Concerns
- CC = pure capability wrapper
- WF = execution orchestrator
- No overlap, no ambiguity

### Maintainability
- Change workflow flow → edit WF only
- Change capability logic → edit CT/CS only
- CC remains stable interface

### Composability
- Same CC used in multiple workflows
- No workflow-specific logic in CC
- True reusability

### Debugging
- Execution trace shows WF decisions
- CC invocation is pure function call
- Clear cause/effect chain

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC No Implicit Chaining
