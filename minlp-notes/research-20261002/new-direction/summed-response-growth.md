# Summing response slopes improves the dimension dependence of random-tilt growth

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/summed-response-growth-adversary.md)
with no substantive mathematical gap found.
This is a quantitative strengthening of
[`smoothed-linear-growth.md`](smoothed-linear-growth.md), using the same
optimizer responses and weak maximal-slope bound. It concerns the perturbed
objective and gives high-probability bounds, not expected solver work.
No literature-priority claim is made.

## 1. Statement

Let \(f\) be continuous on a nonempty compact set \(X\subseteq\mathbb R^n\),
and perturb its linear coefficients independently. Remove constant
coordinates; if none remain, \(X\) is a singleton. Write

\[
w_i=\max_{x\in X}x_i-\min_{x\in X}x_i>0.
\]

For continuous perturbations whose densities are bounded by \(\phi_i\),
define

\[
a_i=6w_i\phi_i,\qquad A=\sum_{i=1}^n a_i.
\tag{1}
\]

For every \(0<\rho<1\), with probability at least \(1-\rho\) the
perturbed objective has a unique global optimizer and global quadratic
growth constant

\[
\boxed{g\ge\frac{\rho}{8A[1+\log(2n/\rho)]}.}
\tag{2}
\]

All logarithms here are natural. The response slopes are generally
dependent; the argument does not require their independence.

For rational QPs in any of the boxes or bounded polytopes covered by the
earlier note, uniform rational-grid perturbations of half-width \(\sigma\)
give the finite-bit version

\[
\boxed{g\ge
\frac{\rho\sigma}
 {24(\sum_iw_i)[2+\log(4n/\rho)]}}
\tag{3}
\]

with probability at least \(1-\rho\). The sampling grid needs only twice
the earlier sufficient number of points. Thus, if \(w_i\le W\), the
denominator scales as \(nW\log(n/\rho)\), replacing the earlier
\(n^2W\) bound. Polynomial-bit sampling and the earlier solver
consequences remain valid.

## 2. The deterministic summed-slope inequality

At the realized coefficient vector \(c\), let \(u_i(t)\) be the largest
coordinate \(i\) among minimizers when only that coefficient is replaced
by \(t\). Put

\[
Z_i=\sup_{t\ne c_i}
       \frac{|u_i(t)-u_i(c_i)|}{|t-c_i|}.
\tag{4}
\]

If every \(Z_i\) is finite, the earlier argument proves uniqueness of
the optimizer \(x^*\). For every \(K_i>Z_i\), its scalar tilt comparison
also proves, for every \(x\in X\),

\[
(x_i-x_i^*)^2\le4K_i\,[F_c(x)-F_c(x^*)].
\]

Letting \(K_i\downarrow Z_i\) handles zero slopes without dividing by
them. Summing gives

\[
\boxed{\|x-x^*\|^2\le
4\,[F_c(x)-F_c(x^*)]\sum_iZ_i.}
\tag{5}
\]

If the sum were zero, this would force every point of \(X\) to equal
\(x^*\). For the nonconstant domain under consideration it is positive.
Hence \(1/(4\sum_iZ_i)\) is a valid global growth constant.

This uses the actual slope in each coordinate. Bounding every slope by
one threshold and then multiplying by \(n\) loses an additional factor
that can be avoided by estimating their sum.

## 3. Continuous tails and truncation

The safe weak bound in the earlier note, with coordinate range \(w_i\),
is

\[
\bigl|\{t:Z_i(t)>s\}\bigr|\le6w_i/s.
\]

Condition on all other coefficients and use the density bound. After
averaging over those coefficients,

\[
\Pr(Z_i>s)\le\min\{1,a_i/s\}.
\tag{6}
\]

In particular every \(Z_i\) is finite almost surely. Let
\(T=2A/\rho\). A union bound gives

\[
\Pr\{\max_iZ_i>T\}\le A/T=\rho/2.
\tag{7}
\]

Since \(T>a_i\), integration of the tail yields

\[
\mathbb E\min\{Z_i,T\}
 \le a_i[1+\log(T/a_i)].
\]

Writing \(p_i=a_i/A\) and using
\(-\sum_ip_i\log p_i\le\log n\), obtain

\[
\begin{aligned}
\mathbb E\sum_i\min\{Z_i,T\}
&\le A[1+\log(T/A)-\sum_ip_i\log p_i]\\
&\le A[1+\log(2n/\rho)].
\end{aligned}
\tag{8}
\]

Markov's inequality bounds the probability that the truncated sum exceeds
\(2A[1+\log(2n/\rho)]/\rho\) by \(\rho/2\). Outside that event and
(7), the original sum equals the truncated sum. Equation (5) proves (2).
No joint-distribution assumption about the \(Z_i\) was used.

For uniform continuous noise on \([-\sigma,\sigma]\),
\(a_i=3w_i/\sigma\), so (2) becomes

\[
g\ge\frac{\rho\sigma}
 {24(\sum_iw_i)[1+\log(2n/\rho)]}.
\tag{9}
\]

## 4. Finite rational grids, including atoms

For coordinate \(i\), use \(M_i\) equally spaced points in
\([-\sigma_i,\sigma_i]\), including both endpoints, with
\(\sigma_i>0\) rational. Suppose \(B_i\) is a deterministic bound on
the number of affine response pieces, uniform over all values of the
other coefficients. The earlier quadratic-face argument supplies exactly
such bounds. Its bad-set component and grid-count lemmas give

\[
\Pr(Z_i>s)\le\min\{1,a_i/s\}+\beta_i,
\quad a_i=\frac{3w_i}{\sigma_i},\quad
\beta_i=\frac{4B_i^2}{M_i}.
\tag{10}
\]

Indeed, before clipping the probability at one, the length term is
\(3w_i/(\sigma_i s)\) and the component term is \(4B_i^2/M_i\).
The inequality
\(\min\{1,v+\beta\}\le\min\{1,v\}+\beta\)
justifies the displayed form. The additive term can include an atom
\(Z_i=+\infty\), caused by a tie at a sampled coefficient.

Set \(A=\sum_i a_i\), and choose powers of two satisfying

\[
M_i\ge\frac{16nB_i^2}{\rho},\qquad
\beta:=\sum_i\beta_i\le\rho/4.
\tag{11}
\]

Take \(T=4A/\rho\). Then

\[
\Pr\{\max_iZ_i>T\}\le A/T+\beta\le\rho/2.
\tag{12}
\]

Integrating (10), including its constant term, gives

\[
\begin{aligned}
\mathbb E\sum_i\min\{Z_i,T\}
&\le\sum_i a_i[1+\log(T/a_i)]+\beta T\\
&\le A[2+\log(4n/\rho)].
\end{aligned}
\tag{13}
\]

The term \(\beta T\le A\) is necessary; dropping it would ignore
the grid atoms. Markov's inequality and (12) now give, with probability
at least \(1-\rho\), finite slopes and

\[
\sum_iZ_i\le\frac{2A[2+\log(4n/\rho)]}{\rho},
\qquad
g\ge\frac{\rho}{8A[2+\log(4n/\rho)]}.
\tag{14}
\]

For common \(\sigma_i=\sigma\), this is (3).

For a common face-candidate bound \(F\), the earlier note permits
\(B_i=B=(F+1)^2\) for every coordinate. The choices are
\(F=3^n\) for a continuous box,
\(F=3^{n_c}\prod_jN_j\) for a mixed box, and \(F=2^m\) for a bounded
polytope with \(m\) inequalities. A common power-of-two grid size
\(M\ge16nB^2/\rho\) therefore suffices. Compared with the earlier
\(8nB^2/\rho\) bound, this adds at most one random bit per coordinate
when choosing the least sufficient power of two. Faces and grid points
are not enumerated.

For algorithmic inputs take rational \(\rho\). A fully rational lower
bound can replace \(2+\log(4n/\rho)\) by
\(2+\lceil\log_2(4n/\rho)\rceil\); integer comparisons compute this
quantity. The optimizer algorithms themselves do not need the growth
constant. The new estimate improves their high-probability numerical
parameter bounds, without changing their scope or establishing expected
polynomial work.

## 5. A linear example: necessary dimension scale and a logarithmic loss

Take \(X=[-1,1]^n\), \(f=0\), and independent
\(b_i\sim\operatorname{Unif}[-\sigma,\sigma]\). The largest valid
global growth constant is exactly

\[
g_*=\tfrac12\min_i|b_i|.
\tag{15}
\]

To see this, the coordinate displacement from the optimal endpoint is
\(d_i\in[0,2]\), and the objective gap is \(\sum_i|b_i|d_i\).
Since \(d_i\ge d_i^2/2\), (15) is valid. Moving only a least-cost
coordinate to its opposite endpoint attains equality.

Its exact distribution is

\[
\Pr(g_*\le t)=1-(1-2t/\sigma)^n,
\qquad 0\le t\le\sigma/2.
\tag{16}
\]

Thus the lower quantile holding with probability \(1-\rho\) is

\[
q_\rho=\frac\sigma2[1-(1-\rho)^{1/n}],\qquad
\frac{\sigma\rho}{2n}\le q_\rho
\le\frac{\sigma[-\log(1-\rho)]}{2n}.
\tag{17}
\]

For fixed failure probability the scale is \(\sigma/n\); for small
\(\rho\) it is \(\sigma\rho/n\). The linear dependence on dimension
and on the small failure probability is therefore necessary in a general
theorem. This example does not prove that the logarithm in (2) or (3)
is necessary.

The maximal response slopes are \(Z_i=2/|b_i|\). With
\(U_i=|b_i|/\sigma\) independent uniform variables on \([0,1]\),

\[
\sum_iZ_i=\frac2\sigma\sum_iU_i^{-1},\qquad
\frac{\sum_iZ_i}{(2n/\sigma)\log n}\longrightarrow1
\quad\hbox{in probability}.
\tag{18}
\]

For an elementary proof, truncate \(U_i^{-1}\) at
\(T=n\log n\). The probability that any term exceeds \(T\) is at
most \(1/\log n\). Each truncated term has mean \(1+\log T\)
and second moment at most \(2T\); Chebyshev's inequality proves (18).
Consequently the deterministic certificate \(1/(4\sum_iZ_i)\) typically
loses a logarithm compared with the exact modulus (15). Removing the
logarithm from a general theorem would require more than a sharper
tail bound for this particular sum.

## 6. Why this still does not prove expected solver work

In the same linear example,

\[
\mathbb E(g_*^{-a})=+\infty\qquad(a\ge1),
\tag{19}
\]

because the density of \(\min_i|b_i|\) is positive near zero.
Therefore integrating a generic work bound proportional to a higher
inverse power of growth cannot establish an expected polynomial bound.

In this linear example, even rational grids remove the divergence but
need not make the bound useful. With an even number \(M\) of grid points,
zero is absent, and
\(|b_i|\) is uniform on

\[
\left\{\frac{\sigma(2j-1)}{M-1}:j=1,\ldots,M/2\right\}.
\]

For fixed \(n\), summing these finite probabilities gives
\(\mathbb E(g_*^{-1})=\Theta_n(\sigma^{-1}\log M)\), while for
\(a>1\),
\(\mathbb E(g_*^{-a})=\Theta_{n,a}(\sigma^{-a}M^{a-1})\).
Thus inverse-growth moments can be exponential in the number of sampling
bits even though every sample is rational. General rational-grid QPs
can still have tie atoms and zero growth, as allowed in Section 4.

These are limitations of a condition-based expected-work argument, not
algorithmic lower bounds. The linear example is solved immediately by
choosing coordinate endpoints. A stronger expected-work result would need
to analyze what the actual solver does near small-growth events, rather
than merely integrate its worst-case bound in \(1/g\).

## 7. Verification

The result uses the previously reviewed response and finite-component
lemmas, an independent derivation of the summed inequality, tail
integration, and elementary scalar examples. The fresh adversarial review
checked the actual note, including continuous and rational-grid constants,
the example's quantiles, the reciprocal-sum limit, and inverse moments.
Its clarification about general grid-QP tie atoms is included above.

The reviewer's targeted inline Python document check passed whitespace,
paired math delimiters, and local links. No executable optimization test,
project-wide check, CI inspection, or new literature search is claimed
for this derivation.
