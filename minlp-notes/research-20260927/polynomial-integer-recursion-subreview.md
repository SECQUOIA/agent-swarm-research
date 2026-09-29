# Independent review of the polynomial integer recursion

Date: 2026-09-28. Scope: Section 6 of
[the polynomial frontier](polynomial-nonlinear-dimension-frontier.md) and
Section 3 of its [oracle audit](polynomial-nonlinear-dimension-oracle-audit.md).
This review does not check the preceding radius, gap, or integer-witness
arguments, and makes no novelty assessment.

**Finding.** After the repair in oracle-audit Section 3.3, I find no remaining
gap in the deterministic fixed-parameter oracle and lattice-recursion step.
The result imports the controlled rational shallow-cut implementation from
Hildebrand--Köppe; this review does not independently reimplement that
ellipsoid algorithm.

## Source checks

I read the local primary texts
`common-range-prior-sources/hildebrand-koppe.txt` and
`sources-hessian-span-prior/delpia-2025.txt`.

- [Hildebrand--Köppe](https://arxiv.org/pdf/1006.4661), Theorem 5.7,
  pages 19--20, gives shallow-cut output length
  \((l+r)(dn)^{O(1)}\). Corollary 5.8, pages 22--24, gives rounded
  ellipsoid output length \((l+\langle\epsilon\rangle)(dn)^{O(1)}\).
  These are the relevant linear bounds on the changing input lengths.
  Section 4 separates the feasibility and shallow-cut costs from the
  dimension-dependent branch count.
- Remark 5.5, page 18, **assumes** that the integer coordinate map and
  slice parameter have lengths \(l(dn)^{O(1)}\). It proves the
  corresponding substituted-polynomial bound, but cannot by itself
  justify the assumption on the map. This was a gap in the earlier
  citation-based explanation.
- Corollary 3.6, page 13, gives ellipsoidal lattice width at most the
  dimension for a lattice-free ellipsoid. Scaling by the rounding ratio
  gives the stated dimension-only bound on the number of slices.
- [Del Pia](https://arxiv.org/pdf/2311.00099v2), Theorem 3, page 13,
  gives exact mixed-integer convex quadratic optimization with
  fixed-parameter dependence on the number of integer variables. The
  definition immediately above it includes exact optimal value and an
  optimizer. Applying this existing result to rational quadratic forms
  avoids an unproved conversion to an irrational lattice basis.

## Independent check of the repaired argument

Let \(A\succ0\) and the center \(a\) have rational entry lengths at
most \(H\). Rational determinant bounds give
\(\lambda_{\min}(A)\ge2^{-\operatorname{poly}(m)(H+1)}\).
A shortest nonzero integer vector for the quadratic form satisfies

\[
 d^TAd\le\min_i A_{ii},\qquad
 \|d\|_2^2\le\frac{\min_i A_{ii}}{\lambda_{\min}(A)}.
\]

Consequently its coordinate lengths are linear in \(H+1\), up to a
dimension factor. It is primitive, since dividing by a nontrivial common
divisor would decrease its value. The integer slice values within a
dimension-only distance of \(d^Ta\) have the same length bound.

Extended gcd gives a unimodular integer matrix \(U\) with
\(d^TU=e_m^T\), whose entries and inverse entries have lengths
\(f(m)(H+1)\). Thus \(y=U(w,t)\) parametrizes exactly all integer
points on \(d^Ty=t\). Merely completing \(d\) as the last column of
an integer basis would not have this property; the repair correctly
avoids the source's displayed shortcut.

If the current set lies in a ball of radius \(R_0\), then
\((w,t)=U^{-1}y\) gives
\(\|w\|\le\|U^{-1}\|R_0\). A larger strict integer-radius ball
therefore retains the whole section and has linearly bounded encoding.
The old bounding polynomial may acquire a linear term; retaining it and
appending this fresh ball is valid.

The exact rational quadratic problems
\(\min_{z\in\mathbb Z^m}(z-a)^TA^{-1}(z-a)\) and the \(2m\)
problems \(\min d^TAd\) subject to \(\pm d_i\ge1\) give the
required closest point and shortest nonzero direction. They satisfy Del
Pia's hypotheses and have polynomial-size rational inputs. Their runtime
is fixed-parameter tractable. The geometric estimate above, rather than
the runtime bound alone, controls the returned direction's bit length.

Substitution of a degree-\(d\) polynomial through the integer affine map
increases coefficient lengths by at most a parameter factor times the
old row and map lengths. The supplied rational LDL shallow-cut oracle
likewise has output length linear in the row and ellipsoid lengths.
Combined with the cited controlled ellipsoid implementation, these facts
give \(L_{j+1}\le f(m,d)(L_j+1)\) for at most \(m\) levels.
They do not create an input exponent that depends on the parameters.

Finally, the LP oracle returns a vertex of a fixed rational multiplier
polytope. Its selected polynomial has query-independent coefficient
bounds. The number of implicit rows enters neither the integer slack
margin nor the oracle's gradient bounds. Strict inequalities are handled
consistently: cuts hold on the closure, while every certified inner
ellipsoid lies in the strict set itself.

An inline `python` check confirmed that this Markdown file has no trailing
whitespace and ends with a newline. No mathematical computation was used
for the source and proof checks. No project-wide checks or CI inspection
were performed.
