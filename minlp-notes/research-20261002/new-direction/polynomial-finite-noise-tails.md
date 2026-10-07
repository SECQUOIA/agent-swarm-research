# Finite-noise growth and active-gradient tails for polynomial mixed boxes

Date: 2026-10-02. Status: passed
[fresh independent review](../reviews/polynomial-finite-noise-tails-review.md).
The quantifier bound below was independently checked in the primary source. This note
supplies a finite-law interface; it does not by itself prove an expected
optimization bound or an exact-output theorem.
An [independent source audit](polynomial-growth-section-audit.md) also
checks the section count against the Basu--Pollack--Roy theorem.

## 1. Model and conclusions

Let `X` be a nonempty bounded rational product box with continuous and
native integer coordinates. Round integer endpoints inward and substitute
fixed coordinates. Let `n>=1` remain, of which `n_c` are continuous, and
write `N_j` for the number of labels of integer coordinate `j`. Set

\[
 R_Z=\prod_{j\in Z}N_j,\qquad
 S=\sum_{i=1}^n\operatorname{width}(X_i)>0.
 \tag{1}
\]

An empty product is one. The base objective `F` is an explicit rational
polynomial, or a sum of explicit rational polynomial factors, of fixed
total degree at most `d`. Let `I_0` count this input, the box, any supplied
decomposition, and a rational noise half-width `sigma>0`. Fixed deterministic
linear offsets can be included in `F`. Sampling precision is not part of
`I_0`. No sparsity assumption is needed for the tail lemmas.

Perturb the objective to `F_gamma(x)=F(x)+gamma'x`. Define `g_*(gamma)`
as the largest nonnegative point-growth constant at a single optimizer,
and set it to zero when distinct optimizers exist. Thus for `epsilon>0`,

\[
 g_*(\gamma)\ge\varepsilon
 \quad\Longleftrightarrow\quad
 \exists x\in X\ \forall y\in X:\quad
 F_\gamma(y)-F_\gamma(x)\ge\varepsilon\|y-x\|^2.
 \tag{2}
\]

Compactness makes this equivalence valid also at equality in the threshold.
It is point growth, not growth measured by distance to the whole minimizer
set: the latter can remain positive in the presence of ties.

There is a base-computable bound `C=2^{poly(I_0)}`, independent of noise
coefficient heights and of every threshold, such that independent uniform
sampling on the `M` equally spaced rational points of `[-sigma,sigma]`
satisfies, on the same grid for every `epsilon>0`,

\[
 \Pr\{g_*<\varepsilon\}
 \le \frac{S\varepsilon}{\sigma}+\frac{2nC}{M}.
 \tag{3}
\]

Define

\[
 D=\max\{1,d-1\},\qquad
 K=n_c3^{n_c}R_ZD^{n_c}.
 \tag{4}
\]

For `tau>0`, the probability that `g_*>0` and the unique optimizer has
some active continuous coordinate with absolute objective gradient at most
`tau` is at most

\[
                  K\left(\frac{\tau}{\sigma}+\frac1M\right).
 \tag{5}
\]

For `n_c=0`, this event is empty and `K=0`. Equations (3)--(5) include
finite-grid atoms at ties and zero active gradients; no almost-sure
genericity assertion is substituted for their probability bounds.

## 2. Two quantified blocks give a uniform scalar-section bound

Fix all noise coefficients except one, denoted by the free scalar `t`.
For a real vector `z`, describe membership in the mixed box by the
quantifier-free formula

\[
 \mathcal D(z)=
 \bigwedge_{i\in C}\{\ell_i\le z_i\le u_i\}
 \ \wedge\!
 \bigwedge_{j\in Z}\ \bigvee_{k=\ell_j}^{u_j}\{z_j=k\}.
 \tag{6}
\]

This is a conceptual finite description, not a label-enumeration step
of the sampler. Its length and number of polynomial atoms are at most
`O(n+sum_j N_j)`, whose logarithm is polynomial in the binary input.
In particular, integer labels do not create additional quantifier blocks.

The good-growth set is defined exactly by

\[
 \exists x\in\mathbb R^n\ \forall y\in\mathbb R^n:
 \mathcal D(x)\ \wedge
 \left[\neg\mathcal D(y)\ \vee
 \left\{F_t(y)-F_t(x)-\varepsilon\|y-x\|^2\ge0\right\}\right].
 \tag{7}
\]

The positive-growth inequality already proves that `x` is the unique
optimizer, so neither a separate optimum-value variable nor another
quantifier block is needed. Formula (7) has two blocks of `n` variables,
one free scalar, at most

\[
 s_0=4n+2\sum_{j\in Z}N_j+2
 \quad\hbox{polynomial atoms, of degree at most}\quad
 d_0=\max\{d,2\}.
 \tag{8}
\]

Degree is measured jointly in `t,x,y`; the term `t(y_i-x_i)` has degree
two. The threshold and all other fixed noise coefficients are real
coefficients. Their sizes do not enter a degree or atom-count bound.

Renegar's primary quantifier-elimination theorem gives a quantifier-free
disjunctive-normal-form output whose number of disjuncts, number of atoms
per disjunct, and degrees are each bounded by

\[
 (s_0d_0)^{2^{O(\omega)}\ell\prod_b n_b}.
 \tag{9}
\]

Here `omega` is the number of blocks, `ell` the number of free variables,
and `n_b` their sizes. See Theorem 1.1, printed page 330, in the
[primary paper](../../literature/papers/renegar1992-on-the-computational-complexity-and/original.pdf).
The theorem applies over real coefficients, so this counting statement
also holds when some fixed noise coordinates come from continuous
distributions during a hybrid comparison. Its dependence on block count
is material: an unrestricted doubly exponential CAD bound would not
supply the sampling precision claimed here.

In (7), `omega=2`, `ell=1`, and both `n_b=n`. Fix once an effective
universal constant `a` large enough for the chosen elimination algorithm's
bounds, and put

\[
 H=(s_0d_0)^{a(n+1)^2},\qquad C=2H^3+1.
 \tag{10}
\]

Equivalently, any explicit coarse upper bound from that fixed algorithm
may be used instead. The sampler computes this bound from the base counts;
it does not run quantifier elimination on the sampled objective.

There are at most `H^2` output polynomial occurrences, each of degree at
most `H`. Discard identically zero polynomials, whose signs are constant.
All remaining real roots number at most `H^3`. Every Boolean combination
of their signs is constant on the intervening open intervals and at
each separate root. Thus both (7) and its complement have at most `C`
interval or point components. This bound is uniform in all fixed noise
values and every positive threshold, including special values at which
polynomials vanish identically or stationary sets become singular.
Since `log s_0=poly(I_0)` and `d` is fixed, `log C=poly(I_0)`.

For completeness, the graph of the best objective value has the same
coarse complexity. Use free variables `(t,z)` and the two-block formula

\[
 \exists x\ \forall y:\quad
 \mathcal D(x)\wedge F_t(x)=z\wedge
 [\neg\mathcal D(y)\vee F_t(y)\ge z].
 \tag{11}
\]

Taking `ell=2` in (9) still gives exponential-in-polynomial base format
size. This graph statement does not represent every optimizer by a finite
list of stationary points, and remains valid with positive-dimensional
minimizer sets.

## 3. Transfer of the sharp growth tail to one fixed finite law

The reviewed [proximal growth theorem](proximal-growth-tail.md) applies
to every continuous objective on compact `X`. For independent continuous
uniform coefficients in `[-sigma,sigma]`, it gives

\[
                  \Pr\{g_*<\varepsilon\}
                         \le S\varepsilon/\sigma.
 \tag{12}
\]

The empirical CDF of the endpoint-inclusive `M`-point uniform grid differs
from the continuous uniform CDF by at most `1/M`. An interval or singleton,
with any endpoint convention, therefore has probability discrepancy at
most `2/M`; a union of at most `C` such pieces has discrepancy at most
`2C/M`.

Replace the continuous coordinate marginals by discrete ones successively.
At each step condition on every other coordinate. Section 2 bounds every
such scalar section, including sections with an arbitrary mixture of
fixed continuous and discrete coefficients. Independence preserves the
two marginal laws being compared. Summing these `n` discrepancies proves
(3). It is not enough to bound only sections encountered under the
all-continuous product measure.

Because `C` is threshold independent, decreasing thresholds from above
also gives (3) with `g_*<=epsilon` in place of `g_*<epsilon`, and

\[
                     \Pr\{g_*=0\}\le 2nC/M.
 \tag{13}
\]

This last event includes all nonunique optima and every zero-growth
unique optimum. The proof does not need to classify either type.

## 4. Active-gradient tails without finite stationary-set assumptions

Fix an integer assignment, a face of the original continuous box, and
an active coordinate `i` of that face. Let `u` be its `k` free continuous
coordinates. After conditioning on all noise except `gamma_i`, the free
stationarity equations are

\[
                         \nabla_u F(u,x_{-u})+\gamma_u=0.
 \tag{14}
\]

The fixed active coordinate makes (14) independent of `gamma_i`.
Each equation has degree at most `D=max(1,d-1)`, including constant
equations when `d=0`. Count only roots at which the
Jacobian of (14), the free Hessian, is nonsingular. Such a root is
isolated over the complex numbers. The isolated-root form of the
standard affine Bezout bound gives at most `D^k` such roots, even when
other components of the stationary equations have positive dimension.
For `k=0`, the empty system contributes one candidate. If degree is
at most one and `k>0`, no free Hessian is nonsingular, so the same safe
bound holds.

For each counted real root, the active gradient equals `gamma_i+b` for
a fixed real `b`. Its absolute value is at most `tau` only on an interval
of length `2tau`. That interval contains at most
`tau(M-1)/sigma+1` grid labels, yielding conditional probability at
most `tau/sigma+1/M`. Root locations may be irrational; this interval
count uses neither their representation nor their computation.

At an optimizer with `g_*>0`, take its smallest original continuous face
and fix its integer labels. Two-sided free directions in (2) show that
the free Hessian is at least `2g_* I`. Therefore its root is among those
counted. There are at most `R_Z` integer assignments, `3^{n_c}` faces,
and `n_c` choices of an active coordinate. Union bounding the preceding
conditional estimate proves (5), with (4).

This argument does not say that all stationary roots are isolated, that
all minimizers have a nonsingular Hessian, or that degeneracies have zero
probability under finite noise. It only needs nonsingularity at an
optimizer already covered by positive point growth. The zero-growth
draws are separately charged to (3).

## 5. A polynomial-bit rare-event budget

Let `B>=2` be any base-computable positive integer bound with
`log B=poly(I_0)`. It may be a
combinatorial factor for a separately proved all-draw fallback, but no
fallback theorem is asserted here. Put `K_+=max(1,K)` and choose

\[
 g_0=\frac{\sigma}{3SB},\qquad
 \tau=\frac{\sigma}{3K_+B},\qquad
 M\ge3B(2nC+K),
 \tag{15}
\]

with `M` a power of two. If there are no continuous coordinates, omit
the gradient condition. Equations (3) and (5) imply

\[
 \Pr\{g_*<g_0\ \hbox{or some optimizer active gradient has
 magnitude at most }\tau\}\le1/B,
 \tag{16}
\]

where the second event is needed only on `g_*>=g_0`. Outside the displayed
bad event, the optimizer is unique. Both threshold reciprocals and `M` have polynomial
bit length in the base input. Their selection is independent of the
sample and of its coefficient height. A sampled coefficient is exactly

\[
             -\sigma+2\sigma k/(M-1),\qquad 0\le k<M,
 \tag{17}
\]

so it uses `log_2 M=poly(I_0)` random bits and polynomial rational
encoding length.

These facts remove the finite-atom and sampling-precision obstacle for
a prospective sparse polynomial smoothed algorithm. To deduce polynomial
expected exact work, one must still prove the good-draw closure/work
bound and an all-draw exact fallback with cost
`B poly(I_0+log M)` and an explicit output representation. A mere
almost-sure termination argument, a doubly exponential fallback whose
logarithm is exponential, or an expanded algebraic-output assumption
does not follow from these tails.

## 6. Verification and attribution

The source check read Renegar's local full text and rendered the primary
PDF's printed page 330 to inspect Theorem 1.1's formulas omitted by text
extraction. The probability arguments are direct consequences of that
block-sensitive bound, the reviewed proximal tail, elementary grid
discrepancy, and the nonsingular-root count. No new literature was ingested,
no external search was performed, and no index was edited. The fresh
actual-file review independently rendered the primary theorem and checked
all probability and counting arguments. It found no substantive gap;
its minor degree-zero wording correction is included. A scoped Python document check passed for
local links, whitespace, paired math delimiters, and the 17 sequential
equation tags. No numerical optimization test or project-wide check was
run. No priority claim is made.
