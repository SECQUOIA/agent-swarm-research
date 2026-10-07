# Classical growth, tube, and parametric-QP source audit

**Scope.** This read-only audit checks the current growth-tail statements in
`appendices/A-finite-noise.tex`, the tube theorem and its application in
`appendices/E-recourse.tex` and `sections/07-recourse.tex`, and the parametric
QP comparisons in `sections/04-quadratic.tex`. It also checks
`evidence/literature-preliminary.md`, the current citation-request keys, local
source metadata, and available primary read text. The current manuscript keys
match `current-citation-requests.txt` and the assembled Luna bibliography. I
did not run builds, tests, CI checks, or any literature KB/session operation.

**Disposition.** I found no material theorem-scope or identity blocker in the
named sources. The 2021 Basu–Lerario citation and the continuous-volume to
finite-grid transfer are correctly separated. Ding and Patrinos–Sarimveis are
used within the scope supported by their read source versions. The three
classical books are metadata-only in the local literature collection; their
well-known theorem scopes are consistent with the draft, but no exact book
theorem or page locator is verified here. One minor citation-placement repair
is suggested for Rademacher's theorem.

## Appendix A: classical growth-tail facts

The live passage at `appendices/A-finite-noise.tex:230–236` states that
Lipschitz maps are differentiable almost everywhere, applies the equal-
dimensional area formula to the Lipschitz map \(P:\mathbb R^n\to\mathbb R^n\),
and uses almost-everywhere differentiability of finite convex functions.

- **`evans2015-measure-theory-and-fine`.** Evans and Gariepy,
  *Measure Theory and Fine Properties of Functions*, revised edition, CRC
  Press, 2015 (ISBN 9781482242393). No primary book package is present under
  `literature/papers/`; local project metadata comes from
  `paper-exact-arithmetic/references.bib`. The [Google Books record and
  contents](https://books.google.com/books/about/Measure_Theory_and_Fine_Properties_of_Fu.html?id=e3R3CAAAQBAJ)
  confirm book identity and coverage of area/coarea formulas for Lipschitz
  maps, but are metadata, not a read copy.
- **`federer1969-geometric-measure-theory`.** Federer, *Geometric Measure
  Theory*, original 1969 edition, Grundlehren 153. No primary book package is
  present. The [Springer record](https://link.springer.com/book/10.1007/978-3-642-62010-2)
  is for the 1996 reprint and identifies the original volume; it is not
  evidence that the 1969 text was read.
- **`rockafellar1970-convex-analysis`.** Rockafellar, *Convex Analysis*,
  Princeton University Press, Princeton Mathematical Series 28 (1970). No
  primary source package is present under `literature/papers/`; local project
  metadata comes from `paper-exact-arithmetic/references.bib`. The
  [Princeton publisher-platform record](https://www.degruyterbrill.com/document/doi/10.1515/9781400873173/html)
  identifies the 1970 book, but is a later reprint/metadata page rather than
  the locally read 1970 text.

The area-formula equality in the manuscript is the equal-dimensional Lipschitz
case: integrate the absolute Jacobian on a measurable set and equate it with
the integral of the map's multiplicity function. This is within the broad
scope of Evans–Gariepy and Federer. The finite-convex differentiability claim
is a standard finite-dimensional convex-analysis theorem within Rockafellar's
scope. No theorem number or page locator for these books is certified because
the cited primary texts were not locally available.

The growth-tail proof also uses the subgradient inequality for maximizers of a
supremum of affine functions, proximal optimality, and monotonicity of the
subdifferential. It derives the coordinate subgradient bounds and the
monotonicity and nonexpansiveness consequences it needs. I found no
mathematical mismatch. The proof is mostly self-contained for these steps; if
the authors want a broad background citation, Rockafellar can be cited near
them without a locator until the primary text is checked.

One placement repair would make the existing source attribution explicit:
the Rademacher sentence at line 231 currently has no citation, while Evans–Gariepy
is attached only to the next, area-formula sentence. Add
`\cite{evans2015-measure-theory-and-fine}` to the Rademacher sentence. This is
not a mathematical correction.

## Appendix E: Basu–Lerario tube estimate

The exact current key is
**`basu2021-hausdorff-approximations-and-volume-of`**. The source is Basu and
Lerario, *Hausdorff Approximations and Volume of Tubes of Singular Algebraic
Sets*, arXiv:2104.05053v1, submitted 11 April 2021. The read local package is
`literature/papers/basu2021-hausdorff-approximations-and-volume-of/` and
contains `paper.md`, `fulltext.md`, and `original.pdf` with status `read`. Its
primary `source_url` is the [arXiv v1 PDF](https://arxiv.org/pdf/2104.05053v1);
the [versioned arXiv record](https://arxiv.org/abs/2104.05053v1) identifies
that version. The separate 2023 journal package is metadata-only/unread and
is not the cited source.

Theorem 1.1, arXiv PDF p. 1, assumes a finite family of real polynomials of
degree at most \(\delta\), its common real zero set \(Z\) with
\(\dim Z\le m\), and a point uniform in an arbitrary Euclidean ball of radius
\(\sigma\). It gives, for every \(\epsilon>0\),
\[
4\left(\frac{4n\delta\epsilon}{\sigma}\right)^{n-m}
 \left(1+\frac{(4\delta+1)\epsilon}{\sigma}\right)^m.
\]
The assumptions and constants match Appendix E lines 90–97 after renaming
\((n,\delta,\sigma)\) to \((q,D,T)\).

The use in the proof is also within the theorem's hypotheses. The constructed
\(P_K\) is nonzero, \(Z(P_K)\subseteq\mathbb R^q\),
\(\deg P_K\le D_*\), and \(\dim Z(P_K)\le q-1\); Section 07 explicitly
requires \(q\ge1\). For \(\epsilon\le T\), Theorem 1.1 gives
\(16qD_*(4D_*+2)^{q-1}\epsilon/T\). The proof at lines 642 onward then
covers every grid atom by its adjacent cube, compares the containing ball and
cube volumes, and uses \(T=\sqrt q R_0\). This yields the proof's coefficient
\(16q^{(q+1)/2}D_*(4D_*+2)^{q-1}\epsilon/R_0\). Section 07 states the larger
\(C(q,D)=16q^{q+1}D(4D+2)^{q-1}\), so its stated bound is valid, though
weaker, for every \(q\ge1\). The added \(\sqrt q/M\) term comes from the
separate cube-covering transfer, not from Basu–Lerario. The manuscript does
not use the continuous tube theorem as a direct count of grid atoms.

The preliminary literature note correctly distinguishes the 2021 arXiv
source from the separate unread 2023 journal package and correctly states that
continuous tube volume does not directly count atoms of a rational grid. Keep
the citation on the arXiv key and do not borrow journal-version pagination.

## Section 04: Ding's thesis

The exact current key is **`ding1996-a-parametric-solution-for-local`**.
Baoyan Ding's thesis is titled *A Parametric Solution for Local and Global
Optimization*. The read local package is
`literature/papers/ding1996-a-parametric-solution-for-local/` and contains the
primary PDF and read text. The [Waterloo repository content URL](https://dspacemainprd01.lib.uwaterloo.ca/server/api/core/bitstreams/2c9e7b72-4454-4349-9741-b33beb9689ad/content)
is the primary PDF; the [repository item record](https://uwspace.uwaterloo.ca/items/0ee267e7-ed4c-4eab-adff-a202444a746a)
is dated 1997. The title page and copyright notice give 1996.

The thesis writes a structured indefinite QP as a positive-semidefinite
quadratic program plus a bilinear term, introduces \(t=D^{\mathsf T}z\), and
minimizes the resulting convex parametric-QP value function. Theorem 2.2.5
(physical PDF p. 29; thesis body p. 20) gives the global-minimizer
correspondence and objective-value recovery without an isolated-minimizer
condition. Chapter 2.3, pp. 30–34, treats the one-negative-eigenvalue case by
scalar parameter intervals and a piecewise-quadratic envelope.

Section 04 lines 410–413 accurately describes the structured indefinite-QP
reduction and recovery scope. It does not attribute a randomized or smoothed
guarantee to Ding. No repair is required. If a pinpoint citation is desired,
use Theorem 2.2.5 and the physical-PDF locator, while preserving the 1996
title-page year and noting the 1997 repository date.

## Section 04: Patrinos–Sarimveis

The exact current key is
**`patrinos2011-convex-parametric-piecewise-quadratic-optimization`**. The
journal article is Patrinos and Sarimveis, *Convex Parametric Piecewise
Quadratic Optimization: Theory and Algorithms*, *Automatica* 47(8):1770–1777
(2011), DOI 10.1016/j.automatica.2011.04.003. The read local package is
`literature/papers/patrinos2011-convex-parametric-piecewise-quadratic-optimization/`.
The read primary is the authors' [2010 technical-report PDF](https://www.chemeng.ntua.gr/labs/control_lab/zipfiles/TR2010-01.pdf),
whose title page adds “and Control Applications”; the [DOI record](https://doi.org/10.1016/j.automatica.2011.04.003)
identifies the shorter 2011 journal title used by the current key. Package
locators below are physical PDF pages of the 22-page report.

Section 4, Proposition 5, pp. 7–8, says a proper convex PWQ objective has a
proper convex PWQ value function and a polyhedral solution multifunction.
Under strict convexity, the optimizer is unique, piecewise affine, and
Lipschitz. Section 4, Theorem 1, pp. 8–9, characterizes critical-region
closures. Section 6, Theorem 6 and Algorithms 1–2, pp. 14–17, gives adjacency
and graph traversal for full-dimensional critical regions. The source does
not establish a polynomial worst-case region-count or bit-complexity bound.

The citation is appropriate for established convex parametric-QP/PWQ formulas
and region machinery. The current phrase “affine optimizer formulas” at lines
407–409 is accurate under the usual single-valued or strict-convexity
assumptions; in the general convex case, the source gives a polyhedral
multifunction, not necessarily one affine optimizer-valued function. For
maximum precision, add “under the usual uniqueness/regularity assumptions,”
or describe the general solution map as polyhedral and set-valued. This is a
scope qualifier, not a blocker for the conventional comparison. Do not
attribute the draft's one-region-per-query extraction or smoothed expected-work
result to this source.

The broader full-citation and bibliography audit noted as pending in
`literature-preliminary.md` remains outside this source check. No bibliography
file was integrated or edited here.
