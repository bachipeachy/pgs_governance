# ASSERT_RB_NO_LOGIC_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_RB_NO_LOGIC_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_RB_NO_LOGIC_V0

implementation:
  module: pgs_governance.registry.handlers.assert_rb_no_logic_v0
  callable: execute
```

## Summary

Validates that RB artifacts contain no execution logic:
1. Binding values must be static configuration (strings, numbers, booleans, lists, maps)
2. No template expressions with conditional logic (if/else, ternary)
3. No callable references or function invocations in binding values
4. Template variables (`{{var}}`) are permitted — they are parameter substitution, not logic

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All RB artifacts

## Handler Behavior

### 1. Inspect Binding Values

For each binding in `core.bindings`, inspect all config values recursively.

### 2. Reject Logic Patterns

Check for disallowed patterns in string values:
- Inline conditionals: `if`, `else`, `switch` expressions
- Callable syntax: `()`, `->`, `=>` in config strings
- Dynamic expression markers beyond `{{var}}` substitution

Violation: Logic pattern detected in binding config.

## Error Messages

### Logic in Binding
```
❌ ASSERT_RB_NO_LOGIC_V0: Execution logic in runtime binding
   RB: RB_EXAMPLE_V0
   Binding: domain.capability_side_effects::CS_STORE_V0
   Field: config.path
   Value: "{{env == 'prod' ? '/prod/data' : '/dev/data'}}"
   Violation: RB binding config must not contain conditional logic
   Fix: Use a plain template variable or static value
```

## Rationale

Runtime bindings are mapping declarations, not programs. Embedding logic in RB
artifacts would shift execution semantics into configuration, bypassing the
protocol execution model. All logic belongs in CT or CS artifacts.

## Version History

- **V0**: Initial implementation (2026-05-04)
