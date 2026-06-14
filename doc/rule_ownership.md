# Rule Ownership & Invariant Classes

**Status:** Doctrine. Constitutional principle for how rules are owned, located, and
evaluated across the PGS ecosystem.

This note records two findings established by audit (2026-06-13) and the principle
they imply. It exists so that future rules land in the right place by construction,
and so the compiler stays a generic evaluator rather than drifting into a rule owner.

---

## 1. The Rule Ownership Principle

> **A rule is owned by the authority that owns its meaning. The compiler owns the
> mechanism that evaluates rules — never the rules themselves.**

| Concern | What it is | Where it lives |
|---------|-----------|----------------|
| **Meaning** (the rule) | An `ASSERT` / `INVARIANT` **artifact** — data declaring *what must hold* and *over what scope* | The authoring boundary: `fb.*` for constitutional rules; the domain repo (e.g. `blockchain::`) for domain rules |
| **Mechanism** (the evaluator) | A handler function — trusted code that *checks* a rule, parameterized by the artifact | `pgs_governance` handler registry (closed, statically imported) |

Adding a rule's **meaning** (a new `ASSERT`/`INVARIANT` artifact) never requires a
code change — it is compiled into the snapshot and discovered generically. Adding a
new **mechanism** (a handler) is a deliberate, governance-reviewed event, and is
deliberately *not* dynamically discovered (Zero Inference / no dynamic imports).
Most domain rules need no new mechanism: they reuse a generic handler and supply
their meaning as data (see `ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0`, which reuses
`assert_ct_surface_closed_v0` and declares its surface in
`allowed_capability_transforms`).

### Corollary: an artifact must be evaluated from itself

> **No governance artifact may exist without being authoritative. A handler must
> evaluate the rule declared by the artifact being asserted — it must never silently
> substitute a different artifact.**

A surface-closure handler that hardcodes the platform artifact code and reads *its*
allowed list — while a domain `ASSERT` declares a different list that is never read —
produces *decorative governance*: the artifact implies enforcement that does not
happen. This is the least defensible state (artifact exists, effect is none) and is
forbidden. Handlers read the allowed surface and scope from
`current_assert_artifact`, and filter the governed set by the artifact's
`scope.applies_to`. (Fixed 2026-06-13 for both surface-closure handlers —
`assert_ct_surface_closed_v0` and `assert_cs_surface_closed_v0`; the platform
`ASSERT_CS_SURFACE_CLOSED_V0` gained an explicit `scope: [PLATFORM]` to match.)

---

## 2. Two classes of invariant

The compiler evaluates exactly one of these classes. Conflating them leads to rules
filed where they can never be enforced.

| | **Compile-time structural invariant** | **Runtime business invariant** |
|---|---|---|
| **Question** | Is the *protocol* well-formed? | Is the *data state* valid? |
| **Examples** | topology acyclic, CT/CS surface closed, no ambient authority, binding surface closed | nonce monotonic, no duplicate transaction, single canonical chain head, validator uniqueness |
| **Evaluated by** | the compiler (S4 GOVERN), via `ASSERT` handlers | the runtime / capability substrate, during execution |
| **Evaluated when** | once, before any execution | continuously, against live data |
| **Owns the meaning** | `fb.*` (constitutional) or the domain (structural) | the domain (runtime) |

The compiler **cannot** and **must not** evaluate runtime business invariants — it
has no live data and runs before execution. The interesting domain rules people
reach for first (`NONCE_MONOTONIC`, `NO_DUPLICATE_TX`, `SINGLE_CANONICAL_HEAD`) are
**runtime** invariants and belong to a separate enforcement path. That path is not
yet specified; designing it is tracked work, not a compiler concern.

---

## 3. Where a new rule goes — decision

1. **Is it about protocol well-formedness (structural) or live data (business)?**
   - Business → runtime enforcement path (out of scope for the compiler). Stop.
   - Structural → continue.
2. **Is it true of every valid PGS protocol, or specific to one domain?**
   - Every protocol → constitutional `INVARIANT`/`ASSERT` artifact in `pgs_governance` (`fb.*`).
   - One domain → `INVARIANT`/`ASSERT` artifact in that domain repo, `governed_by` a constitutional invariant, `scope.applies_to` the domain.
3. **Does an existing handler already evaluate this shape of rule?**
   - Yes → reuse it; supply the rule's meaning as artifact data.
   - No → author a new handler in the `pgs_governance` closed registry (governance-reviewed).

The compiler is never edited to add a rule. If it is, domain knowledge has leaked
into the evaluator — fix it as a generic mechanism, not a special case.