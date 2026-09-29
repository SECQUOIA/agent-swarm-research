# Fresh adversarial review of common-range witness recovery

Date: 2026-09-28. Reviewed manuscript:
[common-range-witness-recovery.md](common-range-witness-recovery.md).
I did not develop this witness proof. I read the complete saved manuscript,
the common-range decision proof and its review, the genericity and
finite-quotient lemmas, and the common-field recovery construction. A
separate fresh reviewer independently attacked the affine-fiber and
recognition steps in Sections 5--6. Neither review found a substantive gap.

The degree bound is genuinely \(2^{O(r)}\), and the complete recovery
cost has the stated form \(2^{O(r)}N^C\) with an absolute input exponent.
This conclusion uses the separately reviewed exact common-range decision
algorithm and the stated classical rational-QP and algebraic-recognition
imports. It is not formal verification or a publication-priority finding.
No mathematical correction was needed during this review.

## 1. The projection and canonical choices are well defined

Symmetry and \(H_iT_0=0\) remove both quadratic kernel terms and mixed
terms involving a kernel coordinate. Consequently all transformed rows,
including cone signs and both signs of equalities, have the form
\(Cv\le b(u)\) with a constant rational \(C\). Farkas elimination
therefore gives an exact finite family of weak quadratic inequalities
in \(u\). Rational minor bounds control each projected row separately;
no common denominator is taken over the entire potentially exponential
family. This gives polynomial coefficient bits and polynomial
\(\log(S+1)\).

The exact finite description proves closedness of this projection.
Convexity comes from the supplied native convex quadratic or SOC model.
Thus a nonempty projection has a unique minimum-norm point \(u^*\).
Its fiber is a nonempty closed polyhedron and has a unique minimum-norm
point \(v^*\). These choices specify one tuple independently of any
approximation accuracy. They need not minimize the original-coordinate
norm, as the manuscript correctly states.

The claim would not follow by asserting that every projection of a closed
convex set is closed. It also would not provide the decision oracle for
an arbitrary quadratic description promised to define a convex set.
The proof uses both the constant eliminated-variable matrix and the
original convex representation.

## 2. Many projected rows do not enlarge the arithmetic exponent

The arithmetic lemma needs genericity only for subsets of at most \(r\)
active rows and for subsets of \(r+1\) rows whose simultaneous vanishing
must be excluded. It does not use a bad polynomial depending on all
\(S\) constraints through its dimension. For a fixed subset, the
underlying incidence calculation has polynomially many variables in
\(r\), and a containing bad hypersurface has degree
\(2^{\operatorname{poly}(r)}\).

For each nonzero perturbation parameter, the selected perturbation
coefficients map onto arbitrary selected quadratics and an arbitrary
objective quadratic. Each substituted bad polynomial is consequently
nonzero. Choosing one nonzero parameter coefficient from each such
polynomial and multiplying gives degree at most
\[
 (S+1)^{r+1}2^{\operatorname{poly}(r)}.
\]
The integer-grid argument depends on this total degree, not on the
number of coefficient variables in the grid. Thus every perturbation
coefficient has bit length
\(O(r\log(S+1))+\operatorname{poly}(r)\).
The complete perturbation vector can be exponentially long; the proof
never constructs it or treats its total length as an algorithmic input.

The unknown-box argument is valid. At small positive perturbations the
original \(u^*\) is feasible. Compactness gives perturbed minimizers,
and every cluster is feasible with norm at most \(\|u^*\|\).
Uniqueness forces every cluster to equal \(u^*\). A sequence of box
boundary minimizers would instead have a boundary cluster, so all box
rows are eventually inactive. The unknown radius therefore occurs in
no eventual KKT coefficient.

At most \(s\le r\) perturbed rows are active. Passing to a subsequence
fixes this set, and the full KKT equations have
\(q=r+s\le2r\) variables. Constraint equations are quadratic in
\(u\), and stationarity is bilinear in \((u,\lambda)\), so every
equation has total degree at most two. Genericity supplies a nonsingular
full KKT Jacobian. Invertibility of the multiplier Hessian is not needed
for this use of the full system.

The finite-quotient lemma with \(a=2\) has dimension
\(L=3^q\le9^r\). Its coefficient bound is polynomial in \(q\)
times \(L\) and the input coefficient-norm logarithm. Hence the
coordinate annihilator heights are
\[
 (\tau+\log(S+1)+1)2^{O(r)}.
\]
The factor-height bound preserves this form for minimal polynomials.
Applying the same system and sequence to any rational linear form in
\(u\) leaves its degree bound \(L\) unchanged. A primitive rational
linear form then proves the joint-field bound \(L\); multiplying the
individual coordinate degrees would give an unnecessarily weaker bound.

All polynomial factors in \(r\), including the logarithm of the generic
bad-set degree, are absorbed into \(2^{O(r)}\). No ambient dimension
or projected-row count enters the exponent of the explicit input size.

## 3. Rational queries approximate the same nonlinear point

The effective meeting radius gives a bound on one projected point.
Increasing its coordinate radius by a factor of \(r\) bounds \(u^*\)
through minimum Euclidean norm. The radius is computed as a bound; the
algorithm does not first need to find that point.

The added norm constraint has Hessian \(8L^TL\) in original
coordinates, where \(\ker L=K\). It annihilates \(K\), and so it
does not increase the common range dimension. Coordinate bounds are
affine. For native PSD rows the norm constraint stays a native PSD row;
for an SOC system the manuscript gives a rational cone representation.

Norm bisection maintains a feasible upper cap. Every feasible point under
that cap is close to the specified \(u^*\) by the convex projection
inequality. Coordinate bisection only has to preserve a nonempty
intersection with this capped set; its rational midpoint need not be
feasible. Each new accuracy request restarts from the original box,
because a previously retained box may exclude \(u^*\) itself.
These invariants supply a certified approximation to one fixed tuple.

Only the current coordinate endpoints and one norm cap are retained.
The query structure is polynomial in the original structure, independent
of the number of earlier bisections. Increased precision changes
coefficient bits. The decision theorem's absolute polynomial dependence
on those bits therefore gives
\(2^{O(r)}(N+p)^C\) cost at requested accuracy \(2^{-p}\).

## 4. Affine recovery does not introduce new algebraic degrees

The polyhedral normal-cone formula places \(v^*\) in the span of its
active rational row normals, including when the fiber has lineality or
an irrational right-hand side. Choosing independent active rows spanning
that vector gives
\[
 v^*=C_I^T(C_IC_I^T)^{-1}b_I(u^*).
\]
The inverse has rational coefficients with polynomial bit length.
The algorithm need not identify \(I\). This existence formula proves
that each fiber coordinate is a rational quadratic polynomial in
\(u^*\), so all coordinates remain in its existing joint field.
If \(v^*=0\), the empty row set suffices.

Here is explicit height accounting. Write
\(d=[\mathbb Q(u^*):\mathbb Q]\) and let \(H\) bound coordinate
minimal-polynomial coefficient bits. The product \(A\) of their
leading-coefficient magnitudes satisfies \(\log A\le rH\), and
every \(Au_j^*\) is integral. For a fiber coordinate, let \(D_0\)
clear the rational coefficients of its quadratic expression, with
\(\log D_0\le N^{O(1)}\). Then \(D_0A^2v_j^*\) is integral.
The square is necessary for quadratic evaluation.

Every conjugate of that coordinate has logarithmic magnitude at most
\(N^{O(1)}+2H+O(\log(r+1))\). Its field norm after the stated
denominator clearing gives an integer annihilator of degree at most
\(d\), with coefficient bits bounded by
\[
 O\!\left(d\,[N^{O(1)}+rH+\log(d+1)]\right).
\]
Substituting \(d,H\le2^{O(r)}N^{O(1)}\) preserves
\(2^{O(r)}N^C\). There is no product of ambient-coordinate degrees.

Outward rational right-hand sides are essential: they preserve
nonemptiness even for a lower-dimensional irrational fiber. The relaxed
minimum-norm rational QP returns a point with norm at most
\(\|v^*\|\). The manuscript's Hoffman bound is valid for every
feasible right-hand side with the same rational matrix. Conic
Caratheodory supplies independent active normals with nonnegative
multipliers, and rational minor estimates bound the reciprocal smallest
singular value uniformly. Thus \(\log H_C\le N^{O(1)}\), without
enumerating active sets.

Repair to the original fiber gives the stated estimate
\[
 \|v_\delta-v^*\|
 \le\zeta+\sqrt{2V\zeta+\zeta^2},\qquad
 \zeta=2H_C\delta.
\]
Taking \(\delta\le2^{-2p}/[32H_C(V+1)]\) suffices for error below
\(2^{-p}\). Its bit requirement is
\(O(p+\log H_C+\log(V+1))\). Rational polynomial evaluation and
exact rational QP have absolute polynomial bit cost at this precision.

The common-field construction then uses polynomially many calls at
precision polynomial in dimension, joint degree, and coordinate height.
All those quantities have the required bounds, so their composition
still takes \(2^{O(r)}N^C\) time. The invertible rational change back
to original coordinates preserves the generated field. Direct original-row
sign checks include every cone right-hand-side sign.

## 5. Source comparison and distinct checks

I inspected the primary
[Jeronimo--Perrucci--Tsigaridas arXiv v1](https://arxiv.org/pdf/1112.0544v1),
including Proposition 10, Remark 11, and Theorem 12. These are the
reference numbers used by the manuscript. The later locally saved 2013
text numbers the coordinate remark and noncompact extension differently.
The source supports the classical arithmetic comparison: its coefficient
bound depends on \(\max(H,2r+2S)\), it treats coordinate outputs, and
it covers a compact minimizer set on a noncompact component. The local
full-KKT proof independently supplies the joint-degree bound used here.
This comparison does not establish priority for the complete implicit
recovery algorithm.

I ran a distinct exact inline `python -` check for
\(U=[\sqrt2,\infty)\), represented by the rational SOC
\(\|(1,1)\|_2\le u\). Use perturbed active row
\(2-u^2-\varepsilon=0\) and objective
\((1+\varepsilon)u^2\). At
\(u=\sqrt{2-\varepsilon}\), \(\lambda=1+\varepsilon\),
the multiplier Hessian vanishes but the full KKT Jacobian has determinant
\(4u^2\ne0\). The command checked the equations, total degree two,
this determinant, and the coordinate relation whose lowest parameter
coefficient is \(t^2-2\). It passed. This specifically challenges any
accidental reliance on an invertible multiplier Hessian.

The separate affine-fiber reviewer ran 12 exact cases with
\[
 C=\begin{pmatrix}-1&0&0\\1&-a&0\end{pmatrix},
 \quad b=(-\sqrt2,0),\quad
 a\in\{1,2^{-3},2^{-20},2^{-100}\}.
\]
The third coordinate is free, and the two constrained normals become
nearly dependent. Three dyadic outward precisions for each matrix gave
rational QP minimizers. The checks verified inclusion, norm monotonicity,
and a direct \(4\delta/a\) repair bound. I independently rederived
the formulas: if \(q\le\sqrt2\le q+\delta\), the relaxed
minimum is \((q,(q-\delta)/a,0)\) for the tested positive ranges,
whereas the original minimum is
\((\sqrt2,\sqrt2/a,0)\). The component errors are at most
\(\delta\) and \(2\delta/a\), giving the asserted bound.
These cases add irrational right-hand sides, lineality, and severe
rational conditioning to the existing checks.

No unchanged test suite was rerun. A targeted document check for this
review passed for local links, paired math delimiters, control characters,
trailing whitespace, and final newline. A scoped `git diff --check`
passed. The finite calculations do not prove the universal perturbation,
height, recognition, or complexity theorems. No project-wide checks,
CI inspection, or Lean formalization were performed.
