# pgs_governance

**Constitutional governance for Protocol-Governed Systems.**

This repository defines what the system is *allowed to be* — the boundary conditions, invariant rules, structural definitions, and federated authority scopes that govern all protocol behavior.

No system behavior is permitted outside what is declared and validated here.

> **New to PGS?** This is one of the repositories in the Protocol-Governed Systems ecosystem.
> For orientation, architecture overview, and end-to-end execution, start at [pgs_workspace](https://github.com/bachipeachy/pgs_workspace).

---

## What this repository contains

### `implementation/`

Runtime governance artifacts:

| Module | Role |
|--------|------|
| `assertions/handlers/` | Executable assertion handlers — each enforces a named invariant at compile time |
| `conformance/` | Conformance oracle and machine — evaluates whether execution traces satisfy declared constraints |
| `constitution_validator/` | Validates constitutional structure at build time |
| `vocabulary/builder/` | Constructs the governed vocabulary from protocol declarations |

### `structure/`

Structural artifact definitions and resolution infrastructure:

| Module | Role |
|--------|------|
| `structure/loading/` | Protocol and vocabulary artifact loaders |
| `structure/resolution/` | Layer resolver, path registry, domain resolver |
| `structure/discovery/` | Artifact discovery across federated domain roots |

### `registry/`

Static conformance seed data referenced by the governance layer.

---

## Layer position

```
pgs_governance      ←  THIS REPO: constitutional rules + structural definitions
pgs_compiler        →  reads governance; compiles protocol source into snapshot
pgs_runtime         →  executes against compiled snapshot
```

`pgs_governance` is the authority layer. The compiler enforces it. The runtime executes within it.

---

## Part of the PGS ecosystem

| Repo | Role |
|------|------|
| `pgs_workspace` | Entry point — snapshot + scripts |
| `pgs_runtime` | Execution engine (pgs_runtime CLI) |
| `pgs_governance` | **This repo** — governance + structure |
| `pgs_compiler` | Compiler pipeline + tooling |
| `pgs_transport` | Ingress/egress adapters |
| `pgs_capabilities` | CT/CS implementations |
| `pgs_blockchain` | Blockchain domain |
| `pgs_ai_governance` | AI governance domain |
| `pgs_change_mgmt` | Governed SDLC — Change Request to Authoring Mandate (new in v0.5.0) |
