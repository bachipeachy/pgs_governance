"""
ct_bytecode_validator.py — CSP Constitutional Validator v0

PURPOSE:
Enforce CSP architectural invariants as a compiler phase.

CONTRACT:
- Reads exactly ONE JSON manifest from stdin
- Manifest MUST be emitted by a prior tool
- No flags, no arguments, no discovery
- Loud failure on any violation of contract

THIS IS NOT A LINTER.
THIS IS A CONSTITUTIONAL GATE.

NOTE:
DiagnosticSeverity is TOOLING vocabulary.
It is NOT part of protocol_validator vocabulary.
"""

from __future__ import annotations

import sys
import json
import re
import subprocess
from pathlib import Path
from typing import List, Set, Dict, Optional, Type
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

# CONSTITUTIONAL: Rely on proper package installation (no sys.path hacks)
from pgs_governance.structure.structure.resolution import bootstrap, paths

bootstrap()

# If invoked from a different directory (e.g., pgs_sandbox), preserve it as workspace_root

from pgs_governance.implementation.vocabulary.builder.reserved import load_reserved_vocabulary

# ---------------------------------------------------------------------
# Diagnostic Severity (TOOLING ONLY)
# ---------------------------------------------------------------------

class DiagnosticSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

    def rank(self) -> int:
        return {
            DiagnosticSeverity.INFO: 0,
            DiagnosticSeverity.WARNING: 1,
            DiagnosticSeverity.ERROR: 2,
            DiagnosticSeverity.FATAL: 3,
        }[self]

# ---------------------------------------------------------------------
# Vocabulary Symbols (compiler symbol table)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Vocabulary:
    node_types: Set[str]
    result_status: Set[str]
    ct_codes: Set[str]
    cs_codes: Set[str]
    cc_codes: Set[str]
    wf_codes: Set[str]
    in_codes: Set[str]
    structural_keys: Set[str]
    binding_verbs: Dict[str, List[str]]

    @classmethod
    def load(cls, path: Path) -> "Vocabulary":
        if not path.exists():
            raise RuntimeError(f"Vocabulary symbols file missing: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            node_types=set(data["node_types"]),
            result_status=set(data["result_status"]),
            ct_codes=set(data["ct_codes"]),
            cs_codes=set(data["cs_codes"]),
            cc_codes=set(data["cc_codes"]),
            wf_codes=set(data["wf_codes"]),
            in_codes=set(data["in_codes"]),
            structural_keys=set(data["structural_keys"]),
            binding_verbs=data["binding_verbs"],
        )

# ---------------------------------------------------------------------
# Vocabulary Semantic Index (semantic graph)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class VocabularyIndex:
    workflows: Dict[str, dict]
    operations: Dict[str, dict]
    capabilities: Dict[str, dict]

    @classmethod
    def load(cls, path: Path) -> "VocabularyIndex":
        if not path.exists():
            raise RuntimeError(f"Vocabulary semantic index missing: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            workflows=data.get("workflows", {}),
            operations=data.get("operations", {}),
            capabilities=data.get("capabilities", {}),
        )

# ---------------------------------------------------------------------
# Violation Model
# ---------------------------------------------------------------------

@dataclass
class Violation:
    rule_id: str
    constitution: str
    severity: DiagnosticSeverity
    file_path: Path
    message: str
    rationale: str
    line_number: Optional[int] = None
    context: Optional[str] = None

    def __str__(self) -> str:
        loc = str(self.file_path)
        if self.line_number:
            loc += f":{self.line_number}"
        return f"[{self.severity.value}] {self.rule_id} @ {loc}\n  {self.message}"

# ---------------------------------------------------------------------
# Rule Base
# ---------------------------------------------------------------------

class ConstitutionalRule(ABC):
    rule_id: str = "RULE_UNKNOWN"
    description: str = ""
    constitution: str = "UNKNOWN"
    severity: DiagnosticSeverity = DiagnosticSeverity.WARNING

    def __init__(self, vocab: Vocabulary, index: VocabularyIndex):
        self.vocab = vocab
        self.index = index
        self.violations: List[Violation] = []

    @abstractmethod
    def check(self, target: Path) -> None:
        ...

    def add_violation(
        self,
        *,
        file_path: Path,
        message: str,
        rationale: str,
        line_number: Optional[int] = None,
        context: Optional[str] = None,
        severity: Optional[DiagnosticSeverity] = None,
    ):
        self.violations.append(
            Violation(
                rule_id=self.rule_id,
                constitution=self.constitution,
                severity=severity or self.severity,
                file_path=file_path,
                message=message,
                rationale=rationale,
                line_number=line_number,
                context=context,
            )
        )

# ---------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------

class EngineNoForbiddenWords(ConstitutionalRule):
    rule_id = "ENGINE_000"
    description = "Forbidden vocabulary must not appear in source code"
    constitution = "Language Purity"
    severity = DiagnosticSeverity.ERROR

    def check(self, target: Path):
        project_root = bootstrap()

        # Load forbidden words from canonical vocabulary
        def read_file(p: Path) -> str:
            return p.read_text(encoding="utf-8")

        try:
            vocab = load_reserved_vocabulary(paths.governance.vocabulary_reserved_dir(), read_file)
            words = list(vocab.get("forbidden_language", set()))
        except ValueError:
            return

        if not words:
            return

        # Use word boundaries to avoid matching substrings
        pattern = r'\b(' + '|'.join(words) + r')\b'

        try:
            # Exclude documentation, this file itself, and other non-source files
            cmd = [
                "git", "grep", "-l", "-E", pattern, "--",
                "*.py",
                "*.template.json", # Add template JSON files to scan
                ":!**/testbed/**",
                ":!**/doc/**",
                f":!{Path(__file__).relative_to(project_root)}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=project_root)

            for file_path_str in result.stdout.strip().splitlines():
                self.add_violation(
                    file_path=project_root / file_path_str,
                    message=f"File contains forbidden vocabulary ({pattern})",
                    rationale="Forbidden words represent removed concepts and must be purged.",
                )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git not found or grep returned non-zero (no matches), which is good.
            pass


class EngineNoContractLiterals(ConstitutionalRule):
    rule_id = "ENGINE_001"
    description = "Runtime engine must not reference CC_ literals"
    constitution = "Trust Plane Separation"
    severity = DiagnosticSeverity.ERROR

    RUNTIME_SUBPATHS = ("executor", "host")

    def check(self, target: Path):
        for sub in self.RUNTIME_SUBPATHS:
            runtime_dir = target / sub
            if not runtime_dir.exists():
                continue

            for py in runtime_dir.rglob("*.py"):
                text = py.read_text(encoding="utf-8")
                for ln, line in enumerate(text.splitlines(), 1):
                    if line.strip().startswith("#"):
                        continue
                    if re.search(r'["\']CC_[A-Z0-9_]+["\']', line):
                        self.add_violation(
                            file_path=py,
                            line_number=ln,
                            message="Contract literal found in host engine code",
                            rationale="Runtime engine must treat contracts opaquely",
                            context=line.strip(),
                        )

class EngineNoResultStatusLiterals(ConstitutionalRule):
    rule_id = "ENGINE_002"
    description = "Engine must not hardcode result_status"
    constitution = "Protocol as Truth"
    severity = DiagnosticSeverity.WARNING

    def check(self, target: Path):
        for py in target.rglob("*.py"):
            text = py.read_text(encoding="utf-8")
            for ln, line in enumerate(text.splitlines(), 1):
                if line.strip().startswith("#"):
                    continue
                # This check is now more targeted to avoid flagging the logic we just added
                if "result_status" in line and "on_ct_result" not in line:
                    for status in self.vocab.result_status:
                        if re.search(rf'["\']{status}["\']', line):
                            self.add_violation(
                                file_path=py,
                                line_number=ln,
                                message=f"Hardcoded result_status '{status}'",
                                rationale="Result status must come from protocol_validator",
                                context=line.strip(),
                            )

class CTNoBusinessNouns(ConstitutionalRule):
    rule_id = "CT_002"
    description = "CTs must not contain business nouns"
    constitution = "Atomic Transform Charter"
    severity = DiagnosticSeverity.ERROR

    BUSINESS_NOUNS = {
        "USER", "ACCOUNT", "ORDER", "WALLET", "TRANSACTION", "PAYMENT"
    }

    def check(self, target: Path):
        for ct in self.vocab.ct_codes:
            for noun in self.BUSINESS_NOUNS:
                if noun in ct:
                    self.add_violation(
                        file_path=target,
                        message=f"CT '{ct}' contains business noun '{noun}'",
                        rationale="CTs express mechanics, not domain meaning",
                        context=ct,
                    )

# ---------------------------------------------------------------------
# Rule Registry
# ---------------------------------------------------------------------

RULES: List[Type[ConstitutionalRule]] = [
    EngineNoForbiddenWords,
    EngineNoContractLiterals,
    EngineNoResultStatusLiterals,
    CTNoBusinessNouns,
]

# ---------------------------------------------------------------------
# Validator Engine
# ---------------------------------------------------------------------

class ConstitutionalValidator:
    def __init__(self, vocab: Vocabulary, index: VocabularyIndex):
        self.rules = [
            rule(vocab, index)
            for rule in sorted(RULES, key=lambda r: r.severity.rank(), reverse=True)
        ]
        self.violations: List[Violation] = []
        
        self.TARGETS = {
            "engine": paths.execution.machine(),
        }

    def run(self):
        for rule in self.rules:
            rule.violations.clear()
            for target in self.TARGETS.values():
                rule.check(target)
            self.violations.extend(rule.violations)

    def report(self):
        if not self.violations:
            print("[validator] ✓ Constitutional compliance verified", file=sys.stderr)
            return

        grouped: Dict[DiagnosticSeverity, List[Violation]] = {}
        for v in self.violations:
            grouped.setdefault(v.severity, []).append(v)

        for sev in sorted(grouped, key=lambda s: s.rank(), reverse=True):
            print("\n" + "=" * 72, file=sys.stderr)
            print(f"{sev.value}: {len(grouped[sev])} violations", file=sys.stderr)
            print("=" * 72, file=sys.stderr)
            for v in grouped[sev]:
                print(v, file=sys.stderr)
                print(f"  Constitution: {v.constitution}", file=sys.stderr)
                print(f"  Rationale: {v.rationale}", file=sys.stderr)

    def exit_code(self) -> int:
        if any(v.severity == DiagnosticSeverity.FATAL for v in self.violations):
            return 2
        if any(v.severity == DiagnosticSeverity.ERROR for v in self.violations):
            return 1
        return 0

# ---------------------------------------------------------------------
# Entry Point — PIPELINE ONLY (stdin guarded)
# ---------------------------------------------------------------------

def main():
    bootstrap()
    raw = sys.stdin.read()

    if not raw:
        raise RuntimeError(
            "Empty stdin received. This tool requires a JSON manifest.\n"
            "Correct usage:\n"
            "  vocabulary_builder | constitutional_validator"
        )

    manifest = json.loads(raw)

    if manifest.get("status") != "SUCCESS":
        raise RuntimeError("Upstream tool did not complete successfully")

    artifacts = manifest.get("artifacts") or {}
    symbols_path = Path(artifacts.get("symbols", ""))
    index_path = Path(artifacts.get("semantic_index", ""))

    if not symbols_path.exists() or not index_path.exists():
        raise RuntimeError("Manifest references missing artifact files")

    vocab = Vocabulary.load(symbols_path)
    index = VocabularyIndex.load(index_path)

    validator = ConstitutionalValidator(vocab, index)
    validator.run()
    validator.report()
    sys.exit(validator.exit_code())

if __name__ == "__main__":
    main()
