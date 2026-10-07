# Targeted implementation verification

Date: 2026-10-03. This record covers only the exact output-interface reference
implementation. No project-wide local verification or CI inspection was run.

From the repository root, the author ran:

```sh
python -m unittest discover -s research-20261003-arithmetic/implementation -p 'test_*.py' -v
python research-20261003-arithmetic/implementation/demo.py
```

The final test run passed all 10 tests. An earlier run found an empty-gradient
row bug for constant objectives; it was corrected, and the constant-objective
test now passes. The later constrained-tangent regression was added following
independent review; the final run includes it.

The deterministic demo reported:

| Diagnostic | Result |
| --- | --- |
| `f(x,y)=x^2`, candidate `(0,1)` | Distance to the optimizer set certified; distance `1/100` to the minimum-norm optimizer not certified. |
| Same objective, candidate `(0,0)` | Distance `1/100` to the minimum-norm optimizer certified. |
| `f(z)=2^(-80)z^2`, candidate `1` | Value gap `2^(-80)` certified; actual point distance is one; distance `1/2` not certified. |
| Twelve squarings from `1/2` | Thirteen recurrence nodes; expanded denominator has 4,097 bits. |

The author also ran an inline Python check of Markdown link targets and
trailing whitespace within this implementation directory; it passed.

The [independent actual-file review](REVIEW.md) compared the implementation
with the mathematical formulas and passed the same ten targeted tests. It
also ran 630 separate exact-rational diagnostic checks, described in that
review. Those ad hoc checks are reported as review evidence; the checked-in
test command above is the reproducible regression suite. No finite diagnostic
is being used in place of a proof of the general theorem.

The implemented output guarantees and deliberate omissions are listed in
[README.md](README.md). In particular, this is a witness checker for a
constructively certified subclass, not a general optimizer.
