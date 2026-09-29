# Narrow source search for unambiguous convex optimization bounds

Date: 2026-09-28. This records a limited search, not a novelty conclusion.

The proposed result in [the unambiguous certificate note](polyhedral-strong-quartic-unambiguous-upper.md) concerns exact value and coordinate comparisons for an explicit rational quartic with a supplied global strong-convexity bound over an arbitrary rational polyhedron. Its proposed classification is UP with a PosSLP oracle and the corresponding complementary class. It is not a claim about approximate optimization or ordinary UP without an oracle.

The following web queries were run:

- `"convex" "UP" "PosSLP" optimization`
- `"strongly convex" "unambiguous" complexity active set`
- `"convex programming" "coUP"`
- `"PosSLP" "coUP"`
- `"PosSLP" "active" "convex"`
- `"unambiguous" "convex optimization" complexity`

The returned results did not identify a matching primary theorem. Most uses of “unambiguous” concerned other meanings, such as quantum-state discrimination or oracle-information games. Those results were not treated as complexity evidence. The search does not exclude terminology variants or earlier unpublished results, and does not establish novelty.

The precise positive source dependency is Grötschel, Lovász, and Schrijver, [Geometric Algorithms and Combinatorial Optimization, 1988](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf). Its author-hosted PDF was downloaded and read directly. Printed pages 189--191 define the elementary arithmetic model and state and prove Theorem 6.6.3: rational LP can be solved using a number of those operations polynomial in the matrix encoding, independent of objective and right-hand-side encoding lengths, with an optimal vertex returned when one exists. Printed pages 168--169 state Theorem 6.2.13 and explain bounded-comparison implementation of the rounding used in that approach. These results concern rational LP; the nonlinear certificate construction is a separate argument.

The [unconstrained source audit](strong-convex-quartic-posslp-upper-prior.md) and [general polyhedral note](polyhedral-strong-quartic-posslp-upper.md) record the other directly examined sources, including Newton-circuit exact comparison, quantitative real-algebraic separation, and polynomial-bit approximation. None of the unsuccessful searches above changes their qualified publication-priority assessment.
