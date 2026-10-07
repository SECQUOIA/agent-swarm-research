# A connected state-count barrier for global-error bag-cell retention

Date: 2026-10-02. Status: exact construction passed
[independent actual-file review](../reviews/global-error-cell-barrier-review.md)
against the retention and whole-hull closure rules in
[smoothed-sparse-polynomial.md](smoothed-sparse-polynomial.md), Sections
2--5, and its [mixed quadratic predecessor](sparse-bag-cell-smoothed-miqp.md).
This is a limitation of those specified rules, not an optimization hardness
result or a contradiction to their stated dimension-dependent bound.

There are connected degree-four instances with actual treewidth \(p-1\),
coordinate curvature \(L=2\), unit coordinate widths, and noise half-width
\(1/100\), on which every bag cell survives until the mesh reaches
order \(\sqrt{p/n}\). One bag then contains at least
\((5n/(6p))^{p/2}\) retained cells, for every noise draw. The current
whole-hull gradient and convex-patch tests cannot close earlier.

## 1. Objective and actual interaction graph

Let \(n\ge p\ge2\). Make vertices \(1,\ldots,p\) a clique, and, if
\(n>p\), attach the path
\(p,p+1,\ldots,n\) at its first vertex. Call this connected graph
\(G=(V,E)\). Its treewidth is exactly \(p-1\): the clique supplies the
lower bound, and a bag \(\{1,\ldots,p\}\) followed by the path-edge
bags supplies a decomposition of that width.

On \([0,1]^n\), set

\[
 \phi(t)=t^2(1-t)^2,\qquad
 \eta=\frac1{100n^2},\qquad \sigma=\frac1{100},
\]
\[
 F_\gamma(x)=\sum_{i=1}^n\phi(x_i)
       +\eta\sum_{\{i,k\}\in E}x_ix_k+\sum_i\gamma_i x_i,
       \qquad |\gamma_i|\le\sigma.                             \tag{1}
\]

Every graph edge has a nonzero coefficient, so this is the actual
interaction graph, not an artificially enlarged supplied bag. The base
input has \(O((n+p^2)\log(n+2))\) bits in an explicit factor encoding.

The coupling and noise have zero diagonal second derivatives, and

\[
 \partial_{ii}F_\gamma=\phi''(x_i)=2-12x_i(1-x_i)\le2.          \tag{2}
\]

Thus \(L=2\) is valid on the full continuous box, with the directly
checkable slack identity \(2-\phi''(x_i)=12x_i(1-x_i)\ge0\).
Using a larger verified constant only weakens the retention rule below.

Write \(P_\gamma\) for the multiaffine part of (1). Its minimum on the
box is attained at a vertex: independent Bernoulli rounding preserves its
expectation, so every value is at least its minimum vertex value. Since
\(\phi\ge0\) and vanishes at both endpoints,

\[
             \min_{[0,1]^n}F_\gamma
              =\min_{a\in\{0,1\}^n}P_\gamma(a)=f^*.            \tag{3}
\]

In fact every optimizer is a vertex, since any nonvertex has a strictly
positive quartic sum. No uniqueness or generic-noise assumption is used.

## 2. Every bag cell survives down to the stated mesh

The algorithm uses \(s=1\), \(h_j=2^{-j}\), and the global rounding
budget

\[
                          E_j=nh_j^2/4.                        \tag{4}
\]

At level zero the allowed grid contains all vertices. Its exact minimum
and feasible incumbent are therefore \(m_0=U_0=f^*\). As long as all
bag cells have survived, all current full-grid tuples are allowed, and
the same identity holds at the next level.

Fix one minimizing vertex \(a\) in (3). For any bag \(B\) and any one
of its grid corner tuples \(v\), complete it by \(y_B=v\) and
\(y_{-B}=a_{-B}\). While the whitelists are full, this is a globally
consistent allowed grid point. Since \(0\le\phi\le1/16\),

\[
 \begin{split}
 F_\gamma(y)-f^*
 &\le |B|(1/16+\sigma)+\eta|E|\\
 &\le \frac{29p}{400}+\frac1{200}
 \le\frac{3p}{40}.                                           \tag{5}
 \end{split}
\]

The edge bound uses \(|E|\le n(n-1)/2\); counting only incident edges
would be sharper but is unnecessary. The noise term changes only in \(B\).

For every candidate bag cell \(C\), its minimum corner min-marginal
therefore satisfies \(q_C\le f^*+3p/40\). The actual rule is

\[
                         q_C-E_j\le U_j.                       \tag{6}
\]

Whenever \(E_j\ge3p/40\), it retains every candidate cell. Induction
from the initial full boxes proves that **all cells in every bag** survive
at every level with

\[
                            h_j^2\ge\frac{3p}{10n}.             \tag{7}
\]

Let \(j_*\) be the last such dyadic level. It exists for \(n\ge p\),
and
\[
 \sqrt{\frac{3p}{10n}}\le h_{j_*}
              <2\sqrt{\frac{3p}{10n}}.
\]
The clique bag has exactly \(h_{j_*}^{-p}\) dyadic cells. Hence its
retained list has at least

\[
                         \left(\frac{5n}{6p}\right)^{p/2}       \tag{8}
\]

entries. Deduplicating corner rows does not repair this count: the full
clique row list has \((h_{j_*}^{-1}+1)^p\) distinct tuples.

The construction is pointwise in \(\gamma\). It applies to independent
continuous noise, to the specified finite rational law, and to every
individual coefficient vector in the noise box. Thus (8) also bounds the
expected number of retained states from below.

## 3. The specified closure rules cannot avoid these levels

Since every bag cell survives through \(j_*\), every coordinate
projection hull is \([0,1]\). Intersecting those hulls over containing
bags still gives the entire original box.

No whole-hull gradient-sign test can force an original bound, even using
the exact gradient range. Set all neighbors of coordinate \(i\) to zero
and evaluate at \(x_i=1/4\) and \(x_i=3/4\). The two derivatives are

\[
                           \gamma_i+3/16,
                   \qquad \gamma_i-3/16.                       \tag{9}
\]

They have opposite signs for every allowed \(\gamma_i\). In particular,
the sound midpoint interval used by the algorithm contains zero, so it
does not fix any coordinate.

At the hull midpoint \(c=(1/2,\ldots,1/2)\), the Hessian is

\[
                          \nabla^2F_\gamma(c)=-I+\eta A_G,      \tag{10}
\]

where \(A_G\) is the adjacency matrix. Its largest eigenvalue is at most
\(-1+\eta(n-1)<0\). It is negative definite. Consequently the stated
test
\(H(c)-(Tr+g_0)I\succ0\), for \(g_0>0\), fails throughout these
levels. There are no integer coordinates to fix, and no continuous
coordinates have been eliminated. More generally, a valid convexity
certificate for this whole hull cannot pass, since (10) is negative.

The specified cutoff also does not invoke fallback before \(j_*\).
In the polynomial theorem, \(W=n\), \(\rho=1/(4B)\le1/4\), and
\(g_0=\rho\sigma/(2W)\le\sigma/(8n)\). Its condition
\(h_J\le1/(4A)\), with \(A=2+nL/g_0\), forces
\[
                      h_J\le\frac{\sigma}{64n^2},              \tag{11}
\]
which is smaller than the lower mesh bound in (7). Thus the algorithm
reaches the large retained list before its scheduled fallback.

## 4. What this does and does not obstruct

With fixed \(L,\sigma\), widths, and degree, (8) rules out a bound
\(f(p)\operatorname{poly}(I)\) on retained-state work for this exact
global-error retention and whole-hull closure mechanism. The polynomial
input exponent cannot be independent of \(p\): for fixed sufficiently
large \(p\), let \(n\) grow and compare (8) with
\(I=O(n\log n)\).

It does **not** contradict the existing theorem's bound, which explicitly
contains a factor of order \(n^p\) and explicitly disclaims FPT in bag
size. It demonstrates why a dimension-independent replacement for that
state-count argument needs an algorithmic change.

This example does not cover additional tests on individual bag cells or
smaller full-domain patches. Cellwise first-order exclusion, second-order
necessary conditions, specialized convex closures, or an early algebraic
recognition rule might prune it much sooner. Such tests must be analyzed
on their actual domains; failure of the whole-hull test is not failure of
every possible local certificate. If applied only after a large candidate
list has been generated, their scanning cost must also be counted.

The instance itself is easy: identity (3) reduces it to binary endpoint
DP, using \(O(2^p)\) states per bag. Thus neither general optimization
hardness nor a lower bound for all sparse certificates follows from (8).
The obstruction is specifically the global rounding allowance in (6),
together with the current closure rules.

## 5. Verification scope

The bounds above are exact and uniform over the entire noise box. This
note was derived from the actual retention, projection-hull, gradient,
Hessian, and cutoff rules in the two linked algorithm notes. A targeted
inline Python document check passed whitespace, paired math delimiters,
and local links. No optimization executable, external search, index edit,
project-wide verification, or CI inspection was performed.
