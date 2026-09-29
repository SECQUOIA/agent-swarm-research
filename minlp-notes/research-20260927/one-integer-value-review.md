# Independent review of optimization with one unbounded integer variable

Date: 2026-09-28. Status: completed adversarial review; no gap found in the
stated one-integer precision theorem or its algorithmic consequences, subject
to the separately reviewed dependencies identified below. This is a
mathematical review, not a formal proof or a novelty determination.

The reviewed manuscript is
[unbounded-misocp-value-frontier.md](unbounded-misocp-value-frontier.md).
The reviewer did not devise its compressed-projection or planar-tail
argument. The full manuscript was read, including the revision that obtains
SOCP attainment from bounded integer optimization. A separate reviewer
independently checked the primary quantifier-elimination coefficient bound
and the factor-height argument.

## Scope of the conclusion

For a rational system of quadratic weak inequalities and affine rows, with
one integer coordinate and arbitrarily many continuous coordinates, the
claimed parameter is the span of the continuous constraint Hessian matrices.
The objective can be any rational quadratic and is excluded from that span.
The proof gives a small feasible integer assignment when feasible, a small
algebraic finite infimum, and a small optimal integer assignment when an
optimum exists. The finite value need not be attained.

The nonconvex conclusion is exact classification and recovery with an NP
oracle for fixed span. Polynomial time without that oracle is asserted only
for rational SOCP with an affine objective. Neither conclusion is an FPT
runtime claim, and neither supplies a practical precision bound.

The following existing results were treated as dependencies, with their
relevant statements and parameter composition checked here:

- The [compressed projection theorem](unbounded-misocp-frontier.md), whose
  rank charts, uniform finite perturbation grid, and bounded-limit argument
  were read in full together with its
  [independent review](unbounded-misocp-review.md).
- The nonconvex algebraic feasible-point and attained-optimizer bounds. The
  [attained-optimizer note](nonconvex-attainment-and-optimizer.md) was read
  to check the exact certificate and attainment interface.
- The exact rational MISOCP feasibility algorithm and the
  [boxed-integer optimization corollary](boxed-misocp-optimization.md).
  The latter was read in full to check its handling of unattained fiber
  infima and its rational-input attainment test.

The genericity and finite-quotient lemmas underlying these dependencies
were not proved again in this review. Their separate reviews remain part
of the evidence for the complete result.

## Compressed elimination and coefficient bounds

Appending the row `q_0(z,x) <= t` adds at most one direction to the
continuous Hessian span. Keeping `(z,t)` as two free real parameters is
legitimate: the lifted polyhedral row coefficients remain polynomial in
those parameters, with polynomial degree and individual coefficient size.
Neither parameter is added to the continuous vector whose Hessian span
controls the construction.

All rank charts must remain present, including exceptional ranks. At each
fixed real pair `(z,t)`, the same generic-grid argument applies. Its grid
size bound depends on dimensions and degrees, not the height or algebraic
nature of that pair. Thus the prefix has quantified block sizes
`1,1,h+2`, with polynomial degree and coefficient size for each atomic
polynomial. The bounded-limit quantifier keeps both free parameters fixed,
so it describes the actual projection, including nonclosed fibers, rather
than its closure.

The exact primary statement of Basu's author survey, Theorem 2.27, was
checked in the local full text
`research-20260925/publication-sources/basu-2014-author-survey.txt`, lines
784--805. Its output polynomial degrees are bounded by

\[
 d^{O(k_\omega)\cdots O(k_1)},
\]

and integer coefficient bit sizes by

\[
 \tau d^{O(k_\omega)\cdots O(k_1)O(\ell)}.
\]

The number of input atoms does not occur in either bound. It does occur in
the number of output atoms and construction time. Substituting the three
block sizes `1,1,h+2` and two free variables therefore gives precisely
`N^{O(h+1)}` for individual output degrees and coefficient sizes. The
separate reviewer reached the same conclusion from the primary statement.
The book's theorem numbering was not checked independently.

This distinction is essential. The argument would not yield a polynomial
algorithm by constructing its potentially exponential Boolean formula.
The manuscript uses that formula only to bound information later recovered
through threshold oracles.

## Factor heights and projection events

The factor-height argument is valid. A primitive integer factor `G` of a
bivariate integer polynomial `P` of total degree at most `D` has total
degree at most `D`. Substituting `z=X, t=X^{D+1}` preserves every coefficient
of both polynomials: their monomial exponents cannot collide. Gauss's lemma
makes the substituted factor an integer factor of the substituted input;
it need not remain irreducible after substitution. The substituted degree
is at most `D(D+1)`.

The manuscript's elementary proof using Cauchy's root bound and elementary
symmetric functions gives a factor coefficient bound
`O(D(D+1)(H+2))` bits. The separate reviewer also obtained the stronger,
unneeded bound `H+D(D+1)+O(log(D+2))` using the usual univariate factor-height
inequality. Either bound suffices, and both remain linear in `H`.

For a primitive irreducible factor `G(z,t)` of positive `t` degree,
`Res_t(G,G_t)` is nonzero in characteristic zero. When `G_z` is nonzero,
`Res_t(G,G_z)` is also nonzero. If they shared a factor over `Q(z)[t]`,
irreducibility would make `G` divide `G_z` there. Gauss's lemma then gives
multivariate divisibility over `Q[z,t]`, contradicting the strict decrease
in `z` degree. Distinct primitive irreducible factors remain coprime over
`Q(z)[t]`, so their pairwise resultants are nonzero as well. Factors that
depend only on `z` are handled separately.

Sylvester determinants have polynomial degree and coefficient bits in
`D,H`. One uniform Cauchy root bound therefore covers every projection
polynomial individually. No product over all atoms or all pairs is needed.
Consequently the tail cutoff has bit length polynomial in `D,H`, independent
of the number of atoms.

Both derivative events and pairwise intersections matter. For example,
`t=(z-C)^2` has no root collision in `t`, but changes monotonicity at `C`;
`Res_t(G,G_z)` detects this point. The upward-closed union

\[
 \{t\ge z\}\ \cup\ \{t\ge2C-z\}
\]

has boundary `min(z,2C-z)`. Its two individual branches are strictly
monotone, but exchange order at `C`; the pairwise resultant detects that
point. These examples support the manuscript's full event family rather
than a discriminant-only argument.

## Tail topology, infima, and optimal integer witnesses

Beyond the event bound, leading coefficients cannot vanish, roots are
simple, and distinct factors do not share roots. Real roots extend as
ordered analytic sections across each entire tail. They cannot disappear
or escape at a finite parameter while the leading coefficient stays
nonzero. All atomic signs, hence the Boolean truth value, are constant on
each section and each open strip.

Upward closure then leaves only an empty fiber, the full real line, or a
single lower boundary section. The same choice applies over the entire
tail. Inclusion or exclusion of the boundary is constant there. Formula
`g'=-G_z/G_t` makes each nonconstant section strictly monotone; if `G_z=0`,
the section is constant. This reasoning covers open endpoints and does
not require closedness of the projected epigraph.

For a finite mixed-integer infimum, no integer fiber can have infimum
minus infinity. On either tail, a finite boundary function has integer
infimum at the first integer or at its infinite-end limit. Strict
monotonicity determines which. An empty tail contributes nothing. A
constant tail is included in the first-integer case. The central interval
contains finitely many integers even though it may contain exponentially
many in the input length; no algorithm enumerates them.

A finite endpoint at a central integer must annihilate a nonzero
specialization of some atom. Atoms specializing identically to zero must
first be removed; the remaining signs would otherwise be locally constant
in `t`, contradicting the endpoint. If all atoms specialized to constants,
the fiber would instead be empty or all of `R`.

For a finite tail limit, writing
`G(z,t)=sum_a z^a G_a(t)` and dividing by its highest `z` power gives
`G_d(limit)=0`. The lower powers vanish because the section has a finite
limit. This is valid at either positive or negative infinity. The selected
coefficient polynomial is nonzero by definition. Its degree and height
are inherited from the factor. Taking the smallest candidate does not
require a polynomial product over candidates: a polynomial for the
selected candidate already suffices.

If an attained optimum occurs beyond a tail's first integer, strict
monotonicity would give another integer fiber with strictly smaller
infimum. That would also give an actual objective value below the claimed
optimum, even if the smaller fiber infimum were unattained. Hence an
optimal tail must be constant. Since graph membership is constant, one
attained point on that graph implies attainment at its first integer.
This proves the optimal-assignment bound without assuming that every
optimal integer is small.

## Exact algorithm and attainment checks

The integer feasibility bound permits a short integer guess, followed by
a short algebraic continuous witness in the fixed fiber. Exact feasibility
and rational quadratic threshold queries are therefore in NP for fixed
span. Substitution can increase coefficient length, but it remains
polynomial for fixed span. No claim of a uniform absolute runtime exponent
is made.

The finite-value bound supplies a number `M` strictly larger than the
absolute value of every possible finite infimum. On a nonempty instance,
a feasible threshold below `-M` is equivalent to unboundedness below.
Bisection uses weak interval containment: a failed threshold exactly at an
unattained infimum is consistent with `theta >= t`. Thus no erroneous
attainment inference enters value recovery. The resulting approximation
precision is polynomial in the proved degree and height bounds, as required
by the separately reviewed algebraic-recognition procedure.

Once the exact value is known, an attainment certificate can verify its
minimal polynomial and isolating interval at the candidate objective value
inside the candidate point's common field. It need not form an unrelated
field compositum. The small optimal integer assignment and the fixed-fiber
optimizer theorem give a bounded certificate whenever attainment holds.
Standard NP certificate-prefix search then recovers an optimizer.

For SOCP with an affine objective, rational thresholds preserve the
continuous Hessian span and admit the deterministic feasibility algorithm.
The revised attainment proof correctly restricts the integer coordinate to
`[-B-1,B+1]`, invokes the reviewed boxed-integer algorithm, and checks both
that its finite value equals the original value and that its value is
attained. A boxed problem cannot be unbounded below when the original
infimum is finite. Empty boxed sets correctly yield failure of attainment.
Equality of two unboxed finite infima alone would not suffice; the
manuscript does not make that mistake. The optional algebraic-threshold
route is unnecessary for this conclusion.

## Significance, novelty, and verification limits

This extends the exact one-integer SOCP conclusion to affine objectives
involving continuous variables and allows finite values produced only by
integer assignments escaping to infinity. The nonconvex theorem gives a
broader precision and oracle-complexity result. These are meaningful
extensions of the earlier integer-only objective statement, but their
algorithmic components remain combinations of established elimination,
monotonicity, recognition, and reviewed projection tools. This review does
not establish priority or assess whether an equivalent theorem appears
under another formulation; the separate prior-work audit is required for
that question.

An inline `python -` SymPy check passed eight exact assertions concerning
the derivative resultant, pairwise crossing, the branch `1/z`, its leading
coefficient limit equation, the cone residual `4-4zx`, and an atom that
vanishes identically after parameter specialization. The initial check
used a structural rather than polynomial equality and the wrong sign for
one constant resultant; those test assertions were corrected. Neither
issue concerned a manuscript claim, and only nonvanishing is needed for
that resultant. These calculations validate the examples, not the general
proof or universal coefficient bounds.

The reviewer also ran a targeted document check on this review for local
links, math delimiters, final newline, trailing whitespace, and control
characters. It passed. No Lean proof, full algorithm implementation,
project-wide verification, or CI inspection was performed. Positive
independent reviews are evidence, not a guarantee of correctness.
