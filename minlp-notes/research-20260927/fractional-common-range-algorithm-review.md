# Independent review of common-range fractional optimizer recovery

Date: 2026-09-28. Status: the recovery argument passes, conditional on its
stated joint-field and height bound and the common-range fractional value
theorem. I read the final
[fractional witness manuscript](common-range-fractional-witness.md),
including its mixed-integer and maximum-of-ratios extensions, and found no
remaining algorithmic gap under those inputs.

This review checks recovery after an exact attained value and an attaining
integer assignment are known, and the uniform-box extension that supplies
attainment and integer recovery. It does not prove the separate arithmetic
bound for the selected point. The underlying arguments read were
[common-range feasible-point recovery](common-range-witness-recovery.md),
[common-range feasibility](common-range-fpt-frontier.md),
[fractional common-range values](common-range-fractional-frontier.md), and
Section 6 of [the quasiconvex value note](quasiconvex-mixed-value-frontier.md).
The field conversion was checked against
[constructive common-field recovery](constructive-common-field-recovery.md).

## 1. Fixed coordinates and the selected point

Let \(F_z\) be the nonempty continuous feasible set at the selected
integer assignment, and let its attained ratio minimum be \(\theta\).
All native rows remain rational after substitution. Their encoding length
must include that of \(z\); an FPT bound in the original input alone
therefore uses the separate bound on a small attaining assignment.

Retain the denominator gradient by replacing the cross-aware kernel with

\[
 K'=K_*\cap\ker(d_x^T),\qquad
 x=T_1u+T_0v,\qquad \dim u\le\rho+1.
\]

The transformation is rational and fixed before choosing the canonical
point. Each native polynomial, cone sign condition, and affine row has a
constant rational coefficient on \(v\). The denominator is independent
of \(v\), so the optimality equation is

\[
 f_v^Tv=\theta d_0(z,u)-f_0(z,u).
\]

Encode it by its two inequality signs. The complete optimal fiber is
\(C'v\le b_\theta(u)\), where \(C'\) is rational and constant.
The two new normals are \(f_v^T\) and \(-f_v^T\); neither contains
\(\theta\). This is the reason the denominator direction matters.

Farkas elimination gives the projection of the optimal set by finitely
many weak polynomial inequalities in \(u\). Thus the projection is
closed. It is convex because the original optimal set is a convex set
intersected with an affine equality. There is a unique minimum-norm
projected point \(u^*\), and its polyhedral fiber has a unique
minimum-norm point \(v^*\).

Closedness is not being inferred from a general statement about convex
projections. Positivity of \(d\) is a hypothesis on the original closed
feasible set; no strict row \(d>0\) is appended to its description.
The selected norms are in the displayed coordinates, which need not be
orthogonal in the original variables.

## 2. Why the compact value oracle is exact

Assume an effective joint-field degree bound and coordinate-height bound
for \((\theta,u^*,v^*)\) of the form \(g(k,\rho)N^C\), with
parameter-only degree and an absolute exponent \(C\). A root bound
then prints a rational \(B\ge1\) containing this pair in
\([-B,B]^{\dim u+\dim v}\), with FPT bit length.

Every test intersects the rational native feasible set with that entire
transformed box and with additional rational norm or coordinate cuts.
The resulting domain is closed and bounded. If nonempty, its denominator
is strictly positive and therefore has a positive minimum there. The ratio
is continuous on that compact domain and attains its minimum \(\beta\).
Consequently

\[
 \beta=\theta
 \quad\Longleftrightarrow\quad
 \text{the test domain contains a point of the original optimal set}.
\]

An empty domain returns false. This argument does not assume attainment
for an unboxed slice. For example, on \(w\ge0\), \(y\ge1\),
the ratio \(w/y\) has attained minimum zero. After the rational cut
\(w\ge1\), its unboxed infimum remains zero but the optimal level is
empty. The cut domain in a full finite box of radius \(B\ge1\) has
minimum \(1/B>0\), so the proposed equality test correctly rejects it.
A positive denominator lower bound need not be part of the input or
computed by the algorithm.

The value comparison is an ordinary exact comparison of two univariate
real algebraic numbers, using their polynomials and isolating intervals.
Each comparison has polynomial cost in those descriptions. There is no
reason to construct a compositum of the fields of all query values.

For native PSD quadratic input, the new norm threshold is a PSD quadratic
row. For native SOC input, it is represented by

\[
 \|u\|^2\le t
 \quad\Longleftrightarrow\quad
 \|(2u,t-1)\|\le t+1,\qquad t\ge0.
\]

Writing \(u=Lx\), its squared Hessian is \(8L^TL\) and kills
\(K'\). Affine cuts and box rows have zero Hessian. Thus every value
query stays within common range at most \(\rho+1\). Native convex
or SOC representations are retained; the squared SOC rows alone are not
used as a convex oracle input.

## 3. Approximation selects the same point at every precision

Let \(O_B\) denote the original optimal set intersected with the full
box. The box contains \((u^*,v^*)\), so its projection still has
minimum-norm point \(u^*\), even though some other optimal fibers may
have been removed. This is the precise box-preservation requirement.
A box for an unspecified optimizer would not suffice.

Use the oracle above to bisect \(\nu=\|u^*\|^2\) between zero and
\((\dim u)B^2\). For requested coordinate error \(\eta\), find a
rational feasible upper threshold
\(\nu\le t\le\nu+\eta^2/16\). Every projected point \(y\)
in the retained optimal norm slice satisfies the projection inequality

\[
 \|y-u^*\|^2\le\|y\|^2-\|u^*\|^2\le\eta^2/16.
\]

Now bisect its \(u\)-coordinate intervals, retaining a half precisely
when the compact ratio oracle returns value \(\theta\). The retained
set stays nonempty. When all widths are at most \(\eta/2\), the
coordinatewise rational midpoint is within \(\eta\) of \(u^*\).
This uses one feasible point in the final retained box and does not require
the midpoint itself to be feasible.

Each new accuracy request must restart from the original full box.
Intermediate coordinate choices can exclude \(u^*\), while preserving
a point in the thin norm slice. Reusing such choices at finer accuracy
would not approximate the same canonical point. The proposed restart
rule avoids this issue. If \(u\) has dimension zero, skip these steps.

## 4. The affine fiber needs no algebraic optimization oracle

At \(u^*\), put \(b^*=b_\theta(u^*)\). For a rational
coordinatewise approximation with error at most \(\delta\), set

\[
 \widehat b=\widetilde b+\delta\mathbf1,
 \qquad b^*\le\widehat b\le b^*+2\delta\mathbf1.
\]

Solve the rational strictly convex minimum-norm QP
\(\min\{\|v\|^2:C'v\le\widehat b\}\). Its feasible set
contains the exact fiber, so its rational minimizer \(v_\delta\)
exists and has norm at most \(\|v^*\|\). This remains true for
opposite equality rows: both right-hand sides must be rounded outward,
independently. Zero and dependent normals cause no difficulty.

The rational-matrix Hoffman estimate from the recovery note supplies a
uniform \(H_{C'}\) with polynomially bounded logarithm. If
\(V\ge\|v^*\|\) and \(\zeta=2H_{C'}\delta\), the same projection
argument gives

\[
 \|v_\delta-v^*\|
 \le\zeta+\sqrt{2V\zeta+\zeta^2}.
\]

For \(0<\epsilon\le1\), taking
\(\delta\le\epsilon^2/[32H_{C'}(V+1)]\) makes this less than
\(\epsilon\). Evaluating the bounded-degree polynomial
\(b_\theta(u^*)\) to this accuracy requires only polynomially many
extra bits in the input size, magnitude bounds, and requested precision.
There is no division by the denominator.

An independent narrow reviewer checked this adaptation, including the
equality rows, zero normals, outward rounding, and rational-QP import.
The active-row formula also gives

\[
 v^*=C_I'^T(C'_IC_I'^T)^{-1}b_I^*,
 \qquad v^*\in\mathbb Q(\theta,u^*).
\]

Thus fiber recovery introduces no field extension. If there are no
\(v\) variables, this stage is empty. The row subsets in this existence
formula are not enumerated by the algorithm.

## 5. Recognition and FPT composition

Approximate the tuple \((\theta,u^*,v^*)\) together, retaining the
specified real root of the already known value. Apply absolute KLL
recognition and the common-field construction with the certified joint
degree and height bounds. Including \(\theta\) makes the final
optimality equation evaluable in the same field. It avoids any implicit
claim that \(\theta\) automatically belongs to \(\mathbb Q(u^*)\).

If query coefficients have \(M=g(k,\rho)N^C\) bits, each rational
value call costs \(g_1(k,\rho)M^{C_1}\), with absolute \(C_1\).
There are polynomially many norm, coordinate, and recognition calls in
the certified bounds and the requested precision. Rational QP,
univariate equality comparison, and common-field recognition also have
absolute polynomial overhead. The composition remains
\(g_2(k,\rho)N^{C_2}\), with absolute \(C_2\). An oracle with
input exponent depending on the parameters would not justify this step.

Finally transform back with the fixed rational coordinate map and verify
the original native constraints, retained cone signs, strict denominator
positivity, and \(f-\theta d=0\) by exact common-field substitution
and sign determination. Since \(\theta\) is independently known to
be the global infimum, this equality verifies optimality. The output need
not include a constraint-qualification-dependent KKT certificate.

## 6. Uniform boxing also gives attainment and integer recovery

The continuous encoding argument can be used before attainment is known:
it bounds the selected point of every nonempty \(\theta\)-level.
Suppose the value theorem supplies an effective bit bound \(M\) for
some attaining integer assignment, conditional on attainment. Fix one
global rational coordinate split from the cross-aware kernel and the
denominator kernel. Substitution of any integer vector with at most
\(M\) bits gives coefficient lengths polynomial in \(N+M\).
The encoding statement therefore prints a single transformed continuous
box containing the canonical point of every nonempty optimal level in
the integer box, with bound \(g(k,\rho)N^C\).

The intersection of both boxes with the original mixed-integer domain
is a finite union of compact continuous fibers. A nonempty intersection
has an attained ratio minimum \(\beta\). The original problem attains
its finite infimum exactly when this boxed domain is nonempty and
\(\beta=\theta\). Necessity uses the small attaining-integer bound
and the uniform canonical box. Sufficiency uses compactness of the
boxed mixed domain.

When equality holds, integer interval bisection keeps a half exactly
when its boxed value is \(\theta\). Each retained half contains an
actual optimizer. Polynomially many queries in the integer-box bit
length fix an attaining assignment. Its canonical continuous point is
still in the same uniform box, so the recovery argument above applies.
The value theorem's integer-size bound by itself would not justify this
integer recovery; compact boxing is the additional algorithmic step.

For an explicitly bounded integer domain, one can use the continuous
common range after fixing each integer assignment. Uniform continuous
value bounds then apply to every fiber in the finite integer box. A
finite global infimum is one of these fiber infima, so it has the same
uniform algebraic bound. Rational recognition queries use the
bounded-integer common-range feasibility oracle. No enumeration of the
integer assignments is required for this bound or algorithm.

The unconditional corollary must use the native model supported by its
value oracle. The fractional value manuscript currently states MISOCP.
The same threshold and Farkas proof also applies to native PSD quadratic
rows when the common-range feasibility theorem is used for that model,
but that extension should be stated rather than assumed from a title.

## 7. The maximum of several positive-denominator ratios

For \(\min_F\max_j p_j/d_j\), assume that each \(d_j>0\)
throughout the original closed feasible set. Let \(\ell\) be the rank
of the denominator gradients restricted to the original common kernel.
Intersect that kernel with all denominator kernels. The retained
dimension is at most \(r_0+\ell\). At a known global optimum
\(\theta\), the optimal set is exactly

\[
 F\cap\bigcap_j\{p_j-\theta d_j\le0\}.
\]

Every new row has rational eliminated-variable normal \(p_{j,v}\),
and its right-hand side is affine in \(\theta\) and has total degree
at most two in \((\theta,u)\). The same Farkas, canonical-point,
field-degree, and height arguments apply. A union over which ratio is
tight is unnecessary. The number of objective ratios enters through the
explicit input length and the logarithmic implicit-row count.

On each compact query domain, every denominator stays positive, so the
maximum of the ratios is continuous and attains its minimum. Equality
of that minimum with \(\theta\) again decides intersection with the
optimal set. Added \(u\)-norm rows preserve the refined kernel, on
which every denominator gradient is zero. Thus the maximum-of-ratios
value oracle has the required parameter control. Final verification
checks all denominator signs and all \(p_j-\theta d_j\le0\).
The independently known global lower bound \(\theta\) then proves
the returned objective equals \(\theta\).

## 8. Targeted verification and limits

Ran one inline `python -` command with exact SymPy arithmetic. It checked
the denominator-gradient kernel refinement, preservation of that kernel
by the added norm Hessian, an irrational optimality equality, and the
rational active-row fiber formula for
\(\|(1,1)\|\le u\), \(1\le w\le2\), \(v\ge u\),
minimizing \(v/w\). Its optimizer is
\((u,w,v)=(\sqrt2,2,\sqrt2)\), with value \(\sqrt2/2\).
All assertions passed. The unbounded version also checked its positive
boxed value symbolically. A second exact calculation checked the rational
cut example in Section 2, which has an attained original optimum but an
unattained cut-domain infimum.

These calculations check finite examples and exact identities, not the
general theorem or an implementation of the value oracle or KLL. The
proof above remains conditional on the separate effective joint-field
bound and the reviewed value and feasibility results. No novelty audit,
project-wide verification, CI inspection, or Lean formalization was
performed.

A targeted inline `python -` document check passed final-newline,
trailing-space, control-character, paired math-delimiter, and local-link
checks for this review only. The final read also corrected an earlier
dependency sentence: the value theorem supplies an attaining-integer size
bound, while the witness manuscript's own compact-box procedure performs
integer recovery.
