# Independent audit of scalar polynomial growth sections

Date: 2026-10-02. Scope: the semialgebraic section count and finite-grid
transfer in the actual
[polynomial finite-noise note](polynomial-finite-noise-tails.md), checked
independently against a second primary quantifier-elimination source.
The count passes. No stationary-point enumeration, external search, or
executable optimization test is used.

## 1. Exact quantified event

Write \(X\) for the nonempty compact mixed box after effective integer
endpoints and fixed coordinates have been handled. There are \(n\ge1\)
remaining coordinates. An integer coordinate \(j\) has \(N_j\) labels.
Fix the growth threshold \(\varepsilon>0\), every linear perturbation
coefficient except one, and call the remaining coefficient \(t\).

Membership in \(X\) has the quantifier-free description

\[
 \mathcal D(z)=
 \bigwedge_{i\in\mathcal C}(\ell_i\le z_i\le u_i)
 \ \wedge\!
 \bigwedge_{j\in\mathcal Z}
             \bigvee_{k=\ell_j}^{u_j}(z_j=k).                    \tag{1}
\]

The good-growth event is exactly

\[
 \exists x\in\mathbb R^n\ \forall y\in\mathbb R^n:
 \mathcal D(x)\wedge
 \left[\neg\mathcal D(y)\vee
   \{F_t(y)-F_t(x)-\varepsilon\|y-x\|^2\ge0\}\right].          \tag{2}
\]

The inequality itself proves optimality and uniqueness of \(x\), so an
optimum-value variable or an extra optimum-testing quantifier is unnecessary.
Conversely, an optimizer with point-growth constant at least
\(\varepsilon\) satisfies (2). Distinct tied optimizers cause (2) to fail:
the other optimizer gives zero objective gap and strictly positive squared
distance. A unique optimizer with zero quadratic growth also fails (2).

Thus the event treats ties and flat unique minima correctly without any
assumption about KKT systems. Singular or positive-dimensional stationary
sets never enter the formulation.

Integer labels enlarge the Boolean formula, not the quantified variable
blocks. Formula (2) has exactly two blocks of \(n\) real variables and one
free real variable. Its polynomial family has size at most

\[
 s_0=4n+2\sum_{j\in\mathcal Z}N_j+2,
 \qquad d_0=\max\{d,2\}                                      \tag{3}
\]

as a bound on total degree. In particular, \(t(y_i-x_i)\) has total
degree two. The threshold and all fixed coefficients are coefficients
of these polynomials, even when they are arbitrary real numbers.

The input polynomial can have many explicit factors or monomials; their
sum is still a single polynomial in the growth comparison. At fixed degree
the dense coefficient representation, if desired for the theorem below,
has only polynomially many positions in \(n\).

## 2. A primary block-sensitive bound

I read **Basu, Pollack, and Roy (1996), Theorem 1.3.1**, printed
pp. 1004--1005, directly in the
[local primary PDF](../../literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf).
The local extraction omits displayed formulas; `pdftotext -layout` on
PDF pages 4--5 exposes the relevant bounds. I also checked the presentation
in **Basu (2014), Theorem 2.27**, printed p. 16, in its
[local PDF](../../literature/papers/basu2014-algorithms-in-real-algebraic-geometry/original.pdf).
These agree with the Renegar bound used by the main note.

The 1996 theorem produces a disjunction of conjunctions of polynomial sign
conditions. For \(\ell\) free variables and quantified block sizes
\(k_1,\ldots,k_\omega\), it bounds the number of disjuncts by

\[
 s^{(\ell+1)\prod_b(k_b+1)}
       d^{(\ell+1)\prod_b O(k_b)},                              \tag{4}
\]

the number of atomic conditions per disjunct by

\[
 s^{\prod_b(k_b+1)}d^{\prod_b O(k_b)},                           \tag{5}
\]

and the output polynomial degrees by \(d^{\prod_b O(k_b)}\).
The theorem is over any real closed coefficient field; its format bounds
do not depend on coefficient heights or on nondegeneracy assumptions.

For (2), \(\ell=1\), \(\omega=2\), and \(k_1=k_2=n\). In particular,

\[
 \begin{split}
 I_{\rm out}&\le s_0^{2(n+1)^2}d_0^{O(n^2)},\\
 J_{\rm out}&\le s_0^{(n+1)^2}d_0^{O(n^2)},\\
 \deg P_{ij}&\le d_0^{O(n^2)}.
 \end{split}                                                    \tag{6}
\]

There is no \(2^n\) in these exponents. Applying an unrestricted CAD
bound, or introducing a new quantified copy for every integer label,
would lose precisely the bound needed here.

Choose a fixed universal constant \(a\) large enough for the selected
constructive quantifier-elimination theorem and set

\[
 H=(s_0d_0)^{a(n+1)^2},\qquad C=2H^3+1.                        \tag{7}
\]

All three quantities in (6) are at most \(H\). At most \(H^2\)
polynomial occurrences, each of degree at most \(H\), contribute at
most \(H^3\) distinct real roots. Nonzero constant polynomials have no
roots; identically zero polynomials have constant sign and are discarded
from the root count. Every Boolean sign formula is constant between
consecutive roots. The open intervals and individual root points number
at most \(2H^3+1\). Hence the good set and its complement each have at
most \(C\) interval or point components.

This is exactly the main note's coarse bound. It remains valid at special
fixed coefficient values where an output polynomial becomes identically
zero. No genericity assumption is needed.

The constant \(a\) is fixed independently of the instance, threshold,
and sampled coefficients. The cited elimination algorithms are constructive,
so a certified coarse constant can be fixed from their analysis. A concrete
sampler implementation would have to specify that numerical constant or
another explicit certified majorant; this audit does not extract one.
The asymptotic theorem and polynomial-bit existence claim require only
one such fixed constant, as explicitly stated in the main note.

## 3. Base size, uniformity, and sampling precision

For binary-encoded bounded integer intervals,
\(\log N_j=O(I_0)\), and \(n\le I_0\). Therefore
\(\log s_0=O(I_0)\) and, for fixed degree,

\[
                         \log C=O(I_0^3).                       \tag{8}
\]

The unspecified constant in (8) depends on the fixed degree and chosen
elimination bound. This is an exponential-in-polynomial component count,
not a double exponential with exponentially many sampling bits.
The large description (1) and quantifier-free output need never be formed
by the sampler. The counts \(N_j,s_0,H,C\), or their sufficient bit-size
bounds, are computable from the original interval encodings.

The count is uniform in all fixed real noise coefficients and every
\(\varepsilon>0\). Applying a real-coefficient format theorem here does
not claim that arbitrary real coefficients support executable exact
bit arithmetic. Only the number and degrees of the defining polynomials
are being bounded. This distinction is necessary during replacement of
continuous noise marginals by rational-grid marginals.

For the endpoint-inclusive uniform grid with \(M\) labels, the empirical
CDF differs from continuous uniform by at most \(1/M\), including its
left limits. Every interval or point therefore incurs probability
discrepancy at most \(2/M\). Conditioning and replacing one marginal at
a time gives, for the actual bad-growth event,

\[
 \left|\Pr_{\rm grid}\{g_*<\varepsilon\}
       -\Pr_{\rm continuous}\{g_*<\varepsilon\}\right|
                 \le \frac{2nC}{M}.                            \tag{9}
\]

Uniformity covers fixed coordinates that are already grid atoms as well
as those still drawn continuously. Combining (9) with the reviewed
[proximal tail](proximal-growth-tail.md) proves the main note's growth
tail on one fixed finite law, for every positive threshold. Taking
thresholds down to zero bounds tie and zero-growth atoms by \(2nC/M\).

If a separately justified fallback budget has logarithm polynomial in
the base input, the residual can consequently be chosen small enough to
pay for its occurrence while retaining polynomial sampling bits. This
does not itself establish the cost of that fallback, the good-draw work
bound, or an exact algebraic-output representation. Those remain separate
obligations, as the main note states.

## 4. Verdict and verification scope

The actual main note's scalar-section formula, \(H,C\) bounds, uniform
finite-grid transfer, and base-input accounting pass this independent
audit. The use of an effective algorithm-dependent constant in (7) is
appropriate for the stated asymptotic theorem; no numerical sampler
implementation is claimed.

A focused child independently derived the same conclusion by eliminating
the two continuous blocks successively after fixing integer assignments.
Its deliberately looser bound has \(\log C=O(I_0^4)\). The direct
two-block formula (2) avoids that extra bookkeeping and matches the
stronger bound used above.

The targeted source commands read the cited primary PDFs with
`pdftotext -f 4 -l 5 -layout` and `pdftotext -f 16 -l 16 -layout`.
An inline Python document check verified whitespace, paired math delimiters,
and local links. No executable optimization test, external literature
search, knowledge-base change, project-wide check, CI inspection, or index
edit was performed. This supplement does not replace the main note's
separate full-file review of the active-gradient argument.
