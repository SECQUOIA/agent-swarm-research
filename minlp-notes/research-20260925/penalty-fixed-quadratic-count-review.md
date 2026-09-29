# Independent review of the fixed-quadratic-count penalty bound

Date: 2026-09-25. Reviewer: `finish_fixed_k_review`.

The refinement in [the upper-bound note](penalty-upper-bound.md), beginning
with “Polynomial-bit penalties with a fixed number of nonlinear
quadratics,” is correct under its stated compactness, convexity, explicit
rational encoding, and refined Slater assumptions. I found no unresolved
proof gap. This review is independent of the author and the earlier
upper-bound reviews. It covers the fixed-count refinement, not a new
derivation of the preceding Basu–Roy radius formulas.

The conclusion is an existence bound: with at most \(k\) nonlinear native
quadratic inequalities per integer slice, a zero-multiplier norm penalty
with \(N^{O(k+1)}\) bits gives both value and solution exactness. The proof
does not establish a polynomial-time procedure for finding the active
affine face, a small numerical coefficient, or novelty of the result.

## Affine-face reduction

At an optimum \(x^*\), imposing equality in every active affine row and
retaining the original affine equalities defines an affine space \(H\).
All omitted affine inequalities have positive slack at \(x^*\). There are
finitely many rows, so one relative neighborhood of \(x^*\) in \(H\)
satisfies all omitted rows simultaneously.

If a point of \(H\) satisfying the nonlinear inequalities had smaller
objective value, the segment to \(x^*\) would satisfy the nonlinear
inequalities by convexity. Points sufficiently close to \(x^*\) on that
segment would satisfy the omitted affine rows and would have strictly
smaller objective value. This is a contradiction. Thus deleting the
inactive affine inequalities preserves the optimal value, even though it
may make the enlarged feasible set unbounded. Convexity of both the
objective and all the retained inequalities is essential here.

A maximal independent subsystem of the equations of \(H\) has polynomial
coefficient height after rational elimination. Free coordinates can be
chosen among the original coordinates. The supplied box therefore bounds
the free coordinates of \(x^*\) without requiring a bound on an arbitrary
inverse parametrization. The added ball contains \(x^*\) strictly and
makes the reduced set compact. It adds exactly one quadratic inequality.
The zero-dimensional case is a rational point and is handled separately.
No algorithm for discovering the active subsystem is assumed.

## Regularization and determinant elimination

For \(0<\varepsilon<1\), relaxing every reduced inequality to
\(q_i(u)\le\varepsilon\) makes the old optimum a strictly feasible point.
The relaxed ball gives a common compact bound for all such problems.
Adding \(\varepsilon\|u\|^2\) makes the objective strictly convex.
Consequently an optimum and nonnegative KKT multipliers exist, including
when the unperturbed problem has no Slater point or has singular Hessians.

The matrix

\[
M=Q_0+2\varepsilon I+\sum_i\lambda_iQ_i
\]

is positive definite because every \(Q_i\) is positive semidefinite and
every multiplier is nonnegative. Its determinant is positive, so the
adjugate expression \(u=p/\Delta\) is valid. The polynomials \(G_i\)
in the note are exactly \(\Delta^2(q_i(u)-\varepsilon)\) after this
substitution, and \(G_0\) is exactly

\[
\Delta^2\bigl(q_0(u)+\varepsilon\|u\|^2-w\bigr).
\]

Thus (19) is both necessary and sufficient for an optimal-value
certificate when \(0<\varepsilon<1\). Conversely, the reconstructed
point satisfies stationarity, primal feasibility, multiplier
nonnegativity, and complementarity; convexity then proves global
optimality. The degree estimates are valid: \(\deg\Delta\le d\),
\(\deg p_j\le d\), \(\deg G_i\le2d+1\), and
\(\deg(\lambda_iG_i)\le2d+2\). There are no remaining primal variables
or hidden quantified matrix variables.

Coefficient height remains polynomial in the original input length.
After affine substitution, there are polynomially many rational quadratic
coefficients of polynomial height. They admit a common denominator of
polynomial bit length. A determinant coefficient is a sum of at most
\(d!(h+2)^d\) products of \(d\) such coefficients. Taking logarithms
shows that coefficient bitsize remains polynomial in \(L\), since
\(d,h\le\operatorname{poly}(L)\). The adjugate and \(G_i\) expressions
have the same property. A possibly large number of distinct monomials is
not a large coefficient-height bound; this distinction is correctly made
in the note.

## The limit formula and effective source

Uniform boundedness of the perturbed minimizers proves
\(\theta(\varepsilon)\to\theta\): the old optimum gives the upper
limit, while every convergent subsequence of minimizers has an unperturbed
feasible limit, giving the lower limit. Multiplier boundedness as
\(\varepsilon\downarrow0\) is neither asserted nor needed.

Formula (20) uses arbitrarily small positive \(\varepsilon\) with an
optimal value arbitrarily close to \(v\). Because the limit exists and
is unique, it defines exactly the singleton \(\{\theta\}\). The
existential quantifiers can be moved past the disjunction
\(\eta\le0\), since their variables do not occur in that disjunct and
their domains are nonempty. The formula therefore has precisely two
quantifier blocks, of sizes \(1\) and \(h+2\le k+3\), with one free
variable. An additional universal block over primal points is unnecessary.

I independently read Theorem 2.27 on printed page 16 of
[Basu's survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
It supplies both the needed output-degree bound and the integer
coefficient-bitsize bound for block quantifier elimination. Substituting
the two block sizes and one free variable gives degree and coefficient
bitsize \(L^{O(k+1)}\). This argument uses the coefficient-height part
of the source, not merely its arithmetic operation bound. I have not
independently reproved the source theorem.

A quantifier-free description of a singleton must contain a nonzero
polynomial vanishing at that point: otherwise all its nonconstant signs
would be locally unchanged. This remains true for arbitrary Boolean
combinations after identically zero polynomials are removed. Removing a
power of the variable and applying the Cauchy bound to the reciprocal
polynomial then gives the stated lower bound for every nonzero optimal
value. No rationality of that value is assumed.

## Distance, Slater margin, and multiplier recovery

The auxiliary residual-distance problem adds only affine inequalities
and one bounded scalar variable. A nonempty infeasible native slice has
strictly positive minimum residual by compactness. The value lemma
therefore gives (21) without a constraint qualification on that slice.

The Slater-margin problem is also a compact convex QCQP. Its nonlinear
rows are the original nonlinear quadratics plus the linear variable \(t\),
so it has at most \(k\) nonlinear inequalities. Refined Slater makes its
optimum strictly positive. Applying the value lemma to objective \(-t\)
therefore gives (23).

The original feasible slice has a convex KKT certificate under refined
Slater. Affine rows may be dependent, active everywhere, or represented
as paired inequalities. Evaluating its globally minimized Lagrangian at
the maximum-margin point gives

\[
\sigma_z\sum_i\mu_i\le f(\bar x,z)-v_z\le2F.
\]

Here \(\mu\) contains only nonlinear multipliers. Native affine terms
are nonpositive at \(\bar x\), while the linking residual is zero, so
the displayed inequality has the correct direction.

After those nonlinear multipliers are bounded, the remaining stationarity
vector belongs to the finitely generated cone of active native affine
normals and both signs of linking normals. A conic representation can be
chosen with linearly independent generators, at most \(n\). Restricting
to a nonsingular row minor preserves its coefficients. Rational
determinant bounds then bound that inverse by
\(2^{\operatorname{poly}(N)}\), even when the stationarity vector or
the nonlinear multipliers are irrational. This bounds one suitable
linking multiplier. The reconstruction retains only active native
affine normals and leaves nonlinear multipliers unchanged, so it
preserves complementarity and stationarity.

When \(k=0\), the same cone argument works without a nonlinear margin
problem. Integer substitution gives rational affine normals of uniformly
polynomial height; these are the coefficients to which the determinant
bound applies. There is no factor counting integer assignments.

Finally, choosing an integer penalty strictly larger than the uniform
multiplier bound and the objective-range divided by the uniform residual
distance makes every nonzero-residual point strictly suboptimal. Its
binary length is \(N^{O(k+1)}\). Passing from the infinity norm to the
1-norm preserves this conclusion because the latter is no smaller and
has the same zero set.

## Verification scope

In addition to the mathematical audit and source reading, I ran one
targeted exact symbolic command, `python - <<'PY'`, using SymPy. It checked
the determinant stationarity identity, both constraint numerators, the
objective numerator, and degree bound in dimension two with

\[
Q_0=\operatorname{diag}(2,0),\quad
Q_1=\begin{pmatrix}2&2\\2&2\end{pmatrix},\quad Q_2=2I,
\]

\[
a_0=(1,-2),\quad a_1=(-1,3),\quad a_2=0,
\qquad(c_0,c_1,c_2)=(1/3,-2/5,-10).
\]

All identities simplified to zero, and every tested polynomial had total
degree at most six, as required by \(2d+2\). This is a check of the
displayed algebra in a nontrivial singular-Hessian example; it is not a
general proof or a verification of quantifier elimination. No Lean build,
project-wide test, or CI inspection was performed.

No correction to the theorem is required by this review. The final
literature qualification should remain: the proof establishes this
consequence of classical tools, while priority of the few-quadratic value
lemma and of the resulting exact-penalty boundary is not established.
