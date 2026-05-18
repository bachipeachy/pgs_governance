# CONSTITUTION_TRACE_EXECUTION_V0

## Machine

```yaml
fqdn: fb.topology::CONSTITUTION_TRACE_EXECUTION_V0
constitution_code: CONSTITUTION_TRACE_EXECUTION_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_V0

core:
  description: Governs trace emission and materialization — declares trace as a mandated protocol artifact
  scope: system
  enforcement_model: runtime_enforced

rules:
  - rule_id: TRACE_OBLIGATED
    applies_to: system
    constraint: trace emission is obligated; not optional
    enforced_by: TBD

  - rule_id: TRACE_EXECUTION_PURITY
    applies_to: system
    constraint: execution MUST NOT write trace to disk during execution loop; collection is in-memory only
    enforced_by: TBD

  - rule_id: TRACE_EGRESS_SOLE_IO
    applies_to: system
    constraint: TraceEgressAdapter is the sole authority for trace I/O
    enforced_by: TBD

  - rule_id: TRACE_PATH_FROM_STRUCTURE
    applies_to: system
    constraint: trace output path MUST be resolved from STRUCTURE; never derived from file traversal or hardcoded literals
    enforced_by: TBD
```

---

## §1. Purpose

Define the contract for trace emission and materialization.

Trace is **obligated**, not optional. But trace I/O is **not** the responsibility of execution.

The TE layer separates two concerns:

| Concern | Owner |
|---------|-------|
| Trace event collection | Execution (TraceEmitter) |
| Trace materialization (I/O) | Egress (TraceEgressAdapter) |

---

## §2. Execution Purity Invariant

Execution MUST be a pure function with respect to trace:

```
execute(snapshot, payload, structure) → (result, trace_events)
```

**Execution SHALL NOT:**
- Open files during execution
- Write trace events to disk during execution
- Accept a file sink as part of the execution call

**Execution SHALL:**
- Collect trace events in memory (TraceEmitter internal buffer)
- Return all events as a value upon completion

**Egress SHALL:**
- Receive the trace event list as a value
- Write events to the STRUCTURE-declared path
- Be the sole authority for trace I/O

---

## §3. Trace Event Contract

All trace events MUST conform to `SCHEMA_TRACE_EVENT_V0`.

Required fields per event:
- `event_type` — enumerated, schema-declared
- `timestamp` — ISO-8601 UTC
- `execution_id` — unique per execution
- `sequence` — monotonically increasing from 1

Optional (ADVANCED policy only):
- `prev_hash` — SHA-256[:16] of previous event JSON

Event types are declared exhaustively in `SCHEMA_TRACE_EVENT_V0`.
No undeclared event types permitted.

---

## §4. Egress Output Contract

The egress adapter MUST:
- Receive `list[TraceEvent]` as its only input (besides the resolved output path)
- Write one JSON line per event (JSONL format)
- Validate output path is absolute and STRUCTURE-resolved
- Fail hard on any I/O error — no silent failures

Output path MUST be resolved from STRUCTURE, not derived from:
- `__file__` traversal
- Hardcoded literals
- Filesystem scanning

---

## §5. Data Root Sovereignty

`data_root` (the base path for all module data) MUST be:
- Passed explicitly by the caller
- Resolved from environment (`PGS_DATA_ROOT`) or CLI argument (`--data-root`)
- Never derived implicitly inside execution or gateway

Missing `data_root` at execution call time MUST cause:
- Immediate failure
- Error code: `DATA_ROOT_REQUIRED`
- No fallback, no default traversal

---

## §6. CS Runtime Path Contract

CS runtimes receive their storage paths via RB binding policy:
```json
{ "path": "{{data_root}}/events/identity_events.jsonl" }
```

The `{{data_root}}` parameter MUST be substituted from the explicitly-provided `data_root`.

CS runtimes:
- MAY perform inline reads and writes (required for read-after-write correctness)
- MUST NOT resolve their own paths (paths come from RB policy only)
- MUST NOT traverse `__file__` or use relative paths

---

## §7. Trace Sink Lifecycle

```
[execution_start]
    TraceEmitter collects events to memory buffer

[execution_end]
    execution returns (result, list[TraceEvent])

[egress]
    TraceEgressAdapter.flush(events, path) writes JSONL
    Path is STRUCTURE-declared (from data_root)
```

No file handle is open during execution.
No sink is injected into execution.

---

## §8. Forbidden Patterns

- Injecting `JsonlTraceSink` or any file sink into `TraceEmitter` during execution
- Resolving `data_root` via `Path(__file__).parent` chains
- Writing trace events inside the execution loop
- Defaulting `data_root` to `None` with implicit fallback
- CS runtimes calling `os.path` or `Path` outside of their declared policy config

---

## §9. Enforcement Locations

| Component | Rule |
|-----------|------|
| `workflow_gateway.py::execute_workflow()` | `data_root` required, no traversal |
| `TraceEmitter.__init__()` | No sink parameter during execution |
| `TraceEgressAdapter.flush()` | Path must be absolute |
| `RuntimeLoader._load_rb_json()` | `data_root` substituted from explicit param |

---

## Version History

- **V0**: Initial TE layer constitution (2026-04-26)
