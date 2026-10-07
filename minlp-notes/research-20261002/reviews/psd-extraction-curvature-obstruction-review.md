# Independent review of the PSD-extraction curvature obstruction

Date: 2026-10-02. Verdict: **PASS**. The final
[obstruction manuscript](../new-direction/psd-extraction-curvature-obstruction.md),
including its PSD-plus-nonnegative extension and direct geometric-grid
resolution corollary, passes this adversarial mathematical review.
No substantive gap remains. This is a preprocessing and specified-grid
obstruction, not optimization hardness or a priority claim.

## Growth, domain, and negative-curvature conventions

The Horn matrix is \(H=\mathbf1\mathbf1^T-2\operatorname{Adj}(C_5)\).
The manuscript recalls a valid elementary proof of copositivity: on the
simplex a maximum cycle edge sum has a minimum-support maximizer whose
support is a clique, hence has value at most \(1/4\). Positive diagonal
congruence preserves copositivity.

The five vectors \(z_i=D^{-1}(e_i+e_{i+1})\) are zeros of the
unperturbed form \(DHD\), not zeros of \(A_d=DHD+\varepsilon I\).
For \(d\ge1\) they all belong to \([0,1]^5\), and the perturbed
growth ratio at every one is exactly \(\varepsilon\). The lower bound
on the whole nonnegative orthant and these feasible equality witnesses
prove that both domains have best margin exactly \(g=1/100\), with
unique minimizer zero. There is no box-versus-orthant loss in this claim.

Completing the first square leaves the displayed four-by-four matrix
\(S\). Its maximum absolute row sum is four, so the ambient quadratic
matrix is bounded below by \(-4I\), independently of \(d\).
Because the objective is \(x^TA_dx\), its Hessian is \(2A_d\).
Thus the stated Hessian negative curvature is at most 8, and
\(\nu_d/g\le800\). A sharper bound is unnecessary. The explicit
negative direction has first coordinate \(-2/d\); it establishes
ambient nonconvexity and is not asserted to be feasible in the orthant.

Every off-diagonal entry is nonzero, so the interaction graph really is
\(K_5\), with bag size five and treewidth four. For integer \(d\),
the family's binary input length is \(\Theta(\log(d+1))\).

## The universal PSD extraction bound

For a decomposition \(A_d=P+R\), with \(P\succeq0\) and \(R\)
copositive, each scaled Horn ray gives

\[
 z_i^TPz_i\le\varepsilon\|z_i\|^2.
\]

The alternating sum identity and total squared lengths are exact:

\[
 e_1=\frac d2(z_1-z_2+z_3-z_4+z_5),\qquad
 \sum_i\|z_i\|^2=8+2/d^2.
\]

PSD Cauchy--Schwarz therefore yields

\[
 P_{11}\le\frac{5d^2}{4}\sum_i z_i^TPz_i
       \le10\varepsilon d^2+\frac52\varepsilon
       =\frac{d^2}{10}+\frac1{40}.
\]

The argument allows singular PSD matrices and arbitrary real entries.
It is not restricted to a spectral projection, sparse extraction, or
an algorithmically chosen family of matrices.

An equivalent rational matrix certificate makes the universal inequality
particularly explicit. Let \(Z\) have columns \(z_i\), and let
\(s=(1,-1,1,-1,1)^T\). Then

\[
 W=\frac{d^2}{4}Z(5I-ss^T)Z^T
   =\frac{5d^2}{4}\sum_i z_i z_i^T-e_1e_1^T\succeq0.
\]

Taking \(\operatorname{tr}(PW)\ge0\) gives the same bound. This
form does not require computing a square root of the extracted matrix.
It is an alternative proof of the scalar step, not an assumption on
the extraction.

Subtracting from \((A_d)_{11}=d^2+\varepsilon\) gives

\[
 R_{11}\ge\frac9{10}d^2-\frac3{200}
          \ge\frac{177}{200}d^2\ge\frac78d^2
 \qquad(d\ge1).
\]

If only nonnegativity of the homogeneous remainder on the unit box had
been assumed, the same ray tests would already suffice for this bound.
Moreover that box nonnegativity is equivalent to orthant copositivity by
positive scaling. Thus the proof has not silently strengthened a local
box positivity requirement in a way that creates the obstruction.

## The additional entrywise-nonnegative extraction is covered

For \(A_d=P+N+R\), absorb the nonnegative diagonal of \(N\) into
\(P\). The new PSD matrix is \(P'=P+\operatorname{diag}(N)\),
and \(R'=R+N-\operatorname{diag}(N)\) remains copositive.
Its diagonal equals that of \(R\). The PSD-only bound therefore proves
the same residual-diagonal bound, with no weaker constant.

This step specifically uses entrywise nonnegativity of \(N\). It does
not claim the result for an arbitrary additional copositive quadratic.
The scope in the final manuscript is correct.

If the remainder is strictly copositive, its best margin satisfies
\(0<g_R\le\varepsilon\), by evaluating its ratio on any of the
five rays and using nonnegativity of the extracted terms. Thus
\(L_R/g_R\ge175d^2\), where \(L_R=2\max_iR_{ii}\).
For a zero-margin remainder the positive-margin certificate has no
success to discover. The statement in terms of a bound on \(\nu/g\)
is precise: those upper bounds stay constant while the residual ratio
diverges. It does not rely on treating a varying exact real ratio as an
integer parameter.

## The added geometric-grid corollary is valid

The prescribed common geometric grid always contains the axis vector
\(e_2\). Since extracted diagonal entries are nonnegative,
\(R_{22}\le101/100\). Its acceptance quantity is consequently at
most \(101/100-(11/5)\sigma\). A positive certificate requires
\(\sigma<101/220<1/2\).

Combining this necessary condition with
\(\sigma=L_R\delta^2/8\) and \(L_R\ge7d^2/4\) gives
\(\delta^{-1}>\sqrt7\,d/4>d/2\). Every interval in the actual
common grid is at most \(\delta\) long, including its initial and
clipped final intervals. Therefore covering \([0,1]\) requires at
least \(1+\delta^{-1}\) labels.

This proves an actual unbounded, potentially exponential-in-original-input
state count for that prescribed grid construction, after every admissible
extraction that permits success. It is stronger than merely substituting
a large parameter into an upper complexity bound. The final text correctly
excludes coordinate-specific grids, modified corrections, implicit
alternative certificates, and joint convex recourse from this corollary.

## Why the positivity restriction is essential

The displayed rank-one extraction \(P_0=(d,h)(d,h)^T\) is PSD and
leaves \(\operatorname{diag}(0,S)+\varepsilon I\). That remainder
has bounded norm and diagonal \(\varepsilon\), independently of
\(d\), but has value \(-4+2\varepsilon\) at the nonnegative vector
\((0,0,1,1,0)\). Thus unrestricted convex extraction can remove the
large diagonal. What fails is simultaneously requiring the residual to
be nonnegative at the same corner.

The five-dimensional family is not evidence of computational hardness:
fixed-dimensional box QP can be solved by other exact methods. The
manuscript correctly limits the conclusion to positivity-preserving
quadratic extraction in the original coordinates and the stated
common-grid reduction. It does not rule out the broader sparse
negative-curvature objective.

## Targeted verification actually performed

The reviewer ran

```sh
python research-20261002/reviews/check_psd_extraction_dual.py
```

The [persistent checker](check_psd_extraction_dual.py) passed 31 exact
principal-minor checks of the constant dual PSD core, the universal
symbolic matrix factorization, and the ray-budget/residual constants.
It also passed 77 exact axis-threshold checks, including \(d=2^{200}\),
and three checks of the actual common grid's interval sizes and label
count. An initial diagnostic assertion compared factored and expanded
symbolic expressions structurally; replacing it by an exact zero-difference
check resolved that representation-only failure. No mathematical bound
was changed.

A separate reviewer reported an independently executed inline rational
diagnostic for \(d=1,\ldots,100\): 500 ray equalities, 100 alternating
identities, 1,000 sampled box-growth checks, 100 sign-changing residual
witnesses, and the extraction constants. Those results are attributed
to that reviewer; this review did not rerun their diagnostic.

The finite checks supplement the universal argument and do not establish
algorithmic hardness. No project-wide checks, CI inspection, or external
literature search were performed for this review.

## Addendum: explicit diagonal preconditioning

The reviewer reread the added diagonal-rescaling paragraph in the actual
note. Its escape from the obstruction is valid. Under \(u=Dx\), the
quadratic matrix becomes
\(H+\epsilon\operatorname{diag}(d^{-2},1,1,1,1)\), whose diagonal
curvature is at most \(2(1+\epsilon)\). Write \(u=(a,y)\ge0\) and
\(b=\|y\|\). Copositivity of the trailing principal submatrix and
\(\|h\|=2\) give \(u^THu\ge a^2-4ab\). For \(b\le a/8\), this is
at least \(a^2/2\ge32\|u\|^2/65\). Otherwise copositivity of the
whole Horn matrix and the perturbation give a lower bound
\(\epsilon b^2\ge\epsilon\|u\|^2/65\). Consequently the asserted
uniform growth \(\epsilon/65\) and ratio bound \(13130\) hold.

This is a concrete limitation of the example: it obstructs the specified
positivity-preserving extraction in the original coordinates, but does
not obstruct combined diagonal preconditioning. The homogeneous orthant
certificate can use its normalized shell after this change; the larger
transformed box does not force the original common-grid lower bound.
This addendum is an algebraic actual-file review, not an additional
numerical test.
