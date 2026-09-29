# Independent review of stable-positive submodular exactness

Review date: 2026-09-27. Reviewed
[stable-positive-submodular-exactness.md](stable-positive-submodular-exactness.md)
and the upper-RLT Proposition 3 added to
[binary-leaf-star-hull.md](binary-leaf-star-hull.md).

The strengthened theorem passes this analytic audit: PSD and the upper
RLT inequalities suffice when the quadratic is submodular and its
positive-diagonal vertices form a stable set. This remains true after
fixing every first moment outside that stable set; the optimum is the
Lovász extension of the eliminated binary value function. I found no gap
in the threshold rounding guarantee or the distinction between this
objective statement and the full moment-hull theorem.

## The upper-only step

The original star proof makes individual leaf complements only to obtain
nonpositive mixed coefficients. That step is unnecessary for an already
submodular star. Every remaining correction is a nonnegative combination
of unary box literals, diagonal products \(x_i(1-x_i)\), or cross
products \(x_i(1-x_j)\). Their linearized evaluations follow from the
upper bounds and means in the box. The final affine square follows from
PSD, and submodular rounding uses only upper bounds on products.

The second clipping correction simultaneously complements the center and
all surviving leaves. On that reduced principal block,

\[
\mu_i'-X_{ij}'=\mu_j-X_{ij},
\qquad
\mu_j'-X_{ij}'=\mu_i-X_{ij}.
\]

Thus upper RLT and PSD are preserved. The qualification about the reduced
block matters: complementing some variables in a larger block while
leaving others untouched need not preserve its upper inequalities. The
star proof already permits elimination through a principal submatrix,
so no larger-block invariance is required.

The fresh subordinate reviewer
`/root/forest_hull_review/upper_star_audit` independently checked every
correction and the degenerate cases. That review found no gap for empty
leaf sets, zero interactions, fixed-sign leaves, clipping equalities, or
hinge ties. It also independently ran the changed exact star check with
the newly added upper-complement and arbitrary-sign-obstruction checks.

## Why cycles cause no gap in this objective statement

Eliminating a positive center gives a concave function of a nonnegative
weighted sum of its binary neighbors. Its binary set function \(f_c\)
is therefore submodular. Fix neighbor means and order them decreasingly.
The marginal differences along that chain define an affine function
\(h_c\) lying below \(f_c\) at every binary point and equal to it at
each chain point.

The star quadratic minus \(h_c\) is nonnegative on its whole local box:
it is affine in each leaf and is nonnegative at every binary leaf vector
after minimizing the center. It is still a submodular star. The upper-only
star theorem therefore gives

\[
L(q_c)\geq h_c(\mu_{N(c)})
 =\mathbb E[f_c(\{b:\mu_b\geq U\})].
\]

This step requires no representing law for an upper-only moment point.
Such a law generally does not exist; the arbitrary-sign obstruction in
the star note explicitly demonstrates that limitation.

One common \(U\) attains these lower bounds simultaneously for every
center. The same coupling maximizes each binary–binary product, which
improves its nonpositive objective coefficient. Nonpositive diagonal
terms improve when the remaining variables become binary. Summing the
inequalities proves the global result even when different centers share
several neighbors or the binary subgraph contains cycles.

At prescribed binary means \(u\), this gives a lower bound equal to the
Lovász extension. The common-threshold law, with every center replaced
by its clipped response, supplies a feasible full moment matrix attaining
that bound. It also belongs to the weaker upper-only region. Thus both
fixed-mean optima equal the same value. No continuous means are fixed in
this conclusion, and it should not be read as preserving them.

There are at most \(|B|+1\) threshold patterns. Choosing the best of their
explicit center completions gives a feasible objective no greater than
any feasible relaxed objective. At a relaxation optimum, the chosen point
is globally optimal. This is an objective extractor, not a distribution
matching the input moment vector.

Individual coordinate complements preserve full SDP–RLT but can turn an
upper inequality into a lower one. Consequently arbitrary signed forests
inherit exactness of the full relaxation, or of upper RLT written after
the chosen transformation. The saved note correctly avoids claiming
invariance of the original upper-only system.

## Focused fixed-mean check

The new script
[check_stable_positive_fixed_means.py](check_stable_positive_fixed_means.py)
uses one five-variable example. Vertices 0 and 1 have positive diagonal
coefficients. They are adjacent to all three other vertices, which also
form a triangle. This tests overlapping centers and cyclic interactions.
Both centers encounter strictly lower-clipped, interior, and strictly
upper-clipped responses among the threshold patterns. The fixed binary
means are \((1/5,1/2,4/5)\).

Exact rational calculations give the following common-threshold law.
Coordinates are ordered as the two continuous centers followed by the
three binary variables; all objective coefficients are recorded in the
script.

| Probability | Point | Objective |
| --- | --- | --- |
| \(1/5\) | \((1,1,1,1,1)\) | \(-31/6\) |
| \(3/10\) | \((1,3/10,0,1,1)\) | \(-407/240\) |
| \(3/10\) | \((1/2,0,0,0,1)\) | \(5/8\) |
| \(1/5\) | \((0,0,0,0,0)\) | \(0\) |

The expected objective is exactly \(-3251/2400\). The script constructs
the exact positive combination of rank-one moment matrices and checks
its binary means and every full RLT inequality. Its PSD property follows
from the displayed positive rank-one decomposition.

For the same fixed means, CVXPY 1.9.3 with Clarabel returned:

| Relaxation | Returned value | Status | Value minus exact expectation | Largest measured primal violation |
| --- | --- | --- | --- | --- |
| Full SDP–RLT | \(-1.354583333336\) | `optimal` | \(-3.102\cdot10^{-12}\) | \(1.150\cdot10^{-11}\) |
| PSD and upper RLT | \(-1.354583333333\) | `optimal_inaccurate` | \(4.241\cdot10^{-13}\) | \(1.842\cdot10^{-9}\) |

The exact calculation proves feasibility and attainment of the proposed
value by that law. The numerical solves challenge a possible lower
relaxation value but do not certify its absence. The upper-only solver
status is reported as returned; it is not promoted to an exact optimum.
The analytic proof supplies the universal lower-bound argument.

## Significance and limits

The structural SDP exactness and fixed-mean identity are the candidate
contributions. Submodular minimization after independent center
elimination and the Lovász convex-closure representation are established
tools. The theorem does not establish new polynomial-time solvability,
an arbitrary-sign graph hull, or exactness after adding general side
constraints.

I directly inspected Burer, Natarajan, and Willemsen,
[*On the Semidefinite Representability of Continuous Quadratic Submodular
Minimization With Applications to Pricing and Moment Problems*,
v3](https://arxiv.org/html/2504.03996v3), Theorem 1, Proposition 4,
Example 4, and Section 6.4. Their low-dimensional theorem concerns the
same upper-only relaxation. Their four-variable counterexample has
adjacent positive-diagonal vertices and therefore does not contradict
the present theorem. They also report that lower RLT and triangle
inequalities do not close that example's gap. These comparisons support
the stated scope distinction; they do not establish priority.

The broader literature comparison remains with the dedicated
[priority review](binary-star-prior-review.md). Equivalent structural
SDP results under different terminology may still exist. No solver
speedup has been measured.

## Commands and verification limits

The targeted command run for the new cyclic example was:

```text
python research-20260927/check_stable_positive_fixed_means.py
```

It was run twice. The first execution stopped because an assertion
accepted only `optimal` and the upper-only solve returned
`optimal_inaccurate`. The revised check reports that status explicitly
and accepts it only with independently checked value and primal-residual
tolerances; the second execution passed and produced the table above.
No coefficients, predicted values, or solver settings were changed to
obtain agreement.

The subordinate review also ran:

```text
python research-20260927/check_binary_leaf_star.py
```

Its changed exact checks passed. No project-wide verification or CI
inspection was performed. These checks do not establish novelty or
replace the analytic proof.
