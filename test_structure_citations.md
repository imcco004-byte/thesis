# Test Structure Audit and Citation Grounds

Date: 2026-04-24

## Scope

This note records a structural audit of all `tests/test_*.py` files in this repository.
The goal was to rule out common false-green patterns where tests can appear to pass
without making a meaningful check.

The audit began by warming the workspace semantic index, then used AST-based source
inspection plus `pytest -rs` runtime verification.

## Audit Criteria

The audit treated the following as valid test-check mechanisms:

- Python `assert` statements.
- `pytest.raises(...)` blocks.
- `numpy.testing.assert_*` helpers.
- Repository helper assertions such as `_assert_*` functions that themselves assert.
- Conditional `pytest.skip(...)` / `@pytest.mark.skipif(...)` when the test is not
  applicable in the current environment or parameter regime.

The audit explicitly searched for these false-green patterns:

- test bodies with no assertion mechanism at all;
- `pass`-only test bodies;
- `return <non-None>` from test functions;
- broad exception swallowing inside tests (`except Exception:` / bare `except:`)
  without re-raise or assertion;
- unconditional skip/xfail markers.

## Repository Findings

- Static source audit found 195 test function/method definitions across `tests/test_*.py`.
- Runtime collection found 214 concrete test cases because parametrized tests expand
  into multiple items.
- No structurally suspicious tests were found.
- No pass-only tests were found.
- No tests return a non-`None` value.
- No tests use `pytest.xfail` or `@pytest.mark.xfail`.
- No tests catch broad exceptions in a way that would silently absorb a failure.

Detected assertion/check styles in the source audit:

- 186 tests use bare `assert`.
- 5 tests use `pytest.raises(...)`.
- 5 tests use `numpy.testing.assert_*` helpers.
- 2 tests use helper assertion functions.
- 3 tests contain imperative `pytest.skip(...)` guards.
- 2 tests use `@pytest.mark.skipif(...)` decorators.

## Skip Inventory

The suite does contain conditional skips, but they are applicability guards rather than
auto-pass patterns.

Decorator-based conditional skips:

- `tests/test_e2e.py:293` skips when `run1/` NPZ data is not present.
- `tests/test_e2e_real_data.py:40` skips when `run1/photon_count0.npz` is absent or
  does not contain `camera_images`.

Imperative conditional skips:

- `tests/test_invariants.py:447` skips spacing checks when injected spacing is below
  the configured resolvability threshold.
- `tests/test_invariants.py:489` skips when spacing is at or below the resolution limit.
- `tests/test_invariants.py:507` skips when fewer than two ions are detected, making
  spacing undefined for that test instance.
- `tests/test_synthetic.py:580` skips `test_spacing_recovery_sweep[1]` because a
  single ion has no spacing difference to measure.

Runtime verification with `pytest -rs` confirmed one active skip in the current
environment:

- `tests/test_synthetic.py:580`: `Need ≥ 2 ions to compute a spacing difference`

That skip is structurally correct: it prevents an inapplicable parameter case from
being misreported as a passing spacing-recovery test.

## Conclusion

Within the limits of a structural audit, the repository's tests do not contain common
automatic-pass patterns. The suite uses recognized pytest/NumPy assertion styles, and
its skips are conditional and documented rather than unconditional silent greens.

This audit does **not** claim every test has strong semantic value; it only rules out
the specific structural patterns most likely to yield false-green results.

## External Grounds

1. Pytest assertion guidance: pytest treats normal Python `assert` statements as the
   standard way to verify expectations in tests and rewrites them to provide failure
   introspection.
  Source: [pytest assertion guide](https://docs.pytest.org/en/stable/how-to/assert.html)

2. Pytest exception testing guidance: `pytest.raises(...)` is the documented way to
   assert that code raises an expected exception.
  Source: [pytest assertion guide](https://docs.pytest.org/en/stable/how-to/assert.html)

3. Pytest false-green warning: pytest documents that returning a non-`None` value from
   a test function is incorrect because return values do not determine pass/fail.
  Source: [pytest assertion guide](https://docs.pytest.org/en/stable/how-to/assert.html)

4. Pytest skip guidance: `skipif` and imperative `pytest.skip(...)` are appropriate
   when a test cannot succeed under current conditions or the test is not applicable.
  Source: [pytest skip and xfail guide](https://docs.pytest.org/en/stable/how-to/skipping.html)

5. NumPy testing guidance: `numpy.testing.assert_array_equal`,
   `numpy.testing.assert_allclose`, and related helpers are documented assertion
   utilities that raise `AssertionError` on mismatch.
  Source: [NumPy testing reference](https://numpy.org/doc/stable/reference/routines.testing.html)

## Suggested Follow-up

If a zero-skip test run is desired, the cleanest change is to split the `n_ions == 1`
case out of `tests/test_synthetic.py::test_spacing_recovery_sweep` and parametrize the
spacing test only over `n_ions >= 2`.
