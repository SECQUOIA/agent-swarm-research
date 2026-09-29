# Independent review of the generic mixed-integer value prior audit

Date: 2026-09-28. Scope: the literature comparisons and qualitative
slice argument in
[the prior audit](generic-convex-mixed-value-prior.md). This review does
not verify the proposed quantitative height theorem.

## Verdict and verified correction

The qualitative slice theorem is valid under its stated assumptions.
No closedness or semialgebraicity is needed. The primary-source spot
checks below support the audit's distinctions between earlier results
and the proposed height bound. They do not establish originality.

One substantive correction was required in the initial audit text:
the qualitative slice already yields a dimension-dependent algebraic
degree bound for a rational semialgebraic epigraph. It does not control
coefficient height or the size of an optimal integer assignment.
The initial sentence saying that it gives no degree or height bound
understates the consequence of classical geometry and real quantifier
elimination. The audit author applied this correction, and this reviewer
re-read the revised paragraph and verified that it states the distinction
correctly.

Indeed, substitute the integral affine parameterization
\(z=z_0+Ty\) into a quantifier-free description of \(E\).
Every resulting polynomial still has total degree at most \(d\),
however large the coefficients of \(z_0,T\) are. Eliminate the
remaining real coordinates \(y\). Ordinary sign-invariant cylindrical
algebraic decomposition gives a univariate formula whose individual
polynomial degrees are at most \(d^{2^{O(k)}}\), independently of
atom count and coefficient height. The finite infimum is a boundary
point of the resulting subset of the line, and therefore a root of one
nonzero output polynomial. Its minimal-polynomial degree satisfies the
same bound. A sharper specified exponent may still be an additional
result, but a bound of the unspecified form \(d^{G(k)}\) already
follows this way.

A separate reviewer independently checked the slice proof and reached
the same degree-versus-height correction.

## Detailed check of the qualitative argument

Write

\[
C_s=\{z:\exists t<s\text{ with }(z,t)\in E\}.
\]

Fix a finite \(V>\theta\). A mixed-integer sequence with objective
values tending to \(\theta\) eventually projects into \(C_V\).
In particular, \(C_V\cap\mathbb Z^k\) is nonempty.

If \(C_V\) has deficient affine dimension, let
\(L=\operatorname{aff}(C_V\cap\mathbb Z^k)\).
This is a proper rational affine space: choose finitely many affinely
independent integer points spanning it. If \(z_0\) is one such point,
the columns of an integral matrix \(T\) can be chosen as a basis of
the lattice
\((L-z_0)\cap\mathbb Z^k\). Then

\[
L\cap\mathbb Z^k=z_0+T\mathbb Z^r,
\qquad L=z_0+T\mathbb R^r.
\]

Restricting \(E\) to \(L\) retains the minimizing sequence and
cannot lower the mixed-integer infimum. Thus it preserves that infimum.
Repeat this preprocessing after each restriction, as the audit requires.

In the full-dimensional case let \(\alpha\) be the continuous
infimum. It satisfies \(\alpha\le\theta\), including the
possibility \(\alpha=-\infty\). If strict inequality holds, choose
a finite \(U\) between them and \((p,t_0)\in E\) with
\(t_0<U\). Choose a fixed \(\lambda\in(0,1)\) such that

\[
(1-\lambda)t_0+\lambda V<U.
\]

Convexity gives
\((1-\lambda)p+\lambda C_V\subseteq C_U\).
Consequently \(C_U\) is full-dimensional. It contains no integer
point because \(U<\theta\). The identity
\(\operatorname{int}\overline{C_U}=\operatorname{int}C_U\)
for full-dimensional convex sets ensures that its closure is
lattice-free. A maximal lattice-free set containing it is a polytope
plus a proper rational linear space. Hence some nonzero integral linear
form \(a\) is bounded above and below on \(C_U\).

The displayed homothety then bounds \(a\) above and below on
\(C_V\). Along the minimizing integer sequence, \(a^Tz\) takes
only finitely many integer values. An infinite subsequence lies in one
hyperplane \(a^Tz=b\), and still has objective values tending to
\(\theta\). Restriction to this rational hyperplane preserves the
mixed-integer infimum and reduces dimension.

The process stops either when continuous and mixed-integer infima agree,
or in dimension zero, where they necessarily agree. Composing the
integral lattice parameterizations remains valid. No convergence of the
integer sequence itself, attainment of a fiber infimum, or closure of
\(E\) was used. Upward closure is also not used in this geometric
argument, although retaining it is natural for the epigraph application.

## Literature spot checks and qualifications

- **Khachiyan--Porkolab.** The locally stored primary text confirms that
  Theorems 1.1 and 1.2 optimize an integer coordinate, Theorem 3.1(ii)
  gives the controlled slab, and the proof of Theorem 3.4 handles an
  algebraic affine equation by expansion over a number field. The audit
  properly credits these ingredients. In the description of Theorem
  1.1, “a size bound depending on input degree, coefficient length and
  quantified dimensions” is clearer than “degree and coefficient
  bounds,” since the theorem's output is an integer vector.
- **Koppe and Bank et al.** The survey's local primary text, Theorem
  6.3, explicitly has domain \(F\cap\mathbb Z^n\). The original
  Bank et al. Theorem 2, printed p. 301, likewise has an entirely integer
  domain and integer-coefficient quasiconvex polynomial objective and
  constraints. The audit correctly excludes this as a theorem for an
  unattained mixed-integer real value.
  [Bank et al. primary PDF](https://www.numdam.org/item/BSMF_1993__121_2_299_0.pdf)
- **Friberg.** Theorem 5, printed p. 41, and its finite-termination proof
  explicitly use bounded integer domains. Assumption 1, p. 40, also
  requires extracting a possibly fractional assignment of the integer
  variables attaining a relaxation's value/attainment pair. Calling this
  only a scalar value/attainment oracle omits part of the assumption.
  The author added assignment extraction, and this reviewer verified the
  corrected wording against the primary text.
  [Primary thesis](https://backend.orbit.dtu.dk/ws/portalfiles/portal/125210367/main.pdf)
- **Baes--Oertel--Weismantel.** Theorem 7, p. 9, assumes a nonempty
  compact mixed-integer feasible set and the mixed-integer Slater
  condition. The following unnumbered paragraph, p. 10, explicitly
  discusses an infimum/supremum extension. The audit preserves this
  qualification and does not dismiss the paper merely for nonattainment.
  [Primary PDF](https://arxiv.org/pdf/1412.2515)
- **Kocuk--Moran.** Theorem 2.12, p. 5 of the final author version, is a
  boundedness equivalence under the stated Dirichlet and interior-point
  hypotheses. It does not state equality of finite values or a bound on
  their algebraic encoding. The audit's comparison is accurate.
  [Final author PDF](https://research.sabanciuniv.edu/id/eprint/37541/2/ExtendedDualFINAL.pdf)
- **Basu--Mishra and lattice-free geometry.** The bounded-polynomial
  counting observation is on printed p. 990 of the handbook chapter.
  The BCCZ containment corollary is Corollary 20, printed p. 15, and
  supports use of a maximal lattice-free container. The audit correctly
  treats both ingredients as established.
  [Handbook chapter](https://www.csun.edu/~ctoth/Handbook/chap37.pdf),
  [BCCZ primary PDF](https://www.andrew.cmu.edu/user/gc0v/webpub/lattice-free-May2010.pdf)

The older Bank--Mandel and Obuchowska comparisons were not independently
re-audited in this review. The main audit accurately identifies their
access limits and reliance on earlier repository notes. No universal
claim that the proposed quantitative theorem is absent from all earlier
literature is justified by these checks.

## Verification record

Targeted local reads used `rg` and `sed` on the two named primary-text
files. Primary PDF inspections were limited to the statements and pages
identified above. A local Python check of this review's final newline,
trailing whitespace, control characters, math delimiters, and relative
Markdown links passed. No numerical testing, Lean proof, project-wide
verification, or CI inspection was used; none is claimed.
