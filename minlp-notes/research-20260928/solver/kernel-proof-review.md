# Independent adversarial review of sparse kernel rounding

Date: 2026-09-28. Reviewer: `kernel_proof_review`, independent of the draft
author. Reviewed the proposed Jackson-kernel argument and the complete
[squared-Fejér draft](sparse-kernel-rounding.md), including its stated
assumptions, equations (1)–(17), and claimed consequences.

The box-only theorem in the reviewed draft passes this audit. I found no
substantive gap in the explicit squared-Fejér construction, positivity degree,
separator consistency, gluing, or objective comparison. This is evidence from
an independent proof review, not a formal proof or a novelty determination.
Several assumptions are essential and should remain explicit.

## 1. Kernel positivity and certificate degree

Fix a kernel output coordinate `y`. If a univariate polynomial `p(x)` is
nonnegative on `[-1,1]` and has degree at most `2s`, the interval positivity
theorem gives

\[
p=\sigma_0+(1-x^2)\sigma_1,
\qquad \deg\sigma_0\le2s,
\qquad \deg\sigma_1\le2s-2,
\]

where both coefficients are sums of squares. Thus the degree
`2(m-1)` of the draft's kernel gives exactly the bounds used in (11).
Multiplying these representations over a bag expands into products of SOS
polynomials, which remain SOS. Every complete preordering term has total
degree at most `2|B_b|(m-1)`, hence at most `2r` for
`m=floor(r/w)+1`. The dependence of a chosen SOS representation on `y`
need not be polynomial or measurable: it is used only to prove pointwise
nonnegativity of the already-defined polynomial `h_b(y)`.

The full preordering is used at this exact step. Ordinary quadratic-module
positivity does not justify arbitrary products of different box generators.

An independently delegated interval audit checked both parity cases. For an
odd actual degree `2s+1`, Markov–Lukács gives
`p=(1+x)a^2+(1-x)b^2`, with `deg a,deg b<=s`. The identity

\[
1\pm x=\tfrac12(1\pm x)^2+\tfrac12(1-x^2)
\]

converts it into the same quadratic-generator form, with complete terms of
degree at most `2s+2`. Therefore a general kernel of degree `q` requires
`|B_b| ceil(q/2)<=r`, not merely `|B_b|q<=2r`. The even degree in the draft
avoids this distinction. The interval formulas were checked against
[Nie and Zhang, equations (4.2)–(4.3)](https://link.springer.com/article/10.1007/s10013-024-00700-3).

### Counterexample to using only the polynomial degree

Take two variables, order `r=1`, and moments

\[
L(1)=1,\quad L(x)=L(y)=\tfrac12,\quad
L(x^2)=L(y^2)=1,\quad L(xy)=-\tfrac12.
\]

Its moment matrix is

\[
M=\begin{pmatrix}
1&1/2&1/2\\
1/2&1&-1/2\\
1/2&-1/2&1
\end{pmatrix},
\]

with eigenvalues `0,3/2,3/2`. Both order-one box localizers equal zero, so
this is feasible for the full preordering truncated at degree two. However,

\[
L((1-x)(1-y))=-\tfrac12.
\]

The degree-one Jackson kernel has `K_1(x,-1)=1-x`. Its two-coordinate tensor
has polynomial degree two, within the moment domain, but is evaluated
negatively. Its positivity certificate needs degree four. This does not
contradict the current draft; it rules out an easy but incorrect weakening
of the certificate-degree condition.

## 2. Squared-Fejér coefficients and the omitted-frequency issue

For `b_j=(m-|j|)_+`, the autocorrelation coefficients satisfy

\[
a_0=m^2+2\sum_{j=1}^{m-1}j^2=\frac{2m^3+m}{3},
\qquad a_0-a_1=\frac12\sum_j(b_j-b_{j-1})^2=m.
\]

There are exactly `2m` nonzero consecutive differences. Expanding
`|D_m(t)|^4` gives the claimed nonnegative trigonometric density and its
normalization. Autocorrelation gives `0<=g_k<=1`; for indices beyond
`2m-2` the coefficient is zero.

The inequality

\[
1-\cos(kt)=2\sin^2(kt/2)
           \le 2k^2\sin^2(t/2)=k^2(1-\cos t)
\]

holds for every integer `k>=0` and every real `t`. Integrating it against
the nonnegative circle density proves (6) for every `k`, including indices
above the kernel degree. The tail case is therefore covered by the proof,
not an unmentioned asymptotic assumption.

In (16), if any `alpha_i>2m-2`, orthogonality makes the integrated polynomial
identically zero; the displayed right side is also zero. The value
`L_b(T_alpha)` remains defined because only objective indices
`|alpha|<=d<=r` are needed. If all indices lie within the kernel support,
orthogonality gives the product of the coefficient multipliers. Interchanging
integration and `L_b` is legitimate because the kernel is a finite sum and
its input degree is at most `2r`.

Thus the draft does not need the stronger condition that the kernel degree
cover every objective frequency. It also does not invert the smoothing
operator, so zero multipliers pose no invertibility problem.

## 3. Local probability laws and exact separator agreement

Nonnegativity of `h_b` and kernel normalization establish that
`h_b dmu^{B_b}` is a genuine probability law. No representing measure for
the original truncated functional is assumed or needed.

For a separator `S`, marginalizing removes every coordinate kernel outside
`S`, since its integral is one. The remaining polynomial in the input
variables has total degree at most `2|S|(m-1)<=2r`. Adjacent moment agreement
therefore makes the two separator densities identical. This is equality of
whole marginal laws, not merely a finite list of their moments. It is the
main reason the subsequent gluing step is valid.

For the gluing, root the bag tree and process parents before children. The
running-intersection property implies that a child's intersection with all
previously attached variables is exactly its parent separator. Indeed, any
variable occurring in that child and an earlier bag occurs along their tree
path and hence in the parent. Conditional extension by the child law
therefore preserves existing bag laws and creates the desired child law.
Regular conditionals exist on these compact Euclidean boxes. Arbitrary
choices on separator-null events have no effect on the assembled law.

Using one common coordinate kernel is essential. If the same separator
coordinate were smoothed with different kernels in different bags, equality
of input moments would generally cease to imply equality of output
marginals. A possible anisotropic extension would have to use a common
kernel for each variable everywhere that variable occurs and separately
respect every bag's degree budget.

## 4. The pseudoexpectation bound and objective comparison

For `P=T_alpha` with `|alpha|<=r`, the identity

\[
1-P^2=\sum_{i:\alpha_i>0}(1-x_i^2)
 \left(U_{\alpha_i-1}(x_i)
       \prod_{j<i}T_{\alpha_j}(x_j)\right)^2
\]

has complete terms of degree at most `2|alpha|`. Positivity gives
`L(P^2)<=1`; positivity of squares and `L(1)=1` give
`|L(P)|^2<=L(P^2)`. This independently verifies (14). Only the local
quadratic module is needed for this particular bound, although the earlier
kernel positivity step needs the full preordering.

The degree condition here is `|alpha|<=r`. Being merely in the functional's
degree-`2r` domain would not justify this squared-polynomial proof. The
draft's choice `r>=d` is sufficient. Writing the sum over positive indices,
as above, avoids the otherwise undefined symbol `U_{-1}` in (15); the
draft already explains that zero indices contribute zero, so this is a
notation issue rather than a gap.

For multipliers in `[0,1]`, telescoping their product gives
`1-prod_i g_i<=sum_i(1-g_i)`. Combining this with the coefficient bound and
`|L(P)|<=1` proves (3). Since the assembled law is box-supported,
`f*<=int f dnu`; applying this to every feasible tuple gives the bound on
the infimum even if the infimum were not attained. The inequality
`m>r/w` gives the final width-dependent bound. Existence of a point no worse
than the mean follows from continuity and compactness; no algorithm for
finding that point follows automatically.

## 5. Strong duality is available, but is unnecessary for rounding

The draft is right not to require strong duality for its moment bound. If
an explicit sparse SOS-certificate consequence is desired, standard finite
dimensional SDP Slater duality applies in the stated box-only model.

Take the restrictions of one global product measure with positive density
throughout the box interior. For every nonzero local polynomial `q` in a
localizer basis,

\[
\int q(x)^2\prod_{i\in I}(1-x_i^2)\,d\mu^{B_b}(x)>0.
\]

Every local moment and localizing matrix is therefore positive definite,
and all separator equalities hold. This is a strictly feasible point in
the affine moment constraints. Redundant equalities can be removed without
changing the feasible set. The objective is finite below by the verified
Chebyshev moment bound. SDP Slater duality consequently gives equality to
the sparse SOS dual and attainment of the dual optimum.

The dual polynomial identity is in the sum of the bag preorderings.
Consistency on tree edges identifies every repeated monomial moment:
bags containing the support of a monomial form a connected subtree, as an
intersection of the variable occurrence subtrees. Thus there is no missing
global coefficient consistency condition in passing to the usual sparse
SOS formulation. This duality argument uses exact real arithmetic and says
nothing about a numerical solver's reported dual residuals.

## 6. Scope, significance, and literature check

The theorem applies to minimization over the full box. Additional local
polynomial constraints or integer equalities are not preserved by this
smoothing. A statement about the constrained optimum would require new
work; simply including those localizers in the input does not solve the
support problem. The need for `2^w` preordering products also remains.

The constant `A(f;B)` depends on the selected decomposition. Its size can
grow with the number of bags, coefficient cancellation, or the chosen
normalization. The exponent is independent of ambient dimension, but an
unqualified claim of a dimension-independent absolute error constant would
be misleading. A width-dependent certificate degree does not establish
practical SDP speed, numerical robustness, or bit complexity.

The following primary sources were examined on 2026-09-28:

- [Laurent and Slot, *An effective version of Schmüdgen's Positivstellensatz
  for the hypercube*](https://link.springer.com/article/10.1007/s11590-022-01922-5),
  especially Proposition 6 and Sections 3.1–3.2. This establishes positive
  Chebyshev/Jackson kernels, their coefficient estimates, and their tensor
  preordering membership for the dense box argument. Those ingredients are
  established prior work. The proposed use of matching smoothed local laws
  requires separate comparison; this source alone does not establish it.
- [Korda, Magron and Ríos-Zertuche, *Convergence rates for sums-of-squares
  hierarchies with correlative sparsity*](https://link.springer.com/article/10.1007/s10107-024-02071-6),
  especially the introductory statement of the sparse box result and its
  full-preordering definition. The inspected box bound has degree exponent
  `2/(w+3)` and uses running intersection. Its degree convention is
  coordinatewise, whereas this draft uses total degree. For fixed width
  these conventions differ by a width factor, not by the convergence
  exponent. Thus the claimed exponent improvement over this particular
  result is supported, subject to the draft's coefficient normalization.
- [Nie and Zhang, *Polynomial Optimization Over Unions of
  Sets*](https://link.springer.com/article/10.1007/s10013-024-00700-3),
  equations (4.2)–(4.3), for the interval positivity degree bounds.

Searches for combinations of “sparse”, “Jackson”, “marginal”, “gluing”, and
“correlative sparsity” did not reveal an equivalent result in this limited
audit. These searches do not establish novelty. The May 2026 preprint
[ *Squared polynomial approximation kernels for the hypercube: improved error
bounds and implications for Lasserre hierarchies*](https://arxiv.org/abs/2605.31496)
also appeared in search results and was passed to the lead researcher for
comparison; its full content was not inspected in this audit.

**Later source correction.** The completed
[ordinary-module prior audit](sparse-putinar-prior.md) independently
inspected July 2025 and February 2026 author slides that already assert
the inverse-square sparse preordering rate. This supersedes the initial
negative-search assessment above. The comparison with the slower printed
theorem remains accurate; novelty of the rate itself is not asserted.
The dense May 2026 kernel and its sparse transfer are assessed in that
later audit and the [final proof audit](signed-kernel-final-audit.md).

## 7. Targeted verification and what remains unchecked

Two local Python checks were run using `tools.exec_command` with
`python - <<'PY' ... PY` in the repository root:

1. An exact SymPy calculation constructed the displayed order-one moment
   matrix. It returned eigenvalues `{3/2: 2, 0: 1}` and evaluated the tensor
   kernel polynomial to `-1/2`. This checks the parity counterexample.
2. An exact `fractions.Fraction` calculation formed the triangular
   autocorrelations for every `m=2,...,40` and `k=0,...,4m`. All 3,315
   coefficient checks passed: the formula for `a_0`, the difference
   `a_0-a_1=m`, the bounds `0<=g_k<=1`, inequality (6), and zero tails beyond
   `2m-2`.

These finite computations catch indexing and arithmetic errors. They do
not prove the general kernel or rounding theorem; the arguments above
address those claims. No project-wide checks or CI inspection were run.
No Lean verification was attempted. No general constrained extension,
sampling complexity claim, or complete literature priority assessment is
certified by this review.

## 8. Follow-up review of the added finite-rounding section

The subsequently added Section 6 was also read. Its quadrature construction
is correct. For `N=m+floor(d_infty/2)`, the difference
`2N-1-[2(m-1)+d_infty]` is one for even `d_infty` and zero for odd
`d_infty`. Thus tensor quadrature exactly preserves normalization,
separator marginals, and each objective expectation. The finite grid bound
(20) follows. The added Slater and certificate argument agrees with the
independent argument in Section 5 above.

One computational claim needs qualification. The straightforward tree
dynamic program has `O(sum_b N^|B_b|)` table entries, but adding every child
message to its parent table costs
`O(sum_b (1+#children(b))N^|B_b|)` arithmetic operations, safely
`O(t N^w)`. Claiming the arithmetic count is always just the number of table
entries requires an additional aggregation argument or a bounded-degree
tree assumption. A large central bag can have many children. This issue
does not affect the rounding or certificate theorem. The conservative
`O(t N^w)` bound was recommended to the draft author.
