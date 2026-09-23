# A dyadic discrete centrality tax for an exact-optimal coupled cube barrier

Status: Proved and independently hostile-audited
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the geometric theorem; priority not claimed

## Result

Let
\[
 F(x)=U(x)+G(x),\quad
 U(x)=-\sum_{i=1}^r\log(1-x_i^2),\quad
 G(x)=-\log(r+4-\|x\|^2).                                    \tag{1}
\]
The [continuous companion](2026-09-04-exact-optimal-hyperoctahedral-box-barrier-tax.md)
proves that \(F\) is genuinely coupled, fully hyperoctahedrally invariant,
and has exact optimal parameter \(r\).

Fix a forward Dikin radius \(R<1\) and a central-tube radius
\(\Delta<\infty\).  For all sufficiently large \(r\), there are positive
dyadic weights \(w_i\) and a positive dyadic tolerance \(\epsilon\), each
with \(O(r)\) bits, such that:

1. the exact analytic center is \(0\);
2. any feasible sequence \(X_0=0,\ldots,X_N\) with arbitrary real labels
   \(s_k\), satisfying
   \[
    d_F(X_k,x(s_k))\leq\Delta,\qquad
    \|X_{k+1}-X_k\|_{F,X_k}\leq R,                              \tag{2}
   \]
   and ending at an actually \(\epsilon\)-accurate point, requires
   \[
                              \boxed{N=\Omega_{R,\Delta}(r\log r)};
                                                                    \tag{3}
   \]
3. an explicit noncentral sequence reaches an actually
   \(\epsilon\)-accurate point in
   \[
                        \boxed{O_{R,\Delta}(r\sqrt{\log r})}    \tag{4}
   \]
   forward \(F\)-Dikin chords.

No monotonicity of the labels \(s_k\) is assumed.  The same lower bound
holds if the metric tube in (2) is replaced by any fixed
Newton-decrement neighborhood \(\lambda_{e^{s_k}}(X_k)\leq\eta<1/2\).
Thus the exact-optimal genuinely coupled barrier has a discrete
\(\Omega(\sqrt{\log r})\) central-neighborhood overhead.

## 1. Uniform monotonicity of the coupled central coordinates

Put
\[
 S=r+4-\|x\|^2,\qquad a={2\over S},\qquad
 b_i={2\over1-x_i^2}.
\]
For a positive objective \(w\), the central equations are
\[
 z_i=e^sw_i=x_i(b_i+a).                                      \tag{5}
\]
Hence every central coordinate is positive.  With
\[
 D_i=u''(x_i)={2(1+x_i^2)\over(1-x_i^2)^2},\qquad E_i=D_i+a,
\]
differentiation in \(s\) gives
\[
 E_i\dot x_i+x_i\dot a=z_i,\qquad
 \dot a=a^2\sum_i x_i\dot x_i.                               \tag{6}
\]
Solving the scalar self-consistency equation yields
\[
 \dot a={a^2K\over1+a^2L},\quad
 K=\sum_i{x_i^2(b_i+a)\over E_i},\quad
 L=\sum_i{x_i^2\over E_i}.                                   \tag{7}
\]
For \(y=x_i^2\) and \(a<1/2\),
\[
 {y(b_i+a)\over E_i}\leq1-y.                                 \tag{8}
\]
Indeed, after multiplying by \(1-y\), the difference between the
right and left sides is
\[
                     2+a(1-2y)(1-y)>0.
\]
Since \(\sum_i(1-x_i^2)=S-4=2/a-4\), (7)--(8) imply
\[
                 0\leq\dot a<a^2(S-4)=2a-4a^2\leq{1\over4}.  \tag{9}
\]
Consequently every \(\dot x_i>0\).

Define the effective scalar label
\[
 q_i=u'(x_i)=b_ix_i=z_i-ax_i.
\]
Because \(D_i\geq2\), \(b_i\geq2\), \(a<1/2\), and (9),
\[
 {d\over ds}\log q_i
 ={D_i(b_i+a-\dot a)\over(D_i+a)b_i}
 \geq {2\over2+1/2}\left(1-{1/4\over2}\right)
 ={7\over10}.                                                 \tag{10}
\]
In the exact product metric coordinate
\[
 \rho(x)=\int_0^x\sqrt{u''(t)}\,dt,\qquad
 h(\log q)=\rho((u')^{-1}(q)),
\]
one has \(h'(\log q)=q/\sqrt{u''}\uparrow1\).  Choose a fixed \(Z\)
so large that this velocity is at least \(1/2\) for \(q\geq(4/5)Z\).
Equation (5) gives
\[
 {q_i\over z_i}={b_i\over b_i+a}\geq{4\over5}.                \tag{11}
\]
Therefore, whenever \(z_i\geq Z\),
\[
                         {d\over ds}\rho(x_i(s))
                         \geq\kappa:={7\over20}.               \tag{12}
\]
This uniform derivative, rather than a central-arc distance inference, is
the key to the arbitrary-label discrete proof.

## 2. Dyadic multiscale instance

Let
\[
 S_r=\sum_{j=1}^{r-1}j^{-3/2},\qquad
 J=\lfloor r^{2/3}\rfloor.
\]
Choose a constant \(K_0=K_0(R,\Delta)\) later, put
\[
 L=\lceil K_0r\rceil,\qquad T=L\log2,
\]
and define ideal thresholds
\[
 a_i^*={T\over S_r}\sum_{j<i}j^{-3/2}.
\]
Round each \(a_i^*/\log2\) to a nondecreasing integer \(m_i\), keeping
\(m_1=0\) and \(m_r=L\), with
\[
                         |m_i\log2-a_i^*|\leq\log2.           \tag{13}
\]
Set
\[
 w_i=2^{-m_i},\qquad
 \epsilon=2r\,2^{-L}.                                        \tag{14}
\]
These are positive dyadic rationals with \(O(r)\) bits.  Write
\(a_i=m_i\log2\); then \(z_i(s)=e^{s-a_i}\), and the level-\(Z\)
activation thresholds are
\[
                             \sigma_i=a_i+\log Z.             \tag{15}
\]

At the terminal central label \(T\), (11) and
\[
                     q(1-x)={2x\over1+x}\leq1
\]
give
\[
 \sum_iw_i(1-x_i(T))
 \leq {5\over4}\sum_i{w_i\over z_i(T)}
 ={5r\over4}e^{-T}<\epsilon.                                 \tag{16}
\]
Thus the terminal central point is actually \(\epsilon\)-accurate.

## 3. Arbitrary-label central-neighborhood lower bound

A forward \(F\)-Dikin chord of starting norm at most \(R\) has
Riemannian length at most \(-\log(1-R)\).  Hence (2) and the triangle
inequality imply
\[
 d_F(x(s_k),x(s_{k+1}))
 \leq D_0:=2\Delta-\log(1-R).                                 \tag{17}
\]
Since \(\nabla^2F\succeq\nabla^2U\), the exact product coordinates also
satisfy
\[
 \|\rho(x(s_k))-\rho(x(s_{k+1}))\|_2\leq D_0.                 \tag{18}
\]

Define the clipped progress potential
\[
 {\cal P}(s)=
 \int_{\sigma_1}^{\min\{\max\{s,\sigma_1\},\sigma_J\}}
       \sqrt{|\{i:\sigma_i\leq u\}|}\,du.                     \tag{19}
\]
For \(j<J\), (13) gives
\[
 \sigma_{j+1}-\sigma_j
 \geq {T\over S_rj^{3/2}}-2\log2
 \geq {K_0\log2\over S_r}-2\log2.                            \tag{20}
\]
Choose \(K_0\) so that the last expression exceeds \(D_0/\kappa+1\).
Equations (12) and (18) then show that one round cannot contain a complete
threshold gap inside \([\sigma_1,\sigma_J]\).  Thus its clipped label
interval lies in one stage or crosses only one threshold.  If \(j\geq1\)
channels are already active, (12) and (18) give
\[
                    |s_{k+1}-s_k|\leq {D_0\over\kappa\sqrt j}
\]
on that clipped interval.  Since the integrand in (19) is at most
\(\sqrt{j+1}\), and the \(j=0\) entrance is handled by the first active
coordinate, one obtains
\[
              |{\cal P}(s_{k+1})-{\cal P}(s_k)|
              \leq {\sqrt2D_0\over\kappa}+O(1).               \tag{21}
\]
This argument is symmetric under exchanging the two labels and therefore
allows arbitrary backtracking.

The start condition \(X_0=0\), (2), (11), and monotonicity of \(h\) imply
\({\cal P}(s_0)=O_\Delta(1)\).  At the endpoint, actual accuracy and
\(w_1=1\) give
\[
                         1-X_{N,1}\leq\epsilon.               \tag{22}
\]
The scalar endpoint asymptotic, \(d_F\geq d_U\), the final tube, and
\(\rho(x_1(s))\leq h(s)\leq\max\{s,0\}+O(1)\) force
\[
                      s_N\geq T-\log(2r)-O_\Delta(1).         \tag{23}
\]
On the other hand,
\[
 T-a_J^*={T\over S_r}\sum_{j=J}^{r-1}j^{-3/2}
          =\Theta(T/\sqrt J)=\Theta(r^{2/3}),
\]
so (13) and (23) imply \(s_N>\sigma_J\) for large \(r\).

Finally, rounding in (13) changes the following summation-by-parts
quantity by only \(O(\sqrt J)\):
\[
\begin{aligned}
 {\cal P}(\sigma_J)
 &=\sum_{j=1}^{J-1}\sqrt j\,(a_{j+1}-a_j)\\
 &={T\over S_r}\sum_{j=1}^{J-1}{1\over j}+O(\sqrt J)
 =\Theta(r\log r).                                            \tag{24}
\end{aligned}
\]
Equations (21)--(24) prove (3).

The standard self-concordant displacement theorem turns
\(\lambda_{e^{s_k}}(X_k)\leq\eta<1/2\) into a fixed metric tube, for
example with radius
\[
                  \Delta_\eta=\log{1-\eta\over1-2\eta}.
\]
This proves the Newton-neighborhood version.

## 4. Explicit noncentral bounded-Dikin path

At the accurate central endpoint, (11) and the scalar metric asymptotic
give
\[
 \rho(x_i(T))\leq (T-a_i)_++O(1).
\]
The ideal tail bound
\[
 T-a_i^*\leq {2T\over S_r\sqrt i}
\]
and (13) imply
\[
                  \|\rho(x(T))\|_2=O(r\sqrt{\log r}).         \tag{25}
\]
Join zero to \(x(T)\) by the straight segment in the product
\(\rho\)-coordinates.  Its \(U\)-length is (25).  Along this
coordinatewise-monotone curve, (5) gives
\[
\begin{aligned}
 L_G
 &\leq\int\sqrt a\,\|dx\|_2+\int a\,x^Tdx\\
 &\leq {1\over\sqrt2}\sum_i x_i(T)
      +\log{r+4\over r+4-\|x(T)\|^2}\\
 &=O(r+\log r).                                               \tag{26}
\end{aligned}
\]
Here the second integral is exact after substituting
\(d\|x\|^2=2x^Tdx\), and its denominator is at least \(4\).
Therefore the same curve has actual \(F\)-length
\[
                              O(r\sqrt{\log r}).               \tag{27}
\]
Partition it into \(F\)-metric arc segments of length at most
\(\log(1+R)\).  Self-concordant norm transport makes each endpoint chord
have starting \(F\)-Dikin norm at most \(R\), proving (4).

## Scope and novelty boundary

This is a geometric round separation for one explicit sparse box domain
and one explicit coupled barrier.  The weights and tolerance are dyadic,
but no claim is made that evaluating a generic barrier oracle is free.
There is no query lower bound, and movement and query costs must not be
multiplied.  The theorem does not cover long steps, infeasible iterates, or
algorithms whose evolution is not represented by bounded primal Dikin
chords.

The candidate contribution is the coexistence of exact optimal parameter,
full signed-permutation symmetry, genuine dense coupling, rational
multiscale data, and a sharp discrete central-neighborhood overhead.  A
targeted search found no matching result; priority requires specialist
review.

## Audit targets

1. Check (7)--(10), especially the global bound on \(\dot a\).
2. Verify that (12), not central arclength, controls arbitrary label jumps.
3. Check dyadic rounding, threshold gaps, and the clipped-potential estimate.
4. Verify endpoint accuracy and endpoint-label forcing.
5. Check the radial metric integral (26) and forward-chord partition.

## Closure audit

The proof was rechecked at research closure.  Differentiating
\(a=2/(r+4-\|x\|^2)\) gives the scalar consistency equation (7).
The coordinate inequality in (8) implies
\(\dot a<a^2\sum_i(1-x_i^2)=2a-4a^2\le1/4\), and then
\[
 {d\log u'(x_i)\over ds}
 ={D_i(b_i+a-\dot a)\over(D_i+a)b_i}\ge {7\over10}.
\]
Together with \(u'(x_i)/z_i=b_i/(b_i+a)\ge4/5\), this verifies the
uniform active-coordinate metric speed \(7/20\) used in the arbitrary-label
argument.

The dyadic rounding changes each threshold by at most \(\log2\).
Choosing \(K_0(R,\Delta)\) as in (20) prevents one bounded move from
crossing a complete early threshold gap.  Splitting a possible one-threshold
crossing verifies the \(O_{R,\Delta}(1)\) increment in (21), while
summation by parts leaves
\((T/S_r)\sum_{j<J}1/j+O(\sqrt J)=\Theta(r\log r)\).
Actual accuracy forces the final first coordinate within \(\epsilon\) of
one; contraction to the product metric and
\(\rho(x_1(s))\le \max\{s,0\}+O(1)\) then give (23), with ample
\(\Theta(r^{2/3})\) margin over \(\sigma_J\).

For the upper path,
\(\nabla^2G=aI+a^2xx^T\) gives
\[
 \sqrt{dx^T\nabla^2G\,dx}
 \le\sqrt a\,\|dx\|_2+a|x^Tdx|.
\]
Coordinate monotonicity and direct integration yield (26); adding this to
the exact product-\(\rho\) length proves (27).  Partition into arclength
\(\log(1+R)\) and the lower self-concordant chord comparison give the
claimed forward \(F\)-Dikin chords.  No runtime, query, infeasible-step, or
unbounded-step conclusion was used.  This closure audit found no
mathematical correction.

A subsequent independent hostile audit rederived (7)--(10), the arbitrary-
label clipped-potential argument, dyadic rounding and \(O(r)\)-bit input
bounds, endpoint forcing, the Newton-decrement-to-metric-tube conversion,
and the noncentral radial-length upper bound.  It returned **PASS**.  It
also identified one notation correction now made in (4): because
\(K_0=K_0(R,\Delta)\), the upper constant is \(O_{R,\Delta}\), not merely
\(O_R\).
