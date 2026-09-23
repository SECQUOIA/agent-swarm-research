# A sharp separable centrality tax in Hessian metric

Status: The scalar-product theorem, sharpness, improved universal
same-accuracy law, nonmonotone counterexample, and trace-spectral extension
independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem and sharpness construction; medium on the
novelty assessment, which is based on a targeted rather than exhaustive
literature search

## Main conclusion

For a product of \(r\) identical one-dimensional barriers, the central path
becomes a translated scalar profile in exact metric coordinates.  If that
profile has nondecreasing metric velocity, then every central-path segment
has length at most

\[
 \boxed{
  L_{\rm cen}\leq \Gamma_r\,d_F(x(s_0),x(s_1)),\qquad
  \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2.}                 \tag{1}
\]

The factor is the exact best universal constant:

\[
 \Gamma_r^2={1\over4}\log r+O(1),\qquad
 \Gamma_r=\Theta(\sqrt{\log r}),                                \tag{2}
\]

and, more strongly, every scalar standard self-concordant barrier with
gradient parameter at most one approaches equality for suitable ordered
weights and endpoints.  Thus the logarithmic factor is not an artifact of
either the ordinary interval barrier or the spectral matrix-ball calculation
from which the inequality first emerged.

For the same entire normalized scalar class, a multiscale sparse-box family
forces \(\Omega_f(r\log r)\) forward bounded-Dikin rounds for any
fixed central neighborhood, even with arbitrary reference labels and only
actual endpoint accuracy assumed.  An explicit noncentral geodesic sequence
uses \(O_f(r\sqrt{\log r})\) rounds.  Thus the
\(\Theta(\sqrt{\log r})\) centrality tax has a universal discrete
counterpart within this precisely defined short-step class.

There is also a matching positive theorem for objective accuracy, not merely
for a prescribed endpoint.  If \(L_{\rm opt}(\epsilon)\) is the shortest
Hessian-metric distance from the analytic center to the positive-objective
\(\epsilon\)-sublevel, then the central arc to its first accurate point obeys
\[
                 L_{\rm CP}(\epsilon)
                 \leq C_{\rm sc}\Gamma_r L_{\rm opt}(\epsilon),
                 \qquad C_{\rm sc}<2,                          \tag{3a}
\]
Together with the multiscale lower family, this proves that the worst
same-accuracy centrality overhead is \(\Theta(\sqrt{\log r})\) for every
fixed normalized scalar barrier in the class.

The monotone-velocity hypothesis is essential.  There are smooth bounded
interval self-concordant barriers for which the scalar metric velocity rises
to a large peak and then falls to one.  Translates of this single profile can
be staggered so that

\[
             {L_{\rm cen}\over d_F}=\Omega(\sqrt r),             \tag{3}
\]

which matches the elementary \(O(\sqrt r)\) bound for an arbitrary
coordinatewise-monotone product path.  Hence self-concordance alone does not
imply (1).

Theorem 1 is a same-endpoint geometric comparison.  The refinement (3a)
does compare with the closest point in an objective-accuracy sublevel.
Neither statement is by itself a runtime or query lower bound.

## 1. Exact metric coordinates for a scalar product barrier

Let \(I=(a,b)\) and let \(f\in C^3(I)\) satisfy \(f''>0\) throughout \(I\).
Assume that
\(f\) has an analytic center \(x_0\), so \(f'(x_0)=0\), and that \(f'\) maps
\((x_0,b)\) onto \((0,\infty)\).  The latter is the relevant branch for a
positive support objective.  Define

\[
 \rho(x)=\int_{x_0}^x\sqrt{f''(u)}\,du,
 \qquad
 x(z)=(f')^{-1}(z),                                               \tag{4}
\]

and, in logarithmic central parameter,

\[
 h(t)=\rho(x(e^t)),\qquad v(t)=h'(t).
                                                                        \tag{5}
\]

For the product barrier and an ordered positive objective,

\[
 F(X)=\sum_{i=1}^r f(X_i),\qquad
 w_1\geq\cdots\geq w_r>0,                                       \tag{6}
\]

the exact central path for minimizing
\(F(X)-e^s\sum_iw_iX_i\) is

\[
 X_i(s)=x(e^sw_i),\qquad
 y_i(s):=\rho(X_i(s))=h(s+\log w_i).                              \tag{7}
\]

The map \(X\mapsto y=(\rho(X_i))_i\) is a global Riemannian isometry:

\[
 d\ell_F^2=\sum_i f''(X_i)dX_i^2=\sum_i dy_i^2.                  \tag{8}
\]

Its image is a rectangular interval and is therefore Euclidean-convex.
Consequently, for any two points in the product domain,

\[
 \boxed{d_F(X,Z)=\|\rho(X)-\rho(Z)\|_2.}                         \tag{9}
\]

In particular, on a central segment \(s_0<s_1\),

\[
 \begin{aligned}
 L_{\rm cen}[s_0,s_1]
   &=\int_{s_0}^{s_1}
      \left(\sum_i v(s+\log w_i)^2\right)^{1/2}ds,\\
 d_F(X(s_0),X(s_1))
   &=\left(\sum_i
      \left[\int_{s_0}^{s_1}v(s+\log w_i)\,ds\right]^2
      \right)^{1/2}.                                             \tag{10}
 \end{aligned}
\]

These identities require neither self-concordance nor a barrier-parameter
estimate.

## 2. Sharp theorem under monotone metric velocity

Set

\[
                 \alpha_i=\sqrt i-\sqrt{i-1}.                    \tag{11}
\]

### Theorem 1 (sharp fixed-order centrality tax)

Suppose \(v(t)\geq0\) is nondecreasing on every translated argument visited
by the segment in (10).  Then

\[
 d_F(X(s_0),X(s_1))
 \leq L_{\rm cen}[s_0,s_1]
 \leq \Gamma_r d_F(X(s_0),X(s_1)),                               \tag{12}
\]

where \(\Gamma_r=\|\alpha\|_2\).  The same conclusion holds for any
absolutely continuous coordinatewise-monotone curve whose nonnegative
velocity coordinates have one fixed decreasing order almost everywhere
throughout the segment.

#### Proof

At each \(s\), ordered weights and monotonicity of \(v\) give

\[
 u_1(s)\geq\cdots\geq u_r(s)\geq0,
 \qquad u_i(s)=v(s+\log w_i).                                    \tag{13}
\]

Every decreasing nonnegative vector has the prefix decomposition

\[
 u=\sum_{j=1}^r(u_j-u_{j+1})\mathbf 1_{[j]},
 \qquad u_{r+1}=0.                                               \tag{14}
\]

The triangle inequality therefore gives the sharp pointwise estimate

\[
 \|u\|_2
 \leq\sum_{j=1}^r\sqrt j\,(u_j-u_{j+1})
 =\sum_{i=1}^r\alpha_i u_i.                                     \tag{15}
\]

Integrate and write
\(H_i=\int_{s_0}^{s_1}u_i(s)ds=y_i(s_1)-y_i(s_0)\).  Then

\[
 L_{\rm cen}\leq\alpha^TH
            \leq\|\alpha\|_2\|H\|_2
            =\Gamma_r d_F(X(s_0),X(s_1)).                        \tag{16}
\]

The first inequality in (12) is the defining lower bound of Riemannian
distance, or directly Minkowski's integral inequality in (10).  \(\square\)

The elementary bounds

\[
 1+{1\over4}\sum_{i=2}^r{1\over i}
 \leq\Gamma_r^2
 \leq1+{1\over4}\sum_{i=2}^r{1\over i-1}                       \tag{17}
\]

follow from
\(\alpha_i=1/(\sqrt i+\sqrt{i-1})\).  They imply (2).

The proof isolates the real condition: not separability by itself, but a
fixed order of coordinate velocities.  Identical scalar barriers with a
nondecreasing profile are a natural and easily checked sufficient condition.

## 3. A differential test for the hypothesis

Along the positive scalar central path, put \(z=f'(x)>0\).  Direct
differentiation of (4)--(5) gives

\[
 v={f'\over\sqrt{f''}},
 \qquad
 {dv\over dt}
 =v\left(1-{v\over2}{f'''\over(f'')^{3/2}}\right).               \tag{18}
\]

Thus the exact local condition is

\[
                 2(f'')^2-f'f'''\geq0.                           \tag{19}
\]

Useful sufficient conditions include \(f'''\leq0\) on the branch, or

\[
 {f'\over\sqrt{f''}}\leq1
 \quad\hbox{together with}\quad
 |f'''|\leq2(f'')^{3/2}.                                        \tag{20}
\]

In particular, a one-dimensional standard self-concordant barrier whose
gradient local norm is at most one has monotone central velocity.  A general
\(\nu\)-self-concordant barrier only gives \(v\leq\sqrt\nu\), which is not
enough when \(\nu>1\).

This sufficient condition also makes the constant in Theorem 1 sharp for
**every fixed scalar barrier**, not merely for the example below.  State the
normalization explicitly: assume \(f\) is standard self-concordant on all of
\(I\),
\[
 |f'''|\leq2(f'')^{3/2},                                       \tag{20a}
\]
and assume the normalized gradient bound \((f')^2\leq f''\) on the positive
branch from the analytic center, in addition to the range assumptions in
Section 1.  Then \(0<v\leq1\), and (18) gives
\[
                         v'\geq v(1-v).                         \tag{20b}
\]
As \(t\to-\infty\), one has \(e^t=f'(x)\to0\), hence \(v(t)\to0\).
Since \(v\) is positive and nondecreasing, it has a positive limit at
\(+\infty\).  That limit must equal one: if it were smaller, (20b) would
eventually bound \(v'\) below by a positive constant.

The profile also has integrable step tails.  For every finite \(t_0\),
\[
 \int_{-\infty}^{t_0}v(t)\,dt=h(t_0)<\infty.                  \tag{20c}
\]
After increasing \(t_0\) so that \(v\geq1/2\), (20b) implies
\[
 (1-v)'\leq-{1\over2}(1-v),qquad
 \int_{t_0}^{\infty}(1-v(t))\,dt<\infty.                      \tag{20d}
\]
Thus \(v-\mathbf1_{(0,\infty)}\in L^1(\mathbb R)\), up to translating
the comparison step.  Moreover, \(h\) is strictly increasing from zero to
infinity.  For any fixed \(r\), choose weights exactly as in (22):
\[
                       h(\log w_i)=T\alpha_i.                   \tag{20e}
\]
The integrable step replacement and the summation-by-parts calculation in
(23)--(25) apply verbatim.  Consequently
\[
 \sup_{w,s_1}{L_{\rm cen}[{-\infty},s_1]\over
                   d_F(x_0,X(s_1))}=\Gamma_r
\]
for every fixed barrier satisfying (20a) and the positive-branch normalized
gradient bound, where the analytic-center start and the supremum are
understood as limits.  This is the precise sense in which the normalized
one-parameter self-concordant class has the universal exact constant
\(\Gamma_r\).

### 3.1 A universal same-accuracy upper bound

The same hypotheses yield a constant-factor comparison with the *closest*
accurate endpoint.  Write metric coordinate \(y=\rho(x)\geq0\) and set
\[
                         p(y)=f'(\rho^{-1}(y)).                 \tag{20f}
\]
Then
\[
 p(0)=0,\qquad p'(y)=\sqrt{f''(\rho^{-1}(y))},\qquad
 \left|{p''(y)\over p'(y)}\right|\leq1,\qquad p(y)\leq p'(y).
                                                                    \tag{20g}
\]
The last two inequalities are respectively standard self-concordance and
the normalized gradient bound.  Integrating the log-Lipschitz estimate for
\(p'\) gives
\[
 \begin{aligned}
 p'(y)(1-e^{-y})&\leq p(y)\leq p'(y)(e^y-1),\\
 {p(y)\over y p'(y)}
   &\leq\min\left\{{e^y-1\over y},{1\over y}\right\}
    \leq {1\over\log2}.                                      \tag{20h}
 \end{aligned}
\]
Indeed, the first term in the minimum increases up to its value
\(1/\log2\) at \(y=\log2\), while the second decreases from that value.

There is a complementary two-radius estimate.  On \(0<y\leq\log2\),
log-Lipschitzness on both \([0,y]\) and \([y,2y]\) gives
\[
 p(2y)\geq2p'(y)(1-e^{-y})
          \geq {y\over\log2}p'(y).                            \tag{20i}
\]
On \(y\geq\log2\), the inequality \(p'/p\geq1\), followed by the
left inequality in (20h), gives
\[
 p(2y)\geq e^yp(y)
          \geq (e^y-1)p'(y)
          \geq {y\over\log2}p'(y).                            \tag{20j}
\]

Let
\[
 G(y)=\sum_iw_i\bigl[b-\rho^{-1}(y_i)\bigr]
\]
be the objective error, and fix
\(0<\epsilon<G(0)\).  Let \(y^\star\) minimize
\(\|y\|_2\) subject to \(G(y)\leq\epsilon\).  This minimizer exists,
the constraint is active, and every coordinate is positive.  The ordinary
KKT condition for minimizing \(\|y\|_2^2/2\) therefore gives a multiplier
\(\lambda>0\) such that
\[
                  y_i^\star p'(y_i^\star)=\lambda w_i.         \tag{20k}
\]
At central parameter \(\eta=\lambda/\log2\), let \(\bar y\) denote the
central metric coordinate.  Thus
\[
 p(\bar y_i)={\lambda w_i\over\log2}
             ={y_i^\star p'(y_i^\star)\over\log2}.            \tag{20l}
\]
Equations (20h)--(20j) and monotonicity of \(p\) imply, coordinatewise,
\[
                         y_i^\star\leq\bar y_i\leq2y_i^\star. \tag{20m}
\]
Hence \(G(\bar y)\leq\epsilon\).  The first accurate central point occurs
no later and is coordinatewise no farther from the analytic center.
Applying Theorem 1 to its central arc proves
\[
 \boxed{L_{\rm CP}(\epsilon)
       \leq2\Gamma_r\|y^\star\|_2
       =2\Gamma_r L_{\rm opt}(\epsilon).}                    \tag{20n}
\]

The lower construction in Section 4.1 has central length
\(\Omega_f(r\log r)\) while (25f) supplies an accurate endpoint at distance
\(O_f(r\sqrt{\log r})\).  Thus, for every fixed normalized scalar barrier,
the worst ratio in (20n) is \(\Theta(\sqrt{\log r})\).  The factor two is
a clean universal certificate; no claim is made here that it is the optimal
dimension-free constant over the entire scalar-barrier class.

The factor two admits a rigorous differential-envelope improvement.  Define
\[
 \upsilon(y)={p(y)\over p'(y)},\qquad k=\log2.                 \tag{20o}
\]
Equation (20g) gives the exact pointwise constraints
\[
 \upsilon(0)=0,qquad0<\upsilon\leq1,qquad
             1-\upsilon\leq\upsilon'\leq1+\upsilon.          \tag{20p}
\]
The global accuracy-safe scale in (20l) is \(k\): the upper comparison in
(20h), together with \(\upsilon\leq1\), says
\[
 {y\over\upsilon(y)}\geq k\qquad(y>0).                       \tag{20q}
\]

Fix a closest-endpoint coordinate \(a=y_i^\star\) and put
\(u=\upsilon(a)\).  Its comparison center \(c a=\bar y_i\) is determined by
\[
 \int_a^{ca}{ds\over\upsilon(s)}
       =\log{a\over ku}.                                     \tag{20r}
\]
The lower differential inequality in (20p) gives
\(u\geq1-e^{-a}\).  The upper inequality and the cap \(\upsilon\leq1\)
give, for \(t\geq0\),
\[
 \upsilon(a+t)\leq\min\{1,(1+u)e^t-1\}.                    \tag{20s}
\]
Integrating the reciprocal of this maximal forward envelope in (20r)
gives
\[
 c\leq C(a):=
 \begin{cases}
  1+\dfrac1a\log\!\dfrac{k}{k(2-e^{-a})-a},
       &2a\leq k(2-e^{-a}),\\[6pt]
  1+\dfrac1a\log\!\dfrac{4a}{k(2-e^{-a})^2},
       &2a\geq k(2-e^{-a}).
 \end{cases}                                                  \tag{20t}
\]
For completeness, before the envelope reaches one, solving (20r) gives
the first branch; after it reaches one, the remaining log-parameter time is
also the remaining metric displacement and gives the second branch.  Both
answers decrease with \(u\), so substituting its lower bound
\(1-e^{-a}\) is valid.  The formulas agree at the branch boundary.

Set
\[
                         C_{\rm sc}:=\sup_{a>0}C(a).           \tag{20u}
\]
This is a finite attained maximum and is strictly smaller than two.  Here is
a fully analytic certificate for the strict inequality.  In the first
branch, the branch condition implies \(a\leq k\), and \(C(a)<2\) is
equivalent to
\(2k(1-e^{-a})>a\).  The difference is strictly concave and vanishes at
both \(0\) and \(k=\log2\), so it is positive in between.  In the second
branch, \(C(a)<2\) is equivalent to
\[
 k(4e^a-4+e^{-a})-4a>0.
\]
Since \(k>2/3\), the left side is larger than two thirds of
\(4e^a+e^{-a}-4-6a\).  The elementary Taylor bounds
\(e^a\geq1+a+a^2/2+a^3/6\) and \(e^{-a}\geq1-a\) reduce positivity to
\[
 1-3a+2a^2+{2\over3}a^3>0.
\]
The last cubic has minimum
\((16-5\sqrt{10})/3>0\).  Finally,
\(C(a)\to1/k\) as \(a\downarrow0\) and \(C(a)\to1\) as
\(a\to\infty\).  Moreover,
\(C(k)=1+k^{-1}\log(16/9)>1/k\), because
\(k+\log(16/9)=\log(32/9)>1\).  Continuity therefore proves attainment
away from the endpoints.  Numerical
evaluation, not used in the proof, gives
\[
             C_{\rm sc}\approx1.831856423
             \quad\text{at}\quad a\approx0.650114384.        \tag{20v}
\]
Consequently the certified same-accuracy comparison strengthens to
\[
 \boxed{L_{\rm CP}(\epsilon)
       \leq C_{\rm sc}\Gamma_rL_{\rm opt}(\epsilon),
       \qquad C_{\rm sc}<2.}                                  \tag{20w}
\]
The bang--bang profile \(\upsilon'=1-\upsilon\) before \(a\), followed by
\(\upsilon'=1+\upsilon\) until the cap one, explains equality in the
differential envelope (20t).  This proves that (20u) is the exact constant
obtainable from (20p) and the profile-independent safe scale \(k=\log2\).
It does **not** prove that \(C_{\rm sc}\) is the optimal same-accuracy
constant over products of one fixed smooth scalar barrier: the profiles
which make (20q) and (20t) sharp need not coincide.  That sharper global
minimax question remains open.

For \(f(x)=-\log(1-x^2)\),

\[
 v(t)=\left(1-{1\over\sqrt{1+e^{2t}}}\right)^{1/2},              \tag{21}
\]

which increases from zero to one.  Theorem 1 therefore recovers the spectral
matrix-ball factor without using any matrix-specific formula.

## 4. Exact sharpness of \(\Gamma_r\)

The constant in Theorem 1 cannot be decreased, even if one fixes the smooth
barrier \(f(x)=-\log(1-x^2)\).

Fix \(r\), let \(h(t)=\int_{-\infty}^t v(u)du\) for (21), and choose a large
\(T\).  Use the full segment from the analytic-center limit
\(s_0=-\infty\) to the terminal parameter \(s_1=0\), and select the weights
so that

\[
       h(\log w_i)=T\alpha_i,
       \qquad i=1,\ldots,r.                                     \tag{22}
\]

The function \(h\) is strictly increasing from zero to infinity, while
\((\alpha_i)\) is strictly decreasing.  Hence (22) has a unique solution
with \(\log w_1>\cdots>\log w_r\), so the weights have the order required
in (6).  The endpoint distance is exactly

\[
                   d_F=T\|\alpha\|_2=T\Gamma_r.                 \tag{23}
\]

Moreover, \(v(t)-\mathbf 1_{(0,\infty)}(t)\) is integrable and
\(h(t)=t+c+o(1)\) as \(t\to\infty\).  Replacing each translated smooth
profile by its step limit changes the total path length by \(O_r(1)\).  For
completeness, \(v(t)=O(e^t)\) at negative infinity and
\(1-v(t)=O(e^{-t})\) at positive infinity.  The reverse triangle
inequality bounds the integrated change in the vector speed by the sum of
these \(r\) scalar \(L^1\) errors, uniformly over their translations.  For
the step profiles, summation by parts gives

\[
 L_{\rm step}=\sum_i\alpha_i h(\log w_i)+O_r(1)
             =T\sum_i\alpha_i^2+O_r(1)
             =T\Gamma_r^2+O_r(1).                               \tag{24}
\]

Hence

\[
                \lim_{T\to\infty}{L_{\rm cen}\over d_F}
                =\Gamma_r.                                      \tag{25}
\]

The sharp factor is a supremum; a finite smooth profile need not attain it
exactly.  More generally, the same construction works whenever a monotone
profile tends from zero to a positive constant and differs integrably from
its limiting step after a translation and normalization.

### 4.1 A universal discrete separation for normalized scalar barriers

The universal profile theorem has a discrete consequence that does not rely
on the special algebra of \(-\log(1-x^2)\).  Fix any scalar barrier satisfying
(20a), the positive-branch gradient bound above, and the assumptions of
Section 1.  Let \(b\) be the right endpoint of its positive branch.  In fact
\(b<\infty\).  Since \(z=f'(x)=e^t\) and
\(v=z/\sqrt{f''}\),
\[
 {d\over dt}x(e^t)=e^{-t}v(t)^2,\qquad
 b-x(e^t)=\int_t^\infty e^{-u}v(u)^2\,du.                       \tag{25a}
\]
The second identity follows by monotone convergence to the branch endpoint;
it also proves finiteness.  Because \(0<v\leq1\), and because
\(v(t)\geq v_0:=1/2\) after some barrier-dependent threshold \(\tau\),
\[
 v_0^2e^{-t}\leq b-x(e^t)\leq e^{-t}
 \qquad(t\geq\tau).                                             \tag{25b}
\]

For each \(r\), put
\[
 T=r,\qquad
 S_r=\sum_{j=1}^{r-1}j^{-3/2},\qquad
 a_i={T\over S_r}\sum_{j<i}j^{-3/2},\qquad
 w_i=e^{-a_i},\qquad
 \epsilon=re^{-T}.                                              \tag{25c}
\]
Consider the product barrier \(\sum_i f(X_i)\) and minimize
\(-\sum_iw_iX_i\).  Its optimum is \(-b\sum_iw_i\).  At central label
\(s=T\), (25a) and \(v\leq1\) show
\[
 \sum_iw_i[b-x(e^{T-a_i})]\leq re^{-T}=\epsilon.                \tag{25d}
\]
Conversely, choose the fixed constant
\(c=\log(2/v_0^2)\).  At \(s=T-c\), every channel with
\(T-c-a_i\geq\tau\) contributes at least \(2e^{-T}\) to the objective
gap by (25b).  Only \(O_f(\sqrt r)\) terminal channels fail this condition,
because \(T-a_i\) is the normalized tail of
\(\sum j^{-3/2}\).  Hence the central point at \(T-c\) is not
\(\epsilon\)-accurate for all sufficiently large \(r\).

The same threshold calculation gives
\[
 L_{\rm cen}(-\infty,T-c)
 \geq v_0\int_{a_1+\tau}^{T-c}
       \sqrt{|\{i:a_i+\tau\leq s\}|}\,ds
 =\Omega_f(r\log r).                                            \tag{25e}
\]
On the other hand, the integrable tails imply
\(|h(t)-\max\{t,0\}|\leq C_f\) after changing \(C_f\).  Therefore the
accurate central endpoint at \(T\) has distance
\[
 \left(\sum_i h(T-a_i)^2\right)^{1/2}
 =O_f(r\sqrt{\log r}).                                         \tag{25f}
\]
The straight line to this endpoint in the exact product metric coordinates
is a geodesic.  Partitioning it into pieces of length \(\log(1+R)\) gives
an explicit feasible sequence of
\[
                         O_{f,R}(r\sqrt{\log r})                 \tag{25g}
\]
forward \(R\)-Dikin chords.

There is a matching central-neighborhood lower for a precise algorithmic
class.  Let \(X_0=(x_0,\ldots,x_0)\), let \(X_N\) be actually
\(\epsilon\)-accurate, and attach arbitrary real labels \(s_k\) to feasible
iterates satisfying
\[
 d_F(X_k,X(s_k))\leq\delta,\qquad
 \|X_{k+1}-X_k\|_{F,X_k}\leq R<1.                               \tag{25h}
\]
Then
\[
                         N=\Omega_{f,R,\delta}(r\log r).         \tag{25i}
\]
Indeed, every round moves its two labeled centers by Hessian-metric distance
at most \(C_{R,\delta}=2\delta-\log(1-R)\).  Use activation thresholds
\(a_i+\tau\), clip labels to the first \(J=\lfloor r^{2/3}\rfloor\)
thresholds, and define
\[
 {\cal P}(s)=\int_{a_1+\tau}^{\min\{\max\{s,a_1+\tau\},a_J+\tau\}}
       \sqrt{|\{i:a_i+\tau\leq u\}|}\,du.                       \tag{25j}
\]
The exact Euclidean product metric, the lower velocity \(v_0\), and the
uniform threshold spacing through \(J\) show exactly as in the spectral-ball
argument that every round changes \({\cal P}\) by
\(O_{f,R,\delta}(1)\) in absolute value.

Neither endpoint progress nor label monotonicity is assumed in (25h).
The start tube makes \({\cal P}(s_0)=O_{f,\delta}(1)\).  At the end,
nonnegativity of every scalar objective gap and \(w_1=1\) give
\(b-X_{N,1}\leq\epsilon\).  Equations (25a)--(25b) and
\(h(t)=t+O_f(1)\) imply that the metric coordinate of \(X_{N,1}\) is at
least \(T-\log r-O_f(1)\).  The final tube and
\(h(s)\leq\max\{s,0\}+O_f(1)\) therefore force
\[
                         s_N\geq T-\log r-O_{f,\delta}(1)
                              >a_J+\tau.                        \tag{25k}
\]
Thus the net clipped progress is \(\Omega(r\log r)\), proving (25i).
The standard self-concordant displacement estimate also imports (25i) to
every fixed Newton-decrement neighborhood
\(\lambda_{e^{s_k}}(X_k)\leq\beta<1/2\), with
\(\delta=\log[(1-\beta)/(1-2\beta)]\).

Equations (25g) and (25i) give an
\(\Omega(\sqrt{\log r})\) bounded-move central-neighborhood overhead for
**every fixed normalized scalar barrier**.  The weights in (25c) are real
numbers and the hidden constants depend on the barrier; this is a geometric
theorem, not a finite-bit or quantum-query lower bound.  The ordinary
interval barrier remains the efficiently describable specialization used
in the spectral and Jordan notes.

The objective data can nevertheless be made dyadic without changing either
order.  Fix a constant \(C_0>3\zeta(3/2)\), take
\(M=\lceil C_0r\rceil\) and \(T=M\log2\), form the thresholds in (25c),
and replace each \(a_i\) by
\[
 \widetilde a_i=k_i\log2,\qquad
 k_i=\operatorname{round}(a_i/\log2),\qquad
 \widetilde w_i=2^{-k_i},\qquad
 \widetilde\epsilon=r2^{-M}.                                   \tag{25l}
\]
For \(j\leq J=\lfloor r^{2/3}\rfloor\), the unrounded gap is at least
\((C_0/\zeta(3/2)+o(1))\log2>2\log2\).  Rounding changes a consecutive
gap by at most \(\log2\), so the charged gaps remain uniformly positive.
Every threshold moves by at most \((\log2)/2\); the
\(O_f(\sqrt r)\) terminal count, harmonic progress, endpoint norm, and
actual-accuracy forcing are therefore unchanged up to constants.
Thus (25e)--(25k) also hold for the dyadic data (25l).  Each weight and
the tolerance has \(O(r)\) binary length.  This only removes a
transcendental-data concern: it does not supply a finite-arithmetic oracle
for an arbitrary fixed barrier or an end-to-end bit-complexity theorem.

## 5. Why self-concordance alone is insufficient

There is always a crude bound for an absolutely continuous
coordinatewise-monotone product path:

\[
 L=\int\|\dot y\|_2
 \leq\int\|\dot y\|_1
 =\|y(s_1)-y(s_0)\|_1
 \leq\sqrt r\,d_F.                                               \tag{26}
\]

The next construction shows that its order is best possible within smooth
self-concordant interval barriers.

Fix \(A>4\) and define, first in metric coordinate \(y\in\mathbb R\),

\[
 p_A(y)={1+2e^{-A}\cosh y\over1+2e^{-A}},
 \qquad
 x(y)=\int_0^y{du\over p_A(u)},
 \qquad
 z(y)=\int_0^yp_A(u)du.                                         \tag{27}
\]

The map \(x:\mathbb R\to(-b_A,b_A)\) has finite endpoints.  Indeed,
for \(y\geq0\),
\[
 p_A(y)\geq {e^{y-A}\over1+2e^{-A}},
\]
so \(1/p_A\) is integrable at positive infinity; evenness handles negative
infinity.  Define
\(f_A\) by

\[
              f_A'(x(y))=z(y),\qquad f_A(x(0))=0.                \tag{28}
\]

Then

\[
 f_A''(x(y))=p_A(y)^2,\qquad
 { |f_A'''(x(y))|\over f_A''(x(y))^{3/2}}
 =2{|p_A'(y)|\over p_A(y)}<2.                                   \tag{29}
\]

Also
\[
 {d\over dy}f_A(x(y))={z(y)\over p_A(y)}.
\]
The ratio tends to \(1\) as \(y\to+\infty\) and to \(-1\) as
\(y\to-\infty\).  Its integral therefore diverges positively at both
ends, proving \(f_A\to+\infty\) at the two finite boundary points.
Moreover, \(|f_A'|/\sqrt{f_A''}=|z/p_A|\) is bounded.  Thus \(f_A\) is a smooth
standard self-concordant barrier with some finite parameter
\(\nu_A=\sup_y(z/p_A)^2=\Theta(A^2)\).  Indeed, (30) is at least
\(A/3\) at \(y=A/2\) for \(A>4\).  It is at most \(A+1\): for
\(0\leq y\leq A\) this follows directly from (30), while for \(y=A+u\)
the denominator's exponential term is at least \(e^u\), which bounds
\((y-1)/(1+e^u)\) by \(A\).  Evenness handles the negative branch.

Its positive-branch central metric velocity, expressed at metric location
\(y\), is explicit:

\[
 v_A={z(y)\over p_A(y)}
 = {y+2e^{-A}\sinh y\over1+2e^{-A}\cosh y}.                     \tag{30}
\]

It is of order \(A\) near \(y=A/2\), but tends to one as
\(y\to\infty\); hence it is not monotone.

To stagger \(r\) copies, let
\(t_- =\log z(A/4)\), \(t_+=\log z(A/2)\).  Their difference is less than
\(\log4<2\): in the explicit formula for \(z\), the common denominator
cancels, the numerator at \(A/2\) is less than \(A\), and the numerator at
\(A/4\) is greater than \(A/4\).  Choose

\[
                  \log w_i=2(r-i),\qquad s_1=t_+.               \tag{31}
\]

The interval for coordinate \(i\) is
\([t_--2(r-i),t_+-2(r-i)]\).  These \(r\) global-time intervals are
disjoint because their widths are less than two.  On each such interval the
full path speed dominates that coordinate's speed, so

\[
                         L_{\rm cen}\geq {rA\over4}.             \tag{32}
\]

At the endpoint,
\(z(y_i)=z(A/2)e^{2(r-i)}\).  The elementary bounds from (27) give

\[
             y_i\leq A+\log(3A)+2r.                              \tag{33}
\]

For \(y\geq A/2\) and \(A>4\),
\[
 z(y)\geq {e^{y-A}-e^{-y-A}\over1+2e^{-A}}
       \geq {1\over3}e^{y-A},
 \qquad z(A/2)<A.
\]
Substituting these inequalities in the endpoint identity gives
\(y_i<A+\log(3A)+2(r-i)\), which implies (33).  Also
\(\log(3A)\leq2\log(A+1)\).  The assumption below therefore gives
\(2r+\log(3A)\leq A/8\), so the stated \(2A\sqrt r\) estimate is
conservative.

Taking, for example, \(A\geq16[r+\log(A+1)]\) yields

\[
 d_F=\left(\sum_i y_i^2\right)^{1/2}\leq2A\sqrt r,
 \qquad
 {L_{\rm cen}\over d_F}\geq{\sqrt r\over8}.                   \tag{34}
\]

Together, (26) and (34) show an exact order-\(\sqrt r\) worst-case tax once
fixed velocity ordering is removed.  The growing parameter
\(\nu_A=\Theta(A^2)\) is material: this does not contradict general
barrier-parameter-dependent comparisons.

The leading constant in (26) is also sharp over this barrier family.  Replace
the window \([A/4,A/2]\) by
\([\delta A,(1-\delta)A]\), separate consecutive translated windows by any
\(B>\log((1-\delta)/\delta)+o_A(1)\) by setting
\(\log w_i=B(r-i)\), and take
\(A\gg rB+\log A\).  Each disjoint window contributes
\((1-2\delta)A\) to the length, whereas every terminal metric coordinate is
at most \(A+O(rB+\log A)\).  First let \(A\to\infty\) and then
\(\delta\downarrow0\).  For every fixed \(r\),

\[
 \sup_{f,w,s_1}{L_{\rm cen}[{-\infty},s_1]\over
        d_F(x_0,X(s_1))}=\sqrt r                                \tag{34a}
\]

over smooth self-concordant interval barriers and positive ordered weights,
where the barrier family may depend on \(r\) and the supremum need not be
attained.  Thus monotone scalar velocity improves the exact worst-case factor
from \(\sqrt r\) to \(\Gamma_r\).  A finite starting parameter can instead be
chosen sufficiently negative; it changes the two sharpness constructions by
\(o(A)\) or \(o(T)\) and leaves their limiting ratios unchanged.

## 6. Spectral and Jordan extensions

The argument has three logically separate inputs:

1. the central path stays in a common diagonal or singular-vector frame;
2. the induced metric on that commuting frame is a product of identical
   scalar metrics;
3. ambient Hessian distance between the two endpoints equals distance in
   that frame.

Inputs 1--2 already prove the central-length formula and an upper comparison
with **commuting-flat distance** for any spectral barrier

\[
                  F(x)=\sum_i f(\lambda_i(x))                    \tag{35}
\]

on a Euclidean Jordan algebra, when the objective and path share a Jordan
frame.  In fact, for a trace-separable spectral barrier, the standard
spectral Hessian formula supplies input 3 as well.

Let \(V\) be a Euclidean Jordan algebra of rank \(r\), normalize primitive
idempotents to have squared norm one, and take

\[
          F(x)=\operatorname{Tr}f(x)=\sum_{i=1}^r f(\lambda_i(x))
                                                                        \tag{36}
\]

on the spectral interval \(\{x:\lambda_i(x)\in I\}\).  In a Jordan frame
diagonalizing \(x\), write
\(u=\sum_i u_i e_i+\sum_{i<j}u_{ij}\) in its Peirce decomposition.  The
spectral Hessian formula has the form

\[
 D^2F(x)[u,u]
 =\sum_i f''(\lambda_i)u_i^2
  +\sum_{i<j}c_{ij}
    {f'(\lambda_i)-f'(\lambda_j)\over\lambda_i-\lambda_j}
       \|u_{ij}\|^2,                                             \tag{37}
\]

with positive normalization constants \(c_{ij}\) and the continuous
divided-difference convention.  Convexity of \(f\) makes every off-frame
term nonnegative.  Almost everywhere along an absolutely continuous path,
\(\dot\lambda_i=u_i\) after resolving repeated eigenspaces.  Therefore

\[
        \|\dot x\|_{F''(x)}^2
        \geq\sum_i f''(\lambda_i)\dot\lambda_i^2
        =\left\|{d\over dt}\rho(\lambda(x))\right\|_2^2.          \tag{38}
\]

For two commuting endpoints with consistently paired ordered eigenvalues,
integration gives the Euclidean metric-coordinate lower bound.  Moving in
their common frame linearly in \(\rho\)-coordinates attains it.  Thus the
ambient Hessian distance is exactly the corresponding Euclidean distance.
For a positive spectral support objective
\(c=\sum_iw_i e_i\), central stationarity is
\(f'(\lambda_i(x(s)))=e^sw_i\), so the central point shares the objective
frame and its eigenvalue profiles are precisely the scalar translates (7).
Theorem 1 therefore applies whenever those profiles obey (19).

The same proof covers rectangular singular-value barriers
\(F(X)=\sum_i f(\sigma_i(X))\) when the even Hermitian-dilation extension
\(g(\lambda)=f(|\lambda|)/2\) is convex and sufficiently smooth at zero
(in particular, the matching derivative condition \(f'(0)=0\) holds), and
the domain is a singular-value interval.  Apply
(37)--(38) to
\(\left(\begin{smallmatrix}0&X\\X^*&0\end{smallmatrix}\right)\).
In particular, it recovers the standard spectral-norm matrix-ball barrier
\(-\log\det(I-XX^*)\) and gives (12) with
\(r=\operatorname{rank}C\), exactly as in the companion spectral-ball note.

For a general invariant barrier that is not trace-separable, frame invariance
or total geodesicity alone does **not** automatically prove global distance
equality; an off-frame shortcut must still be excluded.  Without a
contraction such as (38) or a suitable nonpositively curved symmetric-space
distance formula, (12) should be stated against the commuting-flat distance,
not the ambient distance.

## 7. Relation to prior work and novelty caution

Nesterov and Todd introduced the Hessian Riemannian viewpoint and exact
product-distance structure for self-concordant barriers.  Their Section 6.2
also gives an exact global Euclidean metric coordinate for a classical
hypercube barrier: for \(f(\tau)=-\log\cos\tau\) on
\((-\pi/2,\pi/2)\),
\(\psi(\tau)=\log(\sec\tau+\tan\tau)\), applied coordinatewise, is an
isometry.  In the notation of this note its central profile is
\(h(t)=\operatorname{arsinh}(e^t)\), so its velocity is another explicit
monotone step-profile approximant.  Nesterov and Todd do not optimize the
weighted primal central arc relative to its endpoint chord.  Nesterov and
Nemirovski later bounded primal central-path length in terms of Riemannian
distance by a general \(\nu^{1/4}\)-scale estimate under their hypotheses;
their Example 5.1 treats the standard box barrier
\(-\sum_i\log(1-x_i^2)\), but for a generic length bound rather than the
exact translated-profile ratio here.
See the local summaries
[Nesterov--Todd (2002)](../../literature/papers/nesterov2002-on-the-riemannian-geometry-defined/paper.md)
and
[Nesterov--Nemirovski (2008)](../../literature/papers/nesterov2008-primal-central-paths-and-riemannian/paper.md).

The prefix inequality (15) is a finite-dimensional Lorentz-sequence norm
identity and is not itself new.  Its decreasing-rearrangement ancestry goes
back at least to G. G. Lorentz,
[*On the theory of spaces \(\Lambda\)*](https://doi.org/10.2140/pjm.1951.1.411)
(1951).  That source does not contain an integrated central-curve theorem.

The discrete lower bound (25a)--(25k) has important and substantially closer
prior art. Zong--Lee--Yue,
[*Short-step Methods Are Not Strongly
Polynomial-Time*](https://arxiv.org/abs/2201.02768), define a short-step
trajectory by requiring its whole polygonal interpolation to remain in an
\(\ell_2\) Newton neighborhood. On an ill-conditioned Klee--Minty-type LP
family they prove \(2^{r-3}\) iterations for every self-concordant barrier
whose parameter is independent of the instance scale. Allamigeon--Gaubert--
Vandame,
[*No Self-Concordant Barrier Interior Point Method Is Strongly
Polynomial*](https://arxiv.org/abs/2201.02186), prove a related exponential
lower bound for arbitrary self-concordant barriers by showing that trajectories
in a multiplicative central-path neighborhood inherit a many-segment tropical
limit. Allamigeon--Benchimol--Gaubert--Joswig,
[*Long and Winding Central Paths*](https://arxiv.org/abs/1405.4161), and their
subsequent log-barrier iteration theorem supply the earlier exponential-
curvature and log-barrier constructions. Therefore (25i) is not the first
barrier-universal central-neighborhood iteration lower bound.

Allamigeon--Dadush--Loho--Natura--Végh,
[*Interior Point Methods Are Not Worse than
Simplex*](https://arxiv.org/abs/2206.08810), formalize straight-line complexity
as the minimum number of segments of a polygonal curve traversing a wide
central-path neighborhood and show that the preceding tropical examples have
exponential straight-line complexity. This is the closest general geometric
complexity comparator. Classical self-concordance also supplies the local
Newton-decrement-to-metric-tube estimate and the Dikin displacement estimate
used in (25h); neither estimate is a novelty claim here.

The distinction of (25a)--(25k) is narrower but quantitative in a different
direction: the feasible region is merely a product of intervals equipped with
an arbitrary *fixed identical scalar* normalized barrier; labels may move
nonmonotonically; only the iterates, rather than their entire connecting
segments, must lie in a fixed metric or Newton-decrement tube; and each move is
capped in the starting Dikin norm. The theorem uses actual objective accuracy
and pairs the \(\Omega_f(r\log r)\) central-tube lower bound with an explicit
\(O_{f,R}(r\sqrt{\log r})\) noncentral route to the same accuracy. No screened
source states this product-barrier relative separation. Conversely, its
magnitude is only polynomial, its constants depend on the fixed scalar
barrier, and its real weights need not have a uniform finite-bit description;
it is much more restricted than the tropical arbitrary-barrier impossibility
results.

A targeted primary-source search did not find the combined sharp statement
(1), the assertion that **every fixed scalar standard one-self-concordant
barrier** has worst translated-profile ratio exactly \(\Gamma_r\), the
matching discrete relative separation (25g)--(25i), or the self-concordant
counterexample (27)--(34). The appropriate novelty claim is therefore:
**candidate sharp separable-product synthesis, not found in this targeted
open-literature screen; not a first general path-following lower bound, and
priority requires a specialist search.**

## 8. Consequences and nonconsequences

- The theorem gives an exact centrality overhead for separable support
  objectives: a monotone identical profile loses at most
  \(\Theta(\sqrt{\log r})\) relative to the shortest route to its own central
  endpoint.
- The factor depends on the number of active weighted coordinates, so zero
  objective coordinates should be removed before applying it.
- Products of independent blocks can pool all active scalar or spectral
  coordinates if their metric velocities admit one common fixed order.
- The result does not multiply a query lower bound by a movement bound.
- A central arc-length lower bound does not automatically lower-bound the
  number of iterates of an algorithm allowed to skip between neighborhoods.
- Distance to an objective sublevel can be smaller than distance to a chosen
  central endpoint.  For the normalized scalar class, Section 3.1 controls
  this loss universally and Section 4.1 shows its order is sharp.

## Audit checklist

1. Check that the map (4) really maps the entire relevant scalar branch and
   that the metric-coordinate image used in (9) is an interval.
2. Verify the summation-by-parts identity in (15) and equality condition
   \(H\propto\alpha\).
3. Check integrability of the step-profile error in the sharpness proof for
   (21).
4. Verify the parametric barrier construction (27)--(30), including barrier
   blow-up, finite gradient parameter, and the endpoint estimate (33).
5. Verify the Jordan spectral Hessian normalization in (37), and keep
   commuting-flat and ambient distance separate outside the trace-separable
   setting covered by (38).

## Independent audit outcome

An independent hostile audit returned **PASS** on the mathematical core,
including the exact \(\Gamma_r\) constant, the sharp
\(-\log(1-x^2)\) construction, the exact \(\sqrt r\) nonmonotone supremum,
and the trace-spectral Hessian contraction.  The audit required the explicit
positive-Hessian assumption, the analytic-center limiting start in the two
sharpness constructions, the \(r\)-dependent quantifier for the \(f_A\)
family, absolute continuity for general curves, and smoothness of the even
singular-value extension at zero.  Those corrections are incorporated
above.

A second hostile audit independently checked the delicate parts of
(22)--(34).  It verified the weight/index ordering and the integrable
step-profile replacement in (22)--(25).  For the custom barrier, it checked
that \(x(\mathbb R)\) is bounded, \(f_A\) blows up at both endpoints, the
one-dimensional self-concordance and gradient inequalities hold globally,
and \(A^2/9\leq\nu_A\leq(A+1)^2\).  It also rederived the disjoint-window
ordering, the endpoint estimate (33), the \(\sqrt r/8\) lower ratio, and
the limiting \(\sqrt r\) supremum in (34a).  The audit made the start
\(s_0=-\infty\), generalized-window weights, and elementary boundary and
endpoint estimates explicit.  No counterexample to the corrected theorem
was found.

A further hostile audit checked the universal normalized-barrier claim
(20a)--(20e).  The Section 1 assumptions imply
\(x(e^t)\to x_0\) and hence \(v(t)\to0\) as \(t\to-\infty\).
Self-concordance and \((f')^2\leq f''\) give
\(v'\geq v(1-v)\), so positivity and monotonicity force the other limit to
be one.  They also give the two integrable tails in (20c)--(20d), making
\(h\) a strictly increasing bijection from \(\mathbb R\) onto
\((0,\infty)\).  Thus (20e) defines uniquely ordered positive weights.
For the sharpness limit, replacing each translated velocity by its unit
step changes the vector-speed integral by at most the sum of the scalar
\(L^1\) errors, uniformly over translations.  The exact step length is
\(\sum_i\alpha_i\log w_i\); integrability gives
\(h(t)=t+c+o(1)\), so this equals
\(T\sum_i\alpha_i^2+O_r(1)\).  Together with the exact endpoint distance
\(T\|\alpha\|_2\), this proves the claimed supremum \(\Gamma_r\).  The
analytic-center start is correctly understood as a limit, and finite starts
approximate it.  No correction was required.

An independent hostile audit then checked the universal discrete theorem
(25a)--(25k).  It verified the exact physical-slack identity, the two-sided
tail bound, the inaccurate \(T-c\) center, the
\(\Omega_f(r\log r)\) arc, and the \(O_{f,R}(r\sqrt{\log r})\) geodesic
chord comparator.  It also checked the arbitrary-label clipped potential,
analytic-center start, actual-accuracy endpoint forcing, and Newton-decrement
import.  The audit required one hypothesis clarification: standard
self-concordance must hold on the whole interval because arbitrary feasible
chords in (25h) need not stay on the positive branch; only the normalized
gradient bound is branch-local.  That correction is incorporated above.
No finite-bit or uniform-in-\(f\) claim is made.

The dyadic refinement (25l) was separately audited.  Rounding moves each
threshold by at most \((\log2)/2\), keeps the first
\(J=\lfloor r^{2/3}\rfloor\) gaps uniformly positive, and perturbs their
weighted progress by only \(O(r)\), versus the
\(\Theta(r\log r)\) main term.  At \(s=T\) the objective-gap cancellation
remains exact, while the terminal inactive count and final-label margin
change only by constants.  Endpoint metric coordinates change by at most
\((\log2)/2\) because \(h\) is one-Lipschitz.  Thus all lower and upper
orders persist.  The audit also confirmed \(O(r)\) bits per listed dyadic
weight and tolerance; listing all \(r\) weights explicitly may of course
take \(O(r^2)\) bits.

The universal discrete extension (25a)--(25k) was also hostile-audited.
The identity \(dx(e^t)/dt=e^{-t}v(t)^2\), together with \(v\leq1\),
both proves that the right endpoint is finite and gives the exact tail
formula (25a).  Once \(v\geq1/2\), its two-sided exponential tail estimate
is (25b).  In the threshold family, multiplication by
\(w_i=e^{-a_i}\) cancels the shifted exponent exactly, so every sufficiently
activated channel contributes at least \(2e^{-T}\) at \(T-c\), while every
channel contributes at most \(e^{-T}\) at \(T\).  Only
\(O_f(\sqrt r)\) channels are not activated at the earlier label.  This
verifies the first-accuracy window, the \(\Omega_f(r\log r)\) central arc,
and the \(O_f(r\sqrt{\log r})\) metric-coordinate endpoint bound.

For the discrete lower bound, clipping to the shifted thresholds contracts
every monotone metric-coordinate difference.  The fixed lower velocity and
uniform early-threshold spacing therefore bound the absolute potential
change of every round, including backward and clipping-crossing jumps.
Actual endpoint accuracy gives \(b-X_{N,1}\leq\epsilon\); for all sufficiently
large \(r\), (25b) puts this coordinate on the positive branch and yields
metric displacement at least \(T-\log r-O_f(1)\).  The final tube then
forces (25k), whose margin over \(a_J+\tau\) is
\(\Theta(r^{2/3})\).  The analytic-center start contributes only
\(O_{f,\delta}(1)\) clipped progress.  Finally, the standard
self-concordant displacement estimate gives exactly
\(\delta=\log[(1-\beta)/(1-2\beta)]\) for
\(\beta<1/2\).  Thus the theorem needs neither monotone labels nor an
endpoint-label assumption.  Its constants may depend on the fixed scalar
barrier, as stated.  No correction was required.

Finally, an independent hostile audit checked the same-accuracy refinement
(20f)--(20n).  It verified
\(p'=\sqrt{f''}\),
\(p''/p'=f'''/[2(f'')^{3/2}]\), both log-Lipschitz envelopes in
(20h), and the split at \(y=\log2\) in (20i)--(20j).  For the closest-point
problem, continuity and coercivity give existence, monotonicity makes the
constraint active, and the Mangasarian--Fromovitz constraint qualification
gives KKT without any convexity assumption.  The stationarity signs exclude
zero coordinates and yield (20k).  The audit then confirmed the scaling
\(\eta=\lambda/\log2\), the coordinate sandwich (20m), the first-accuracy
direction, and composition with Theorem 1.  Thus (20n) and the matching
per-fixed-barrier \(\Theta(\sqrt{\log r})\) worst-case law are valid.  No
correction was required.

The sharper scalar-envelope calculation (20o)--(20w) was then independently
hostile-audited.  The audit verified the differential inequalities
\(1-\upsilon\leq\upsilon'\leq1+\upsilon\), the direction of the safe
scale \(k=\log2\), the integral equation (20r), and the maximal forward
envelope in (20s).  Direct integration reproduced both branches and their
transition in (20t), including monotonic decrease with the initial value
\(u\).  It also checked the analytic proof \(C_{\rm sc}<2\) and independently
reproduced the numerical value in (20v).  The audit caught one attainment
gap: endpoint limits alone did not suffice.  The explicit interior value
\(C(k)=1+k^{-1}\log(16/9)>1/k\), now included above, repairs it and proves
interior attainment by continuity.  The final scope is important and was
also confirmed: \(C_{\rm sc}\) is exact for the relaxed differential
envelope with the profile-independent safe scale, not a proved sharp global
minimax constant for products of one fixed smooth barrier.
