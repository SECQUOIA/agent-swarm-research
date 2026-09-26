# A logarithmic degree bound for positive multilinear relaxation gaps

Date: 2026-09-04. Status: proof independently checked by two agents; no mathematical issue identified. See `notes/review-positive-multilinear-upper.md` and `notes/review-positive-multilinear-upper-second.md` for review records. Companion to `results/positive-multilinear-gap.md`. This simpler O(log d) proof is retained as a preliminary result; the stronger `results/positive-multilinear-sharp-degree-growth.md` determines the sharp asymptotic growth ln d/ln ln d with leading constant one.

## Statement

Let f(x)=Σ_e a_e∏_{i∈e}x_i be multilinear on [0,1]^n, with a_e≥0 and maximum monomial degree d≥2. Affine terms can be removed because they change neither gap. Put

\[
K=1+\lfloor\log_2(d-1)\rfloor,\qquad c=1-e^{-1}.
\]

At every x∈[0,1]^n,

\[
\operatorname{tbtgap}_f(x)
\le \frac{2(K+1)}{c}\operatorname{chgap}_f(x).
\tag{1}
\]

The same bound holds on every nonnegative box, as shown below. Thus the degree-dependent worst ratio is O(log d). The sparse dyadic counterexamples establish a lower bound Ω(log d/log log d). This theorem is an upper bound on relaxation strength, not a polynomial-time algorithm for the exact convex envelope. The proof constructs O(log d) explicit vertex distributions with the specified means.

## The deficiency representation

For each monomial e choose r(e) with minimum coordinate u_e=x_{r(e)}. Put

\[
T_e=\min\left\{u_e,\sum_{j\in e\setminus\{r(e)\}}(1-x_j)\right\}.
\]

This equals its term-by-term gap. For a binary random vector X with E X=x define its monomial deficiency by

\[
D_e(X)=X_{r(e)}1\{X_j=0\text{ for at least one }j\in e\setminus\{r(e)\}\}.
\]

Then E D_e=u_e−E∏_{i∈e}X_i≥0, and

\[
\operatorname{tbtgap}_f(x)=\sum_ea_e T_e,\qquad
\operatorname{chgap}_f(x)=\max_{E X=x}E\sum_ea_eD_e(X).
\tag{2}
\]

The latter equality follows from the positive-coefficient concave-envelope formula and the vertex-distribution characterization of the convex envelope.

## Independent rounding handles two classes of terms

Call a coordinate low if x_i≤1/2, and high otherwise. Terms with at least two low coordinates have independent-rounding deficiency

\[
u_e\left(1-\prod_{j\ne r(e)}x_j\right)\ge u_e/2\ge T_e/2.
\]

For terms with all coordinates high, u_e>1/2. Write S_e=Σ_{j≠r(e)}(1−x_j). Independence, 1−y≤e^{-y}, and 1−e^{-s}≥c min{1,s} imply

\[
u_e\left(1-\prod_{j\ne r(e)}x_j\right)
\ge c u_e\min\{1,S_e\}
\ge(c/2)T_e.
\]

Consequently the independent distribution supplies at least (c/2)T_e for every term except those with exactly one low coordinate. All terms have nonnegative deficiencies in every distribution, so no loss must be subtracted for terms outside these classes.

## Couplings at dyadic scales

For each B∈{1,2,4,...,2^{K-1}}, construct a random binary vector as follows. Draw U uniformly on (0,1).

- For every low coordinate, set X_i=1[U≤x_i].
- For every high coordinate, put y_i=1−x_i and h_i=min{B y_i,1}. If y_i=0, set X_i=1. Otherwise, conditional on U, let X_i fail independently of the other high coordinates with probability y_i/h_i when U≤h_i and with probability zero otherwise.

All marginals are correct: low coordinates are immediate; for high coordinates the failure probability is h_i(y_i/h_i)=y_i. The conditional probabilities lie in [0,1] because B≥1.

Consider a term with exactly one low coordinate, its anchor, with marginal u≤1/2. For the other r=|e|−1≤d−1 coordinates, let their failure probabilities be y_1,...,y_r, and set

\[
N(s)=|\{j:y_j\ge s\}|,\qquad S=\sum_jy_j.
\]

For U≤u, every index with B y_j≥U has conditional failure probability at least 1/B. This is equality when B y_j≤1; if B y_j>1 its conditional failure probability is y_j>1/B. The high coordinates fail independently given U. Hence the expected deficiency G_B for this term satisfies

\[
\begin{aligned}
G_B
&\ge\int_0^u\left[1-(1-1/B)^{N(t/B)}\right]dt\\
&\ge c\int_0^u\min\{1,N(t/B)/B\}\,dt\\
&=c\int_0^{u/B}\min\{B,N(s)\}\,ds.
\end{aligned}
\tag{3}
\]

When N=0, the integrand is zero, including the B=1 case.

For 0<s≤u with N(s)>0, choose the largest power of two B≤min{N(s),u/s}. It belongs to the chosen scale set because N(s)≤r≤d−1. This B is greater than half of min{N(s),u/s}; it also satisfies s≤u/B and B≤N(s). Therefore

\[
\sum_B1\{s\le u/B\}\min\{B,N(s)\}
\ge\frac12\min\{N(s),u/s\}.
\tag{4}
\]

The inequality is trivial when N(s)=0. Combining (3) and (4),

\[
\sum_BG_B\ge\frac c2\int_0^u\min\{N(s),u/s\}\,ds.
\tag{5}
\]

## A tail-integral lemma

The nonincreasing function N satisfies

\[
\int_0^u\min\{N(s),u/s\}\,ds\ge\min\{u,S\}.
\tag{6}
\]

If S≤u, every y_j≤u and ∫_0^uN(s)ds=S. Since sN(s)≤∫_0^sN(t)dt≤S≤u, the integrand in (6) equals N(s) throughout, proving equality.

If S>u, then ∫_0^uN(s)ds≥u: this is immediate if some y_j≥u, and otherwise this integral equals S. By continuity of the integral, choose v≤u with ∫_0^vN(s)ds=u. For every s≤v, monotonicity gives sN(s)≤∫_0^sN(t)dt≤u. Thus the integrand equals N(s) on (0,v), whose integral is u. This proves (6). The case u=0 has T_e=0 and needs no division or integral argument.

Equations (5)–(6) show that the sum of the K dyadic-distribution deficiencies for every one-low-coordinate term is at least (c/2)T_e.

## Finishing the bound

Take the uniform mixture of the independent distribution and the K dyadic distributions. It has mean x. For every monomial, the sum of its deficiencies across these K+1 distributions is at least (c/2)T_e, using independence for terms with zero or at least two low coordinates, and dyadic scales for terms with exactly one low coordinate. Every omitted contribution is nonnegative. Multiply by a_e, sum over terms, and divide by K+1. Equation (2) yields

\[
\operatorname{chgap}_f(x)\ge\frac{c}{2(K+1)}\operatorname{tbtgap}_f(x),
\]

which is (1).

## Extension to every nonnegative box

Let the domain be [ℓ,v] with 0≤ℓ≤v. First fix coordinates with v_i=ℓ_i; substituting their nonnegative values preserves nonnegative coefficients and does not increase the degree. Scale each remaining coordinate by x_i=ℓ_i+(v_i−ℓ_i)t_i, t_i∈[0,1]. Every original monomial becomes a sum of monomials in t with nonnegative coefficients and degree at most d.

For any decomposition g=∑_kh_k on a common domain,

\[
\operatorname{cav}g\le\sum_k\operatorname{cav}h_k,
\qquad
\operatorname{vex}g\ge\sum_k\operatorname{vex}h_k.
\]

Indeed, the right sides are respectively a concave majorant and a convex minorant of g. Therefore the hull gap of each original monomial is no greater than the sum of hull gaps of its expanded monomials. Summing this inequality over original monomials shows that the original term-by-term gap is no larger than the term-by-term gap after expansion. The convex-hull gap of the complete polynomial is invariant under the affine change of variables. Applying (1) to the expanded polynomial proves the same bound for the original term-by-term relaxation on [ℓ,v]. If only affine terms remain after substitution, both gaps are zero.

## Follow-up

The leading constant is not optimized. The exact degree-two bound is much better than (1). The stronger harmonic-coupling argument in `results/positive-multilinear-sharp-degree-growth.md` closes the asymptotic gap, including its leading constant. A source review is recorded in `notes/positive-multilinear-novelty.md`; the review of this new logarithmic upper bound should be distinguished from the reviewed counterexample itself.
