"""Deterministic validation applied after each stage.

Pydantic proves the shape is right. These checks prove the *content* hangs
together: no duplicate ids, no dangling references, no empty sections, no
coverage claim that the artifacts do not support.

Every check returns warnings (the ticket continues, flagged) or errors (the
ticket cannot proceed).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..models import (
    TEST_PLAN_SECTIONS,
    AutomationCandidate,
    AutomationReadiness,
    PlaywrightBundle,
    RequirementAnalysis,
    TestCaseSuite,
    TestPlan,
)

#: Patterns that must never appear in generated Playwright code.
FORBIDDEN_CODE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("page.waitForTimeout", "hard wait (page.waitForTimeout) is banned"),
    ("waitForTimeout(", "hard wait (waitForTimeout) is banned"),
    ("cy.wait(", "Cypress API found in a Playwright spec"),
    ("xpath=", "XPath locator is banned"),
    ("//div[", "XPath locator is banned"),
    ("nth-child(", "positional CSS selector is banned"),
)

#: Secret detectors for generated code.
#:
#: These match a credential name assigned a *quoted literal*, and capture that
#: literal so an obvious placeholder can be excused. They deliberately do NOT
#: match a bare declaration: the correct, secure pattern
#:
#:     const PASSWORD = process.env.TEST_PASSWORD || 'password-placeholder';
#:
#: contains the substring "password =", so the previous substring matcher
#: warned on exactly the code we want the agent to write. The only way to
#: satisfy that check was to stop naming the variable PASSWORD, which trains
#: readers to ignore secret warnings.
SECRET_CODE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"""(?i)\b(?:password|passwd|pwd)\s*[:=]\s*(['"`])(.*?)\1"""),
        "possible hard-coded password",
    ),
    (
        re.compile(r"""(?i)\b(?:api[_-]?key|apikey)\s*[:=]\s*(['"`])(.*?)\1"""),
        "possible hard-coded API key",
    ),
    (
        re.compile(r"""(?i)\b(?:secret|auth[_-]?token|access[_-]?token)\s*[:=]\s*(['"`])(.*?)\1"""),
        "possible hard-coded secret",
    ),
    # A JWT is structural enough to flag on sight.
    (re.compile(r"Bearer\s+ey[A-Za-z0-9_\-]{10,}"), "possible hard-coded bearer token"),
    # Provider key shape. The old bare "sk-" matched ordinary identifiers such
    # as getByTestId('task-list').
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"), "possible hard-coded secret key"),
)

#: A literal containing one of these is scaffolding, not a leaked credential.
PLACEHOLDER_MARKERS: tuple[str, ...] = (
    "placeholder",
    "todo",
    "changeme",
    "change-me",
    "your-",
    "your_",
    "example",
    "dummy",
    "fake",
    "xxx",
    "<",
    "process.env",
)


def _looks_like_placeholder(literal: str) -> bool:
    value = literal.strip().lower()
    if not value:
        return True
    return any(marker in value for marker in PLACEHOLDER_MARKERS)


def scan_for_secrets(content: str) -> list[str]:
    """Return one message per distinct secret-shaped literal in ``content``.

    Credential-named variables that read from the environment, and literals
    that are plainly placeholders, are not reported.
    """
    messages: list[str] = []
    for pattern, message in SECRET_CODE_PATTERNS:
        for match in pattern.finditer(content):
            groups = match.groups()
            # Patterns with a capture group carry the literal in group 2;
            # the structural ones (JWT, sk-key) have none and always count.
            if len(groups) >= 2 and _looks_like_placeholder(groups[1]):
                continue
            if message not in messages:
                messages.append(message)
            break
    return messages


@dataclass
class ValidationResult:
    """Outcome of one validation pass."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def merge(self, other: ValidationResult) -> ValidationResult:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        return self


# --------------------------------------------------------------------------
def validate_analysis(analysis: RequirementAnalysis, ticket_key: str) -> ValidationResult:
    result = ValidationResult()

    if analysis.ticket_key.strip().upper() != ticket_key.strip().upper():
        result.errors.append(
            f"Analysis is for {analysis.ticket_key!r} but this ticket is {ticket_key!r}"
        )

    req_ids = [r.id for r in analysis.requirements]
    ac_ids = [a.id for a in analysis.acceptance_criteria]
    result.merge(_duplicate_check(req_ids, "requirement"))
    result.merge(_duplicate_check(ac_ids, "acceptance criterion"))

    if not analysis.requirements:
        result.errors.append("No requirements were extracted from the ticket")

    known = set(req_ids)
    for criterion in analysis.acceptance_criteria:
        for rid in criterion.requirement_ids:
            if rid.strip().upper() not in known:
                result.warnings.append(
                    f"{criterion.id} references unknown requirement {rid}"
                )

    for requirement in analysis.requirements:
        if requirement.provenance.value == "EXPLICIT" and not requirement.source_quote.strip():
            result.warnings.append(
                f"{requirement.id} is marked EXPLICIT but carries no source quote"
            )

    if not analysis.acceptance_criteria and not analysis.missing_information:
        result.warnings.append(
            "No acceptance criteria and no missing_information entry explaining why"
        )
    return result


# --------------------------------------------------------------------------
def validate_test_plan(
    plan: TestPlan, analysis: RequirementAnalysis, ticket_key: str
) -> ValidationResult:
    result = ValidationResult()

    if plan.ticket_key.strip().upper() != ticket_key.strip().upper():
        result.errors.append(
            f"Test plan is for {plan.ticket_key!r} but this ticket is {ticket_key!r}"
        )

    titles = [s.title.strip().lower() for s in plan.sections]
    for index, expected in enumerate(TEST_PLAN_SECTIONS):
        actual = titles[index] if index < len(titles) else ""
        if expected.lower() not in actual and actual not in expected.lower():
            result.warnings.append(
                f"Section {index + 1} is titled {plan.sections[index].title!r}, "
                f"expected {expected!r}"
            )

    for section in plan.sections:
        if len(section.content.strip()) < 40:
            result.errors.append(
                f"Section {section.number} ({section.title}) is empty or too thin"
            )

    known = {r.id for r in analysis.requirements} | {
        a.id for a in analysis.acceptance_criteria
    }
    if not plan.scenarios:
        result.warnings.append("The test plan lists no high-level scenarios")
    for scenario in plan.scenarios:
        refs = [
            r.strip().upper()
            for r in (*scenario.requirement_ids, *scenario.acceptance_criteria_ids)
        ]
        unknown = [r for r in refs if r not in known]
        if unknown:
            result.warnings.append(
                f"Scenario {scenario.id} references unknown ids: {', '.join(unknown)}"
            )
    return result


# --------------------------------------------------------------------------
def validate_test_cases(
    suite: TestCaseSuite, analysis: RequirementAnalysis, ticket_key: str
) -> ValidationResult:
    result = ValidationResult()
    key = ticket_key.strip().upper()

    if suite.ticket_key.strip().upper() != key:
        result.errors.append(
            f"Test suite is for {suite.ticket_key!r} but this ticket is {key!r}"
        )

    result.merge(_duplicate_check([c.id for c in suite.test_cases], "test case"))

    known_req = {r.id for r in analysis.requirements}
    known_ac = {a.id for a in analysis.acceptance_criteria}

    for case in suite.test_cases:
        if not case.id.startswith(f"{key}-TC-"):
            result.warnings.append(
                f"Test case id {case.id} does not start with {key}-TC-"
            )
        unknown = [
            r for r in (x.strip().upper() for x in case.requirement_ids) if r not in known_req
        ] + [
            a
            for a in (x.strip().upper() for x in case.acceptance_criteria_ids)
            if a not in known_ac
        ]
        if unknown:
            result.errors.append(
                f"{case.id} references ids that do not exist in the analysis: "
                + ", ".join(sorted(set(unknown)))
            )
        if not case.expected_result.strip():
            result.warnings.append(f"{case.id} has no expected result")
        if (
            case.automation_candidate is not AutomationCandidate.NO
            and not case.automation_rationale.strip()
        ):
            result.warnings.append(
                f"{case.id} is an automation candidate but gives no rationale"
            )

    # Every acceptance criterion needs at least one positive case.
    covered: set[str] = set()
    for case in suite.test_cases:
        covered.update(a.strip().upper() for a in case.acceptance_criteria_ids)
    for ac_id in sorted(known_ac - covered):
        result.warnings.append(f"{ac_id} has no test case covering it")
    return result


# --------------------------------------------------------------------------
def validate_playwright(
    bundle: PlaywrightBundle, suite: TestCaseSuite, ticket_key: str
) -> ValidationResult:
    result = ValidationResult()
    key = ticket_key.strip().upper()

    if bundle.ticket_key.strip().upper() != key:
        result.errors.append(
            f"Playwright bundle is for {bundle.ticket_key!r} but this ticket is {key!r}"
        )

    if not bundle.files:
        result.errors.append("The Playwright bundle contains no files")

    case_ids = {c.id for c in suite.test_cases}
    automatable = {
        c.id
        for c in suite.test_cases
        if c.automation_candidate in (AutomationCandidate.YES, AutomationCandidate.PARTIAL)
    }

    for trace in bundle.traces:
        tc_id = trace.test_case_id.strip().upper()
        if tc_id not in case_ids:
            result.errors.append(
                f"Automated test {trace.test_name!r} traces to unknown test case {tc_id}"
            )
        elif tc_id not in automatable:
            result.warnings.append(
                f"{tc_id} was automated but is marked automation_candidate=No"
            )

    traced = {t.test_case_id.strip().upper() for t in bundle.traces}
    for missing in sorted(automatable - traced):
        result.warnings.append(f"{missing} is an automation candidate but was not automated")

    for file in bundle.files:
        lowered = file.content.lower()
        for needle, message in FORBIDDEN_CODE_PATTERNS:
            if needle.lower() in lowered:
                result.errors.append(f"{file.path}: {message}")
        for message in scan_for_secrets(file.content):
            result.warnings.append(f"{file.path}: {message}")
        if file.kind == "spec" and "@playwright/test" not in file.content:
            result.warnings.append(f"{file.path}: does not import @playwright/test")
        if file.kind == "spec" and "test(" not in file.content:
            # Playwright refuses to collect a spec with no tests ("No tests
            # found"), so an empty describe block is not a usable artifact.
            result.errors.append(
                f"{file.path}: contains no test() calls, so Playwright cannot collect it. "
                "If nothing is automatable, return an empty file list with "
                "readiness=NOT_APPLICABLE instead of an empty spec."
            )

    has_placeholder = any(
        marker in f.content.upper() for f in bundle.files for marker in ("TODO", "PLACEHOLDER")
    )
    if bundle.readiness is AutomationReadiness.READY and has_placeholder:
        result.errors.append(
            "readiness=READY but the generated code still contains TODO/PLACEHOLDER markers"
        )
    if (
        bundle.readiness is AutomationReadiness.NEEDS_CONFIGURATION
        and not bundle.missing_information
    ):
        result.warnings.append(
            "readiness=NEEDS_CONFIGURATION but missing_information is empty"
        )
    return result


# --------------------------------------------------------------------------
def _duplicate_check(ids: list[str], label: str) -> ValidationResult:
    result = ValidationResult()
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in ids:
        normalized = value.strip().upper()
        if normalized in seen:
            duplicates.add(normalized)
        seen.add(normalized)
    if duplicates:
        result.errors.append(f"Duplicate {label} ids: {', '.join(sorted(duplicates))}")
    return result
