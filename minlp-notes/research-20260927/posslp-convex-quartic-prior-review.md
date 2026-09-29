# Independent review of the exact convex-quartic prior comparison

Date: 2026-09-28. Scope: the cited comparisons in
[the prior note](posslp-convex-quartic-prior.md), including its ordinary
SOCP deduction. This review does not validate the cubic-root simulation
or the unconstrained quartic construction; their proof reviews are separate.
The SOS and convexity-recognition sources received a second, delegated
primary-text check.

The principal source comparisons are supported. The SOCP deduction is
valid, with the input constant substituted before applying Slater
duality. The conditional SOS-membership consequence needs the source
polarity adjustment described below. The main note incorporated that
adjustment, clarified the moment order, and made Lasserre's constraint
sign convention explicit during this review. These findings are a narrow source and deduction
audit, not a priority or novelty endorsement.

Tarasov--Vyalyi's Theorem 3 establishes polynomial equivalence of
arithmetic-circuit comparisons over the arithmetic, division-free,
monotone, and addition/scaled-squaring bases. Theorem 4 reduces comparison
over the last basis to exact SDP feasibility. Section 2 uses scalar
addition epigraphs, two-by-two PSD square epigraphs, and Ramana's extended
dual. Its published theorem is an SDP result: the ordinary SOCP statement
in the repository should remain identified as a deduction, not quoted as
their theorem. The cited preprint supports the broad prior-hardness
claim. [Tarasov--Vyalyi v1, Theorems 3--4 and Section 2](https://arxiv.org/pdf/cs/0512035v1).

Here is an independent check of the deduction's vulnerable steps. Write
the product of gate slacks as

\[
H(x)=H_0+\sum_i x_iH_i\in K,
\qquad K=\mathbb R_+^a\times(S_+^2)^b,
\]

and minimize \(c^Tx+c_0\). Under the product trace inner product, its
ordinary dual is

\[
\max_Y\ c_0-\langle H_0,Y\rangle,
\qquad \langle H_i,Y\rangle=c_i\ \text{for all }i,
\qquad Y\in K.
\]

This follows from the Lagrangian
\(c^Tx+c_0-\langle Y,H(x)\rangle\). In particular, the dual value is
a lower bound on the circuit value. Off-diagonal trace terms only
introduce factors of two; they require no irrational coefficients.

Starting at one, every actual addition/scaled-square gate value is
strictly positive. Induction forces every feasible predecessor coordinate
to be at least its positive actual value, which justifies monotonicity
of squaring on the relevant range. The actual circuit tuple attains the
finite primal optimum. Choosing each gate coordinate strictly above its
required lower bound in topological order makes each scalar slack
positive and each square block positive definite. There is no singular
input-enforcing block after substituting one. Generalized Slater duality
therefore supplies equality of primal and dual values and dual
attainment. The needed statement is explicit on printed page 265 of
[Boyd--Vandenberghe, Section 5.9](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).

For the two circuits, dual feasibility for \(A\) and primal feasibility
for \(B\) give \(d_A\le A\) and \(p_B\ge B\). The block

\[
\begin{pmatrix}d_A-p_B&1\\1&t\end{pmatrix}\succeq0
\]

forces \(d_A-p_B>0\): a zero first diagonal would contradict the
nonzero off-diagonal entry. Conversely, attained optima with \(A>B\)
permit \(t=1/(A-B)\). Thus the signs are correct in both directions.
All dual equations, cone blocks, and the final gap block have polynomial
encoding length. A feasible point, a Slater point, or \(t\) may require
far more bits; the reduction only prints the defining equations. The
conversion
\(\|(2b,a-c)\|_2\le a+c\) for a symmetric two-by-two PSD block
uses rational coefficients and is exact. No boundedness, strict
feasibility, or short-witness promise should be attached to the final
combined SOCP without an additional proof. No such promise is needed
for ordinary exact SOCP feasibility.

The Hesse comparison also survives inspection. Its v1 Section 1.3 uses
the exact question \(\exists x\in P:f(x)\le0\); Table 1 marks exact
convex-quartic decision as unknown. Corollary 1.2 instead returns an
additive \(\varepsilon\)-optimal point in time polynomial in the input
length and \(\log(1/\varepsilon)\). Section 1.4 distinguishes exact
SOS-convex SDP representations from their unexamined polynomial-time
solvability. These statements support a comparison with exact threshold
hardness, not a claim that approximation resolves the threshold.
[Slot--Steurer--Wiedmer v1, Corollary 1.2, Table 1, and Section 1.4](https://arxiv.org/html/2511.03440v1).

The repository's cube and unconstrained problems fit that decision
framework if their reductions are correct. An inverse-exponential lower
bound on the absolute nonzero minimum would be needed to turn the
displayed approximation runtime into a polynomial-time exact-sign
procedure; strong convexity alone supplies no such separation. A PosSLP
lower bound would add information to the table, while leaving its
questions about polynomial time and standard membership classes open.
The [arXiv record](https://arxiv.org/abs/2511.03440) still listed only
v1, submitted 5 November 2025, when checked. The
[STOC 2026 accepted-paper list](https://acm-stoc.org/stoc2026/accepted-papers.html)
includes the paper. The proceedings text was not checked.

The SOS implications are mathematically appropriate but need precise
coefficient fields and constraint signs. Helton--Nie's Lemma 8 assumes
an SOS Hessian, a zero value, and a zero gradient at a point; its
conclusion is a real SOS representation. Strong convexity is sufficient
to obtain the attained minimizer used when applying it to
\(G-\min G\). Consequently, on this class,
\(G\ge0\) everywhere if and only if \(G\) is real SOS. The lemma
does not provide rational squares or a polynomial binary bound for an
optimal Gram matrix. Pin the citation to the inspected version:
[Helton--Nie v5, Lemma 8, printed page 10](https://arxiv.org/pdf/0705.4068v5).

Lasserre writes the feasible region as \(K=\{g_j\ge0\}\). Corollary
2.5 assumes Slater feasibility, an attained minimum, SOS-convex \(f\),
and SOS-convex \(-g_j\), and obtains

\[
f-f^*=\sigma+\sum_j\lambda_jg_j,
\qquad \lambda_j\ge0,
\]

with a real SOS remainder. Therefore the phrase "SOS-convex objective
and constraint functions" must either state convex rows
\(h_j\le0\), or explicitly use SOS-concave \(g_j\ge0\).
For a quartic and affine cube rows, the resulting degree-four SOS
description has moment order two, the first admissible order. This
representation does not itself bound the binary complexity of solving
the SDP or comparing its exact value. The updated moment-order wording
in the main note is correct, and its updated sign convention and versioned
URL address this finding. The inspected source is
[Lasserre v2, Assumption 2.1 and Corollary 2.5, printed pages 2--3](https://arxiv.org/pdf/0801.3754v2).

The conditional nonnegativity/SOS-membership lower bound requires an
explicit orientation check. The current proposed map satisfies

\[
V>0\iff\min G_V<0,
\qquad V\le0\iff\min G_V>0.
\]

It directly reduces PosSLP to failure of nonnegativity and failure of
SOS membership. To reduce PosSLP to membership, apply the same map to
the integer circuit with output \(1-V\). Since \(V\) is an integer,

\[
V>0\iff1-V\le0
\iff\min G_{1-V}>0
\iff G_{1-V}\text{ is nonnegative}
\iff G_{1-V}\text{ is real SOS}.
\]

This uses only one added subtraction gate and preserves every target
promise already proved uniformly for the construction. No assumption
that a complexity class is closed under complement is necessary. The
main note now includes this step. It remains conditional on the separate
proof of the strict, nonzero minimum-sign reduction.

The AOPT comparison is accurate. Theorem 2.1 concerns recognizing
convexity, even for homogeneous quartics; Propositions 3.4--3.5 concern
recognizing strong and strict convexity at fixed even degree at least
four. Their reductions include nonconvex outputs. These theorems do not
give optimization hardness under a supplied valid strict Hessian
certificate. [Ahmadi--Olshevsky--Parrilo--Tsitsiklis, Theorem 2.1 and Propositions 3.4--3.5](https://web.mit.edu/~a_a_a/Public/Publications/convexity_nphard.pdf).

The remaining nearby comparisons were checked at their relevant
statements. The OPT-gate theorem is a pseudogate construction for bounded
convex programs under explicit Slater conditions, including independence
of equality rows; it supplies a fixed-point representation, not an exact
threshold algorithm. The source does not even require an objective-value
circuit when its subgradient pseudogate is supplied.
[Filos-Ratsikas--Hansen--Høgh--Hollender v3, Definition 3.4, Theorem 3.2, and Remark 2](https://arxiv.org/pdf/2111.06878v3).
The ICALP 2025 paper explicitly records the old PosSLP-to-SDP reduction
and studies reductions from stochastic games; this supports its limited
contextual use in the note.
[Bodirsky--Loho--Skomra, introduction](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.145/LIPIcs.ICALP.2025.145.html).

Verification consisted of reading the cited primary statements and
checking the displayed conic dual and strict-gap construction by hand.
The author-hosted Boyd PDF was retrieved with Python's
`urllib.request` and read using `pdftotext -layout`; the web PDF viewer
had failed to open it. No broad literature search, complete rereading
of every cited paper, audit of the final STOC proceedings, or independent
proof check of the root/quartic reductions was performed. The review
therefore cannot exclude an equivalent earlier restricted result.
No project-wide checks or CI inspection were performed. The targeted
command `git diff --no-index --check /dev/null research-20260927/posslp-convex-quartic-prior-review.md`
reported no whitespace diagnostics; its exit status was 1 because the
file is new. A Python heredoc using `pathlib` and `re` checked every local
Markdown link and balanced `\[`/`\]` and `\(`/`\)` delimiters: one local
link resolved and both delimiter checks passed. No numerical test was
needed for the source comparisons or this symbolic duality argument.

**Witness-size source addendum, 2026-09-28.** This subsequent check
concerns two specific prior results, not the proposed new witness-size
construction or a search for all equivalent constructions.

[Safey El Din--Zhi v1, Proposition 2.5](https://arxiv.org/pdf/0910.2973v1),
PDF page 9, printed page 7, states a rational-coordinate bit bound
\(\ell D^{O(n)}\) for a nonempty set defined by strict polynomial
inequalities. No convexity hypothesis occurs in that proposition.
Nonemptiness appears in the introductory sentence, although it is
omitted from the proposition's displayed wording. The source explicitly
attributes the result to Basu--Pollack--Roy's Theorem 4.1.2 and its proof
on page 1032. For the intended application, state the hypothesis as a
nonempty basic open set, such as \(G<0\). Arbitrary negations of strict
atoms can express equalities and are not a sound interpretation here.

The original
[Basu--Pollack--Roy journal version](https://www.math.purdue.edu/~sbasu/jacm95.ps)
confirms the narrower statement directly. Theorem 4.1.2 starts on
printed page 1031 and continues on page 1032: if
\(S=\{x\in\mathbb R^n:P(x)>0\text{ for every }P\in\mathcal P\}\)
is nonempty, the integer polynomials have degree at most \(D\), and
their coefficients have bit length at most \(\ell\), every
semialgebraically connected component contains a rational point with
numerator and denominator bit lengths \(\ell D^{O(n)}\). Convexity is
not required. The author-hosted PostScript is linked from
[Basu's publication page](https://www.math.purdue.edu/~sbasu/); the
[journal DOI](https://doi.org/10.1145/235809.235813) is
`10.1145/235809.235813`. The inspected
[cached PDF](../literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf)
has this theorem on PDF pages 30--31. Its local provenance identifies it
as a PDF conversion of the author-posted journal PostScript. The primary
text was re-extracted with
`pdftotext -f 30 -l 31 -layout literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf -`.

[Pataki--Touzov v2](https://arxiv.org/pdf/2103.00041v2), pages 2--3,
recalls Khachiyan's convex-quadratic system
\(x_i\ge x_{i+1}^2\), \(x_m\ge2\). It forces
\(x_1\ge2^{2^{m-1}}\), hence exponential rational-coordinate bit
length. Their formal Theorem 1, page 9, requires dual singularity degree
\(k\ge2\), fixes trailing coordinates, and makes the hierarchy
conditional on \(x_k\) being sufficiently large. It does not say all
points in every strictly feasible SDP require huge representations.
The explanation on page 4 explicitly gives a modified chain allowing
the leading variables to vanish. The abstract's broad phrasing should
therefore not replace the theorem's hypotheses.

Independently, the old chain is strictly feasible by setting \(x_m=3\)
and \(x_i=x_{i+1}^2+1\) backwards, and it is unbounded by increasing
\(x_1\). Its large coordinates force numerator size. The proposed
target adds distinct restrictions: one strongly SOS-convex quartic row,
a compact full-dimensional sublevel of small norm, and exponential
denominator size for every rational feasible point. The two cited
results do not establish that simultaneous restriction. The general
upper bound permits exponential bit length at fixed degree, so such a
lower bound would not contradict it. This source check does not establish
priority or verify that the new construction achieves those promises.
After this addendum, the local Python document check was rerun: both
local links resolved, math delimiters balanced, and no trailing
whitespace was found.
