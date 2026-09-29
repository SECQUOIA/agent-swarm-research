# Rational Gram certificate size: primary-literature comparison

Date: 2026-09-28. Status: source comparison, not a construction or a
priority claim. The constrained SOS comparison has a separate
[primary-source review](gram-bit-size-constrained-sos-prior-review.md).

The achieved result is now the separately
[reviewed interior-Gram lower bound](interior-gram-bit-lower-bound.md):
every rational positive definite Gram needs exponentially many bits,
while the same constructed polynomial has a short singular rational
Gram and a short SOS certificate. The stronger all-PSD target below
remains open in this work.

Exponential bit requirements are established for general SDP feasibility
and constrained SOS proofs. The sources checked here do not establish
the proposed combination: ordinary rational quartic input, strict global
positivity, strong SOS-convexity with a supplied small rational positive
definite Hessian Gram, rational ordinary Gram feasibility, and a
superpolynomial lower bound for every rational ordinary Gram matrix.
An unsuccessful search does not establish that this combination is new.

The proposed construction remains separate from this literature audit.
In particular, this note does not prove that such quartics exist.

## 1. Which certificate and which size?

For an ordinary quartic, use the full monomial vector
\(v_2=(X^\alpha)_{|\alpha|\le2}\). Its Gram spectrahedron is

\[
\mathcal G(f)=\{Q\succeq0:v_2^TQv_2=f\}.
\]

This differs from the Gram matrix of one SOS term in a certificate
\(g=\sigma+\sum_i\lambda_iq_i\), where the polynomial represented by
that Gram changes with the equality multipliers. It also differs from a
Gram for \(u^T\nabla^2 f(X)u\).

A rational-entry bit bound counts reduced numerators and denominators.
A norm bound controls magnitudes only. A positive definite Gram proves
strict feasibility in the coefficient-matching affine space; it does
not supply a quantitative interior radius. Strict positivity of \(f\)
on real points alone does not assert a positive definite Gram.

All comparisons use expanded rational polynomial or matrix input.
For fixed quartic degree, the full polynomial coefficient vector and
ordinary Gram matrix have polynomial dimension in the number of
variables. An exponential bound in a construction parameter with
polynomial input length establishes superpolynomial output length; it
does not automatically establish \(2^{\Omega(L)}\) in total input length
\(L\). Algebraic or circuit encodings are different certificate models.

## 2. General SDP and the scope of Pataki--Touzov

[Pataki and Touzov, *How Do Exponential Size Solutions Arise in
Semidefinite Programming?*, arXiv:2103.00041v2](https://arxiv.org/pdf/2103.00041v2),
published in *SIAM Journal on Optimization* 34 (2024), 977--1005,
recalls Khachiyan's system

\[
x_i\ge x_{i+1}^2\quad(i<m),\qquad x_m\ge2.
\]

It is strictly feasible and forces \(x_1\ge2^{2^{m-1}}\). Its
exponential bit requirement arises from unbounded magnitudes. Their
Theorem 1, printed page 9, describes a variable hierarchy after
reformulation, fixing trailing coordinates and taking another
coordinate sufficiently large. It does not say that every strictly
feasible SDP has only large solutions. Their unconstrained univariate
optimization example in Section 3 concerns a dual SDP and explicitly
distinguishes large magnitude from large bit length. The constrained
example revisits O'Donnell.

The historical attribution is checked in this primary paper.
Ramana's 1997 original article was located, but the attempted open PDF
endpoint failed; no detailed theorem from that article is treated as
independently read here. The
[Porkolab--Khachiyan technical-report abstract](https://dimacs.rutgers.edu/archive/TechnicalReports/abstracts/1996/96-18.html)
states an upper bound on the logarithm of a real feasible solution's
norm. That statement alone is not a rational-denominator bound.

## 3. Constrained SOS lower bounds and failed direct transfers

[O'Donnell, ITCS 2017](https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.59/LIPIcs.ITCS.2017.59.pdf),
Theorem 1, has a quadratic system with bounded variables and
degree-two certificates requiring exponential bits, even with fixed
additive tolerance. Its proof forces a doubly exponential SOS Gram
diagonal. The matrix represents an SOS term modulo the constraints.
The target itself is linear and not globally nonnegative.

[Raghavendra and Weitz, ICALP 2017](https://drops.dagstuhl.de/storage/00lipics/lipics-vol080-icalp2017/LIPIcs.ICALP.2017.80/LIPIcs.ICALP.2017.80.pdf),
Theorem 2, gives Boolean quadratic systems with low-degree certificates
but large coefficients through degree \(\sqrt N\). Section 5.1 already
uses a unique-real-zero chain
\(q_i=y_i^2-y_{i+1},q_m=y_m^2\) and a target
\(\epsilon-y_1\), positive at that zero. Its argument forces a large
last equality multiplier at every degree. Thus uniqueness of the real
zero and positivity on the constrained set are already present in
this prior work.

The [separate review](gram-bit-size-constrained-sos-prior-review.md)
records equations, constants, and the exact transfer obstruction.
O'Donnell's example has a small degree-four certificate, so its
degree-two Gram bound cannot justify a quartic transfer. For the
Raghavendra--Weitz chain, prescribing small equality multipliers in
\(f=\lambda\sum_iq_i^2+\epsilon-y_1\) rules out SOS feasibility
itself. A large ordinary Gram cannot compensate for that failure.

## 4. Boundedness and rational Gram existence are established

[Chua, Plaumann, Sinn, and Vinzant, *Gram Spectrahedra*](https://arxiv.org/pdf/1608.00234),
Lemma 1.5, proves compactness of polynomial Gram spectrahedra and
identifies interior SOS polynomials with the existence of a positive
definite Gram. Lemma 1.6 equates rational Gram feasibility with a
rational SOS decomposition; the following discussion explains rational
feasibility in the interior by density in the rational affine Gram
space. These facts give no polynomial denominator bound. Consequently,
compactness of a proposed ordinary Gram spectrahedron is automatic,
not an added achievement. Any quantitative small-norm assertion still
needs its own bound in the chosen basis.

[Bodirsky, Loho, and Skomra, ICALP 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/LIPIcs.ICALP.2025.145/LIPIcs.ICALP.2025.145.pdf),
Theorem 9, realizes the singleton \(\{2^a\}\), for any integer
\(a\), as a projection of a spectrahedron with representation size
polynomial in the bit size of \(a\). Negative exponents already give
compact projected coordinates with huge denominators. The proof joins
a repeated-squaring primal system to dual optimality equalities. It
does not assert boundedness or strict feasibility of the full lift,
and does not identify it with an ordinary polynomial Gram spectrahedron.

## 5. Upper bounds, including a substantive correction

[Safey El Din and Zhi, *Computing Rational Points in Convex
Semialgebraic Sets and SOS Decompositions*](https://arxiv.org/pdf/0910.2973),
Theorem 1.1, decides rational feasibility for a convex semialgebraic
set and gives coordinate bits \(\sigma D^{O(k^3)}\), where \(k\)
is its dimension, \(D\) bounds defining polynomial degrees, and
\(\sigma\) bounds input coefficient bits. Section 5 applies this to
rational SOS decompositions. It covers rational points on lower
dimensional sets; nonempty real feasibility alone need not imply
rational feasibility. This is a large upper bound, not a polynomial
bound in general Gram dimension.

The early [Magron--Safey El Din preprint, arXiv:1802.10339](https://arxiv.org/pdf/1802.10339),
Proposition 3.4, states a coefficient-bit bound \(\tau d^{O(n)}\)
for interior SOS input. **Do not use that early bound as the current
comparison.** The corrected
[arXiv:1811.10062v4](https://arxiv.org/pdf/1811.10062v4),
Proposition 10 and Theorem 12, states
\(\tau d^{d^{O(n)}}\) for weighted rational SOS coefficients.
The corrected Proposition 4 obtains a rational positive definite Gram
through rational sampling in Gram dimension. The 35-page PDF on the
author's homepage inspected during this audit still displayed the
older estimate, so the versioned arXiv URL is important.

[Davis and Papp, *Rational Dual Certificates for Weighted
Sums-of-Squares Polynomials with Boundable Bit Size*](https://arxiv.org/pdf/2305.19039),
introduction, explicitly notes that correction. Their Theorem 2.9
bounds integer dual certificates using the polynomial's distance to
the WSOS boundary and representation parameters. Theorem 1.4 converts
a rational dual certificate to a rational Gram by an explicit formula.
This is relevant to alternative certificates, but it does not give a
uniform polynomial bound after the distance parameter is omitted.
No blanket lower bound on all proof systems follows from a lower
bound on ordinary Grams.

## 6. Recent weak membership and quantitative strict feasibility

[Gärtner, Magron, and Vallentin, *Sums of Squares in Polynomial
Time*, arXiv:2606.25118v1](https://arxiv.org/html/2606.25118v1),
Theorem 1.1, proves polynomial-time weak membership for the SOS cone
under dense rational encoding. Theorem 1.2 computes a rational
positive definite Gram for an approximately closest normalized SOS
polynomial. It does not require that the returned polynomial equal
the input exactly.

Corollary 1.3 adds the relevant exact statement: given rational
\(\epsilon>0\), if the input has an ordinary Gram with smallest
eigenvalue at least \(\epsilon\), an exact rational Gram can be
computed in polynomial time. The encoding length of \(\epsilon\)
is part of that statement. A prospective family with only long exact
Grams must therefore lack a polynomial-bit lower bound on an ordinary
Gram's positive eigenvalue margin. A small supplied Hessian Gram is a
different certificate. This is compatible with efficient weak
membership and does not establish exact SOS membership complexity.

## 7. Verification and remaining uncertainty

Primary text was inspected for the named theorem statements above.
The constrained lower bounds received a separate reader's proof-level
check. The author read that review and checked its distinction between
degree-two Grams and higher-degree equality multipliers. Other cited
algorithms were not rederived in full. No new mathematical construction
is verified by this note.

Searches covered rational feasible points, bounded spectrahedra,
denominator lower bounds, SDP bit complexity, ordinary Gram matrices,
constrained SOS proofs, and exact rational SOS algorithms. The search
also found *On the Bit Size of Sum-of-Squares Proofs for Symmetric
Formulations*, [arXiv:2509.06928](https://arxiv.org/pdf/2509.06928).
Its Section 4 theorems provide coefficient-magnitude bounds under
symmetry and other hypotheses. They were not treated as a general
rational-denominator theorem.

The checked literature does not settle whether the proposed strongly
SOS-convex quartic combination has already been achieved under another
formulation. Any future novelty claim must also compare its precise
bit lower bound, ordinary basis, strict Gram feasibility, and total
input length. No project-wide checks or CI inspection were run.

Targeted checks actually run: a Python check passed for this note and
the constrained-SOS review, verifying final newlines, trailing
whitespace, control characters, paired math delimiters, and two local
Markdown links. The targeted command
`git diff --check -- research-20260927/gram-bit-size-prior.md research-20260927/gram-bit-size-constrained-sos-prior-review.md`
also returned successfully. These document checks do not verify the
cited mathematical algorithms or establish novelty.
