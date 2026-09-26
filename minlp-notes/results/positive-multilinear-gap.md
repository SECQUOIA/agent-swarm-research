# Sharp asymptotic gaps for positive multilinear relaxations

Date: 2026-09-04. Status: analytic proof and exact hull formula independently audited by two agents; no unresolved mathematical issue identified. See `notes/review-positive-multilinear.md` and `notes/review-positive-multilinear-second.md`. Novelty review is recorded separately in `notes/positive-multilinear-novelty.md`.

Lean verification (updated 2026-09-20): the
[disproof](../formal/topics/07-multilinear-disproof/README.md),
[exact finite formula](../formal/topics/08-exact-multilinear/README.md), and
[sharp leading growth](../formal/topics/09-sharp-multilinear/README.md)
packages prove these conclusions using actual continuous graph-hull and
individual-monomial envelope gaps. The disproof uses the weaker estimate
`0 < chgap ≤ s + 2L/2^s` and exact `tbtgap = L`. The sharp-growth theorem
covers the original termwise relaxation on all finite nonnegative boxes
and exactly-n ambient dimension; its finite harmonic certificate differs
from the one in the analytic sharp-growth note.

The [September 16 completion](../formal/topics/10-multilinear-completion/README.md)
also proves general envelope attainment and interpretation, exact individual
monomial envelopes, construction counts and sparsity, the actual family's
ratio limit, and the four examples printed in the
[focused paper](../paper-multilinear-gap/README.md). Its
[coverage map](../paper-multilinear-gap/formal/COVERAGE.md) and
[verification record](../formal/topics/10-multilinear-completion/VERIFICATION.md)
give the statements and recorded checks. This does not extend verification
to every claim in this broader note: arbitrary-failure-count bit-reversal
and XOR constructions, the original integral bound for arbitrary partitions,
homogenization, coefficient removal, and the dense-model numerical experiments
remain outside those packages. The constant 24 and optimized fixed-point,
Lambert W, and second-order upper bounds in companion notes are also outside
their scope.

## Main conclusion

Let R(d) be the supremum of the term-by-term gap divided by the convex-hull gap over positive-coefficient multilinear polynomials of maximum degree at most d, all dimensions, finite boxes with nonnegative lower bounds, and points with positive hull gap. Let C(n) be the analogous supremum in n variables. Then

\[
\boxed{R(d)\sim\frac{\ln d}{\ln\ln d}},\qquad
\boxed{C(n)\sim\frac{\ln n}{\ln\ln n}}.
\]

Thus the conjectured universal constant does not exist, and the correct worst-case growth is determined to leading constant one. The lower bound below uses a sparse unit-coefficient polynomial and has an exact hull-gap formula. The matching upper bound uses harmonic conditional-failure couplings and an optimized mixture; its complete proof is in [the sharp degree-growth result](positive-multilinear-sharp-degree-growth.md). An earlier, simpler [logarithmic upper bound](positive-multilinear-degree-upper-bound.md) is retained as a separate argument.

The upper bound applies to the original term-by-term relaxation on every finite nonnegative box; affine rescaling and positive expansion require only an inequality between the original and expanded term gaps, as proved in the upper-bound notes. The lower construction already uses the unit cube. See the proof and novelty review records for the distinction between mathematical verification and the bounded literature search.

## Exact lower-bound construction

For every integer L≥2, a positive multilinear polynomial in n=2^L+L variables has fewer than 2n monomials, every coefficient equal to one, and a point in [0,1]^n where

\[
\operatorname{tbtgap}(x)=L,\qquad
\operatorname{chgap}(x)=s+(L-s)2^{-s},
\]

with s chosen so that

\[
(L-s+1)2^{-(s+1)}\le1\le(L-s+2)2^{-s}.
\]

Consequently the exact ratio is asymptotic to ln n/ln ln n and is unbounded. The total number of variable occurrences is O(n log n). This contradicts Conjecture 1 in the authors' technical-report version of Luedtke, Namazifar, and Linderoth, *Some Results on the Strength of Relaxations of Multilinear Functions*, and Conjecture 4.1 in the published version. A separate argument below proves the explicit lower bound L/[5+log_2(1+L ln2)] even when the block partitions are not nested.

Primary source: [authors' open technical report](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf), conjecture on p.22; local source [[luedtke2012-some-results-on-the-strength]] p.22. An open-web search on 2026-09-04 found the original conjecture but no resolution for positive multilinear functions. The 2017 Boland et al. unbounded-ratio theorem concerns mixed-sign bilinear functions and does not settle this positive-coefficient conjecture. Novelty remains subject to further literature review.

## Construction

Let m=2^L. There are m leaf variables z_1,...,z_m and L anchor variables a_1,...,a_L. Set

\[
u_j=2^{-j},\qquad k_j=m u_j=2^{L-j},\qquad j=1,\ldots,L.
\]

At level j, partition the m leaves into 2^j disjoint blocks, each of cardinality k_j. Write this partition as P_j. The partitions may be arbitrary; consecutive dyadic blocks provide one concrete nested choice. Define

\[
f_L(a,z)=\sum_{j=1}^L\sum_{B\in P_j}a_j\prod_{i\in B}z_i.
\]

Every coefficient is one. There are ∑_{j=1}^L2^j=2m−2 monomials, each distinguished by its anchor and block. There are Lm+2m−2 variable occurrences in total. Evaluate at

\[
a_j=u_j,\qquad z_i=1-1/m.
\]

Each monomial has concave-envelope value u_j, because u_j≤1/2≤1−1/m. Its convex-envelope value is

\[
\max\{0,u_j+k_j(1-1/m)-k_j\}
=\max\{0,u_j-k_j/m\}=0.
\]

Each level has 2^j monomials and 2^j u_j=1. Thus the term-by-term lower bound is zero and its upper bound is L. The upper bound is the concave envelope of f_L: simultaneously nested Bernoulli events attain the upper bound for every positive monomial. Consequently

\[
\operatorname{tbtgap}(x)=L,\qquad \operatorname{cav}f_L(x)=L.
\]

## Reducing the hull gap to a random failure count

The convex envelope of a multilinear function at x is the minimum of its expectation over distributions on binary vertices with mean x. Let A_j and Z_i denote any such binary random variables, and put

\[
R=m-\sum_i Z_i.
\]

Then E R=1 and P(A_j=1)=u_j. Let N_j denote the number of blocks in P_j containing at least one failed leaf. At every binary vertex,

\[
\sum_{B\in P_j}A_j\prod_{i\in B}Z_i=A_j(2^j-N_j).
\]

Since the blocks in each P_j are disjoint, every hit block requires at least one failed leaf, and therefore

\[
0\le N_j\le\min\{2^j,R\}.
\]

Since ∑_j2^j E A_j=L, the hull gap satisfies

\[
H_L:=\operatorname{chgap}(x)
=\max\mathbb E\sum_{j=1}^LA_jN_j
\le\sup\mathbb E\sum_{j=1}^LA_j\min\{2^j,R\},
\tag{1}
\]

where the supremum on the right ranges over all joint distributions of R∈{0,...,m} and A_j∈{0,1} with E R=1 and E A_j=u_j. Dropping the geometric restrictions on the hit-block counts can only increase the upper bound.

Fix the distribution of R. For any nondecreasing function g, the largest possible E[A g(R)] over binary A with P(A=1)=u is obtained by selecting the upper u-tail of R, splitting an atom if necessary. To see this, move any selected probability mass from a smaller value of R to a larger unselected value; the objective does not decrease. Equivalently, let U be uniform on (0,1) and let r(U) be a nonincreasing quantile representation of R. Then the maximum is ∫_0^u g(r(t))dt. This choice is simultaneously feasible for all anchors in the surrogate upper bound by setting A_j=1[U≤u_j]. Hence

\[
H_L\le \sup_{r}\int_0^1
\sum_{j:t\le2^{-j}}\min\{2^j,r(t)\}\,dt,
\tag{2}
\]

where r is nonnegative, nonincreasing, bounded by m, and ∫_0^1r(t)dt=1. Dropping monotonicity and the upper bound only enlarges the supremum used below.

## Exact hull gap for nested dyadic partitions

Take the partitions P_j to be the nested dyadic partitions: label leaves by L-bit strings, and put leaves in the same level-j block exactly when their first j bits agree. For any integer R∈{0,...,m}, there is a failed-leaf set hitting exactly min(2^j,R) blocks at every level j simultaneously. Specifically, take the first R strings in bit-reversal order. Their first j bits are the reversals of the residues 0,...,R−1 modulo 2^j, so exactly min(2^j,R) distinct blocks are hit. Apply a uniformly random bitwise XOR shift to all leaf labels. This preserves every level's hit count and gives each leaf failure probability R/m.

Consequently every joint distribution of R,A with the required means can be implemented without loss in (1), and the first upper bound in (1) is an equality for this dyadic construction.

For 0≤l<L set w_l=2^{-(l+1)}, and set w_L=2^{-L}. These are the probabilities of the intervals where exactly anchors 1,...,l are selected under the upper-tail coupling (l=0 means no anchors). Define

\[
S_l(r)=\sum_{j=1}^{l}\min\{2^j,r\},\qquad
B_q=(L-q+2)2^{-q},\quad 1\le q\le L.
\]

Choose s∈{1,...,L−1} satisfying B_{s+1}≤1≤B_s. Such an s exists because B_1=(L+1)/2≥1, B_L=2^{1-L}≤1, and B_q strictly decreases with q. Equality at an endpoint permits either adjacent choice and gives the same formula below.

**Exact formula.** The convex-hull gap of the dyadic polynomial is

\[
\boxed{H_L=s+\frac{L-s}{2^s}},\qquad
\boxed{\frac{\operatorname{tbtgap}(x)}{\operatorname{chgap}(x)}
=\frac{L}{s+(L-s)/2^s}}.
\tag{4}
\]

To prove the upper bound, note for all r≥0 that

\[
S_l(r)\le sr+F_l(s),\qquad
F_l(s)=\begin{cases}
0,&l\le s,\\
2^{l-s+1}-2,&l>s.
\end{cases}
\]

For l≤s this follows termwise from S_l(r)≤lr. For l>s, cap the first l−s terms by 2^j and each of the remaining s terms by r. The sum of the caps is 2^{l−s+1}−2. Equality holds throughout the interval [2^{l−s},2^{l−s+1}]. Integrating this bound over the quantile intervals and using E R=1 gives

\[
H_L\le s+\sum_{l=s+1}^Lw_l(2^{l-s+1}-2)
=s+(L-s)2^{-s}.
\]

For attainment, define two joint distributions indexed by q=s and q=s+1. Draw l with probabilities w_l, set A_j=1[j≤l], and set

\[
R_l^{(q)}=\begin{cases}
0,&l<q,\\
2^{l-q+1},&l\ge q.
\end{cases}
\]

Each anchor has probability ∑_{l=j}^Lw_l=2^{-j}, and the expected failure count is

\[
\mathbb E R^{(q)}
=\sum_{l=q}^{L-1}2^{-l-1}2^{l-q+1}
+2^{-L}2^{L-q+1}
=(L-q+2)2^{-q}=B_q.
\]

Mix these two distributions with weight

\[
\theta=\frac{1-B_{s+1}}{B_s-B_{s+1}}
\]

on q=s and 1−θ on q=s+1. The weight lies in [0,1] and the mixture has E R=1. Both component distributions attain S_l(R)=sR+F_l(s) at every l: for l<s, R=0; for l=s the endpoints are 0 and 2, where S_s(r)=sr; for l>s the endpoints are exactly 2^{l-s} and 2^{l-s+1}. Therefore the mixture attains the upper bound. The XOR-randomized bit-reversal construction realizes it with all leaf marginals equal to 1−1/m, completing the proof.

The threshold B_{s+1}≤1≤B_s implies s=log_2 L+O(1), and (L−s)/2^s is bounded. Thus H_L=log_2 L+O(1) and the exact ratio is asymptotic to L/log_2 L, or equivalently to log_2 n/log_2 log_2 n. The earlier logarithmic bound below is retained as an independent proof of unboundedness that works for arbitrary equal-size partitions, without using nested dyadic structure.

## An elementary logarithmic upper bound

Write δ=2^{-L}. For 0<t≤δ the summand in (2) is at most

\[
\sum_{j=1}^L2^j=2^{L+1}-2,
\]

so that interval contributes at most 2. For t>1/2 no anchor is selected and the contribution is zero.

For δ<t≤1/2, let l be the largest integer with t≤2^{-l}. Then 1≤l≤L−1 and 2^l≤1/t. For any r>0,

\[
\sum_{j=1}^{l}\min\{2^j,r\}
\le r\left(3+\log_2^+\frac{1}{tr}\right),
\tag{3}
\]

where log^+(s)=max{0,log(s)}. Indeed, if r≥2^l the sum is less than 2r. If 0<r<2, the sum is lr, and l≤1+log_2(2^l/r). Otherwise let h=⌊log_2 r⌋, so 1≤h≤l. Terms with j≤h sum to less than 2r, and the other l−h terms each equal r. Since h>log_2 r−1, their total is at most r[3+log_2(2^l/r)]. Finally use 2^l≤1/t. At r=0 both sides of (3) are interpreted as zero.

Let D=(δ,1/2) and M=∫_D r(t)dt≤1. Since log_2^+s≤ln(1+s)/ln2, (3) implies

\[
H_L\le2+3M+
\frac{1}{\ln2}\int_D r(t)\ln\left(1+\frac1{t r(t)}\right)dt.
\]

The integrand is defined to be zero when r=0, consistently with its limiting value. If M>0, Jensen's inequality for the probability measure r(t)dt/M gives

\[
\begin{aligned}
\int_Dr(t)\ln\left(1+\frac1{t r(t)}\right)dt
&\le M\ln\left(1+\frac1M\int_{D\cap\{r>0\}}\frac{dt}{t}\right)\\
&\le M\ln\left(1+\frac{(L-1)\ln2}{M}\right)\\
&\le \ln(1+(L-1)\ln2).
\end{aligned}
\]

The final inequality uses the fact that M↦M ln(1+B/M) is increasing for B≥0, which follows from ln(1+s)≥s/(1+s). For M=0 the integral is zero. Therefore

\[
H_L\le5+\log_2(1+(L-1)\ln2)
\le5+\log_2(1+L\ln2).
\]

Together with tbtgap=L this proves the claimed divergent lower bound on the ratio. H_L is positive: for example, independent Bernoulli variables give a strictly smaller expectation than the concave envelope because every monomial has at least two nonconstant factors.

## Equivalent universal coupling guarantee

The upper-bound distributions depend on the prescribed marginals and the degree allowance, but not on the polynomial coefficients or its monomial list. Consequently, for every x and d, one joint Bernoulli distribution with E X=x simultaneously satisfies, for every subset e with 2≤|e|≤d,

\[
\mathbb P(X_i=1\text{ for all }i\in e)
\le (1-\alpha_d)\min_{i\in e}x_i
+\alpha_d\max\{0,\sum_{i\in e}x_i-|e|+1\},
\]

where the harmonic construction gives α_d=1/Z_d and Z_d∼ln d/ln ln d. Thus all intersection probabilities move a common guaranteed fraction of the way from their individual upper Fréchet bounds toward their individual lower bounds. No choice of a larger worst-case order is possible: multiply these inequalities by the positive coefficients of the dyadic construction and sum. Its exact gap ratio forces α_d≤(1+o(1))ln ln d/ln d. Therefore the best universal fraction is asymptotic to ln ln d/ln d.

This is a simultaneous statement about one common coupling, not a collection of separately optimized termwise distributions. It follows directly from the termwise estimates in the harmonic proof and the positive weighted lower construction, without requiring an algorithm for the exact convex envelope.

## Homogeneous positive polynomials

The counterexample can also have every monomial of the same degree. Its largest degree is d=2^{L-1}+1 and its smallest degree is two. Introduce d−2 padding variables and, for each degree-k monomial, multiply it by the first d−k padding variables. Every resulting monomial is multilinear of degree d and still has coefficient one.

At the point where all padding variables equal one, every feasible binary coupling fixes them at one almost surely. The convex-hull gap therefore equals the original one. Each monomial's envelope formulas on that face also reduce to the original formulas, so its term-by-term gap is unchanged. The exact ratio in (4) is preserved, while the variable count increases by only d−2=O(n). The number of monomials stays linear, but their total variable occurrences become O(n²) after padding; the original O(n log n) incidence bound belongs to the nonhomogeneous construction.

This homogeneous extension uses a face of the larger unit box. If a strictly interior point is required, move all padding coordinates sufficiently close to one. The relevant envelopes are finite piecewise-linear functions on the cube and hence continuous there, while the original hull gap is positive. Thus each finite example's ratio can be made arbitrarily close to (4) at interior points. This continuity statement does not claim the exact formula away from the face.

The [coefficient-removal lemma](positive-multilinear-coefficient-removal.md) gives a stronger statement when dimension is unrestricted: for every fixed degree allowance d, its worst-case supremum is unchanged by simultaneously requiring unit coefficients, homogeneous degree d, and strictly interior evaluation points. The proof uses exact envelope preservation under variable cloning followed by random monomial sampling. It does not preserve a fixed number of variables or assert a small explicit sampled polynomial.

## Exact computational checks

`code/multilinear_ratio/dyadic_exact.py` verifies the explicit coupling and upper certificate with rational arithmetic for L=2,...,12. It checks anchor marginals, E R=1, simultaneous block-hit counts, XOR leaf marginal counts (exhaustively through L=6), every integer failure count in the pointwise upper bound, and equality of the attained and certified hull gaps. All checks pass. The independent first audit, `notes/review-positive-multilinear.md`, additionally reports solving the full binary-vertex envelope LPs at L=2 and L=3 and reconstructing exact primal and dual certificates. That was a review-time check; its code and certificate vectors were not archived, so it cannot be replayed from repository artifacts. A new independent reproduction, written from the review's description on 2026-09-25, is [`code/multilinear_review_repro/dyadic_full_vertex_lp.py`](../code/multilinear_review_repro/dyadic_full_vertex_lp.py). It solves the convex- and concave-envelope LPs over all 64 and 2048 binary vertices with Gurobi, rebuilds exact rational primal and dual certificates from the optimal bases, and checks them exactly. It also checks the defect identity and `N_j<=min(2^j,R)` at every vertex. It reproduces the review's values: convex envelope 1/2 and 1, concave envelope 2 and 3, hull gap 3/2 and 2, and ratio 4/3 and 3/2 for L=2 and L=3; see [the log](../code/multilinear_review_repro/dyadic_full_vertex_lp-2026-09-25.log).

| L | Variables n | Monomials | Exact hull gap | Exact ratio |
|---:|---:|---:|---:|---:|
| 3 | 11 | 14 | 2 | 3/2 |
| 6 | 70 | 126 | 3 | 2 |
| 7 | 135 | 254 | 13/4 | 28/13 |
| 10 | 1034 | 2046 | 31/8 | 80/31 |
| 12 | 4108 | 8190 | 33/8 | 32/11 |

## Supplementary dense model and numerical checks

The initial discovery used a dense symmetric variant:

\[
\widetilde f_L(a,z)=\sum_{j=1}^L\frac1{u_j\binom m{k_j}}
\sum_{|K|=k_j}a_j\prod_{i\in K}z_i.
\]

It has the same term-by-term gap L. Given R failed leaves, the normalized level gap is A_j g_j(R)/u_j, where

\[
g_j(r)=1-\binom{m-r}{k_j}/\binom m{k_j}\le\min\{1,u_jr\}.
\]

Its exact hull gap therefore satisfies the same upper bound. Unlike the sparse block model, this dense model admits an exact LP over the failure-count distribution alone: conditional on R, choose the failed leaves uniformly. `code/multilinear_ratio/multiscale_counterexample.py` solves this LP in floating point, with variables p_r=P(R=r) and z_{jr}=P(A_j=1,R=r), constraints z_{jr}≤p_r, ∑_rp_r=1, ∑_rrp_r=1, ∑_rz_{jr}=u_j, and objective ∑_{j,r}z_{jr}g_j(r)/u_j.

The following numerical values concern only the dense symmetric model. They are not claimed to be the hull gaps of the sparse block construction. The proof of unboundedness for both models is analytic and independent of these values.

| L | Variables n | Dense-model hull gap (floating point) | Ratio L/H_L |
|---:|---:|---:|---:|
| 5 | 37 | 2.4691810344 | 2.0249629049 |
| 8 | 264 | 3.0179569701 | 2.6507998885 |
| 10 | 1034 | 3.3127642317 | 3.0186271345 |
| 13 | 8205 | 3.6782006438 | 3.5343368291 |

The sparse construction removes the original model's large monomial count and small coefficients. Its degree is unbounded and its marginals approach the boundary. The companion `results/positive-multilinear-sharp-degree-growth.md` proves the matching asymptotic upper bound, with leading constant one, in maximum degree and dimension. Fixed degree therefore gives a dimension-independent bound. Exact finite-degree worst ratios and lower-order asymptotics remain unresolved.
