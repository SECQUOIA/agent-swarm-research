# Original-source audit for the Hessian-span Hölder bound

Date: 2026-09-27. This targeted follow-up partly closes the access gap in
[the first prior audit](hessian-span-holder-prior.md). The full Luo–Sturm
chapter *Error Bounds for Quadratic Systems* was obtained and inspected.
The original Wang–Pang article and Section 7.6 of the different Luo–Sturm
Handbook chapter remain unavailable in this pass. Search failure is not
evidence of novelty.

The strongest new comparison is mathematical: the proposed qualitative
exponent follows from a short Hessian-span argument in the full Shor lift,
combined with existing facial-reduction error bounds. Thus it should be
presented as a structural refinement of established theory, with priority
still unresolved, rather than as a new error-bound mechanism. The separate
[Hu–Li and conic comparison](hessian-span-holder-hu-li-comparison.md)
records that derivation and its independent check.

## The full quadratic-systems chapter was accessed

Zhi-Quan Luo and Jos F. Sturm, *Error Bounds for Quadratic Systems*,
in *High Performance Optimization* (2000), pp. 383–404,
[publisher chapter](https://doi.org/10.1007/978-1-4757-3216-0_16),
[publisher PDF](https://link.springer.com/content/pdf/10.1007/978-1-4757-3216-0_16.pdf).

An ordinary HTTP request to the publisher PDF URL returned the complete
22-page PDF. In the same session the web-reading tool redirected that URL
to the chapter abstract. Consequently the abstract-only web response is
not an accurate record of what was available to this audit. No login,
payment, author contact, or access-control workaround was used.

The substantive comparison is as follows. Theorem 16.3, p. 386, recalls
Wang–Pang's convex-system bound and prints an ambient-dimension bound
\(d\le n+1\); it sends the definition of \(d\) to the original article
and supplies no proof. Corollary 16.4 gives the one-half exponent for the
minimizer set of a convex quadratic over a polyhedron. The main new
Theorem 16.13, p. 393, gives a one-half exponent for one arbitrary quadratic
equality over a polytope. Its proof inducts on the number of vertices, not
on a span of quadratic forms. Corollary 16.14, pp. 397–398, extends this
to bounded test sets and an unbounded polyhedron. Theorem 16.16, p. 399,
treats continuous quadratic pieces on a polyhedral partition. The final
section, p. 400, conjectures an exponent \(2^{-m}\) for a vector of \(m\)
quadratic equations. These inspected results do not state a Hessian-span
bound. They also do not reproduce the multirow convex reduction proof
needed for the remaining Wang–Pang comparison.

The one-dimensional Hessian-span case is already covered by older
results, as explained in the first audit. For larger spans, the maximum
of quadratic rows generally has quadratic dominance boundaries, so the
piecewise-quadratic theorem on a *polyhedral* partition does not apply
automatically.

### A discrepancy in reproductions of the old parameter

The printed \(d\le n+1\) statement was checked visually on p. 386,
in addition to extracting its text. It cannot simply be combined with the
indexed-row definition reproduced by
[Jiang–Li, Section 3.1](https://rjjiang.github.io/papers/EBKLTRS_mor.pdf).
That definition assigns \(d=k+1\) to \(k\) copies of
\(x^2-y\le0\), together with \(y^2\le0\), as checked in the first audit.
For \(k>2\), this exceeds \(n+1=3\).

This does not disprove existence of an exponent with an ambient-dimension
bound: duplicates can be removed, and the example admits the exponent
\(1/4\). It does mean that the two secondary reproductions should not be
treated as identical definitions without resolving preprocessing or a
possible imprecision in one account. The original 1994 text remains the
right source for that question. No assertion about an error in the
original paper follows from this discrepancy.

## What was and was not retrieved

| Source | Access in this pass | Consequence for the comparison |
| --- | --- | --- |
| Wang–Pang, *Global error bounds for convex quadratic inequality systems* (1994), [DOI](https://doi.org/10.1080/02331939408844003) | Publisher abstract; ordinary publisher PDF request returned HTTP 403. OpenAlex and Semantic Scholar supplied no open full-text location. | The original proof and any preprocessing remain uninspected. |
| Luo–Sturm, *Error Bounds for Quadratic Systems* (2000), DOI ending `_16` | Complete 22-page publisher PDF, pp. 383–404. | The precise comparisons above use the actual primary text. |
| Luo–Sturm, *Error Analysis*, *Handbook of Semidefinite Programming* (2000), [DOI](https://doi.org/10.1007/978-1-4615-4381-7_7) | Publisher metadata; PDF URL redirected to an access page. The earlier audit inspected the two-page preview. | Sections 7.6.1–7.6.2 remain uninspected. The preview cannot settle the question. |
| Hu–Li, *Facial reduction for the Shor SDP relaxation of QCQPs* (2023), [published paper](https://asvao.biemdas.com/issues/ASVAO2023-2-5.pdf) | Complete open paper, separately inspected and reviewed. | Its further relaxation is different from the full Shor lift; the distinction matters for transferring an error bound. |

The local literature catalog was searched by filenames for Wang, Pang,
Luo, Sturm, error bounds, and Handbook. No matching original was found.
Searches then used the exact titles, DOIs, alternate title *Error bounds
for mixed semi-definite and second-order cone programming*, the chapter
section names, and historical author/preprint identifiers. Current author
pages, the Tilburg records, historical SDP bibliographies, publisher
URLs, OpenAlex locations, and Semantic Scholar metadata were checked.
No claim of an exhaustive search is made.

One useful archival trace was recovered: OpenAlex associates the
quadratic-systems chapter with CiteSeer identifier `10.1.1.56.3474` and
the former author URL
`http://www.crl.mcmaster.ca/People/Faculty/Luo/luo.publications/qerb.ps.Z`.
The McMaster host did not resolve. The CiteSeer endpoints redirected to
unavailable archive pages; the Internet Archive availability query
returned no snapshot for that exact author URL. This dead trace was
superseded by the successful publisher download. It is recorded to
prevent repeating the same failed retrieval path.

## Why Hu–Li alone is insufficient, and why generic conic theory is close

Hu–Li's equation (4.1) only requires the lower-right block \(X\) to be
positive semidefinite; it drops the full Shor relation
\(X\succeq xx^T\). Its strict feasibility therefore need not establish
regularity of the original quadratic feasible set. For example,
\((x-1)^2\le0\) has the singleton feasible set \(\{1\}\), whereas
the further relaxation \(X\ge0,\ X-2x+1\le0\) is strictly feasible at
\((x,X)=(2,1)\). Its singularity count cannot directly be substituted
for the original system's error exponent.

There is nevertheless a close route through the *full* Shor lift. After
translating a feasible point to the origin, the lift has a feasible PSD
matrix \(E_{00}\). Every PSD exposing matrix must annihilate its first
row and column. The remaining block is a member of the current
restricted Hessian span. Each reduction that changes the PSD face kills
a nonzero member of that span. Existing partial-polyhedral facial
reduction permits affine slack reductions without a square-root loss.
Consequently at most \(h\) curved steps suffice; the known conic bound
then has exponent \(2^{-h}\). A bounded rank-one lift of a test point
transfers its original residual, and convexity makes the lift's
projection exact. Full details, source propositions, and the independent
check are in the separate comparison note.

This is a derivation made in this research session from existing
theorems, not evidence that those authors explicitly stated it. It
substantially narrows the possible qualitative contribution. An effective
coefficient bound for the error constant would be a separate question;
none of the above supplies such a bound with the proposed dependence on
\(h\).

## Verification record

The full chapter was read through `pdftotext -layout`, with targeted
searches and manual inspection of the relevant sections; p. 386 was also
rendered and viewed to confirm the parameter statement. `pdfinfo`
reported 22 pages and 2,013,160 bytes. The downloaded PDF's SHA-256 is
`daba0690c6a1d82c1649db6936463f83e3b9ec815c33661098e8f39346ae32c8`.
Session copies are `/tmp/holder-quadratic-publisher` and
`/tmp/holder-quadratic-publisher.txt`; the publisher links above are the
durable references. No project-wide verification or CI inspection was
performed. A targeted Python check of this Markdown file confirmed its
final newline, absence of trailing whitespace and unexpected control
characters, and existence of both local link targets.
