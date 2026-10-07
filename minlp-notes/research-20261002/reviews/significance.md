# Significance and tractability review of geometric-grid DP

Date: 2026-10-02. Scope: the initial [candidate theorem](../geometric-dp/theorem.md),
the September 29 decomposition results, and explicit adverse examples. This is
an independent local review, not a literature search or a novelty judgment.
The final paragraphs record subsequent results that answer some of this
initial review's limitations.

The defensible assessment is a useful, simple conditioned oracle algorithm
that removes two concrete restrictions of the repository's previous adaptive
algorithm. It is not yet evidence of a major practical MINLP advance. Its
strong points are that it finds its own centers, handles arbitrary tree
decompositions and boundary minimizers, and replaces local optimization
subproblems by finite tables. Its efficiency still rests on global separation
from every competing solution, a small supplied decomposition, a valid global
curvature bound, and an exact arithmetic model. Those qualifications belong
beside the result, rather than only in a limitations paragraph.

The argument is more than the statement that bounded-width discrete DP is
efficient. The actual step to retain is the coupling of a valid second-order
rounding correction with geometric grids and recentering: global quadratic
growth makes the correction small at the next selected point. The DP,
interpolation inequality, geometric spacing, and guessing of an unknown
constant are standard ingredients. Whether this particular combination and
its bound are new requires the separate literature audit. Simplicity of the
proof is a virtue; it does not establish priority.

The comparison with the previous notes must keep their cost models separate:

| Result | What it establishes | What the new construction changes |
|---|---|---|
| [Decomposition certificates, Theorem 3.4](../../research-20260929/theory-decomposition/decomposition-certificates.md) | An affine-message certificate with `O(N C^p log(N/eps))` leaves/cells, given an accurate center and slopes; arbitrary trees and boundary minima already allowed | The new algorithm finds its own centers and uses no slopes, but its final product tables can require `O(N C^p log(N/eps)^p)` entries and its total work another logarithmic factor |
| [Adaptive matching, Theorem 2](../../research-20260929/theory-decomposition/adaptive-matching.md) | A constructive algorithm without `x*`, on paths and with `grad F(x*)=0`; the stated count is a count of certificate boxes | Shared coordinate grids give a global algorithm on branching trees and at boundary minima, with a better displayed conditioning power but a larger logarithmic power and a different cost measure |
| Earlier integer-separator remark | Exact fixing of every separator integer value introduces domain-cardinality factors | Geometric integer grids can avoid enumerating a long interval under a useful mixed-domain growth bound and eventually certify a pure integer optimum exactly |

Here `p=w+1`. The new result does not match the old linear-logarithm
certificate count and does not prove the old affine-message localization
property. Exact agreement on separator values removes the copy-drift
mechanism altogether. Arbitrary branching is then ordinary finite-state DP:
children contribute sums of tables, not a Cartesian product of child
configurations. This is a substantive change in representation, not a theorem
that the old representation was well behaved after all. The new boundary
argument is also real: mean-preserving rounding cancels first-order terms,
so it needs no stationarity assumption at the minimizer.

The reduced conditioning dependence is attractive but needs the same care.
With `K=max(1,L/c)`, the bound is of the form

```
(N + number of factors) C^p K^(p/2)
    (1 + log_+(L n s^2/eps))^(p+1).
```

This is polynomial in accuracy bits at fixed width and conditioning. It is
not a uniform polynomial-time theorem for bounded-treewidth MINLP. Nor is
the displayed bound fixed-parameter tractable in width alone in the usual
parameterized sense: the exponent on the accuracy-bit parameter grows with
width. The old bound counted boxes while allowing low-dimensional nonlinear
optimization within them. The new count charges table arithmetic but treats
factor evaluation as an oracle. Neither comparison is a wall-clock dominance
result. The new theorem also still requires a supplied valid `L`; the older
unknown-constant corollary addressed more constants.

Global quadratic growth deserves the strongest scrutiny. On a compact box,
a unique minimizer with a local quadratic lower bound has some positive
global growth constant: combine the local bound with a positive minimum
objective gap outside a neighborhood. Thus the existence of `c>0` can be
fairly broad. A quantitatively useful `c`, uniform over a growing family, is
the real assumption. It combines local sharpness with global separation and
can encode the hard part of deciding among remote solutions.

An exact example makes this distinction explicit. For `0<delta<=1`, let

```
F_delta(x) = (x^2-1)^2 + delta(x+1)/2,    -1 <= x <= 1.
```

The unique minimizer is `x*=-1`, `F_delta(x*)=0`, and the upper coordinate
curvature is `L=8`, independent of `delta`. The exact largest growth constant
is `c=delta/4`, because

```
F_delta(x) - (delta/4)(x+1)^2
  = (x^2-1)^2 + (delta/4)(1-x^2) >= 0,
```

with equality at `x=1`. The curvature at `x*` remains 8 while `L/c=32/delta`
diverges. At `delta=0` both endpoints minimize, so no positive point-based
growth constant exists. More generally a point at distance `D` and objective
gap `delta` forces `c<=delta/D^2`. If such gaps scale with the requested
tolerance, the uniform guarantee again contains a power of `1/eps` through
conditioning. This example shows deterioration of the theorem's guarantee;
it does not prove the proposed algorithm runs slowly on this particular
polynomial.

The hypothesis is not equivalent to convexity. Nonconvex objectives can
satisfy a useful global lower bound; for example
`F(x)=x^2+2 sin^2(pi x)` on `[-1,1]` has `c=1` and positive upper curvature
`2+4 pi^2`, while its second derivative takes negative values. A theorem for
this class can have content beyond strongly convex optimization. But tests
on strongly convex quadratics alone would not demonstrate that content:
those problems already admit much simpler optimization methods.

Several natural extensions do not follow by changing notation:

1. A growth bound relative to the *set* of minimizers does not give the
   displayed contraction. Two selected points can lie near different
   components of that set while being far apart. The proof specifically
   controls `||y-z||` through distances to one common `x*`. A multiple-center
   argument would need its own complexity bound. Failure of the assumption
   does not invalidate the lower bounds, or prove that every such instance
   is difficult for the algorithm.
2. Coupled constraints destroy the rounding argument's feasible product
   structure. For example, dyadic grids on `[0,1]^2` contain no feasible
   point for `x+y=1/3`. The same equality-constrained problem may be easy
   after elimination; the example shows that the stated grid algorithm
   does not automatically cover it. Dropping constraints still gives an
   objective lower bound, but the grid minimizer need not be a feasible
   upper bound for the constrained problem.
3. Finite smooth penalties do not generally repair that problem exactly.
   For `min x` on `[-1,1]` subject to `x=0`, the penalized objective
   `x+rho x^2` minimizes at the infeasible point `-1/(2 rho)` when
   `rho>=1/2`. An exact absolute-value penalty introduces an upward kink
   and is not coordinate semiconcave with any finite `L`. Reformulations
   can also increase width or worsen conditioning.

The integer conclusion is interesting, but its premise must be stated on
the actual mixed domain. For

```
F_delta(z) = (z-(1-delta)/2)^2,    z in {0,1},    0<delta<1,
```

the continuous extension has Hessian 2, the unique integer minimizer is 0,
and `F_delta(1)-F_delta(0)=delta`. The largest integer growth constant is
`c=delta`, not a constant derived from the extension's strong convexity.
Adding continuous coordinates with a sum of squares gives the same issue
on a mixed domain. Again, the binary example does not imply slow execution:
both integer values already fit in a tiny table. It disproves the tempting
inference that strong convexity supplies a well-conditioned integer theorem.

Every finite integer problem with a unique optimizer has a positive
point-based growth constant. Its size can be exponentially small relative
to the bit length of the input. Long integer intervals therefore do not
become uniformly easy merely because the stage bound contains `log s`:
conditioning can carry a power of `s`. The point-oracle construction in
[oracle-limits.md](../geometric-dp/oracle-limits.md) explains why such a
dependence is unavoidable in the general oracle class. An integer analogue
places one smooth well of radius less than one half at an unknown integer
in `[0,S]`; all other integer values are equal, `L=O(1)`, and
`c=Theta(S^-2)`. Identifying the exceptional integer needs order `S` point
queries in the worst case.

Exact stopping also belongs only to the pure integer corollary as stated.
Even `F(x)=(x-1/3)^2` on `[0,1]`, starting from a dyadic center with dyadic
parameters, can never put its continuous optimizer on any finite grid.
Adding an independent integer square gives a mixed example with the same
obstruction. Accuracy certificates remain valid; exact continuous optimality
does not follow from the integer argument.

The arithmetic and certificate costs are not peripheral implementation
details. An exact factor oracle can hide arbitrarily costly evaluation or
comparison. With rational polynomial factors, a separate bit bound must
include coefficient size, degree, expression representation, grid-coordinate
size, and the size of sums in messages. Binary-encoded very high powers can
already make exact evaluated rationals enormous. Rational geometric grids
permit an eventual Turing analysis under suitable encoding assumptions; the
current operation count is not that analysis.

A practical checker must either trust or establish a valid curvature bound
over the entire continuous extension, including intervals between integers.
Proving a tight global derivative bound can itself be difficult. Supplied
factorwise bounds are often simpler but may be loose enough to dominate the
conditioning cost. The final certificate does not need `c`; that separation
between proof of validity and proof of fast discovery is a strong feature.

For fixed final grids, a direct check enumerates bag assignments and checks
the min-sum recurrence, requiring order `(N+number of factors)q^p` table
work. One may store only separator messages, which, after removing contained
bags, use order `N q^(p-1)` numbers, and regenerate factor values and bag
assignments during checking. Storing full evaluated bag tables instead costs
order `N q^p` numbers. Thus certificate storage can be smaller than table
work, but verification is not automatically cheap. The preceding search
stages need not be included in the final certificate. Certified interval
evaluation also needs a budget for errors accumulated across all factors and
message sums; the exact-oracle proof does not itself provide that budget.

Two improvements to the presentation are available without stronger
assumptions. First, the unknown-`c` epsilon algorithm actually terminates
without any growth hypothesis. At the final scheduled width `h_J`, every
selected node has

```
D(y) <= (L n/8)(h_J + theta s)^2.
```

The schedule gives `L n h_J^2/8 <= eps/7`. Taking `theta<=h_J/s` therefore
gives `D(y)<=4 eps/7`. Growth supplies the good complexity estimate, not
bare termination. Second, an all-integer method can always reach exact full
enumeration by choosing `h<1` and `theta s<1`; no uniqueness assumption is
needed for that fallback. The useful claim is the conditioned bound that
can avoid this enumeration.

The next evidence that would materially change this assessment is a complete
bit-cost theorem for a concrete factor representation, a certified numerical
implementation with recorded verification cost, and tests on nonconvex
families with controlled global separation. Such tests should report
conditioning, table cardinalities, bag width, actual factor cost, and memory.
A faster result on broad constrained MINLP instances, or a general
multiple-minimizer extension, remains a separate research problem. The
current candidate deserves further development as a transparent oracle
algorithm; claims of general solver superiority or a major new MINLP
complexity theorem would outrun the evidence.

Targeted verification for this review: an inline `python3` script using
`fractions.Fraction` checked the displayed near-tie identity and inequality
at 195 rational points, and the integer gap identity for three rational
values of `delta`; all assertions passed. The universal identities above
are algebraic arguments, not inferred from those samples. Local Markdown
sources were inspected with `rg`, `cat`, and `sed`. A second inline
`python3` script checked these two new documents' five local Markdown links;
all resolved. No project-wide checks were run and no CI status or logs were
inspected.

Subsequent work has answered part of the arithmetic and uniqueness concerns
raised above. The rational-polynomial extension supplies an explicit bit
bound with numerical degree counted. The reviewed
[exact mixed-box QP corollary](../geometric-dp/exact-box-qp.md) combines it
with standard rational-height and reconstruction facts to return an exact
rational optimizer in polynomial bit time at fixed width and polynomially
bounded curvature/growth ratio. The algorithm need not be given the growth
constant, and its accepted certificate does not rely on that promise.
It terminates for every unique-optimum rational mixed-box QP, because
uniqueness gives some positive growth constant; that constant can still be
too small for the polynomial-time guarantee.

The [finite-optimum corollary](../geometric-dp/exact-nonunique-box-qp.md)
uses the new coordinate-anchor algorithm and extends exact recovery to
finite nonunique optimal sets, paying for the number of distinct optimal
coordinate values. Its arithmetic transfer has a fresh independent review
and exact checks; the underlying anchor progress theorem has its own review.
These results make the program's theoretical contribution stronger than
the initial arbitrary-real oracle statement. They do not establish a
fast solver for general coupled-constraint MINLP, practical competitiveness,
or external originality. The standard height arguments should remain
clearly separated from the proposed discovery algorithms.
