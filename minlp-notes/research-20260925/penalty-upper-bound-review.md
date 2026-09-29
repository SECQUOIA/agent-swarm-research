# Independent review of the quadratic-model penalty upper bound

Date: 2026-09-25. Scope: the theorem and proof in
[penalty-upper-bound.md](penalty-upper-bound.md), including its effective
algebraic source, sparse KKT system, reciprocal graph, and encoding argument.

**Verdict:** the mathematical construction gives the stated
\((N+1)2^{O(n)}\) penalty-bit upper bound. The effective algebraic citation
and constants have now been corrected and independently rechecked. The initial
draft used an older source version. Those source corrections are substantive;
the older explicit exponents should not be treated as independently certified. No other proof
gap was found. The result is a useful quantitative consequence of established
convex duality and effective algebraic geometry, not a new general theorem
about small semialgebraic points.

## Required source correction

Use Basu and Roy, *Bounding the radii of balls meeting every connected
component of semi-algebraic sets*, Journal of Symbolic Computation 45(12),
1270–1279 (2010), [DOI 10.1016/j.jsc.2010.06.009](https://www.sciencedirect.com/science/article/pii/S0747717110000891).
The [final author manuscript dated 5 June 2010](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf)
differs materially from the cited 2009 draft.

- The final Theorem 3, printed p. 5, bounds every bounded component of a
  **weak** sign condition. Its constants differ from the old theorem.
- The final Theorem 4, also p. 5, supplies the meeting radius. Its concluding
  line mentions ordinary and weak sign conditions; its Section 5 proof
  explicitly treats weak conditions. Only the latter are needed here.
- The final proof of Theorem 2, printed p. 12, includes a factorial-bit term
  in the subresultant and Cauchy bounds that is absent from the stated
  Theorem 2/4 formula. A conservative exponent should retain that term, or
  dominate it by \(K'\operatorname{bit}(K')\). This is a conservative
  treatment of a statement/proof discrepancy, not a claim that the theorem
  itself is false.

[The detailed source audit](penalty-upper-bound-source-review.md) gives the
corrected explicit exponents and verifies their asymptotic growth. Its
important corrections were independently checked against the final primary
PDF by this reviewer. In particular the final bounded-radius exponent has
a factor \(2KD_b\), with \(D_b=k(2d-1)+2\), rather than the coefficient
used in the initial draft. For fixed degree at most three, both corrected
radii still satisfy

\[
 \log_2 R\le(\tau+\log(s_0+1)+1)2^{O(k)}.
\]

Restrict the application to a finite union of weak basic closed sets,
meaning conjunctions of polynomial equalities and non-strict inequalities.
For a nonempty union, apply the meeting theorem to a nonempty member. If
the union is bounded, every member and all its connected components are
bounded, so the containment theorem applies to every point of every member.
No claim about arbitrary Boolean formulas is needed.

The old draft's proof contains an intermediate assertion that a full
algebraic component formed from active constraints remains inside a bounded
semialgebraic component. The disk intersected with y ≥ −1/2 disproves that
assertion at its rightmost point: only the circle constraint is active, but
the full circle leaves the cut disk. The final proof works with the extremal
coordinate fiber and a nearby strip, avoiding that step. This is an additional
reason to use the final source rather than its earlier draft.

## Slice regularity and the sparse KKT certificate

On each original-feasible integer slice, the stated Slater condition gives
ordinary convex KKT multipliers. Strictness is required only for constraints
nonaffine in the continuous variables; affine inequalities may be tight.
Explicitly classify nonlinearity after fixing the integer assignment, or
state that any stronger global classification is intended. Native affine
equalities represented by pairs of affine inequalities pose no difficulty.
The model's explicit boxes make the slice compact, ensuring existence of
an optimum. Polynomial objectives and constraints are differentiable and
have full continuous domain.

Let e = rank(A), retaining e independent **original** linking rows J. At
an optimal KKT point, project stationarity onto the quotient by row(A).
The quotient has dimension n − e, and the projected negative objective
gradient lies in the cone of projected active native gradients. Conic
Carathéodory selects at most n − e such gradients. Their indices form I.
The remainder lies in row(A), so the rows J complete stationarity.

This proves existence of a certificate using at most n multiplier variables
and n primal variables. Importantly, no projected coefficients, inverse
matrices, or quotient basis enter the semialgebraic system. The written
certificate retains the original rows and gradients, so there is no
unaccounted coefficient-height growth from this existence argument.

The resulting KKT system is nonempty and weak basic closed. Its dimension is
at most 2n. A point supplied by the meeting theorem may differ from the point
used to select I, but remains a valid KKT point and hence a global optimum
by convexity. The proof therefore does not require isolated solutions or
boundedness of the whole multiplier set.

The revised draft incorporates the following simplification: I was selected
from active constraints, so require \(g_i(x)=0\) for i in I instead of
\(\mu_i g_i(x)=0\). The selected original point still satisfies the system,
and every new solution still satisfies complementarity. This reduces the
maximum degree to two without adding variables. This correction was checked
again in the final certificate and its radius call. The original degree-three
argument was already correct; the simplification affects constants only.

The polynomial-count upper bound in the draft is conservative and sufficient,
including zero-coordinate padding to 2n variables.

## Signs and norm constants

The convex Lagrangian at a KKT certificate has global minimum v_z. For every
native point, the native contribution satisfies \(\sum_i\mu_i g_i\le0\).
Deleting it **increases** the Lagrangian, correctly yielding

\[
 f(x,z)+\lambda_z^T r(x,z)\ge v_z.
\]

At most n linking multiplier coordinates are nonzero. A meeting radius R_M
therefore gives \(\|\lambda_z\|_1\le nR_M\), and Hölder's inequality gives

\[
 f(x,z)+\rho\|r(x,z)\|_\infty
 \ge v_z+(\rho-nR_M)\|r(x,z)\|_\infty.
\]

The one-norm of λ, not its infinity norm alone, is the relevant constant for
an infinity-norm residual penalty. The draft accounts for this factor.

## Reciprocal graph for infeasible slices

For a nonempty original-infeasible native slice, compactness gives
\(\delta_z=\min_{X_z}\|r\|_\infty>0\). The proposed constraints

\[
 t\ge0,\quad -1\le tr_j\le1\ \forall j,\quad
 tr_j\in\{-1,1\}\text{ for at least one j}
\]

force \(t\|r\|_\infty=1\). In particular t = 0 is impossible. Conversely,
\(t=1/\|r\|_\infty\) satisfies all the constraints. Thus the set is exactly
the continuous reciprocal graph over the compact native slice, and it is
nonempty and compact.

Choose the index and sign of the equality to express this graph as a finite
union of at most 2m weak basic closed sets. Each branch is bounded because
it lies in the graph. The equality uses an existing polynomial from the
two inequalities, so the count s + 2m + 1 and degree two are correct.
The final Theorem 3 applies branch by branch without increasing dimension.
Since it bounds every point, it bounds the largest graph coordinate
\(\delta_z^{-1}\), rather than merely one arbitrary sample.

No Slater condition for original-infeasible slices and no KKT system for the
distance minimization are needed. Empty native slices are omitted. The
original-feasibility assumption ensures at least one feasible slice exists.

## Uniform coefficient heights and the final penalty

Under the explicit expanded rational encoding, let N count all coefficients,
indices, and finite box bounds. Every admissible integer coordinate has
absolute value at most \(2^{O(N)}\). The product of all input denominators
has O(N) bits. Multiplying completed certificate polynomials by that common
positive denominator clears their coefficients without changing their
solutions or rescaling the multiplier coordinates.

Substitution into total-degree-two monomials introduces products of at most
two bounded integers. Their bitsizes are O(N). Summing at most O(N)
explicit monomials adds only O(log N) bits. Differentiation introduces a
factor at most two. Adding multiplier and reciprocal variables changes
degree but does not multiply coefficient magnitudes. Consequently one
uniform coefficient bound \(\tau=O(N)\) covers all slices and both systems.
The row-basis choice introduces no new coefficients.

A full-box objective bound F has O(N) bits: bound each monomial by the
square of a coordinate-magnitude bound and sum coefficient magnitudes.
The native boxes make the integer assignment set finite. The same effective
radius bound applies to each assignment, so no factor equal to the number
of assignments is required.

With corrected radii R_M,R_D bounded by 2^E, the proposed choice

\[
 \rho=(n+2F+1)2^E
\]

is strictly larger than nR_M. Feasible slices therefore exclude every
nonzero-residual minimizer. In infeasible slices,

\[
 f+\rho\|r\|_\infty\ge-F+\rho/R_D>F\ge v.
\]

A primal optimum remains feasible and attains v, proving both value and
solution-set exactness at multiplier zero. The one-norm penalty is at least
the infinity-norm penalty and vanishes at the same points, so the conclusion
transfers without further constants.

For fixed degrees, k ≤ 2n or k = n + 1, and \(\tau=O(N)\), the corrected
exponents give the claimed \((N+1)2^{O(n)}\) ordinary penalty-bit bound.
The proof supplies an exponent with polynomial encoding length, but printing
the full binary expansion of ρ can still require exponentially many bits.
It gives no polynomial-time smallest-penalty algorithm.

## Significance and verification record

The quantitative upper bound complements the repeated-squaring lower
construction at the scale of exponential dependence on continuous
dimension. Its value is making that scale precise for the stated convex
quadratic slices. The proof remains an application of established small-point
bounds and the established feasible/infeasible-slice exactness argument.
The sparse KKT and reciprocal graph are useful devices; no claim of a major
independent novelty follows from them alone.

Two reviewers independently checked the KKT, height, sign, norm, and
reciprocal steps. A separate source audit discovered the final source
version; its substantive corrections were rechecked directly by the primary
reviewer against the final PDF and the revised main note. The local Lefebvre–Schmidt Assumption 5 and
Theorem 14 were also read. No solver tests or Lean formalization were used,
since those would not settle the source-scope and general proof questions.
No project-wide verification or CI inspection was performed.
