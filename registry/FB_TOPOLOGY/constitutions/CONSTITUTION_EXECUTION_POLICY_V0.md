# CONSTITUTION_EXECUTION_POLICY_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_EXECUTION_POLICY_V0
constitution_code: CONSTITUTION_EXECUTION_POLICY_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_V0

core:
  description: Governs execution policy profiles — the licensing seam between BASIC and ADVANCED machine
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: POLICY_LOAD_BEFORE_EXECUTION
    applies_to: system
    constraint: policy profile MUST be resolved before execution starts
    enforced_by: TBD

  - rule_id: POLICY_IMMUTABLE_DURING_EXECUTION
    applies_to: system
    constraint: policy profile MUST NOT change after execution begins
    enforced_by: TBD

  - rule_id: POLICY_EXPLICIT_PROFILE
    applies_to: system
    constraint: policy profile MUST be one of BASIC or ADVANCED; no implicit default
    enforced_by: TBD
```

---

## §1. Purpose

Define execution policy profiles that govern machine behavior.

Policy is the **licensing seam** between Basic and Advanced Machine.

Policy determines capabilities, not code.

---

## §2. Policy Dimensions

| Dimension | Description | Schema |
|-----------|-------------|--------|
| trace_depth | Minimal or Full event emission | SCHEMA_TRACE_EVENT_V0 |
| replay_guarantee | Whether execution is replay-safe | boolean |
| audit_trail | Whether audit events are emitted | boolean |
| encrypted_execution | Whether execution context is encrypted | boolean |
| aot_compilation | Whether ahead-of-time compilation is enabled | boolean |

---

## §3. Policy Profiles

### §3.1 BASIC (OSS)

| Dimension | Value | Notes |
|-----------|-------|-------|
| trace_depth | minimal | Required events only |
| replay_guarantee | false | No replay support |
| audit_trail | false | No audit events |
| encrypted_execution | false | Plaintext context |
| aot_compilation | false | Interpreted only |

### §3.2 ADVANCED (Licensed)

| Dimension | Value | Notes |
|-----------|-------|-------|
| trace_depth | full | All events emitted |
| replay_guarantee | true | Guaranteed identical replay |
| audit_trail | true | Full audit chain |
| encrypted_execution | optional | Context encryption available |
| aot_compilation | optional | Compilation hooks available |

---

## §4. Policy Loading

Policy profile MUST be resolved before execution starts.

Resolution order:
1. Explicit runtime binding (`rb_code.policy_profile`)
2. Workflow declaration (`wf_code.default_policy`)
3. System default (`BASIC`)

Policy is immutable once execution begins.

---

## §5. Policy Enforcement

| Violation | Action |
|-----------|--------|
| Feature used without policy authorization | ABORT |
| Policy dimension missing from profile | ABORT |
| Policy changed mid-execution | ABORT |
| Unknown policy profile requested | ABORT |

---

## §6. Licensing Boundary

BASIC profile is unrestricted (OSS).

ADVANCED profile requires valid license.

License validation occurs at policy load time, not execution time.

| Check | When | Failure Mode |
|-------|------|--------------|
| License presence | Policy load | Fall back to BASIC |
| License validity | Policy load | Fall back to BASIC |
| License expiry | Policy load | Fall back to BASIC |

No execution-time license checks. No runtime license enforcement.

---

## §7. Extension Rules

New policy dimensions require:
- Schema update (SCHEMA_EXECUTION_POLICY_V0)
- Constitution update (this document)
- Default value for BASIC profile
- Explicit value for ADVANCED profile

No implicit dimensions. No undeclared behavior switches.

---

## §8. Forbidden Patterns

- Policy logic in Python code
- Conditional imports based on policy
- Feature flags outside policy profiles
- Runtime policy mutation
- Policy inheritance or composition

---

## §9. Versioning

Changes to policy profiles require:
- New constitution version
- Schema migration
- All existing profiles validated against new schema
