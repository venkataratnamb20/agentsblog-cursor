# Code quality

Agents Blog code is written so a reader can change one behavior without hunting through a large function or an unclear name. These rules apply in every language the repository grows into. The stack is not chosen yet. Until it lands, `lint`, `typecheck`, and `coverage` may print a clear no-op message and exit 0. Once a toolchain exists, those targets enforce the gates below and fail on a violation.

## Clean Code and SOLID

- Use meaningful names. A name states the role of the value in the domain (`subscriberEmail`, `publishPost`) and avoids abbreviations that only the author can expand.
- Keep functions small and single-purpose. Each function does one thing, sits at one level of abstraction, and returns early on invalid input.
- Follow DRY. One rule lives in one place. Callers share that place instead of copying the rule.
- Follow KISS. Prefer the simplest implementation that meets the current behavior.
- Follow YAGNI. Add a branch, parameter, or abstraction when a real caller needs it.
- Delete dead code. Commented-out blocks, unused exports, and unreachable branches do not stay in the tree.
- Single responsibility: a module changes for one reason.
- Open/closed: extend behavior through a new type or strategy instead of editing a stable branch for every new case.
- Liskov substitution: a subtype honors the contract of its supertype, including error behavior.
- Interface segregation: callers depend on the narrow surface they use.
- Dependency inversion: domain code depends on abstractions. Adapters bind those abstractions to I/O, frameworks, and clocks.

## Test-driven development

Write tests before production code, one behavior at a time:

1. **Red.** Add a failing test that names the behavior.
2. **Green.** Write the smallest production change that makes that test pass.
3. **Refactor.** Clean the code while the tests stay green.

Run the relevant tests at each step. A change that skips the red step is unfinished.

## Behavior-driven development

User journeys are specified in Gherkin and live with the BDD suite (`test-bdd`). Each scenario is one observable outcome, in the language of a reader or subscriber. The first journeys are:

```gherkin
Feature: Subscribe
  Scenario: Visitor subscribes with a valid email
    Given a visitor is on the blog
    When they subscribe with "reader@example.com"
    Then the subscription is confirmed

Feature: Read post
  Scenario: Reader opens a published post
    Given a published post titled "Agents at work"
    When the reader opens that post
    Then the post title and body are shown

Feature: Search
  Scenario: Reader searches for a published phrase
    Given a published post contains "worktree"
    When the reader searches for "worktree"
    Then that post appears in the results
```

A scenario describes what the user sees. It does not name internal types, storage, or UI widgets.

## Data structures and complexity

Choose the structure from the access pattern:

| Access pattern | Structure |
| --- | --- |
| Key lookup or update | Hash map |
| Membership only | Set |
| Ordered scan or stable ranking | List or array |
| First-in, first-out work | Queue or deque |
| Prefix or range search on ordered keys | Balanced tree or sorted index |

On a hot path, state the time and space complexity in a short comment next to the operation (for example `O(1)` average lookup, `O(n)` scan). Pick the structure whose complexity matches how often the path runs. Replace it when a profile shows the path is hot and the current complexity no longer fits.

## TypeScript

- Enable TypeScript `strict`.
- Lint with ESLint and format with Prettier.
- The `lint` target fails when ESLint reports any warning. The warning count in CI is zero.
- `format` leaves Prettier's output unchanged in CI.

## Python

- Follow PEP 8.
- Lint and format with ruff.
- Annotate public functions with type hints.
- Document public modules, classes, and functions with Google-style docstrings.

```python
def confirm_subscription(email: str) -> bool:
    """Confirm a newsletter subscription.

    Args:
        email: Address the visitor submitted.

    Returns:
        True when the address is accepted and stored.

    Raises:
        ValueError: If email is empty.
    """
```

The `lint` target fails when ruff reports any warning.

## Quality gates

| Gate | Threshold |
| --- | --- |
| Coverage of core logic | 100% |
| CI coverage gate | 80% minimum, and the gate is never lowered |
| Cyclomatic complexity | At most 10 per function |
| Function length | At most 40 lines, excluding blank lines and comments |
| Lint warnings | Zero |

Core logic means domain rules and application services. Generated code and thin framework adapters sit outside the 100% core target and still count toward the 80% CI gate.

`coverage` fails when core logic is below 100% or when the CI figure is below 80%. `lint` fails on any warning. Complexity and function-length limits are part of the same lint failure, so a long or highly branched function cannot merge by silencing the warning.

## Until the stack lands

`lint`, `typecheck`, and `coverage` have no compiler, linter, or coverage tool to run yet. Each of those targets prints a clear message that names the future check and exits 0. That temporary success is only valid while the toolchain is absent. When the stack lands, the same target names run the real tools and enforce the gates in this document.
