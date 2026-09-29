# Prior audit: degree required for a rational convex singleton polynomial

Date: 2026-09-28. Scope: independent literature comparison for the proposed
degree lower bound accompanying
[the univariate realization note](univariate-convex-zero-realization.md).
The reviewer also reconstructed the proof, but this file records the prior
comparison. No equivalent result was identified in the passages inspected.
This is not evidence establishing novelty.

The candidate result concerns the cubic

\[
 p_n(x)=(x+2)(x-1)^2+2^{-2n},\qquad n\geq1.
\]

It is irreducible over the rationals and has exactly one real root
\(\alpha_n\). The claim is that every rational globally convex polynomial
whose only real zero is \(\alpha_n\) has degree greater than
\(\sqrt{3}\,2^{n/2}/2\). Thus even a cubic described with \(O(n)\) bits
can require exponentially large degree in this class of realizations.
The multiplier existence argument supplies realizations, so this is a
degree obstruction rather than nonexistence.

The analytic step is a short consequence of the classical Markov
inequality. The arithmetic step forces every rational realization to
retain a nonreal conjugate close to the real axis, well separated from
the real minimizer. These ingredients should be credited separately.

## Classical derivative inequalities

**A. Markov, *On a question by D. I. Mendeleev*.** The original paper was
read on 24 October 1889 and published in 1890. The openly available
[English translation by Carl de Boor and Olga Holtz](https://www.math.auckland.ac.nz/hat/fpapers/markov4.pdf)
states and proves, in Problem No. 2, pages 14–16, the exact bound

\[
 \|P'\|_{[a,b]}\leq \frac{2D^2}{b-a}\|P\|_{[a,b]},
 \qquad D=\deg P.
\]

The final conclusion on page 16 was inspected directly. Iteration gives
the derivative estimates used by the candidate proof. Taylor expansion
then excludes a complex zero within distance
\((b-a)/(4D^2)\) of an endpoint where a normalized polynomial equals one
and has norm at most one on the interval. This zero exclusion is an
elementary consequence of an old theorem, not a new derivative bound.

**Rafał Pierzchała, *Markov's inequality and polynomial mappings*,
Mathematische Annalen 366 (2016), 57–82.**
[Theorem 1.1 and Definition 1.2](https://link.springer.com/article/10.1007/s00208-015-1294-9)
were inspected. Theorem 1.1 restates the interval inequality; Definition
1.2 formulates iterated derivative estimates on Markov sets. The paper
also uses Taylor expansion to control polynomials off such a set.
Consequently, the general method of passing from derivative estimates
to nearby complex estimates is established prior. The inspected
statements do not give the rational convex singleton degree obstruction.

**Oleksiy Klurman, *V. Markov's problem for monotone polynomials* (2012).**
[Theorems 1.2 and 2.1](https://arxiv.org/pdf/1205.0846) give sharp derivative
estimates under monotonicity on an interval. The first derivative still
has quadratic dependence on degree in the uniform norm. This is relevant
shape-preserving approximation theory, but the inspected result is a
derivative extremal problem, not a statement about rational algebraic
zeros or required convexifying multiplier degrees. A sharper use of such
estimates could improve constants in the candidate argument; it would
not make its analytic mechanism new.

The one-page author abstract of **András Kroó and József Szabados,
*On Bernstein and Chebyshev type problems for k-monotone polynomials*
(2010)** was also
[inspected](https://web.ujaen.es/revista/jja/pdf/pre/jja-0002-02-10-5.pdf).
It describes sharp derivative orders for polynomials with nonnegative
first \(k\) derivatives. Only that abstract was available at this URL;
the full paper was not examined in this audit.

## Convexifying multipliers

**Krzysztof Kurdyka and Stanisław Spodzieja, *Convexifying positive
polynomials and sums of squares approximation*, SIAM Journal on
Optimization 25 (2015), 2512–2536.**
[Sections 3–5](https://arxiv.org/pdf/1507.06191) were inspected, especially
Remark 3.2, Lemma 3.3, Remarks 3.4 and 3.6, and Example 3.5.

Example 3.5 is a serious nearby precedent: the exponent in the prescribed
multiplier \((1+x^2)^N\) cannot be bounded from the degree of the input
polynomial alone. However, its input \((x-k)^2+1\) is already convex, so
the constant multiplier one works. The example therefore does not bound
the degree of every admissible multiplier. Remark 3.6 allows powers of
any fixed positive polynomial with positive second derivative, again
under strict positivity of the input. The candidate quantifies over
every rational convex polynomial with the specified singleton zero,
and gives a lower bound in the input bit length. It must not be presented
as the first coefficient-dependent degree phenomenon in convexification.

**Abdulljabar Naji Abdullah, Klaudia Rosiak, and Stanisław Spodzieja,
*Convexifying of polynomials by convex factor*, Analytic and Algebraic
Geometry 4 (2022), 21–51.** The
[publisher volume](https://repozytorium.uni.lodz.pl/bitstream/handle/11089/44825/Krasinski_Spodzieja_Algebraic%204-.pdf?isAllowed=y&sequence=1)
was inspected at Lemma 3.1, Corollaries 3.2, 5.1–5.2, and 6.3; DOI:
[10.18778/8331-092-3.03](https://doi.org/10.18778/8331-092-3.03).
On compact convex sets, powers of a positive strongly convex base
convexify an input bounded below by a positive constant. The stated
exponent depends on derivative bounds, that lower bound, and the base.
The unbounded version inspected uses logarithmic strong convexity and a
positive leading form. These are sufficient constructions with explicit
dependence on conditioning data. They do not give a lower bound over
all polynomial multipliers or preserve an isolated irrational zero
under a strict-positive-input hypothesis.

## Degree obstructions for positive-coefficient multiples

**T. S. Motzkin and E. G. Straus, *Divisors of polynomials and power series
with positive coefficients*, Pacific Journal of Mathematics 29 (1969),
641–651.** The
[primary publisher PDF](https://msp.org/pjm/1969/29-3/pjm-v29-n3-p13-s.pdf)
was inspected at the definitions and Theorem 2.1, Corollary 2.4, and
Theorem 2.5. Here “positive” means nonnegative coefficients, not positive
function values.

For a quadratic with conjugate roots of arguments \(\pm\theta\),
Theorem 2.1 gives the minimal degree \(\lceil\pi/\theta\rceil\) of a
nonnegative-coefficient multiple. This is an established example of a
nearby complex root forcing high degree in every admissible multiple.
It is conceptually close and must be acknowledged. Its coefficient
restriction is stronger than convexity on the positive half-line and
does not follow from global convexity. Hence its lower bound does not
directly apply to all convex realizations. No conversion proving the
two formulations equivalent was found or established here.

The introduction of **Erik I. Verriest and Nak-seung Patrick Hyun,
*Roots of Polynomials with Positive Coefficients*,
MTNS 2018**, was
[inspected](https://mtns2018.hkust.edu.hk/media/files/0073.pdf) as a later
entry into this literature. It discusses positive-coefficient
multipliers and earlier minimal-degree work. Those coefficient
conditions should not be silently substituted for function convexity.

## Search scope and assessment

Searches combined variants of “convex polynomial” with “complex zeros,”
“nonreal roots,” “root-free,” “zero exclusion,” “sector,” and “degree
bound”; “convexifying” with “multiplier,” “lower bound,” and “degree
bounds”; and “rational convex polynomial” with “unique zero” and
“algebraic.” Monotone-polynomial derivative results and
positive-coefficient multiples were examined as alternative terminology.
Many hits concerned convex images of holomorphic functions, convex hulls
of roots, or robust stability of polynomial families; these are different
uses of convexity.

Local Markdown literature searches found mostly convex-envelope and
optimization uses of “convexifying.” The catalog entry for
[Kopotun–Shadrin's free-knot shape-preserving approximation paper](../literature/papers/kopotun2003-on-k-monotone-approximation-by/paper.md)
was read; it concerns approximation by splines and supplies no equivalent
exact-zero claim. Existing local singleton prior notes were also
searched for the convexification references.

The candidate is best described as an explicit arithmetic degree
obstruction obtained from classical Markov theory. Its quantified
conclusion is stronger than the prescribed-power obstruction in the
inspected convexification paper. An exact equivalent under another
formulation remains possible. The audit does not support a claim that
this is the first such obstruction or that the proof method is new.

The practical consequence proved is limited: a rational univariate
convex polynomial representation can require exponential dense output,
even for a cubic singleton. It does not rule out short arithmetic
circuits, sparse representations, nonpolynomial convex functions,
auxiliary-variable formulations, or efficient algorithms using an
algebraic-number representation directly.

No project-wide verification or CI inspection was performed. The only
file check for this audit tested its local links, final newline, and
absence of trailing whitespace and control characters.
