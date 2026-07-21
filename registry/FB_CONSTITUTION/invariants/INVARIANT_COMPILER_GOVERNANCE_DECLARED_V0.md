# INVARIANT_COMPILER_GOVERNANCE_DECLARED_V0

## Machine

```yaml
invariant_code: INVARIANT_COMPILER_GOVERNANCE_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_COMPILER_V0

core:
  description: >
    CONSTITUTION_COMPILER_V0 MUST be present in every compiled artifact set.
    Its machine block MUST declare a non-empty rules list that includes the
    governing constraints for the compiler pipeline. The compiler constitution
    is a static governance declaration — not an execution instruction set.
    Absence of the constitution from the compiled set violates COMPILER_SELF_APPLICABLE.

  enforcement_stage:
    - compiler_assert

  scope:
    - ALL_BUILD_CONTEXTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_constitution: "CONSTITUTION_COMPILER_V0 absent from compiled artifact set"
    - empty_rules: "CONSTITUTION_COMPILER_V0 machine block has no declared rules"
    - runtime_phase_discovery: "Compiler reads its own governance artifacts to determine execution order at runtime"
```

---

## Purpose

Enforces `COMPILER_SELF_APPLICABLE` from CONSTITUTION_COMPILER_V0: the compiler must
be capable of validating its own governance artifacts, which requires those artifacts to
be present in the compiled set.

The phase sequence and compiler rules are governance declarations — they live in the
constitution as static constraints that conforming compilers must satisfy. They are NOT
execution instructions that a compiler reads and interprets at runtime to determine what
to do next.

A compiler that reads `CONSTITUTION_COMPILER_V0` at runtime to decide phase ordering has
inverted the model: governance drives execution rather than governing it.

## Relationship to CONSTITUTION_COMPILER_V0

Directly enforces `COMPILER_SELF_APPLICABLE` (compiler validates its own governance)
and validates that the static declaration surface is present and non-empty. The
assertion is structural — it checks the artifact exists and is well-formed, not that
the runtime interprets it.
