# Product-disk central-readout query hierarchy

**Status.** Proved; independently hostile-audited; targeted literature
screen completed. Apparent novelty requires specialist priority review.

## Main result

There is a separable SOCP over
\[
                         C=(B_2^2)^N
\]
with one direct \(Q_3\) block per disk such that:

1. every central-path Newton Hessian has a dimension-independent condition
   number, and its graph is a disjoint union of constant-size components;
2. at one fixed public central multiplier, a fixed scalar affine readout
   requires \(\Omega(N)\) quantum queries at constant additive accuracy;
3. a full explicit constant-suboptimality optimizer also requires
   \(\Omega(N)\) quantum queries;
4. nevertheless the normalized central-point state is exactly preparable
   with one hidden-bit query.

The randomized query lower bounds in items 2--3 are also \(\Omega(N)\).
Querying all \(N\) bits gives matching upper bounds, so the arbitrary-input
scalar and explicit-output laws are \(\Theta(N)\) in both models.
Under the zero-versus-one-mark promise, the scalar-readout bounds are the
tight \(\Theta(\sqrt N)\) quantum and \(\Theta(N)\) randomized bounds.

Thus bounded cone size, disconnected block structure, bounded Newton
condition, and even trivial central-state preparation do not make accurate
classical scalar readout sublinear. Sections 1--7 are data-query/readout
theorems, not IPM iteration lower bounds. Section 8 separately proves a
path-length lower bound for bounded-Dikin feasible trajectories on one
fixed packed-PSD lift and standard barrier; it is not a general IPM or QIPM
iteration lower bound.

## 1. Full product-disk family

Let \(b=(b_1,\ldots,b_N)\in\{0,1\}^N\), and define
\[
 c_i(b_i)=
 \begin{cases}
   e_1,&b_i=0,\\
   -e_2,&b_i=1.
 \end{cases}
                                                               \tag{1}
\]
Consider
\[
 \operatorname*{minimize}_{z_i\in B_2^2}
                  \sum_{i=1}^N c_i(b_i)^Tz_i.                  \tag{2}
\]
Equivalently, \((1,z_i)\in Q_3\) for every \(i\). Each objective block has
norm one, the global objective norm is \(\sqrt N\), and all constraint and
cone data are public.

For the direct reduced barrier
\[
                  F(z)=-\sum_{i=1}^N\log(1-\|z_i\|_2^2),       \tag{3}
\]
the central point at multiplier \(\eta\geq0\) is
\[
 z_i(\eta)=-r(\eta)c_i(b_i),\qquad
 r(\eta):=\frac{\eta}{\sqrt{1+\eta^2}+1}.                     \tag{4}
\]
Indeed, stationarity along \(-c_i\) is
\[
                       \eta=\frac{2r}{1-r^2}.
\]

At a vector of radius \(r\), the block Hessian is
\[
 \nabla^2[-\log(1-\|z\|^2)]
 =\frac{2}{1-r^2}I+\frac{4}{(1-r^2)^2}zz^T.                  \tag{5}
\]
Its transverse eigenvalue is \(2/(1-r^2)\), and its radial-to-transverse
ratio is
\[
 \frac{1+r^2}{1-r^2}=\sqrt{1+\eta^2}.                        \tag{6}
\]
All blocks have the same radius. Consequently
\[
 \boxed{\ \kappa(\nabla^2F(z(\eta)))=\sqrt{1+\eta^2}\ }       \tag{7}
\]
for every \(N\). At the fixed public checkpoint
\[
             \eta_0=2,\qquad r_0=r(2)=\frac{\sqrt5-1}{2},
                                                                    \tag{8}
\]
the condition number is exactly \(\sqrt5\).

At the checkpoint itself, (5) is diagonal in the coordinate basis because
each \(z_i\) lies on a coordinate axis. Its actual scalar graph has
treewidth zero. The fixed structural Hessian supergraph is a disjoint union
of two-vertex cliques and has treewidth one. The direct conic
Newton/KKT graph likewise has only constant-size disconnected components.

The reduced barrier parameter in (3) is exactly
\(\nu_{\rm red}=N\). The direct ambient product \(Q_3^N\) has
\[
                 L=N,\qquad D_{\rm ambient}=3N,\qquad
                 \nu_{\rm ambient}=2N.                       \tag{9}
\]
These are the one-\(Q_3\)-per-disk counts. The separate full-product
factorization argument also proves that \(L=N\) is minimal among globally
labelled analytic full-slack factorizations through \(Q_3\) factors. Indeed,
for the full extreme slack rows
\[
                 S_a(x,z)=1-x_a^Tz,qquad
                 x\in(S^1)^N, z\in S^1,
\]
the cylindrical-zero continuation argument assigns every productive
channel to at most one source disk. The diagonal mixed form for disk \(a\)
has rank one, so at least one productive \(Q_3\) channel is assigned to that
disk. The productive channel sets are disjoint, giving \(L\geq N\), and the
direct construction attains equality. Unlike the higher-dimensional
\(Q_3\) theorem, no additional sphere-to-circle phase obstruction is needed
when the contact circle itself has dimension one. The query proof below
needs only the explicit direct representation, not this analytic
minimality.

Consequently the arbitrary-input scalar theorem below has the exact law
\[
        Q_2=\Theta(\nu_{\rm red}),\qquad
        R_2=\Theta(\nu_{\rm red}).                           \tag{9a}
\]
This identity is a property of the explicit family, not an inference that a
barrier parameter is generally an iteration or query lower bound.

In particular, the underlying domain in Sections 1--5 is the full product
of disks, before any instance-dependent objective is chosen. The sliced
variant in Section 6 is a different optimization family: after its public
equality elimination it is a product of intervals and may admit a smaller
LP description, so full-product disk minimality must not be attributed to
that reduced problem.

## 2. A hard scalar at a finite central multiplier

Write \(w=|b|\). From (1) and (4),
\[
 x_i(\eta)=
 \begin{cases}
   -r(\eta),&b_i=0,\\
   0,&b_i=1.
 \end{cases}
\]
Define the fixed public linear readout
\[
             P_\eta(z):=Nr(\eta)+\sum_{i=1}^N x_i.           \tag{10}
\]
At the exact central point,
\[
                         P_\eta(z(\eta))=r(\eta)w.            \tag{11}
\]
In particular, at the finite checkpoint (8),
\[
                         P_{\eta_0}=r_0w.                    \tag{12}
\]

An additive-\(r_0/2\) estimate of (12) determines the integer \(w\) exactly
by rounding and therefore computes \(\operatorname{PARITY}(b)\). Since
bounded-error quantum query complexity of parity is \(\lceil N/2\rceil\),
and randomized query complexity is \(N\), evaluating this single scalar has
\[
              Q_2(P_{\eta_0})=\Omega(N),\qquad
              R_2(P_{\eta_0})=\Omega(N).                     \tag{13}
\]
The lower bound holds at fixed \(\eta_0\) and fixed condition
\(\sqrt5\); no near-boundary limiting argument is involved.

Under the promise \(w\in\{0,1\}\), (12) is either zero or \(r_0\).
Consequently its bounded-error complexities are
\[
              \Theta(\sqrt N)\ \text{quantum},\qquad
              \Theta(N)\ \text{randomized}.                 \tag{14}
\]
The upper bounds use Grover search or classical scanning.

The centering term \(Nr_0\) in (10) is public. It removes an extensive
all-zero baseline, so the unique-OR readout itself has an \(N\)-independent
gap. If one instead normalizes the functional to operator norm one, the
required additive precision becomes \(\Theta(N^{-1/2})\); this equivalent
precision accounting must not be hidden.

## 3. Full explicit optimizer output

The unique optimum of each disk block in (2) is
\[
                           z_i^*=-c_i(b_i).                  \tag{15}
\]
For every feasible \(z_i\),
\[
 \|z_i+c_i\|_2^2
 =\|z_i\|_2^2+1+2c_i^Tz_i
 \leq 2(1+c_i^Tz_i).                                       \tag{16}
\]
The total objective gap is
\[
                       \sum_i(1+c_i^Tz_i).                  \tag{17}
\]
If (17) is less than \(1/8\), then every block obeys
\[
                         \|z_i-z_i^*\|_2<1/2.               \tag{18}
\]
The two possible prototypes, \(-e_1\) and \(+e_2\), have distance
\(\sqrt2\). Nearest-prototype decoding of an explicit output satisfying
(18) therefore recovers every \(b_i\). Computing parity of the recovered
string proves
\[
 \boxed{\ \Omega(N)\ \text{quantum and randomized input queries for a
 full explicit \(1/8\)-suboptimal solution.}\ }              \tag{19}
\]
This is stronger than the elementary \(\Omega(N)\) time needed to write
\(N\) coordinates: (19) is an input-query lower bound.

At the exact optimum the scalar
\[
                            N+\sum_i x_i^*=w                 \tag{20}
\]
gives the same scalar-readout hierarchy as (12). Notice that the optimum
objective value itself is always \(-N\); (20) is a fixed solution
observable, not the optimum value.

## 4. Why state-only output is easy

The normalized absolute central point is
\[
 \frac{z(\eta)}{\|z(\eta)\|}
 =-\frac1{\sqrt N}\sum_{i=1}^N |i\rangle|c_i(b_i)\rangle,   \tag{21}
\]
independently of \(\eta>0\). A single coherent query to \(b_i\), together
with public controlled gates, prepares (21) exactly. The same is true at
the optimum.

Therefore no query lower bound for merely producing the normalized
absolute solution state follows from (13) or (19). Estimating (10) from
that state to the stated additive error requires resolving an
\(O(1/N)\) population fraction in the unique-mark case; state preparation
and accurate scalar extraction are different tasks.

A normalized state of the **centered correction** relative to the all-zero
path would be \(|j\rangle\) under the unique-mark promise and would inherit
the \(\Theta(\sqrt N)\) search bound. That is a different output contract
from the absolute central-point state.

## 5. Oracle accounting

For coefficient or block access, one query to block \(i\) is exactly one
query to \(b_i\). A squared-coordinate SQ sampler chooses a uniform block
and returns its occupied axis; it can be simulated with one hidden-bit
query. The norm is the public value \(\sqrt N\).

A canonical coherent preparation unitary is
\[
 |0\rangle\longmapsto
 \frac1{\sqrt N}\sum_i |i\rangle
 \begin{cases}
   |e_1\rangle,&b_i=0,\\
   |-e_2\rangle,&b_i=1,
 \end{cases}                                                \tag{22}
\]
and it and its canonical inverse each use one standard bit-oracle query.
Thus every allowed coefficient, block, vector-SQ, or canonical coherent-SQ
call is simulated with \(O(1)\) queries to \(b\), so the parity and search
lower bounds transfer.

There are three essential qualifications.

1. If an interface reports the exact aggregate norm of the first-coordinate
   subvector, then it reports \(\sqrt{N-w}\) and leaks \(w\). Ordinary vector
   SQ reports the global norm, not arbitrary group norms.
2. Free exact SQ/norm access to the hidden-dependent central iterate can
   likewise leak \(w\). The theorem starts from raw formulation access; it
   does not grant a compiled trajectory oracle.
3. An arbitrary unitary completion whose unspecified action is allowed to
   encode global information about \(b\) invalidates any black-box lower
   bound. Equation (22) fixes the canonical completion used in the
   reduction.

## 6. A sign-balanced sliced variant with hard optimum value

The full-disk family makes a central/optimizer readout hard, but its optimum
value is the public constant \(-N\). A second variant makes the optimum
value itself hard while preserving all raw SQ magnitude metadata.

Impose the public slice \(y_i=x_i\), and use
\[
              \widetilde c_i(b_i)
       =\frac1{\sqrt{10}}\bigl(1,3(-1)^{b_i}\bigr).          \tag{23}
\]
With the orthonormal coordinate
\[
              (x_i,y_i)=\frac{t_i}{\sqrt2}(1,1),
\]
the problem reduces to
\[
 \min_{t\in[-1,1]^N}\sum_i\alpha_i(b_i)t_i,\qquad
 \alpha_i(0)=p:=\frac2{\sqrt5},\quad
 \alpha_i(1)=-q:=-\frac1{\sqrt5}.                           \tag{24}
\]
All raw block norms, coordinate magnitudes, sampling probabilities, and
even the two aggregate coordinate-column norms are independent of \(b\).
Only a queried sign depends on the hidden bit.

For \(w=|b|\),
\[
       v^*(b)=-(N-w)p-wq
              =-\frac{2N}{\sqrt5}+\frac{w}{\sqrt5}.         \tag{25}
\]
Hence additive error below \(1/(2\sqrt5)\) determines \(w\), proving
\(\Omega(N)\) quantum and randomized query lower bounds for the scalar
optimum value itself. Under \(w\in\{0,1\}\), the corresponding bounds are
\(\Theta(\sqrt N)\) and \(\Theta(N)\).

The reduced barrier is
\[
                         -\sum_i\log(1-t_i^2).
\]
At multiplier \(\eta\),
\[
 t_i(\eta)=
 \begin{cases}
  -r(\eta p),&b_i=0,\\
  +r(\eta q),&b_i=1,
 \end{cases}
\qquad
 h(a)=\sqrt{1+a^2}\bigl(\sqrt{1+a^2}+1\bigr),              \tag{26}
\]
where \(h(a)\) is the scalar barrier Hessian at the stationary point with
force \(a\). Since \(p/q=2\),
\[
                   \kappa\leq\frac{p^2}{q^2}=4
                   \qquad\text{for every }\eta\geq0.        \tag{27}
\]

At the explicit public checkpoint
\[
                         \eta_1=2\sqrt5,
\]
we have \(\eta_1p=4\), \(\eta_1q=2\), and the centered linear-objective
readout is
\[
 \begin{aligned}
  S_b
    &:=L_b(\eta_1)+Np\,r(4)
      =w\Delta_{\rm cp},\\
  \Delta_{\rm cp}
    &:=\frac1{\sqrt5}\bigl(2r(4)-r(2)\bigr)
      =\frac{\sqrt{17}-\sqrt5}{2\sqrt5}
      \approx0.42195.                                      \tag{28}
 \end{aligned}
\]
Thus the finite-checkpoint scalar also has the parity/search hierarchy with
a fixed additive gap.

If an algorithm is instead granted the exact norm of the already reduced
coefficient vector, then
\[
                 \|\alpha\|^2=(N-w)p^2+wq^2
\]
reveals \(w\) for free. This derived oracle is strictly stronger than raw
SQ access in (23), and is excluded.

## 7. Raw-norm/accuracy law and the product-versus-direct boundary

The sign-balanced sliced family has a useful exact rescaling. Let
\(\Gamma>0\) be the public raw objective norm and multiply every block in
(23) by \(\Gamma/\sqrt N\). Then

\[
 v_\Gamma^*(b)
   =-{2\Gamma\sqrt N\over\sqrt5}
     +{\Gamma\over\sqrt{5N}}w.                              \tag{29}
\]

Consequently additive value error \(\epsilon\) is equivalent, up to the
fixed factor \(\sqrt5\), to Boolean-mean error
\(\delta=\epsilon/(\Gamma\sqrt N)\). Standard approximate counting gives,
for \(0<\epsilon\leq c_0\Gamma\sqrt N\),

\[
 \boxed{
 Q=\Theta\!\left(\min\left\{N,{\Gamma\sqrt N\over\epsilon}\right\}\right),
 \qquad
 R=\Theta\!\left(\min\left\{N,{\Gamma^2N\over\epsilon^2}\right\}\right).
 }                                                               \tag{30}
\]

These are bounded-error worst-case query laws under coefficient, paired
block, classical vector-SQ, and the following specified canonical coherent
access. The normalized sliced-objective state is
\[
 |c_b\rangle={1\over\sqrt{10N}}\sum_i
       \bigl(|i,x\rangle+3(-1)^{b_i}|i,y\rangle\bigr).
\]
Its global norm, squared-sampling law (uniform \(i\), followed by \(x\) or
\(y\) with probabilities \(1/10,9/10\)), and all magnitudes are public.
Writing \(U_b=O_bU_{\rm pub}\), where \(O_b\) phases only the
\(|i,y\rangle\) branch, specifies a completion for which \(U_b\), its
inverse, and the ordinary coherent bit oracle simulate one another with
constant overhead. Arbitrary off-subspace completions and a free exact norm
of the reduced objective remain excluded.

Equivalently, all hidden signs can be moved out of the objective and into
the sparse slice. Use the entirely public pairs
\[
              c_i={\Gamma\over\sqrt{10N}}(1,3)
\]
and impose \(y_i=(-1)^{b_i}x_i\). The hidden equality matrix has disjoint
rows \(( -(-1)^{b_i},1)\), hence \(EE^T=2I\), condition one, public row
norms and singular values, public column degrees, and a public squared-SQ
sampling law. For coherent matrix access, specify the public completion
\(V_{\rm pub}\) preparing
\[
 {1\over\sqrt{2N}}\sum_i(-|i,x_i\rangle+|i,y_i\rangle)
\]
and \(V_b=O_b^{(x)}V_{\rm pub}\), where \(O_b^{(x)}\) phases the
\(x_i\) branch by \((-1)^{b_i}\). Then
\(V_bV_{\rm pub}^{-1}=O_b^{(x)}\), giving constant-overhead equivalence
with bit queries. Arbitrary unitary completions are excluded.

In the hidden orthonormal coordinate
\[
       (x_i,y_i)={t_i\over\sqrt2}(1,(-1)^{b_i}),
\]
the projected coefficient is again \(2\Gamma/\sqrt{5N}\) or
\(-\Gamma/\sqrt{5N}\). Thus (29)--(31), including their query laws and
state/full-output separation, transfer exactly. At the optimizer the
ambient pair is \((-(-1)^{b_i},-1)/\sqrt2\); at the checkpoint it is
\((-r(4),-r(4))/\sqrt2\) or \((r(2),-r(2))/\sqrt2\). These states use
one queried controlled pair preparation, with constant-overhead
postselection only for the unequal central amplitudes. A gap below
\(\Gamma/\sqrt{5N}\) fixes the sign of every \(x_i\) and decodes all bits.
A canonical coherent basis change costs one equality-sign query. Its
classical materialization, the exact reduced norm, and exact projection
success probability are not free because they reveal the hidden statistic.
This makes (30) a sparse-constraint lower bound with a completely public
objective as well as an objective-query lower bound in the original
encoding.

The upper bounds estimate \(w/N\) by amplitude estimation or sampling and
are capped by reading all bits. The matching lower bounds are
the Nayak--Wu additive-counting bound and the standard randomized
Bernoulli/Yao bound, with monotonicity giving the saturated regimes. At the
exact-count endpoint, adjacent values in (29) are separated by
\(\Gamma/\sqrt{5N}\), and parity supplies the cap directly.

The finite central checkpoint rescales without changing this law. Taking
\[
                       \eta_\Gamma={2\sqrt{5N}\over\Gamma}
\]
keeps the two effective radial forces equal to four and two. After
subtracting the public all-zero baseline, the per-mark central-value gap is
\[
 {\Gamma\over\sqrt N}\,
 {\,\sqrt{17}-\sqrt5\,\over2\sqrt5},                         \tag{31}
\]
so the same inverse map to \(w/N\) proves (30) for the exact checkpoint
scalar. All block Hessians remain uniformly conditioned by (27).

The normalized optimizer state is a uniform signed superposition and is
exactly one-query preparable. The normalized central state has two public
per-bit amplitudes; postselection has probability bounded away from zero
and one, so it is heralded-exact in \(O(1)\) expected queries and
constant-error in \(O(1)\) worst-case queries. In contrast, any explicit
feasible optimizer of objective gap below
\(\Gamma/\sqrt{5N}\) has the correct sign in every interval and recovers
all \(N\) bits.

Equation (30) gives an exact normalized-precision phase boundary. Writing
\(\rho=\epsilon/\Gamma\), quantum scalar readout saturates at \(N\) queries
once \(\rho\lesssim N^{-1/2}\). For the one-direct-ball construction in
[the companion theorem](2026-09-04-one-lorentz-constant-barrier-value-lower.md),
the corresponding laws are
\[
 Q=\Theta(\min\{N,1/\rho\}),\qquad
 R=\Theta(\min\{N,1/\rho^2\}),
\]
so quantum saturation occurs only at \(\rho\lesssim N^{-1}\). Thus, at the
same raw norm \(\Gamma=\sqrt N\) and fixed additive accuracy, the displayed
direct \(Q_3^N\) sliced host has \(Q=\Theta(N)\), whereas the direct-ball
host has \(Q=\Theta(\sqrt N)\); both have \(R=\Theta(N)\) and
constant-query normalized solution states. This is a comparison between
two different feasible geometries, not a formulation separation for the
same optimization problem. It nevertheless isolates a sharp
product-versus-direct readout boundary: \(\nu_{\rm red}=N\) versus one
coincides here with a half-power shift in \(N\) in the quantum saturation precision,
but the query law is proved by counting and is not inferred from the
barrier parameter. Since the public slice reduces the feasible set to a
product of intervals, full-product analytic minimality is not claimed for
this particular sliced optimization problem.

## 8. One-factor PSD synthesis: iteration, state, and readout on one instance

The unsliced family in Sections 1--5 can instead be represented by one
real PSD factor. Put the disk vectors into the columns of
\(W\in\mathbb R^{2\times N}\), introduce \(S\in\mathbb S^N\), and impose

\[
 Z=\begin{pmatrix}S&W^T\\W&I_2\end{pmatrix}\succeq0,\qquad
 S_{ii}=1,\qquad D:=S-W^TW.                                  \tag{32}
\]

This projects exactly onto \((B_2^2)^N\). Use the restricted standard
log-determinant on the relative-open barrier domain \(Z\succ0\):
\[
                           F(S,W)=-\log\det D.                \tag{33}
\]
Although (32) has one PSD cone factor of order \(N+2\), partial minimization
over \(S\) gives
\[
             \bar F(W)=-\sum_i\log(1-\|w_i\|^2),\qquad
             \nu_{\rm slice}=N.                              \tag{34}
\]
At every auxiliary-centered point, an exact residual-coordinate
elimination makes the bordered Newton graph a forest of \(N\) stars.
Thus its latent treewidth is one and the exact projected Newton solve costs
\(O(N)\) arithmetic, even though the naive lifted Hessian is dense; see the
[packing-invariant Newton-forest theorem](2026-09-04-psd-column-packing-newton-forest.md).
No \(O(N)\) bound is claimed for materializing a dense full lifted
direction or state.

Set the maximizing directions in the packed formulation to
\(\widetilde c_i=-c_i(b_i)\). Its exact central path has
\[
 W_i(\tau)=r(\tau)\widetilde c_i=-r(\tau)c_i(b_i),\qquad
 D(\tau)={2\over\sqrt{1+\tau^2}+1}I_N.                       \tag{35}
\]
Hence it is the same projected path as (4). The fixed-checkpoint scalar,
the one-query normalized projected central state, and the
\(\Omega(N)\) query lower bound for a projected \(1/8\)-suboptimal
explicit solution all transfer verbatim. The qualifier “projected” is
essential for the state claim: the auxiliary center
\(S=W^TW+D\) contains a dense hidden Gram matrix, and no one-query
preparation of a normalized full \((S,W)\) state is asserted.

This same formulation also has a genuine path-length lower bound for its
fixed standard barrier. Start at the public analytic center
\(W=0,D=I_N\). Fix \(0\leq\rho<1\), \(0<R<1\), and an integer \(m\geq1\).
Suppose the initial feasible point is within center local norm \(\rho\), and
each of \(T\) outer rounds consists of at most \(m\) feasible chords, each
of starting-point Dikin norm at most \(R\). If the final minimizing
objective gap is at most \(\epsilon\), then

\[
 T\geq
 {\left[
 \sqrt N\log\!\left({N\over2\epsilon}\right)
 -\log{1\over1-\rho}\right]_+
 \over m\log{1\over1-R}}.                                  \tag{36}
\]

Indeed the minimizing block gap
\(1+c_i^Tw_i\) is exactly the maximizing gap
\(1-\widetilde c_i^Tw_i\), so the audited one-factor packed-PSD
[determinant-distance theorem](2026-09-04-psd-packing-geodesic-iteration-lower-bound.md)
applies with \(b=H=N\) and \(q_0=1\).
At \(\epsilon=1/16\), (36) is
\(\Omega_{\rho,R,m}(\sqrt N\log N)\), while full projected output and the
fixed scalar still cost \(\Theta(N)\) input queries and the normalized
projected central state still costs one query.

These costs are simultaneous obstructions on one formulation:
\[
 L=1,\quad \nu_{\rm slice}=N,\quad
 T_{\rm bounded\text{-}Dikin}=\Omega(\sqrt N\log(N/\epsilon)),\quad
 Q_{\rm scalar/full}=\Omega(N)\ \text{at the stated fixed accuracies},
 \quad Q_{\rm projected\ state}=1.
\]
They must not be multiplied. Equation (36) is restricted to feasible
primal trajectories for the fixed standard log-determinant, with bounded
chords and a bounded number of substeps per round. It does not cover long
steps, custom barriers, nontrajectory quantum algorithms, or arbitrary
QIPMs.

### Public-objective sparse-constraint strengthening

The Section 7 hidden-equality encoding can be placed in the same one-factor
PSD lift (32). Add the disjoint rows
\(y_i=(-1)^{b_i}x_i\) and use the public objective pairs
\(\Gamma(1,3)/\sqrt{10N}\). All hidden formulation data are now signs in a
condition-one, two-sparse equality slice; the PSD affine map and objective
are public. Partial minimization and equality elimination give
\[
                   -\sum_i\log(1-t_i^2),
\]
so the exact restricted parameter is still \(N\). After this hidden
orthonormal equality elimination, the residual Newton graph is a forest.
If the equality multipliers are retained, constant-size bags give
treewidth at most two. Both forms have \(O(N)\) exact projected arithmetic,
although materializing the hidden basis itself costs \(N\) input queries.
The optimizer, checkpoint, scalar, state, and explicit-output conclusions
in Section 7 all hold on this one-factor formulation.

The bounded-Dikin movement lower bound also survives, now by a direct
weighted determinant proof. Let
\[
 a_i=|\beta_i|\geq{\Gamma\over\sqrt{5N}},\qquad
 g_i=a_i(1-s_it_i)\geq0
\]
be the coefficient magnitude and individual objective gap, where
\(s_it_i=1\) at the optimum. If \(\sum_i g_i\leq\epsilon\), then
\[
 D_{ii}=1-t_i^2
 \leq {2g_i\over a_i}.
\]
Hadamard's determinant inequality and AM--GM give
\[
 \det D
 \leq\prod_i{2g_i\over a_i}
 \leq\left({2\sqrt5\,\epsilon\over\Gamma\sqrt N}\right)^N. \tag{37}
\]
For the one \(N\)-column PSD block, the log-determinant Hessian makes every
path length at least
\(|\Delta\log\det D|/\sqrt N\). Starting at \(D=I_N\), the same
bounded-chord conversion as in (36) therefore yields
\[
 T\geq
 {\left[
 \sqrt N\log\!\left({\Gamma\sqrt N\over2\sqrt5\,\epsilon}\right)
 -\log{1\over1-\rho}\right]_+
 \over m\log{1\over1-R}}.                                  \tag{38}
\]

At \(\Gamma=\sqrt N\) and fixed sufficiently small \(\epsilon\), this
single public-objective sparse-data formulation simultaneously has one PSD
factor, \(\nu_{\rm slice}=N\), latent projected treewidth one,
\(\Omega_{\rho,R,m}(\sqrt N\log N)\) bounded-Dikin rounds,
\(Q=R=\Theta(N)\) scalar and projected explicit-output queries, and \(O(1)\)
normalized projected-state queries. Again these costs are not multiplied,
and no easy full lifted-state claim is made.

## 9. Scope and literature position

Sections 1--7 are query/readout and explicit-output lower bounds. Their
cost cannot be multiplied by the number of central-path steps. Section 8
does prove a separate iteration lower bound for the explicitly restricted
fixed-logdet bounded-Dikin-chord model, but not for arbitrary IPMs or QIPMs.
None of the results contradict fast quantum state preparation, because
(21) is explicitly one-query preparable for the projected variables.

For the sign-balanced sliced family, reading all input signs and evaluating
(25) gives the matching \(O(N)\) upper bound. Thus constant-additive
optimum-value estimation has the exact no-advantage law
\[
 Q_2=\Theta(N)=\Theta(\nu_{\rm red}),\qquad
 R_2=\Theta(N)=\Theta(\nu_{\rm red}),
\]
under the stated arbitrary-string promise and raw formulation interface.
The Newton solves are not the source of this cost: after the public slice
elimination they are diagonal and take \(O(N)\) classical arithmetic over
the whole vector.

The fixed additive accuracy in (12), (20), (25), and (28) is
\(O(1/N)\) relative to an extensive uncentered baseline. The centered
unique-OR observables have a constant absolute gap, but a norm-one
normalization of the readout moves the dependence into the requested
precision.

A conventional path follower that returns only a point in a constant local
neighborhood is not automatically required to approximate (10) or (28) to
constant additive error. At fixed \(\eta\), the dual local norm of the
corresponding extensive linear functional is \(\Theta(\sqrt N)\).
Consequently, a generic local-norm error bound must be
\(O(N^{-1/2})\), rather than merely \(O(1)\), to force the scalar accuracy
used in (13). The scalar theorem applies to algorithms whose output contract
explicitly asks for that observable to the stated precision (or whose center
accuracy is strong enough to imply it).

The query ingredients are classical. Beals--Buhrman--Cleve--Mosca--de Wolf
prove the exact \(N/2\) bounded-error quantum query complexity of parity;
the standard unstructured-search lower bound gives \(\Omega(\sqrt N)\).
Recent quantum LP work also proves additive-error optimum-value lower bounds
by Boolean-function reductions. A targeted search did not find the
product-disk finite-central-checkpoint construction, its simultaneous
dimension-independent conditioning, the raw-SQ oracle accounting, or the
state-versus-scalar hierarchy. A second targeted search did not find the
one-factor PSD synthesis combining exact projected Newton sparsification,
one-query projected state preparation, linear readout hardness, and a
bounded-Dikin log-determinant path lower bound on the same instance.
Novelty is plausible only for these combinations.

Primary query reference:

* R. Beals, H. Buhrman, R. Cleve, M. Mosca, and R. de Wolf,
  [Quantum Lower Bounds by Polynomials](https://arxiv.org/abs/quant-ph/9802049).
* A. Nayak and F. Wu,
  [The quantum query complexity of approximating the median and related
  statistics](https://arxiv.org/abs/quant-ph/9804066).
* G. Brassard, P. Høyer, M. Mosca, and A. Tapp,
  [Quantum Amplitude Amplification and
  Estimation](https://arxiv.org/abs/quant-ph/0005055).

Related oracle-interrogation reference:

* W. van Dam,
  [Quantum Oracle Interrogation: Getting All Information for Almost Half the
  Price](https://arxiv.org/abs/quant-ph/9805006).

Adjacent quantum-IPM/optimal-value Boolean-reduction reference:

* S. Apers and S. Gribling,
  [Quantum speedups for linear programming via interior point
  methods](https://arxiv.org/abs/2311.03215).
