# Independent review of comparison at strongly monotone cubic zeros

Date: 2026-09-28. Status: pass; no substantive gap found in the frozen
[candidate proof](strong-monotone-cubic-posslp-upper.md).
The reviewed SHA256 was
`2ca17182ab151a147fec67f0bad559d55b8bd4acfc11db5ed88edba016e68686`.
The subsequent amendment with SHA256
`b6cb69fdffedb41eb4a307503beabbad5094b857cf51865b7d5296b6e0989ee4`
was also inspected and passes; its changes are identified below.
This reviewer did not construct the result. The review independently
reconstructed the proof and checked its application of the two primary
algorithmic sources. The earlier lower-bound constructions remain stated
dependencies; their transfer to the present class was checked here.

Global strong monotonicity supplies both existence and the inverse bound
needed by Newton iteration. On the boundary of a sufficiently large ball,
\(T(x)^Tx>0\). A fixed point of the projected map satisfies
\(T(x)^T(y-x)\ge0\) throughout that ball. Taking \(y=0\)
excludes its boundary, and interior variations force \(T(x)=0\).
This proves existence without assuming surjectivity or a potential.
Uniqueness and \(\|p\|\le\|T(0)\|/\mu\) follow directly
from strong monotonicity. Differentiation gives
\(v^TJ_T(x)v\ge\mu\|v\|^2\); Cauchy--Schwarz then gives
\(\|J_T(x)v\|\ge\mu\|v\|\). This argument is valid for a
nonsymmetric Jacobian.

The four local bounds in (8) are conservative and sufficient. A cubic
component has second partial derivatives bounded by
\(6C(1+nR)\). Converting the componentwise bilinear bound to Euclidean
norms costs at most \(n^{3/2}\), giving the stated Jacobian Lipschitz
constant. The degree-four observable gives the stated gradient bound.
Using \(n\le L\), \(nR\le2^{5L}\), and
\(1+nR\le2^{5L+1}\), every displayed bound is below \(2^{30L}\)
for \(L\ge2\). These are universal estimates, independent of the
finite checks recorded below.

The retained ball survives every rejection. Inside the cube, let
\(r=\|x-p\|\). Rejection gives
\(r>\mu\rho/B\), while monotonicity gives
\[
 T(x)^T(p-x)\le-\mu r^2
 <-\mu^3\rho^2/B^2.
\]
Moving from \(p\) by at most \(\delta\) changes the left side by at
most
\[
 B\delta=\mu^3\rho^2/(2B^2).
\]
Thus the same ball \(\overline B(p,\delta)\) lies strictly on the
retained side of every residual cut. Also
\(\delta/\rho=\mu^4/(8B^4)<1\), so that ball lies in the cube.
Every outside-cube coordinate cut therefore retains it as well. The
outside-cube branch runs before using local derivative bounds. A zero
normal cannot occur on a rejected residual query.

The volume argument uses a full-dimensional fixed ball, rather than just
the zero or a ball depending on the query. The translated cube with side
\(\delta/n\) fits inside the ball, and its volume exceeds the stated
target \(\nu\). Its logarithmic reciprocal, the outer radius, and all
oracle arithmetic have polynomial encoding length. Acceptance implies
\(\|x-p\|\le\rho\), even though it need not mean membership in the
smaller retained ball.

I read the relevant primary GLS theorem, rounded update, supporting
lemmas, and weaker-oracle remark. Their proofs use the retained cut
inequality for containment and use neither membership in the retained
ball nor the meaning of an acceptance flag. Normalization to infinity
norm one supplies their oracle format. The rounded algorithm supplies
polynomial bit bounds; its containment proof accounts for the update
enlargement and rounding. The candidate's cut-or-stop consequence is
therefore valid. Dimension one is correctly handled separately by
bisection. See [GLS, Section 3.2, Theorem 3.2.1, Lemmas
3.2.8--3.2.10, and Remark 3.2.33](https://www.mpi-inf.mpg.de/fileadmin/inf/d1/ellipsoid-lovasz.pdf).

For Newton iteration, integration along the segment from \(p\) to
\(x_k\), followed by the inverse bound, gives
\(e_{k+1}\le Be_k^2/(2\mu)\). The scaled initial error is at most
\(1/8\). Induction proves both the displayed doubly exponential
decay and that every iterate stays within the region where the local
bounds apply. No step requires a symmetric Jacobian. Solving
\(J^TJd=J^TT(x_k)\) is exactly equivalent to solving
\(Jd=T(x_k)\), because \(J\) is invertible. The normal matrix is
positive definite, so rational LDL elimination has nonzero positive
pivots and needs neither square roots nor adaptive pivot tests. Shared
circuit nodes keep the construction polynomial even when expanded
rational coordinates become long.

The singleton argument for the algebraic gap is sound. A quantifier-free
formula defining one real point must have a nonzero polynomial that
vanishes there; otherwise all of its finitely many sign conditions are
constant on a neighborhood. Basu's theorem explicitly includes output
coefficient-bit bounds, as well as degree bounds. With one quantified
block, one free variable, and fixed degree, these give the claimed
effective singly exponential bounds. No complex zero-dimensionality
assumption is needed. See [Basu, Theorem
2.16](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf).

More explicitly, write \(q=2^{a(L)}\). After removing a power of
\(z\), a polynomial vanishing at a nonzero \(\alpha\) has a nonzero
integer constant term, degree at most \(q\), and coefficient magnitude
at most \(2^q\). If \(|\alpha|<1\), it follows that
\(1\le q2^q|\alpha|\), hence
\(|\alpha|\ge2^{-2q}=g\). The case \(|\alpha|\ge1\) is immediate.
Only the bound is used; the reduction does not execute quantifier
elimination or print \(g\) in expanded binary form.

The chosen Newton count gives the error bound \(g/8\). When
\(\alpha=0\), \(|\widehat\alpha|\le g/8\); otherwise
\(|\widehat\alpha|\ge7g/8\) with the correct sign. These two facts
verify all five entries of the table, including equality. Every selected
expression has a strict nonzero sign. Formula (21) converts a division
by either sign of nonzero rational into an integer numerator over a
positive denominator. The construction consequently produces one
ordinary division-free integer circuit whose positivity answers the
chosen predicate. Rational warm-start comparisons occur in ordinary
polynomial time and do not introduce PosSLP queries.

The certificate format is sufficient and has the stated verification
cost. For a symmetric rational \(M\succ0\),
\(\det M/(\operatorname{tr}M)^{m-1}\le\lambda_{\min}(M)\)
because every other eigenvalue is at most the trace. Determinants,
positive definiteness, and the polynomial identity are checkable with
polynomial rational bit complexity. The resulting modulus has polynomial
bit length. Rejecting malformed certificates can be implemented by
returning a fixed no-instance of PosSLP. This certifies the displayed
subclass; it does not claim efficient recognition of strong monotonicity
for every cubic map.

The lower-bound transfer preserves the certificate basis. For the
linked quartics, setting \(T=\nabla F\) or \(T=\nabla G\) makes
\(J_T\) their Hessian, with the supplied full positive definite Gram
on \((v,x\otimes v)\). Coordinate observables are affine, and the
value observable has degree four. The coordinate construction excludes
equality at its comparison threshold, so changing the observable's sign
gives all four order predicates, with strict and nonstrict versions
equivalent on those reduced instances. There is no asserted equality
lower bound.

The degree frontier also passes. An affine symmetric Jacobian that is
positive definite on every real line has zero linear part. Subtracting
its constant symmetric part times \(x\) leaves a field satisfying
\(\partial_iU_j+\partial_jU_i=0\). Differentiating three such
identities and combining them gives
\(2\partial_i\partial_jU_k=0\), so the field is affine. Its unique
zero and every fixed-degree observable are therefore computable in
polynomial rational time. The frozen nonpotential example has the full
Gram \(\operatorname{diag}(I_n,I_{n^2}+2ww^T)\), where
\(w=\operatorname{vec}(I_n)\). The theorem's unconstrained domain,
supplied modulus, and absence of a practical numerical speed claim are
properly delimited. This review establishes no publication priority.

The amendment explicitly displays \(\delta/\rho<1\) where the retained
ball is placed in the cube and repairs the missing backslash before
`quad` in (18). Both changes were inspected and are correct. The author
may update the status after this review.

A separately proposed post-freeze example was also checked independently.
For
\[
 T(x,y)=(1+x^2+y^2)(x,y)+(x^2y/2,0),
\]
the Jacobian entries are
\[
 J_{11}=1+3x^2+y^2+xy,\quad J_{12}=2xy+x^2/2,
 \quad J_{21}=2xy,\quad J_{22}=1+x^2+3y^2.
\]
In the ordered basis \(z=(xv_1,xv_2,yv_1,yv_2)\),
\[
 v^TJ_Tv=\|v\|^2+z^TQz,\qquad
 Q=\begin{pmatrix}
 3&1/4&1/2&2\\
 1/4&1&0&0\\
 1/2&0&1&0\\
 2&0&0&3
 \end{pmatrix}.
\]
The leading principal minors are
\(3,47/16,43/16,65/16\), so \(Q\succ0\). This gives a full
positive definite certificate and strong monotonicity with modulus one.
Since \(J_{12}-J_{21}=x^2/2\) is nonconstant, the map cannot be a
gradient plus a fixed skew linear map. Adding a rational constant vector
preserves every derivative and hence the certificate. The actual
amendment states these facts correctly. It changes the illustration,
not the theorem or proof reviewed above.

The targeted verification commands were:

- `sha256sum research-20260927/strong-monotone-cubic-posslp-upper.md`:
  matched the initial frozen hash and, in the subsequent check, the
  amended hash stated above.
- An inline `python3 - <<'PY' ... PY` program using only `fractions`
  and `itertools`: passed all checks described below. This command used
  exact rational arithmetic, not floating point.
- `git diff --check -- research-20260927/strong-monotone-cubic-posslp-upper-independent-review.md`:
  passed.

The inline program checked the four squared derivative inequalities for
all \(2\le L\le64\), \(1\le n\le L\): 2,079 pairs. At both
modulus endpoints it checked the retained-radius identity, interior
margin, and radius ordering; it also checked the precision inequality.
For the two-dimensional radial cubic plus five rational skew matrices,
it checked 45 exact normal-equation solves against direct solves, their
positive LDL pivots, and the Gram identity. Five nearby Newton steps
satisfied the local quadratic estimate with Jacobian Lipschitz bound
18 on the radius-three ball. It checked all five predicate formulas
at the gap boundaries and error endpoints, and formula (21) for both
signs of divisor and zero numerators. All passed. These finite checks
supplement the universal arguments above; they do not implement the
ellipsoid algorithm or the full reduction. No project-wide tests, CI
inspection, or formal verification were performed. The main candidate
was not edited by this reviewer.

Final administrative reconciliation: the main file's SHA256 is
`a3322129b57f590a9121aaf2d8fd80e29a457bc64747235fa7c582c7cc17c058`.
The final status and review link, the explicit requirement that the
positive definite Gram matrix be symmetric, and the revised verification
disclosures were inspected. They agree with this review and preserve its
pass verdict. The verification text distinguishes reviewer checks from
author checks and makes no claim of implementing the full reduction.
The hash was confirmed with the same targeted `sha256sum` command above.
The targeted review-file `git diff --check` passed after this addition.
