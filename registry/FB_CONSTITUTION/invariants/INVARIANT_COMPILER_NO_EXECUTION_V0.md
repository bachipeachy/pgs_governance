# INVARIANT_COMPILER_NO_EXECUTION_V0

## Machine

```yaml
invariant_code: INVARIANT_COMPILER_NO_EXECUTION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_COMPILER_V0

core:
  description: >
    Compiled CT and CS artifacts MUST NOT carry execution-time state in their
    materialized frontmatter. Fields that only appear as the result of executing
    an artifact (trace_id, execution_result, runtime_output, invocation_id,
    execution_state, runtime_state) are forbidden in compiled artifact frontmatter.
    The compiler phase MUST NOT invoke CT or CS implementations — compiled artifacts
    are static declarations, not execution receipts.

  enforcement_stage:
    - compiler_assert

  scope:
    - ALL_BUILD_CONTEXTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - execution_state_in_frontmatter: "CT/CS artifact frontmatter contains trace_id, execution_result, or runtime_output"
    - compiler_invokes_ct: "Compiler phase calls CT implementation module during compilation"
    - compiler_invokes_cs: "Compiler phase calls CS implementation module during compilation"
    - execution_contamination: "Compiled artifact preserves side-effect outputs in its canonical form"
```

---

## Purpose

Enforces the compile-time purity boundary declared in §9 of CONSTITUTION_COMPILER_V0:
"Execution of protocol behavior during compilation" is a forbidden pattern.

CT and CS artifacts are pure declarations at compile time. A compiled artifact's
frontmatter must reflect the declared structure, not an execution output. If a compiled
CT artifact contains `execution_result` or `trace_id` fields, the compiler has violated
the boundary between compilation and execution.

This invariant is structural — it checks what is present in the compiled artifact, not
what the compiler did at runtime. It is checkable from the artifact alone.

## Relationship to CONSTITUTION_COMPILER_V0

Directly enforces §9 Forbidden Pattern #6 (`Execution of protocol behavior during
compilation`) and the CT Purity doctrine: CT implementations have zero side effects and
must never be invoked during compilation.
