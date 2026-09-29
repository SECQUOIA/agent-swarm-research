# Review of the positive-denominator domain lift

Date: 2026-09-28. I independently checked the proposed reduction and then
read Section 9 of [the fractional optimizer note](common-range-fractional-witness.md#9-an-explicitly-positive-denominator-domain).
No gap was found. The corollary follows from the complete positive-denominator
optimization theorem already assembled in that note and
[the fractional value note](common-range-fractional-frontier.md).
This review checks the new reduction, parameter calculation, and transfer
of output guarantees; it does not reprove those underlying theorems or
establish novelty. A separate narrow reviewer also checked the projection
and attainment equivalences.

Let the finite objective family have size \(m\ge1\), let the original
native rational SOC set be \(F\), and write

\[
 d_j(z,x)=a_{j,z}^{T}z+a_{j,x}^{T}x+b_j,
 \qquad
 D=F\cap\bigcap_{j=1}^{m}\{d_j>0\}.
\]

The intended problem is to minimize \(\max_j p_j/d_j\) on the
mixed-integer part of \(D\). No sign promise is imposed on the rest
of \(F\). The set \(D\) is relatively open in \(F\); it need
not be open in the ambient space.

For each denominator the proposed cone is exactly

\[
 \|(2,d_j-s)\|_2\le d_j+s
 \quad\Longleftrightarrow\quad
 4-4d_js\le0,\qquad d_j+s\ge0.
\]

The sign condition is essential. The product inequality gives
\(d_js\ge1\), so the factors are nonzero and have the same sign.
The sum condition excludes two negative factors. Consequently the cone
is equivalent to \(d_j>0\), \(s>0\), and \(d_js\ge1\).
Conversely, at every point of \(D\), the finite number

\[
                         s=\max_j\frac1{d_j(z,x)}
\]

satisfies all the cones simultaneously. One shared real variable is
therefore sufficient. No separate strict row, lower bound on the
denominators, or explicit nonnegativity row for \(s\) is required.
An identically zero or negative constant denominator correctly makes the
lift infeasible.

Let \(\widetilde F\) be the augmented feasible set. It is a closed
convex set given by rational affine SOC rows, and its projection is
exactly \(D\). The same projection identity holds after requiring
\(z\in\mathbb Z^k\), since the new coordinate is continuous.
Keep every numerator and denominator independent of \(s\). Then the
original and lifted mixed-integer problems have exactly the same set of
objective values. This proves, without a compactness assumption, that
they have the same feasibility status, extended-real infimum, and
unboundedness-below status. An original minimizer lifts using the displayed
finite \(s\), and a lifted minimizer projects to an original minimizer.
Finite attainment and nonattainment are therefore preserved in both
directions.

The cross-aware parameter calculation can be made exact. Let
\(K_*\subseteq\mathbb R^n\) be the original common continuous
kernel, let \(\rho=n-\dim K_*\), and put

\[
 L=K_*\cap\bigcap_j\ker a_{j,x}^{T},\qquad
 \ell=\dim K_*-\dim L.
\]

With full coordinate order \((z,x,s)\), the Hessian of the new
squared residual \(4-4d_js\) acts on a continuous direction as

\[
 \widetilde H_j(0,v,\sigma)
   =-4\bigl(\sigma a_{j,z},\ \sigma a_{j,x},\ a_{j,x}^{T}v\bigr).
\]

The extended native Hessians require exactly \(v\in K_*\).
It follows that the full new common continuous kernel is

\[
 \widetilde K_*
 =L\times
   \{\sigma\in\mathbb R:
       \sigma(a_{j,z},a_{j,x})=0\text{ for every }j\}.
\]

In particular,

\[
 \widetilde\rho\le\rho+\ell+1.
\]

If at least one denominator has a nonzero full gradient, equality holds.
If all denominators are constant, then \(\ell=0\), every new
residual is affine in \(s\), and \(\widetilde\rho=\rho\).
The stated upper bound is correct in all cases and is sufficient for the
corollary.

Every lifted denominator has continuous gradient \((a_{j,x},0)\).
The last coordinate in the displayed Hessian action shows that this
gradient annihilates \(\widetilde K_*\). Thus the new restricted
denominator rank is exactly zero, rather than merely bounded by the old
\(\ell\). Applying the existing theorem with parameters
\((k,\widetilde\rho,0)\) gives the claimed
\(f(k,\rho,\ell)N^C\) bound. For one ratio, \(\ell\le1\)
and \(\widetilde\rho\le\rho+2\).

Using full Hessians is necessary here. A denominator depending only on an
integer coordinate has \(a_{j,x}=0\), so the new continuous-continuous
Hessian block vanishes. Its integer-\(s\) cross block still excludes
the \(s\) direction from the cross-aware kernel. The manuscript's
definition and proof include this case.

The construction introduces one continuous variable and \(m\) cones,
each with two norm entries and rational affine data copied from an input
denominator. Its explicit bit length is polynomial in the original input
length, with an absolute exponent. No reciprocal is computed or printed
when constructing the instance. The reciprocal choice above proves
existence of a lift and is not an input-size assertion. The existing
theorem supplies its own bounds for the lifted canonical point, including
\(s\), whenever the optimal level is nonempty.

All denominators are strictly positive throughout the entire real lifted
feasible set. This is the global positivity needed by the value theorem;
positivity only on integer fibers is not being substituted for it.
The attainment algorithm boxes the lifted variables, including \(s\),
so its queried feasible sets remain closed and compact. On each nonempty
such set, every denominator has a positive minimum and the maximum of
ratios is continuous. The compact value comparisons in the existing
proof therefore remain valid. No compactness claim is made for the
original positive domain inside an original-coordinate box.

Discarding \(s\) from an exact lifted optimizer gives an exact original
optimizer. It cannot increase the field degree or output length. The
selected point is canonical for the lifted construction; its projection
need not minimize a norm in the original coordinates. Section 9 states
this limitation correctly.

The lift does not preserve geometric boundedness: whenever it is
nonempty, increasing \(s\) preserves feasibility. Nor does closedness
of the lift force attainment. For example, on \(0\le x\le1\), the
positive-domain objective

\[
                  \max\{x/1,\ 0/x\},\qquad x>0,
\]

has infimum zero and no minimizer. Its lift requires \(s\ge1\)
and \(xs\ge1\). Along \(x\downarrow0\), the auxiliary coordinate
diverges, so the same infimum remains unattained in the closed lift.
Bounding or penalizing \(s\) before applying the proven canonical-point
bound would change the problem. None of these changes is made in the
manuscript.

The usual maximum-of-ratios problem has a finite nonempty objective
family. If an empty family is admitted by another convention, its
objective must be defined separately and the maximum reciprocal formula
cannot be used. Infinite families are outside the explicit finite input
model and would require an additional uniform bound for a shared lift.

Targeted verification used an inline `python -` command with exact SymPy
arithmetic. It checked the residual identity, the symbolic full-Hessian
action, three common-kernel examples, the integer-only denominator cross
block, and reciprocal boundary points with denominators \(1/1000\),
\(2/3\), and \(17/2\). The kernel examples used the native residual
\((z+x_1)^2-1\): correlated denominators
\(z+x_2+2,2z+2x_2+3,x_1+1\) gave new codimension three; the
integer-only denominator \(z+2\) gave two; constant denominators
\(2,3\) left it at one. Every new denominator annihilated each computed
kernel. All assertions passed. These finite calculations support the
algebra and boundary cases, not the universal complexity theorem.

A second targeted inline Python command checked this review's final
newline, trailing whitespace, control characters, paired math delimiters,
and local Markdown link targets. No project-wide verification, CI
inspection, or formal proof check was performed.
