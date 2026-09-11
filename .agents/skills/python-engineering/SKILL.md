---
name: python-engineering
description: Build or modify Python code with strict Google-style documentation, type safety, dependency injection, and pytest coverage. Use for Python application and library implementation work in this project.
---

# Python Engineering

Act as an expert Python engineer. When the user asks for Python work, deliver a complete, maintainable solution that follows the requirements below while preserving the task's actual scope.

## Production code

- Give every authored class and function a Google-style docstring. Document all `Args`, `Returns`, and explicitly raised `Raises` entries that apply.
- Include a small, runnable doctest example in every such docstring. Keep examples deterministic and free of external services, clocks, random values, or local files unless those are injected.
- Use strict type annotations for every parameter, return value, and non-obvious local variable. Prefer concrete built-in generics (`list[str]`, `dict[str, int]`) and `Protocol` for behavioral dependencies.
- Keep business logic pure where practical: input values in, values or deliberate exceptions out. Isolate I/O at application boundaries.
- Inject external dependencies—HTTP clients, persistence, clocks, configuration, filesystem access, and randomness—rather than constructing or hardcoding them in domain logic. Use small interfaces or callables that tests can replace.
- Do not silently swallow errors. Define and document task-specific exception types when callers need to distinguish failures.

## Tests

- Add or update a separate pytest suite under `tests/` for changed behavior.
- Use `pytest.fixture` for reusable setup and dependency fakes.
- Use `@pytest.mark.parametrize` to cover normal, boundary, and error paths. Assert observable results and exception types/messages rather than implementation details.
- Run relevant pytest tests and doctests when the environment permits. If a required dependency is unavailable, report the exact command needed and what validation was still completed.

## Completion check

Before handing off, verify imports or compilation, test coverage for the implemented behavior, doctest validity, and formatting/linting tools already configured by the project. Do not introduce a framework, dependency, or external service unless the task requires it.
