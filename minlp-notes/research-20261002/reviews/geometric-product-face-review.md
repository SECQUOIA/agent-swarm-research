# Independent review of the geometric coordinate-fiber certificate

Date: 2026-10-02. Verdict: **pass**. This review read the complete
[author note](../new-direction/geometric-product-face-certificate.md)
and checked its reduction to the
[geometric copositivity argument](../new-direction/geometric-copositive-certificate.md).
No substantive gap was found. No priority claim is made.

The preprocessing correctly makes the polynomial-identity test complete
for constancy on the proposed mixed face. If a free integer coordinate
has exactly two labels \(l,u\), replacing its square by
\((l+u)y_i-lu\) preserves the objective on the entire feasible domain.
This changes only a free unary term and the constant; it preserves
active diagonal curvature and adds no interaction edge. After fixed
coordinates are removed, every remaining free coordinate has at least
two distinct feasible values. A four-point rectangle difference forces
each free-free cross coefficient to vanish if the objective is constant
on the face. The remaining univariate quadratic must have zero linear
and quadratic coefficients on a real interval or three integer labels.
A reduced two-label term is affine, and constancy at its two values
forces its linear coefficient to vanish. Thus the reduced identity is
equivalent to actual constancy, without an extra assumption on the
original polynomial.

After inward rounding of integer bounds and substitution of fixed
coordinates, the affine slope minima are attained at feasible endpoints.
A negative minimum disproves optimality of the face: a sufficiently
small positive move in the corresponding continuous active coordinate
makes the linear term dominate its quadratic term.

Under the verified nonnegative slopes, radial scaling is valid:

\[
 F(tu,y)-f_0-t^2(F(u,y)-f_0)
       =t(1-t)a(y)^Tu\ge0 \qquad(0\le t\le1).
\]

This also shows that the true growth constant equals the minimum of
the objective-to-squared-distance ratio on the normalized active shell
\(\max_i u_i=1\). That shell, including its mixed free-coordinate
domain, is compact. Consequently an exact optimal face of the stated
form automatically has positive growth: the shell objective is strictly
positive and its squared active norm is bounded between one and \(m\).
This observation removes any need for a separate growth-existence
promise when the supplied candidate face is indeed the exact optimal set.
It does not supply its numerical constant or discover the face.

Independent active-grid and free-endpoint rounding preserves the
expectation of every affine and cross term. Only the active diagonal
variances remain. Negative active diagonal entries are allowed:
\(A_{ii}-\sigma\le L/2\) is the only upper bound used. The variance
estimate and \(\eta=\delta/m\) give the additive correction
\(Lm\eta^2/8=\sigma/m\). A coordinate originally equal to one
remains one, so every rounding outcome belongs to the constrained
finite grid. Therefore the DP minimum proves the shell inequality
\(F-f_0\ge\sigma\|x\|^2+b_\delta\). Radial scaling proves the
stated global inequality, even when \(b_\delta\le0\).

For a positive root bound, \(x\ne0\) gives a strictly positive
objective gap. Together with the polynomial identity at \(x=0\),
this proves that the entire supplied face is exactly the optimal set.
Euclidean distance to that face is precisely \(\|x\|\), including
when some free coordinates are integer. The accepted margin is thus
an independently verified global growth constant.

When the true margin is \(g>0\), the success threshold
\(\sigma\le g/4\) gives
\(b_\delta\ge g-(2+1/m)\sigma\ge g/4\). A failed predecessor
therefore yields \(\sigma>g/16\) at a later first success. An initial
success instead has \(\sigma=L/32\). These cases prove exactly

\[
 \sigma\ge\min\{L/32,g/16\},\qquad
 L/\sigma\le32\max\{1,L/g\}.
\]

Unlike the homogeneous case, \(g\) can greatly exceed \(L\), so
a constant-factor estimate of \(g\) would be an incorrect conclusion.
The note states the correct conditioning guarantee. The same cases
give \(O(1+\log\kappa)\) trials and
\(\delta^{-1}\le2\sqrt\kappa\).

The DP needs only active geometric-grid labels, at most two labels
per free coordinate, and one owned-active-coordinate OR flag. Every
factor must be assigned once, and the verifier must recompute all
Bellman minima rather than trust a minimizing assignment alone.
Combining children sequentially avoids dependence exponential in their
number. Powers of the logarithmic grid-size dependence on \(m\)
can be absorbed into a parameter-dependent constant times \(m\).
The asserted fixed-parameter bound therefore has an absolute input
exponent. Integer interval lengths affect endpoint encoding, not the
number of labels. A suitable fixed product of the coefficient, grid,
and endpoint denominators covers all local values; message additions
and minima do not multiply these denominators across bags.

The argument in Sections 1--4 is restricted to a supplied coordinate
face and continuous active coordinates. Radial
normalization need not preserve integer active coordinates. A tilted
optimal set such as the diagonal of \((x-y)^2\) is not covered.
These limitations are stated accurately in the author note.

This review checked the written proof independently. It did not run
the author's diagnostic implementation. A scoped whitespace and
Markdown-link check was performed for this review artifact. No
external search, project-wide verification, or CI inspection was
performed.

The completed Section 5 extends the result to a supplied coordinate
fiber with continuous or rational-lattice coordinates in both its active
and free parts. This review also read the complete
[physical-shell note](../new-direction/mixed-shell-certificate.md)
and checked the proposed extension against its construction. The
extension passes: it preserves the physical Euclidean metric and needs
no rescaling by coordinate side widths.

All shell geometry uses only active coordinates. In particular, the
bottom radius includes only active lattice spacings and active
continuous side distances, and the shell grid's dimension parameter
is the active count \(m\). Free coordinates retain at most two feasible
endpoint labels. The free two-label square reduction remains valid for
rational lattices: the identity at its two labels does not require
spacing one. The extension keeps the active quadratic coefficients
and their supplied curvature scale unchanged; no active-coordinate
unary reduction is needed.

Independent rounding has no extra free-coordinate error. The verified
fiber identity removes its free-free quadratic block, and independence
preserves every active-free cross expectation. Consequently the active
variance correction is exactly \(\sigma S^2/m\), and the shell DP
threshold \(M_{S,\delta}\ge\sigma S^2/m\) proves the claimed growth
on that shell, uniformly for every free assignment. The OR flag records
only active displacement. Changing a free endpoint label must never
satisfy the shell constraint.

Below the bottom radius, every active lattice displacement is zero.
Holding the free assignment fixed, the uniform continuous first-order
checks make the linear part nonnegative along every available active
continuous ray. Scaling such a ray to the bottom shell is feasible by
the definition of the radius. This proves the missing inner-region
bound without imposing any sign condition on active lattice gradients.
If the fiber is exactly the optimal set, the outer region times the
free box is compact and has a strictly positive objective gap. The
same radial argument extends a positive growth constant inward.
Thus exactness again guarantees termination without an additional
growth-existence assumption.

Every shell test succeeds at \(\sigma\le g/3\), because its grid
points have active squared norm at least \(S^2\). The first-success
argument therefore gives \(\sigma\ge\min\{L/32,g/12\}\), and
\(L/\sigma\le32\max\{1,L/g\}\). The number of physical shells
is polynomial in the encoded active geometry. Giving the free variables
two labels changes no exponent in the established sparse DP bound.
It also adds only their input denominators to the rational-size proof.

The endpoint branch is complete when all active quadratic diagonals
are nonpositive. A proposed active value strictly between its feasible
endpoints cannot belong to an exact optimal fiber: fixing the free
assignment and other active values, concavity supplies a distinct
active endpoint of no greater objective. Once the proposed active
values are endpoints, the DP flag must record only an active change.
Let its minimum gap be \(\Delta>0\). Rounding all coordinates to
their endpoints gives

\[
 F(x,y)-f_0\ge\Delta\Pr(U_A\ne v)
 \ge\Delta\max_i\frac{|x_i-v_i|}{w_i}
 \ge\frac{\Delta}{\sum_{i=1}^m w_i^2}\|x-v\|^2.
\]

The event with unchanged active coordinates has objective gap zero
regardless of its free endpoint assignment, by the checked fiber
identity. This verifies the stated margin and the claimed decision
for exactness of the proposed fiber. The no-active-coordinate case is
correctly separated as whole-domain constancy.

This addendum independently checks the corollary's proof, including its
endpoint branch. It does not report an executable mixed-fiber test or
replace the separate review of the underlying physical-shell theorem.
The same scoped whitespace, mathematical-delimiter, and local-link
checks passed after adding it.
