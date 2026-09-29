# Adversarial review of the polynomial nonlinear-dimension theorem

Date: 2026-09-28. Reviewed the complete
[main manuscript](polynomial-nonlinear-dimension-frontier.md), the
[oracle audit](polynomial-nonlinear-dimension-oracle-audit.md), and the
[prior comparison](polynomial-nonlinear-dimension-prior.md). This was a fresh
review of the complete argument. A separate reviewer checked the integer
recursion and its primary sources; that
[focused subreview](polynomial-integer-recursion-subreview.md) records its
scope and findings.

**Verdict.** I find no remaining mathematical or bit-complexity gap in the
revised theorem: for explicitly encoded rational rows

\[
 C_i v+p_i(z,u)\le0,
 \qquad z\in\mathbb Z^k,
 \quad u\in\mathbb R^r,
 \quad v\in\mathbb R^n,
\]

with constant rational \(C_i\) and globally jointly convex polynomials
\(p_i\) of degree at most \(d\), exact feasibility and recovery of an
original feasible integer assignment have a deterministic bound
\(f(k,r,d)N^C\), with absolute \(C\). No supplied box, Slater point,
or rational continuous feasible point is needed. This verdict incorporates
the substantive repair to the lattice-map height argument described below.
It does not establish novelty, implement the full algorithm, or assert an
FPT exact continuous witness or optimization algorithm.

1. **The implicit Farkas description is exact and has the required size
   bounds.** Normalizing \(\{\lambda\ge0:C^T\lambda=0\}\) by
   \(\mathbf1^T\lambda=1\) loses no nonzero multiplier. A nonzero
   vector in that cone has strictly positive coordinate sum. The normalized
   set is a compact rational polytope, so it suffices to test its vertices.
   Each vertex has at most \(\operatorname{rank}C+1\) nonzero entries
   and is specified by rational minors of a matrix whose entries do not
   depend on the query point. This supplies a uniform coefficient bound.
   There can be exponentially many vertices, but their logarithmic count
   is polynomial in the explicit input size. Clearing denominators within
   each selected polynomial is sufficient; no product over all implicit
   rows is used.

   The coefficient matrix being constant is essential. It proves that
   eliminating \(v\) gives one fixed finite family of polynomial
   inequalities. In particular, its weak feasible set in \((z,u)\) is
   closed. The subsequent projection onto \(z\) need not be closed;
   the proof does not require that stronger statement.

2. **The continuous witness radius and the reciprocal gap use the correct
   radius theorems.** I independently inspected the displayed formulas in
   [Basu--Roy, Theorems 3 and 4](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf).
   Their logarithmic bounds depend linearly on coefficient bits and on the
   logarithm of the row count, with a dimension-and-degree factor. This
   supports using an exponential implicit family without constructing it.

   After fixing a rational \(z\), the meeting bound gives a feasible
   \(u\) of controlled magnitude. The minimum-norm point of the
   nonempty linear \(v\)-fiber lies in the span of independent active
   normals. Solving its active equalities gives exactly the formula in
   the manuscript. This bounds \(v\) even when the original polyhedron
   is unbounded or has lineality. No rationality of \(u\) is needed
   for this magnitude estimate.

   For the gap, the boxed residual epigraph is compact, and its projection
   \(E_z\) is compact. If its minimum \(t\) is \(\alpha_z>0\),
   then the reciprocal graph \(ty=1\), \(y\ge0\), over \(E_z\)
   is compact and has maximum \(y=1/\alpha_z\). The theorem containing
   every bounded component therefore bounds that maximum. A theorem merely
   meeting each component would not suffice. The revised proof uses the
   containing theorem and has no such direction-of-bound error.

   The compositions preserve an absolute input exponent. With parameter
   tuple \(\pi=(k,r,d)\), let \(L_z\), \(L_R\), and \(L_\Delta\)
   denote integer-box, continuous-radius, and inverse-gap bit bounds.
   The estimates have the form

   \[
   L_z\le f(\pi)N^{c_1},\qquad
   L_R\le f(\pi)(L_z+1)N^{c_2},\qquad
   L_\Delta\le f(\pi)(L_z+L_R+1)N^{c_3}.
   \]

   Here the \(c_i\) are absolute. Polynomial evaluation introduces
   factors such as \(d\), not a parameter-dependent power of a varying
   coefficient bit bound. There are only constantly many radius, gap, and
   mesh stages. Their composition is thus \(f(\pi)N^C\). The separate
   recursion issue was more delicate and is addressed in item 7.

3. **The integer radius imports the size theorem, not an implicit-formula
   algorithm.** I independently inspected
   [Khachiyan--Porkolab, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf).
   Its integer-point bound uses degree, coefficient length, and quantifier
   dimensions, without the number of predicates. The formula here has
   only \(r\) quantified continuous variables after eliminating \(v\).
   Its real solution set in \(z\) is convex because the original rows
   are jointly convex. Appending an integer coordinate fixed to zero
   converts feasibility into the theorem's attained integer optimization
   setting. This remains valid for a nonclosed projection and for an
   unbounded original model. The manuscript does not incorrectly apply
   the source's explicit-formula algorithm to an unconstructed row list.

4. **The relaxed grid reduction preserves the original integer assignment.**
   A small feasible anchor has \(|u|,|v|\le R\). Rounding only \(u\)
   to the dyadic grid changes every residual by at most the derivative
   bound times the mesh. The selected constants put all native rows and
   wider boxes strictly inside the relaxed system. Original affine
   equalities are relaxed as their two opposite rows, so they do not leave
   a hidden lower-dimensional strict-feasibility requirement.

   Conversely, strict \(|z_j|<B_z+1\) implies \(|z_j|\le B_z\)
   for integer \(z_j\). A point satisfying the strict relaxed system
   gives a boxed original residual below \(\Delta\), so the original
   fiber at that same \(z\) is feasible. The proof neither enumerates
   the grid nor claims that the rounded continuous point is itself an
   original feasible point. Its additional integer dimension is exactly
   \(r\).

5. **The strict membership LP defines one fixed family at every rational
   query.** The phase-I LP is feasible, has a finite attained optimum
   because of the box rows, and has the normalized multiplier polytope
   as its dual feasible region. Strict feasibility is equivalent to a
   negative optimum. An optimum of zero is correctly rejected. An optimal
   dual vertex returns a violated polynomial from the same fixed family
   at all queries, with coefficient bounds independent of the queried
   rational point. Its multiplier is retained while taking its gradient.

   This avoids the invalid substitution of an oracle for \(F\le0\)
   into an algorithm using \(F-1<0\). Those sets can have the same
   integer points and different rational-query memberships. Nonnegative
   combinations preserve convexity here because every native polynomial
   function is convex. Convexity merely of the original feasible set,
   or quasiconvexity of individual rows, would not justify this step.

6. **The rational shallow cuts and the volume threshold are sufficient.**
   In coordinates normalized by \(L\operatorname{diag}(\sqrt{d_i})\),
   the queried LDL-based points are signed coordinate vectors. Their
   cross-polytope axis lengths are
   between \(1/[2(s+1)]\) and \(1/(s+1)\). Their convex hull therefore
   contains the claimed conservative inner ellipsoid with
   \(\beta=2s(s+1)\). If all points are strict members, their convex
   hull, including this closed inner ellipsoid, is contained in the open
   strict set.

   If a query violates \(F<0\), convexity and a nonzero gradient give
   \(g^Tx<g^Ty\) for every feasible \(x\). Cauchy--Schwarz in the
   ellipsoid norm gives the displayed shallow offset. A zero gradient
   certifies emptiness because a convex function is then globally
   minimized at the violated query. All query points and cut normals are
   rational; the square roots in the geometric inequalities are not
   irrational algorithm inputs.

   After individual positive denominator clearing, every integer strict
   member has margin at least one in every row. A uniform gradient bound
   on the enlarged outer ball supplies a common positive-radius ball
   around that integer member. Its logarithmic volume bound depends on
   coefficient bits and radius bits, not on how many implicit rows exist.
   The same reasoning applies after each integer affine substitution.

7. **A real gap in the original justification was repaired.** The first
   version cited Hildebrand--Köppe Remark 5.5 for the entire coefficient
   recursion. That remark assumes short lattice coordinate maps; it does
   not itself establish that assumption. Repeatedly applying an unspecified
   polynomial bit bound would give only a dimension-dependent input
   exponent. The independent oracle review identified this issue, and
   both this reviewer and the focused subreview checked the saved repair.

   The revised argument uses the exact rational quadratic algorithm of
   [Del Pia, Theorem 3](https://arxiv.org/pdf/2311.00099v2) for the closest
   integer point and for the \(2s\) constrained shortest-direction
   problems. It needs no rational representation of a square-root lattice
   basis. If \(A\) has entry bit bound \(H\), then a shortest nonzero
   integer \(a\) satisfies \(a^TAa\le A_{11}\). A rational determinant
   lower bound on \(\lambda_{\min}(A)\) makes every such minimizer
   have bit bound \(\operatorname{poly}(s)(H+1)\). It is primitive.
   The flatness bound limits the number of branch values to a function of
   dimension, and these values have the same linear type of bit bound.

   Extended gcd yields a unimodular \(U\) with \(a^TU=e_s^T\), and
   the correct section is \(y=U(w,t)\). This identity is essential:
   merely placing \(a\) as a column of a unimodular matrix would not
   parameterize \(a^Ty=t\). The entries of \(U\) and \(U^{-1}\)
   have linear-in-\(H\) bit bounds, with dimension factors. Substitution
   into degree-\(d\) rows preserves that type of bound. A new strict
   origin-centered ball follows from
   \(\|w\|\le\|U^{-1}\|R_0\), so translated sections do not create
   a mismatch with the bounded-input convention.

   I also inspected Hildebrand--Köppe Corollary 5.8's linear output-bit
   statement and the relevant shallow-cut and flatness statements in
   [the primary paper](https://arxiv.org/pdf/1006.4661). The controlled
   rounded ellipsoid implementation, together with the direct map bounds,
   gives \(L_{j+1}\le f(s,d)(L_j+1)\). Depth at most \(k+r\) changes
   the parameter factor and leaves the input exponent absolute. The
   revised main manuscript now includes this argument, rather than relying
   solely on the conditional remark.

8. **The intrinsic parameter is valid under the stated convexity premise.**
   Coefficientwise kernels of the full polynomial Hessians give exactly
   the continuous directions along which all gradients have zero
   derivative. The directional derivative along each such direction is
   therefore constant, yielding an affine term with a constant coefficient
   on \(v\). Rational linear algebra supplies a rational basis and
   complement. Expanding only after restricting to \((z,u)\) keeps the
   monomial count a function of \((k,r,d)\) times the explicit input
   size.

   For globally convex polynomials, every full Hessian is positive
   semidefinite. If its continuous block annihilates \(a\), the full
   quadratic form at \((0,a)\) is zero, so the full matrix annihilates
   \((0,a)\). This proves the proposed continuous-block shortcut and
   excludes hidden integer--linear-continuous cross terms. Without global
   convexity, \(g(z,v)=zv\) has a zero continuous Hessian block and a
   nonconstant derivative in the continuous direction, showing why that
   premise cannot be dropped.

The theorem offers a useful exact decision guarantee for a model with few
nonlinear continuous directions and an unrestricted linear continuous
extension. Its proof is a structural combination of existing quantitative
real algebraic geometry, Farkas duality, and integer optimization methods.
The precise implicit-family reduction and its bit accounting are the
candidate addition. The prior audit appropriately credits those ingredients
and does not infer priority from an unsuccessful search. This review found
no reason to strengthen its novelty or practical-speedup claims.

The targeted command

```text
python research-20260927/check_polynomial_oracle_interface.py
```

passed 25 exact strict-projection queries, 144 exact gradient cuts, 30
rational ellipsoid test points, and four integer-section maps, as well as
boundary, zero-gradient, and affine-substitution checks. I read the exact
checker and ran it after the substantive lattice-map correction. These
checks support the stated finite identities and boundary cases. They do
not prove the general radius bounds, the full lattice algorithm, or its
bit complexity; those conclusions rest on the mathematical argument and
the inspected primary results. No Lean formalization, project-wide check,
or CI inspection was performed. A positive review is evidence of scrutiny,
not a guarantee of correctness.
