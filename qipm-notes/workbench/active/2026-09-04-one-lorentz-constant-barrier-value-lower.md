# One Lorentz cone: constant-barrier optimum-value parity and easy solution states

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on novelty

## Main theorem

For every \(N\geq2\) and public scale \(C>0\), there is an SOCP with one Lorentz cone
\(Q_{2N+1}\), a public two-sparse and perfectly conditioned equality slice,
and a sign-balanced hidden objective such that:

1. the restricted standard Lorentz barrier has exact parameter
   \(\nu_{\rm red}=1\), while the ambient normal barrier has parameter two;
2. at the public central multiplier \(\eta_0=1/C\), the reduced Newton
   Hessian has condition number at most \(3/\sqrt5\), has a one-hub
   treewidth-one representation, and is solved classically in \(O(N)\)
   arithmetic;
3. for \(0<\epsilon\leq c_0C\), where \(c_0>0\) is any sufficiently small
   universal constant, estimating the ordinary optimum value to additive
   error \(\epsilon\) has the exact worst-case laws

\[
 \boxed{
 Q=\Theta\!\left(\min\left\{N,{C\over\epsilon}\right\}\right),
 \qquad
 R=\Theta\!\left(\min\left\{N,{C^2\over\epsilon^2}\right\}\right).} \tag{1}
\]

Here \(Q\) and \(R\) denote worst-case bounded-error quantum and randomized
query complexity, respectively, with success probability at least \(2/3\).

4. the same accuracy-parametric laws hold for the ordinary objective value
   at the exact central point \(z(\eta_0)\), while a full explicit feasible
   solution of objective gap below \(C/(8\sqrt5N)\) costs
   \(\Theta(N)\) input queries; but
5. the normalized exact optimizer state has a heralded preparation using
   \(O(1)\) expected canonical hidden-bit queries, and a deterministic
   constant-error optimizer or central-point state uses \(O(1)\) queries.

On the same instances, any feasible trajectory built from a bounded number
of bounded-Dikin chords per outer round needs
\(\Omega(\log(C/\epsilon))\) rounds to reach objective gap \(\epsilon\)
from the analytic center. This path-length bound is simultaneous with, and
is never multiplied by, the query bounds.

Taking \(C=N\) and fixed \(\epsilon\) gives
\(Q=R=\Theta(N)\). The lower bounds in (1) survive coefficient access, constant-size paired
coordinate access, classical vector-SQ access, and a specified canonical
coherent state-preparation interface for the raw conic objective. All raw
norms, coordinate magnitudes, and squared-sampling distributions are public.
Under the zero-versus-one-mark promise and additive error below half the
relevant adjacent value gap, hence for a sufficiently small constant times
\(C/N\), the scalar law instead becomes the sharp Grover separation

\[
                         Q=\Theta(\sqrt N),\qquad R=\Theta(N).          \tag{2}
\]

An equivalent encoding makes the objective completely public and moves
every hidden sign into a disjoint two-sparse equality row; its equality
hidden slice matrix has condition one. This is a constant-barrier,
constant-conditioned state/scalar/full-output
separation. The query separation alone is not a general IPM iteration lower
bound; Section 10 gives only the fixed-barrier bounded-move result. The cone
dimension is \(2N+1\); no bounded-block-cap claim is made.

## 1. Sparse SOCP and sign-balanced access

Let \(b=(b_1,\ldots,b_N)\in\{0,1\}^N\). Use one vector

\[
                  z=(x_1,y_1,\ldots,x_N,y_N)\in B_2^{2N}               \tag{3}
\]

and the public equalities

\[
                              y_i=x_i\qquad(i\in[N]).                   \tag{4}
\]

The ball is represented by \((1,z)\in Q_{2N+1}\). Every row of (4) has
two nonzeros, the rows are orthogonal, and their nonzero singular values are
all \(\sqrt2\).

The hidden objective pair is
\[
 c_i(b_i)={C\over\sqrt{10N}}\bigl(1,3(-1)^{b_i}\bigr).                 \tag{5}
\]
The choice \(C=N\) is the important fixed-additive-accuracy specialization.
Every pair has norm \(C/\sqrt N\), so the full raw objective has the public
norm

\[
                                  \|c\|_2=C.                            \tag{6}
\]

Its coordinate magnitudes are fixed. Squared-coordinate sampling chooses a
uniform \(i\), then the \(x\)-coordinate with probability \(1/10\) or the
\(y\)-coordinate with probability \(9/10\); only the returned sign of the
latter depends on \(b_i\). Even the two coordinate-column norms,
\(C/\sqrt{10}\) and \(3C/\sqrt{10}\), are public.

An orthonormal coordinate on the equality slice is

\[
                    (x_i,y_i)={t_i\over\sqrt2}(1,1),
                    \qquad \|t\|_2\leq1.                               \tag{7}
\]

The reduced objective is \(\beta(b)^Tt\), where

\[
 \beta_i(b_i)=
 \begin{cases}
  2C/\sqrt{5N},&b_i=0,\\
  -C/\sqrt{5N},&b_i=1.
 \end{cases}                                                           \tag{8}
\]

Thus the public equality elimination is numerically harmless, but the norm
of the projected objective contains the hidden statistic.

## 2. Ordinary optimum value has an accuracy-parametric Hamming ledger

Write \(w=|b|\), \(u=w/N\), and \(R_w=\|\beta(b)\|_2\). From (8),

\[
                 R_w^2={C^2(4N-3w)\over5N},\qquad
                 \operatorname{OPT}(b)=-R_w.                            \tag{9}
\]

Equivalently,

\[
 {R_w\over C}=\phi(u):=\sqrt{{4-3u\over5}},\qquad
 {3\sqrt5\over20}\leq |\phi'(u)|={3\over10\phi(u)}
                         \leq {3\sqrt5\over10}.                        \tag{10}
\]

Thus additive error \(\epsilon\) in \(-C\phi(w/N)\) is equivalent, up
to universal constants, to additive error
\(\delta=\epsilon/C\) in the Boolean mean \(w/N\). A mean estimate with
accuracy \(\epsilon/(C\,3\sqrt5/10)\) gives an
additive-\(\epsilon\) value estimate. Conversely, clamp any value estimate
to \([-2C/\sqrt5,-C/\sqrt5]\) and apply the public inverse of
\(-C\phi\). The left inequality in (10) turns value error \(\epsilon\)
into mean error at most \(20\epsilon/(3\sqrt5C)\).

The standard worst-case approximate-counting bounds, in the regime
\(0<\delta\leq c_0\), are

\[
 Q_{\rm count}(N,\delta)=\Theta(\min\{N,1/\delta\}),\qquad
 R_{\rm count}(N,\delta)=\Theta(\min\{N,1/\delta^2\}).                 \tag{11}
\]

The upper bounds use amplitude estimation or ordinary sampling, capped by
reading all \(N\) bits. Nayak--Wu's additive-counting lower bound at weights
near \(N/2\) gives the quantum term in (11), including its cap at \(N\).
For the randomized term, Yao's principle applied to Bernoulli product
distributions of means \(1/2\pm\Theta(\delta)\) gives
\(\Omega(1/\delta^2)\) queries when \(\delta\geq\Theta(1/\sqrt N)\):
the transcript divergence is \(O(q\delta^2)\), while the realized weights
are separated with constant probability. At
\(\delta=\Theta(1/\sqrt N)\) this is \(\Omega(N)\), and monotonicity in
the demanded accuracy proves the cap for smaller \(\delta\). At the
still smaller exact-counting endpoint, parity gives the same cap directly.
Floors, ceilings, and the finitely many small \(N\) cases affect only
universal constants. Equations (9)--(11) prove (1).

In normalized accuracy \(\delta=\epsilon/C\), (1) is the three-regime
phase diagram

\[
\begin{array}{c|c|c}
\text{accuracy regime}&Q&R\\ \hline
N^{-1/2}\lesssim\delta\leq c_0&\Theta(\delta^{-1})&
                                      \Theta(\delta^{-2})\\
N^{-1}\lesssim\delta\lesssim N^{-1/2}&\Theta(\delta^{-1})&
                                      \Theta(N)\\
0<\delta\lesssim N^{-1}&\Theta(N)&\Theta(N).
\end{array}
\]

Thus the usual quadratic counting advantage holds at moderate precision,
classical queries saturate first, and the quantum advantage disappears only
at inverse-linear normalized precision. This boundary occurs although the
restricted barrier parameter is one.

For the exact-counting endpoint, adjacent squared norms differ by
\(3C^2/(5N)\), and \(R_w+R_{w+1}\leq2R_0=4C/\sqrt5\). Therefore

\[
 R_w-R_{w+1}
 ={3C^2/(5N)\over R_w+R_{w+1}}
 \geq {3C\over4\sqrt5N}.                                               \tag{12}
\]

An additive estimate with error below \(3C/(8\sqrt5N)\) identifies the
integer \(w\) by nearest-neighbor rounding in the public list (9), hence
computes parity. For \(C=N\), this is fixed additive accuracy.

Under the promise \(w\in\{0,1\}\), (12) reduces the value problem to
unique unstructured search. Grover search and the standard lower bound
prove (2) at error \(\Theta(C/N)\). The uncentered optimum is
\(\Theta(C)\), so the corresponding relative accuracy is \(\Theta(1/N)\).
Subtracting the public baseline \(-R_0\) makes the unique-mark scalar
bounded when \(C=N\), with a constant gap, without changing its
absolute-accuracy contract.

## 3. Exact restricted barrier and a uniformly conditioned checkpoint

Restricting the standard Lorentz barrier through (7) gives

\[
                             F(t)=-\log(1-\|t\|_2^2).                    \tag{13}
\]

This barrier has exact self-concordance parameter one. Its gradient dual
norm is bounded by one and tends to one at the boundary; equivalently this
is the exact reduced-ball barrier theorem. The ambient cone barrier
\(-\log(u^2-\|z\|^2)\) has parameter two.

At central multiplier \(\eta\), rotational symmetry gives

\[
 t(\eta)=-r(\eta R_w){\beta\over R_w},\qquad
 r(a)={a\over\sqrt{1+a^2}+1},                              \tag{14}
\]

because \(a=2r/(1-r^2)\). At the public choice

\[
                              \eta_0={1\over C},                         \tag{15}
\]

the effective radial force satisfies

\[
                {1\over\sqrt5}\leq a_w:={R_w\over C}
                           \leq {2\over\sqrt5}.                         \tag{16}
\]

For a point of radius \(r\),

\[
 \nabla^2F(t)={2\over1-r^2}I
              +{4\over(1-r^2)^2}tt^T,                                  \tag{17}
\]

whose radial-to-transverse eigenvalue ratio is

\[
                         {1+r^2\over1-r^2}=\sqrt{1+a^2}.                 \tag{18}
\]

Equations (16)--(18) prove

\[
                 \boxed{\ \kappa(\nabla^2F(t(\eta_0)))
                                  \leq {3\over\sqrt5}.\ }               \tag{19}
\]

The Hessian is diagonal plus rank one. One latent hub gives a star and
treewidth one, so the exact reduced Newton solve costs \(O(N)\) field
operations. Retaining the public equalities gives one global rank hub and
one equality-row vertex per coordinate. Bags
\(\{h,x_i,\lambda_i\}\) and \(\{h,y_i,\lambda_i\}\) give augmented
treewidth at most two and the same linear arithmetic bound. Equation (19)
concerns the reduced positive Hessian; it is not an unscaled indefinite-KKT
spectral-condition claim.

## 4. A hard ordinary scalar at the fixed central point

The ordinary linear objective evaluated at (14)--(15) is

\[
                 L_w=-R_w r(R_w/C)=-C h(w/N),                           \tag{20}
\]

where \(h(u)=\phi(u)r(\phi(u))\). Since
\(r'(a)=1/(\sqrt{1+a^2}(\sqrt{1+a^2}+1))>0\), (10) and (16) give

\[
 |h'(u)|=|\phi'(u)|\,[r(\phi(u))+\phi(u)r'(\phi(u))]
 \geq {3\sqrt5\over20}(\sqrt6-\sqrt5)>0.                              \tag{21}
\]

The same derivative is bounded above by a universal constant. Hence the
central scalar is also bi-Lipschitz equivalent, after division by \(C\),
to \(w/N\), and has the full query laws (1).

For the exact-counting endpoint, put \(g(R)=Rr(R/C)\). On the full range
(16),

\[
 g'(R)=r(R/C)+{R\over C}r'(R/C)
       \geq r(1/\sqrt5)=\sqrt6-\sqrt5.
\]

Combining this inequality with (12), adjacent central values are separated
by at least

\[
       \Delta_{\rm cp}:={3C(\sqrt6-\sqrt5)\over4\sqrt5N}.               \tag{22}
\]

Therefore error below \(\Delta_{\rm cp}/2\) again determines \(w\), and
the unique-mark promise again gives (2). This is not automatic for a path
follower that returns only a constant local-neighborhood point: the local
dual norm of the objective is \(\Theta(C)\) here, so a generic local-norm
guarantee must be tightened to \(O(\epsilon/C)\) to force ordinary scalar
error \(O(\epsilon)\).

## 5. Full explicit output is also query-linear

The unique reduced optimizer is

\[
                              t^*=-{\beta\over R_w}.                     \tag{23}
\]

For every feasible \(t\),

\[
 \|t-t^*\|_2^2
 \leq2(1-(t^*)^Tt)
 ={2\over R_w}\bigl(\beta^Tt-\operatorname{OPT}\bigr).                 \tag{24}
\]

Every coordinate of \(t^*\) has magnitude at least
\(1/(2\sqrt N)\). Since \(R_w\geq C/\sqrt5\), any explicit feasible output
of objective gap

\[
                             \epsilon<{C\over8\sqrt5N}                 \tag{25}
\]

obeys \(\|t-t^*\|_2<1/(2\sqrt N)\). Its coordinate signs recover every
hidden bit: \(t_i^*<0\) for \(b_i=0\) and \(t_i^*>0\) for \(b_i=1\).
Parity therefore gives an \(\Omega(N)\) quantum input-query lower bound,
in addition to the \(\Omega(N)\)-word dense-output cost. Reading all bits
and writing (23) matches it up to constants.

## 6. Why normalized state output is easy

The canonical normalized raw objective state is

\[
 |c_b\rangle={1\over\sqrt{10N}}\sum_{i=1}^N
   \bigl(|i,x\rangle+3(-1)^{b_i}|i,y\rangle\bigr).                       \tag{26}
\]

It is prepared by a public amplitude split and one phase query to \(b_i\).
Project each coordinate pair onto the public line
\((|x\rangle+|y\rangle)/\sqrt2\). The success probability is

\[
                        {\|\beta\|^2\over\|c\|^2}
                        ={4N-3w\over5N}\in[1/5,4/5].                    \tag{27}
\]

Conditioned on success, the remaining state is exactly
\(|\beta\rangle=\beta/R_w\); a heralded exact preparation therefore uses
constant expected queries. Fixed-point amplification gives a deterministic
constant-error preparation with \(O(1)\) queries. A public sign produces the
normalized optimizer state \(-|\beta\rangle\), and the normalized central
state is identical because (14) changes only its norm.

Thus a state-only output contract is constant-query easy even though both
the norm \(R_w\) and every classical scalar in Sections 2 and 4 are
query-linear for arbitrary strings. The state-preparation circuit does not
report its hidden success probability exactly; granting that probability or
the norm of the postselected state for free would grant the answer.

## 7. Exact access boundary

The raw interfaces covered by the theorem are:

- coefficient queries to either entry in (5);
- paired block queries returning the two entries of one \(c_i\);
- classical SQ access giving the public norm (6), the public squared-sampling
  law, and queried signed values; and
- the particular coherent preparation (26) and its canonical inverse.

Every call is simulated by at most one standard query to \(b_i\), so parity
and search lower bounds transfer with constant overhead. An arbitrary
unitary completion may not encode global information away from the specified
preparation subspace.

For the matching upper bound under the coherent interface, the specified
canonical completion is \(U_b=O_bU_{\rm pub}\), where \(U_{\rm pub}\) is
the public amplitude split and \(O_b\) is the phase query on the
\(|i,y\rangle\) coordinates.  Thus \(U_bU_{\rm pub}^{-1}=O_b\): one
preparation-oracle call exposes one ordinary coherent bit query, and
reading all bits takes \(N\) calls.  This equivalence is not asserted for
an unspecified black-box completion.

The following stronger interfaces are deliberately excluded:

1. free exact norm access to the equality-eliminated coefficient \(\beta\),
   because (9) then reveals \(w\);
2. free exact postselection probabilities in (27);
3. free exact norm or scalar access to the hidden central iterate; and
4. an oracle that directly returns the requested optimum or central scalar.

A data structure supplying any of the first three from raw access must pay
the lower bound during its construction. An online coordinate wrapper can
instead forward future reduced-coordinate queries to the raw source with
constant overhead; there is no preprocessing lower bound for that weaker
passthrough service.

## 8. Equivalent public-objective, hidden-sparse-constraint encoding

The same reduced instance can put all hidden data in the sparse equality
matrix. Let \(\sigma_i=(-1)^{b_i}\), keep the one-ball constraint (3), use
the entirely public objective pairs

\[
             c_i={C\over\sqrt{10N}}(1,3),
\]

and replace (4) by

\[
                        y_i=\sigma_i x_i\qquad(i\in[N]).                \tag{28}
\]

Write \(E_b\) for the equality matrix, with row \(i\) equal to
\((-\sigma_i,1)\) on the \(i\)-th coordinate pair. Its rows have disjoint
support and

\[
                  E_bE_b^T=2I_N.                                      \tag{29}
\]

Hence every row norm and every nonzero singular value is \(\sqrt2\), the
nonzero spectral condition number is one, every column has degree one and
norm one, and the sparsity pattern is public. Row sampling and squared-entry
sampling are public; only a queried sign carries \(b_i\). A coefficient,
row, or canonical coherent matrix-SQ query is simulated with one bit query.
For example, let the public completion \(V_{\rm pub}\) prepare the
normalized flattened baseline matrix state

\[
 {1\over\sqrt{2N}}\sum_i
       \bigl(-|i,x_i\rangle+|i,y_i\rangle\bigr),
\]

and let \(O_b^{(x)}\) apply phase \(\sigma_i\) to \(|i,x_i\rangle\).
The specified canonical completion is
\(V_b=O_b^{(x)}V_{\rm pub}\), and it prepares

\[
 {1\over\sqrt{2N}}\sum_i
       \bigl(-\sigma_i|i,x_i\rangle+|i,y_i\rangle\bigr)
\]

with one phase query. Conversely
\(V_bV_{\rm pub}^{-1}=O_b^{(x)}\), so the matrix-state interface and the
ordinary coherent bit oracle simulate one another with constant overhead.
This statement depends on the specified completion; arbitrary
off-subspace unitary completions are excluded.

An orthonormal nullspace coordinate is now hidden:

\[
                 (x_i,y_i)={t_i\over\sqrt2}(1,\sigma_i).                \tag{30}
\]

Projecting the public objective onto (30) gives

\[
 {C\over\sqrt{20N}}(1+3\sigma_i)
 =\begin{cases}
   2C/\sqrt{5N},&b_i=0,\\
   -C/\sqrt{5N},&b_i=1,
  \end{cases}                                                          \tag{31}
\]

exactly (8). Therefore every value, central-path, conditioning, and
explicit-output complexity conclusion above transfers. For the latter,
the distance proof gives the correct nonzero sign of every
\(t_i=\sqrt2x_i\), so \(\operatorname{sign}(x_i)\) directly recovers
\(b_i\); equivalently, exact feasibility gives
\(\sigma_i=\operatorname{sign}(x_iy_i)\). Thus the hidden nullspace basis
does not obstruct the decoder. The equality signs do not alter the star
representation or the treewidth-two augmented representation.

The solution-state separation also transfers. The public objective state
has pair amplitudes proportional to \((1,3)\). One query coherently
implements the pair basis whose null direction is
\((1,\sigma_i)/\sqrt2\); projection succeeds with the same probability
(27), and its normalized output is \(|\beta\rangle\). Thus a heralded
exact state still has \(O(1)\) expected queries, while a constant-error
state has \(O(1)\) worst-case queries. Applying the inverse hidden
pair-basis map uses one additional query and produces the normalized ambient
\((x,y)\) optimizer or central-point state, so the ambient-state contract is
also \(O(1)\).

The access caveat changes in an important and favorable way. The raw
objective and all of its SQ metadata are now public, but the nullspace
basis is hidden. A free classical description of (30) would reveal every
bit and is not part of the input oracle. It may instead be constructed at
\(\Theta(N)\) query cost or exposed as an online coherent basis-change
oracle, each call to which costs one raw equality/bit query. The scalar
lower bound is therefore a sparse-constraint query lower bound, not an
objective-readout artifact.

We use the affine SOCP representation \((1,z)\in Q_{2N+1}\), so \(E_b\)
is the whole homogeneous equality slice and has condition one. If the cone
axis is instead introduced as a variable with an additional row fixing
it to one, the combined equality operator has nonzero condition number
\(\sqrt2\), still a public constant.

## 9. QIPM interpretation and novelty screen

This example makes four quantities maximally different:

\[
\begin{array}{c|c}
\text{quantity}&\text{value or cost}\\ \hline
\text{ambient/reduced barrier parameter}&2/1\\
\text{selected reduced-Hessian condition}&\leq3/\sqrt5\\
\text{normalized optimizer or central state}&O(1)\text{ queries}\\
\text{optimum/central scalar at error }\epsilon&
 Q=\Theta(\min\{N,C/\epsilon\}),\quad
 R=\Theta(\min\{N,(C/\epsilon)^2\})\\
\end{array}                                                             \tag{32}
\]

In the first encoding the equality rows and nullspace basis are public and
perfectly conditioned. In the second the objective is public and the
equality matrix is sparse and perfectly conditioned, while its signs and
nullspace basis are hidden. In either case, the hard work is estimating the
norm of the projected objective to the requested precision, not solving the
Newton system. Thus neither a constant barrier parameter, bounded latent
treewidth, constant selected condition, nor easy solution-state preparation
controls classical scalar readout complexity.

The parity and Grover lower bounds are prior work; see
Beals--Buhrman--Cleve--Mosca--de Wolf,
<https://arxiv.org/abs/quant-ph/9802049>. The sharp approximate-counting
tradeoff is due to Nayak--Wu,
<https://arxiv.org/abs/quant-ph/9804066>, with the matching quantum upper
bound supplied by amplitude estimation; see Brassard--Høyer--Mosca--Tapp,
<https://arxiv.org/abs/quant-ph/0005055>. Apers--Gribling prove more general
Boolean reductions for additive-error LP optimum values under row-query and
quantum-inspired access, <https://arxiv.org/abs/2311.03215>. Existing QIPM
analyses explicitly distinguish quantum linear solving, tomography, and
classical output; for SOCP see Kerenidis--Prakash--Szilagyi,
<https://arxiv.org/abs/1908.06720>.

A targeted search found no prior one-Lorentz-cone theorem simultaneously
combining exact reduced barrier parameter one, a perfectly conditioned
two-sparse slice, constant selected Newton condition, raw-SQ-safe sign
balancing, constant-query solution-state preparation, and sharp
accuracy-parametric quantum and randomized optimum-value laws. The
public-objective/hidden-constraint encoding appears especially new. The
construction and combination appear new, but priority is not established
and specialist review remains necessary.

## 10. Same-instance bounded-Dikin path-length lower bound

The fixed reduced barrier also gives an actual movement lower bound for a
bounded-move model, rather than an inference from
\(\nu_{\rm red}=1\). Start at the analytic center \(t=0\), or within local
norm \(\rho<1\) of it. Fix a chord bound \(0<\mathcal R<1\) and an integer
\(m\geq1\). Suppose each of \(T\) outer rounds consists of at most \(m\)
feasible straight chords, each of starting-point Dikin norm at most
\(\mathcal R\). If the final point has ordinary objective gap at most
\(\epsilon\), then

\[
 T\geq
 {\left[
 \log\!\left({C\over2\sqrt5\,\epsilon}\right)
 -\log{1\over1-\rho}\right]_+
 \over m\log{1\over1-\mathcal R}}.                                    \tag{33}
\]

To prove this, put \(q(t)=1-\|t\|^2\) and
\(d=-\beta/R_w\). The gap is
\(g=R_w(1-d^Tt)\), so feasibility gives
\[
 q(t)\leq1-(d^Tt)^2\leq {2g\over R_w}.
\]
Moreover the Hessian (17) satisfies, in every direction,
\[
 \|\dot t\|_{t}^{\,2}\geq
       \left({d\over ds}\log q(t+s\dot t)\big|_{s=0}\right)^2.
\]
Thus the barrier-metric distance from the analytic center to the
\(\epsilon\)-accurate set is at least
\([\log(R_w/(2\epsilon))]_+\), which is bounded below using
\(R_w\geq C/\sqrt5\). A Dikin chord of starting norm at most
\(\mathcal R\) has metric length at most
\(-\log(1-\mathcal R)\), and the approximate start costs at most
\(-\log(1-\rho)\). Summing the chord lengths proves (33).

At normalized accuracy \(\epsilon/C=\Theta(1/N)\), this gives
\(\Omega_{\rho,\mathcal R,m}(\log N)\) bounded-Dikin rounds on the same
instances whose scalar and sufficiently accurate explicit output require
\(\Theta(N)\) queries. These are simultaneous lower bounds and must not be
multiplied. Equation (33) applies only to feasible primal chord
trajectories for the fixed restricted barrier; it does not cover long
steps, custom barriers, higher-order arcs not decomposed into counted
chords, or arbitrary QIPMs.

## 11. Scope

1. Equation (1) is a total formulation-query/output lower bound. It cannot
   be multiplied by a path iteration count.
2. The fixed checkpoint result requires explicit scalar accuracy; a constant
   local-neighborhood guarantee alone is insufficient.
3. The full cone has growing dimension. Under a fixed Lorentz block cap, the
   structural and reduced-barrier ledgers change and must be analyzed using
   the separate capped product-ball theorems.
4. The proof is exact-arithmetic. Objective coefficients have magnitude
   \(\Theta(C/\sqrt N)\), and hidden equality coefficients are only signs.
   For \(C=N\), \(O(\log N)\) ordinary precision bits suffice for constant
   relative accuracy. Scaling the objective is what turns the adjacent norm
   gap into a fixed additive constant; with \(C=1\), the same hardness is
   expressed as inverse-linear output precision. No ambient
   indefinite-KKT bit-stability theorem is claimed.

## Independent hostile audit

The auditor rederived both equality eliminations, projected coefficients,
public norm and sampling laws, optimum ledger, and the general minimum
adjacent spacing \(3C/(4\sqrt5N)\). It checked the inverse-Lipschitz
reduction to approximate counting, the quantum and randomized all-regime
laws, and the parity and unique-mark endpoints with their separate error
thresholds.

For the path calculation, the audit solved the radial central equation,
verified the Hessian eigenvalues and the bound
\(\kappa\leq3/\sqrt5\), and distinguished this reduced positive-Hessian
condition number from an indefinite-KKT convention.  The
diagonal-plus-rank-one solve and its star latent representation give linear
arithmetic and treewidth one; retaining the pair equalities gives
treewidth at most two. The central scalar derivative bound,
explicit-output sign recovery, and every numerical constant in Sections
4--5 also checked.

Finally, the auditor verified the raw-state normalization, success
probability \((4N-3w)/(5N)\), heralded exact versus bounded-query
constant-error state guarantees, and constant-overhead simulation in both
directions for each specified canonical completion. It also checked
\(E_bE_b^T=2I\), the hidden-basis coherent projection, and the ambient
feasible-output decoder. The theorem does not grant a projected norm, a
postselection probability, a hidden scalar, a hidden classical nullspace
basis, or an arbitrary unitary completion.

A separate hostile audit checked the same-instance Dikin corollary:
objective gap implies \(q\leq2\epsilon/R_w\), the Hessian dominates the
squared differential of \(\log q\), and bounded-chord lengths give exactly
(33), including the approximate-start subtraction. It confirmed that this
is a fixed-barrier feasible-trajectory statement and is not multiplied by
the formulation-query lower bound.
