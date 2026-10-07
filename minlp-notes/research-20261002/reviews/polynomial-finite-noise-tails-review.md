# Independent review of the polynomial finite-noise tails

Date: 2026-10-02. Verdict: **pass**. This review read the complete
[author note](../new-direction/polynomial-finite-noise-tails.md), the
finite-grid section of the
[proximal growth note](../new-direction/proximal-growth-tail.md), and
the relevant primary quantifier-elimination statement. The finite-law
growth and active-gradient bounds are sound. They do not alone prove
an expected optimization bound or an exact-output theorem.

For every positive threshold, the existential-universal formula is
exactly the good point-growth event. A feasible witness whose objective
gap dominates \(\varepsilon\|y-x\|^2\) is automatically the unique
optimizer. Conversely, the infimum defining the growth constant gives
every required inequality when \(g_*\ge\varepsilon\), including
equality. Tied optimizers fail every positive-threshold test. The domain
restriction on the universally quantified variable is correctly an
implication, written using the complement of its domain formula.

The integer restrictions introduce finitely many linear atoms but no
new real variables or quantifier blocks. The number of atoms is bounded
by the stated \(s_0\); its logarithm is polynomial in the encoded
interval lengths. The scalar noise term \(t(y_i-x_i)\) has joint
degree two, so \(d_0=\max\{d,2\}\) is a valid degree bound for the
entire matrix formula. Neither the threshold nor the fixed values of
other noise coordinates increase these counts. Those values may be
arbitrary real numbers during the hybrid comparison.

This review independently read and rendered printed page 330 of
[Renegar, Part III](../../literature/papers/renegar1992-on-the-computational-complexity-and/original.pdf).
Theorem 1.1 gives quantifier-free disjunctive-normal-form output with
the number of disjuncts, atoms per disjunct, and polynomial degrees
bounded as required in the note. Its exponent depends on the product
of block sizes and exponentially on the number of blocks. With one
free variable and two blocks of size \(n\), one effective constant
times \((n+1)^2\) in the exponent is sufficient. The theorem explicitly
has a real-number-model statement, separate from its integer-coefficient
bit bound. Thus output format complexity is uniform in all coefficient
values; no hidden dependence on sampling precision enters this use.

An effective universal constant in \(H\) can be fixed from that
algorithm once. Computing the coarse integer bound \(H\) uses only
base counts. It does not require constructing the exponentially long
domain disjunction, running elimination, or inspecting a sampled
objective. Since \(\log H\) is polynomial in the base encoding,
the bound itself and the resulting sampling precision have polynomial
binary length.

The root-cell count is correct. At most \(H^2\) output polynomial
occurrences, each of degree at most \(H\), have at most \(H^3\)
distinct real roots altogether. Identically zero polynomials contribute
constant signs and no roots. The truth value is constant on every
open interval between roots and at each individual root. Consequently
\(2H^3+1\) bounds the number of components of either truth set,
including all degenerate parameter slices. The same component bound
works for every positive threshold on one chosen sampling grid.

The endpoint-inclusive grid has CDF discrepancy at most \(1/M\).
Both open and closed interval endpoints are covered by the corresponding
one-sided CDF limits, giving discrepancy at most \(2/M\) per interval
or singleton. Conditioning on the other coefficients and replacing
one marginal at a time therefore adds at most \(2nC/M\) to the
continuous-noise tail. Uniformity on every scalar slice is essential
here and has been established. Taking thresholds decreasing to a
specified value proves the non-strict bound; decreasing to zero gives
the stated bound on zero point growth, including ties.

For the active-gradient estimate, fix an integer assignment, continuous
face, and active coordinate \(i\). The free stationarity equations
are independent of \(\gamma_i\). Every nonsingular real root is also
an isolated complex root, and the isolated-root affine Bezout bound
limits their count by \(D^k\). This remains true when singular or
positive-dimensional stationary components coexist. If the original
degree is at most one, a positive-dimensional free Hessian cannot be
nonsingular; the stated safe bound still applies. For each counted
root, the active gradient has the form \(\gamma_i+b\), with \(b\)
fixed under the conditioning. Its small-gradient event is an interval
of length \(2\tau\), with the stated finite-grid probability bound.

At an optimizer with positive point growth, Taylor expansion in every
two-sided free direction gives a free Hessian at least \(2g_*I\).
Thus the relevant stationary root is nonsingular and occurs in the
counted set. Summing over at most \(R_Z3^{n_c}n_c\) face-coordinate
choices proves the claimed \(K\) bound. No assertion that all
stationary sets are finite or that finite-grid degeneracies have
probability zero is needed.

The rare-event budget also checks exactly. Its growth contribution is
at most \(1/(3B)+2nC/M\); its active-gradient contribution on the
good-growth event is at most \(1/(3B)+K/M\). The chosen lower bound
on \(M\) makes their sum at most \(1/B\). When there are no
continuous variables, the gradient event is empty and its term is
correctly omitted. The thresholds and grid depend only on base data,
and their encoding lengths are polynomial. The separate obligations
for a good-draw solver, an all-draw fallback, and an exact output
representation remain explicitly open in this note.

For source verification, the successful targeted rendering command
was `pdftoppm -f 2 -singlefile -scale-to 1800 -png` applied to the local
Renegar PDF; the resulting page image was inspected. Scoped whitespace,
mathematical-delimiter, and local-link checks passed for this review.
No external search, additional delegation, optimization experiment,
project-wide verification, or CI inspection was performed.
