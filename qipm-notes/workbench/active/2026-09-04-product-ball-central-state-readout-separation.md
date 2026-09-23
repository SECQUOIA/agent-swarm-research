# Product-ball central states: trivial preparation, Grover-hard readout, and treewidth-one Newton systems

Status: Proved; targeted literature screen and independent hostile audit completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and the raw-query adversary bound; moderate on novelty

## Main theorem

Fix an even integer \(s\geq4\), a number of source balls \(B\geq1\), and
a Lorentz block cap \(d\geq3\).  Put

\[
 \ell_d=\begin{cases}
 \left\lceil s/(d-2)\right\rceil,&3\leq d<s+1,\\
 1,&d\geq s+1.
 \end{cases}                                                \tag{1}
\]

There is an indexed family of linear objectives over

\[
                         C=(B_2^s)^B                         \tag{2}
\]

with the following simultaneous properties.

1. In the globally labelled analytic full-slack factorization class, the
   cap-optimal Lorentz formulation has \(B\ell_d\) cone blocks. Its optimal
   ambient logarithmically homogeneous barrier parameter is \(2B\ell_d\),
   while its standard reduced barrier has exact parameter \(B\ell_d\).
2. The exact reduced Newton graph has latent treewidth one and
   \(O(B(s+\ell_d))\) vertices and edges.  At the central point used below,
   an explicit diagonal rescaling makes the equality-restricted barrier
   Hessian have condition number at most \(27/2\), independently of
   \(B,s,d\).  For the direct-ball branch \(d\geq s+1\), the sharper bound is
   \(5/3\).
3. The normalized quantum state of the complete primal \(w\)-part of that
   exact central point can be prepared with one query to the canonical
   objective phase oracle.
4. Nevertheless, a specified classical bit associated with one ball has
   bounded-error quantum query complexity \(\Theta(\sqrt{s})\) and
   randomized query complexity \(\Theta(s)\).  Returning all \(B\) bits has
   the tight direct-sum law

   \[
      \boxed{Q=\Theta(B\sqrt{s}),\qquad R=\Theta(Bs).}       \tag{3}
   \]

These bounds continue to hold under the canonical global or blockwise
sample-and-query interfaces defined below.  In contrast, a dense classical
description has an unconditional \(\Omega(Bs)\)-word write cost, so the
query advantage in (3) disappears in total time under that output contract.
A sparse correction description (one exceptional index per ball) retains
the quadratic query separation.

This is an exact output-contract separation on a cap-optimal sparse SOCP
family.  It is not an iteration lower bound.  In fact, the Newton solve is
classically linear-time and the selected central point has a closed form.
The only quantum advantage left in (3) is unstructured input/readout search,
not linear algebra.

## 1. Hidden phase objectives

For each ball \(a\in[B]\), let \(j_a\in[s]\) be the unique hidden marked
index and define

\[
 \sigma_{ai}=1-2\mathbf 1\{i=j_a\},\qquad i\in[s].          \tag{4}
\]

The optimization objective is

\[
             \min_{w\in C}\ \sum_{a=1}^B\sum_{i=1}^s
                         \sigma_{ai}w_{ai}.                 \tag{5}
\]

Scaling (5) by any public positive number changes only the path
parameterization, not the construction.  Every objective entry has the same
squared magnitude.  This is the key reason that norm and sampling access do
not reveal the marked locations.

Let \(H\subset[s]\) be the public first half.  At the central point below,
the affine diagnostic

\[
 p_a(w)=\sqrt{s}\sum_{i\in H}w_{ai}+{|H|\over2}             \tag{6}
\]

obeys

\[
                  p_a(w)=\mathbf 1\{j_a\in H\}.             \tag{7}
\]

Thus additive error below \(1/3\) in each requested \(p_a\) returns the
corresponding half-location bits.  Equation (6) is a requested scalar
functional, not a claim that an arbitrary constant local-norm approximation
to the central point preserves it.  Its norm grows with \(s\), and this
distinction is material.

## 2. The cap-optimal reduced barrier and its exact central point

First suppose \(3\leq d<s+1\).  Partition each ball's coordinates into
\(\ell=\ell_d\) nonempty groups \(G\), as evenly as possible, with
\(|G|\leq d-2\).  The standard grouped Lorentz lift reduces to

\[
 \sum_G t_{aG}=1,\qquad
 q_{aG}:=t_{aG}-\|w_{aG}\|_2^2>0,                          \tag{8}
\]

with barrier

\[
                         F(t,w)=-\sum_{a,G}\log q_{aG}.     \tag{9}
\]

For \(d\geq s+1\), use the direct lift
\((1,w_a)\in Q_{s+1}\) and
\(F(w)=-\sum_a\log(1-\|w_a\|^2)\); this is the \(\ell=1\)
case of the calculations below with the scalar \(t_{a1}=1\) fixed.

Consider the central problem \(F+\eta\langle\sigma,w\rangle\).  The
\(t\)-stationarity equations make every \(q_{aG}\) in a fixed ball equal
to a common \(q\), while \(w\)-stationarity gives

\[
                 w_{aG}=-{\eta q\over2}\sigma_{aG}.        \tag{10}
\]

Writing \(\tau=\eta q/2\), summing (8) gives

\[
                         \ell q+s\tau^2=1.                 \tag{11}
\]

At the public multiplier

\[
                    \eta_0={4\ell\over3\sqrt{s}},          \tag{12}
\]

equations (10)--(11) have the exact solution

\[
 \boxed{
 q={3\over4\ell},\qquad
 w_{ai}=-{\sigma_{ai}\over2\sqrt{s}},\qquad
 t_{aG}={3\over4\ell}+{|G|\over4s}.}                      \tag{13}
\]

Strict convexity makes this the unique central point.  Substitution into
(6) proves (7).

The exact frontier theorem for globally labelled analytic full product-ball
slack factorizations shows that (8) uses the minimum possible number
\(B\ell_d\) of Lorentz factors under the cap, within that selected-factor
class. Simultaneously it has the minimum ambient dimension and ambient
normal-barrier parameter:

\[
 \begin{array}{c|c|c|c}
 &\#\text{ blocks}&D_{\rm amb}&\nu_{\rm ambient}\\ \hline
 3\leq d<s+1&B\ell_d&B(s+2\ell_d)&2B\ell_d\\
 d\geq s+1&B&B(s+1)&2B.
 \end{array}                                               \tag{14}
\]

The reduced barrier (9) has exact parameter \(B\ell_d\).  These barrier
parameters describe standard path-following upper bounds; none is used as
an iteration lower bound.

## 3. Treewidth and conditioning at the hard readout point

For one group, the exact Hessian identity is

\[
 \nabla^2[-\log(t-\|w\|^2)]
 =\operatorname{diag}\!\left(0,{2\over q}I\right)
  +{1\over q^2}(1,-2w)(1,-2w)^T.                           \tag{15}
\]

One latent hub represents the rank-one term.  Connecting the group scalars
to the one equality row \(\sum_Gt_{aG}=1\) produces a tree for each source
ball, and the \(B\)-ball graph is a forest.  Hence its exact structural
treewidth is one and exact elimination takes
\(O(B(s+\ell_d))\) field operations.  A positive-diagonal signed two-hub
representation has treewidth two.  A binary summation-tree replacement for
the equality row makes row degree constant without changing linear size or
bounded latent treewidth; for fixed \(d\), every remaining group degree is
also constant.

Conditioning is also benign at (13).  Rescale a scalar perturbation by
\(z=\sqrt\ell\,\delta t\), put \(y=\delta w\), and let

\[
                         A=2\sqrt\ell\,w_G.
\]

Up to the common factor \(\ell\), the block Hessian quadratic form is

\[
          {16\over9}(z-A^Ty)^2+{8\over3}\|y\|^2.           \tag{16}
\]

For the balanced partition,

\[
 \|A\|^2={\ell|G|\over s}<2.                              \tag{17}
\]

On the coupled two-dimensional subspace, nine times the matrix in (16) is

\[
 \begin{pmatrix}
 16&-16\|A\|\\
 -16\|A\|&24+16\|A\|^2
 \end{pmatrix}.                                           \tag{18}
\]

Its determinant is \(384\), its trace is below \(72\), and the orthogonal
\(y\)-eigenvalue is \(8/3\).  Therefore the block condition number is at
most

\[
                         {72^2\over384}={27\over2}.         \tag{19}
\]

Restricting to the tangent equations \(\sum_Gz_{aG}=0\) preserves these
Rayleigh-quotient bounds.  If \(\ell=1\), the scalar perturbation is fixed;
the direct-ball Hessian has tangential and radial eigenvalues \(8/3\) and
\(40/9\), hence condition number \(5/3\).  This is a Hessian statement in
the displayed scaling, not a finite-precision condition bound for every
possible augmented KKT formulation along the whole path.

## 4. Matched access models

The raw oracle is the standard indexed unique-mark oracle

\[
 O_j:\ |a,i,b\rangle\longmapsto
 |a,i,b\oplus\mathbf 1\{i=j_a\}\rangle,                   \tag{20}
\]

or its equivalent phase version.  One objective-coefficient query is one
use of (20).

Let \(O_\sigma\) denote the diagonal phase oracle and let \(U_{\rm unif}\)
be a fixed public unitary preparing the uniform index state. Canonical full
sample-and-query access adds:

- the public norm \(\|\sigma\|_2=\sqrt{Bs}\);
- public uniform squared-coordinate sampling; and
- the particular coherent preparation

  \[
     U_\sigma|0\rangle={1\over\sqrt{Bs}}
       \sum_{a,i}\sigma_{ai}|a,i\rangle,                  \tag{21}
  \]

  with the full unitary completion fixed to
  \(U_\sigma:=O_\sigma U_{\rm unif}\).

Global and conditional blockwise versions have constant raw-query overhead.
Conversely, with this canonical unitary completion,
\(O_\sigma=U_\sigma U_{\rm unif}^{-1}\), so the models are query-equivalent
up to constants. An arbitrary unitary completion that encodes extra
information outside the preparation subspace is not included.

A block call that returns all \(s\) coefficients classically is a different
interface: it solves one block in one call but transfers \(\Theta(s)\)
words.  Likewise, an oracle that directly returns (6) makes the requested
scalar trivial.  The lower bound begins with formulation access, not a
central-point scalar oracle.

## 5. Exact query and output hierarchy

The normalized \(w\)-state at (13) is

\[
 {|w\rangle}=-{1\over\sqrt{Bs}}
       \sum_{a,i}\sigma_{ai}|a,i\rangle,                  \tag{22}
\]

which differs from (21) only by a global phase.  Thus one query prepares the
exact central state.  The public values in (13) also make all block norms
and all squared-coordinate sampling distributions explicit.  State output
alone therefore contains no readout guarantee.

For one ball, deciding whether \(j\in H\) has quantum query complexity
\(\Theta(\sqrt{s})\).  A direct adversary matrix joins every marked index in
\(H\) to every one in its complement.  Its norm is \(s/2\); after masking a
single queried coordinate, its norm is \(\sqrt{s/2}\).  The adversary ratio
is \(\sqrt{s/2}\).

For all \(B\) balls, take the sum of these adversary matrices, each acting on
one tensor factor.  The terms commute and share a top eigenvector, so the
numerator norm is \(Bs/2\).  A query \((a,i)\) kills every term except the
one for block \(a\), leaving norm \(\sqrt{s/2}\).  The general adversary
bound therefore gives

\[
                         Q=\Omega(B\sqrt{s}).               \tag{23}
\]

Enumerating the \(B\) marked locations among \(Bs\) positions costs
\(O(\sqrt{(Bs)B})=O(B\sqrt{s})\) queries, proving the matching upper bound
and joint success probability. For the randomized lower bound, apply Yao's
principle to independent uniform marked locations in the \(B\) blocks. An
algorithm that returns the entire output with probability at least \(2/3\)
returns the bit of each individual block with probability at least \(2/3\).
Choosing a uniformly random block and simulating all other independently
sampled blocks for free gives a one-block algorithm with expected query
cost \(T/B\). Half-location under a uniform unique mark needs
\(\Omega(s)\) expected randomized queries, so \(T=\Omega(Bs)\);
exhaustive search matches it.

The consequences depend sharply on the output contract:

\[
\begin{array}{c|c|c}
\text{output contract}&\text{quantum queries}&
                         \text{randomized queries}\\ \hline
\text{normalized exact central state}&\Theta(1)&\text{not comparable}\\
\text{one specified }p_a&\Theta(\sqrt{s})&\Theta(s)\\
\text{all }B\text{ diagnostics or marked-index corrections}
   &\Theta(B\sqrt{s})&\Theta(Bs)\\
\text{dense classical central vector}&\Omega(Bs)\text{ total writes}
   &\Omega(Bs)\text{ total writes}.
\end{array}                                                \tag{24}
\]

For a dense classical vector, coordinatewise error below
\(1/(4\sqrt{s})\) reveals every exceptional sign in (13).  A sparse
description relative to the public all-plus baseline consists exactly of
the \(B\) marked indices and has the middle-row complexities in (24).  An
online SQ wrapper for the central vector can instead forward each future
coordinate query to the source oracle with constant overhead; there is no
offline preprocessing lower bound for such a passthrough interface.

## 6. QIPM interpretation

This family separates three costs that are often conflated.

- **Iteration geometry.**  The exact reduced parameter is
  \(\nu_{\rm red}=B\ell_d\), but this supplies an iteration upper bound, not
  a lower bound.
- **Newton algebra.**  The latent graph has treewidth one, the exact solve is
  linear-time, and the selected Hessian is uniformly conditioned after a
  public diagonal scaling.
- **Output information.**  A central state is immediate, a compact
  classical answer has the Grover direct-sum law, and dense tomography pays
  linear output size.

In particular, when \(d\geq s+1\), one has
\(\nu_{\rm red}=B\), condition number \(5/3\), and treewidth one, yet the
all-scalar readout still costs \(\Theta(B\sqrt{s})\) quantum queries and
\(\Theta(Bs)\) randomized queries.  Thus no bound depending only on barrier
parameter, Newton treewidth, and Newton conditioning can control classical
readout complexity.  Conversely, the family gives no QLSA speedup: the
classical Newton step is already linear, and the only sublinear quantum task
is promise-aware search in the objective phases.

## 7. Literature and novelty screen

The following ingredients are prior work.

- Grover search and the general adversary characterization give the query
  bounds.  Lee, Mittal, Reichardt, Spalek, and Szegedy develop the state
  conversion/adversary framework and its composition properties:
  <https://arxiv.org/abs/1011.3020>.
- A strong direct-product theorem for quantum query complexity is given by
  Lee and Roland: <https://arxiv.org/abs/1104.4468>.
- Kerenidis, Prakash, and Szilagyi's SOCP QIPM returns a classical
  approximate solution and explicitly charges quantum linear algebra and
  tomography: <https://arxiv.org/abs/1908.06720>.
- Dalzell et al.'s end-to-end QIPM resource analysis identifies tomography
  and conditioning as central practical costs:
  <https://arxiv.org/abs/2211.12489>.
- Apers and Gribling prove Grover/composition lower bounds for LP solving and
  spectral approximation in row-query and quantum-inspired SQ models:
  <https://arxiv.org/abs/2311.03215>.  Their 2026 revision explicitly
  returns a classical approximate LP solution.  The result here uses a
  different product-ball central-point family and isolates the output
  hierarchy rather than a tall-matrix row bottleneck.

A targeted search for quantum product-ball optimization, SOCP central-path
query lower bounds, and state-versus-classical readout separations found no
prior theorem combining (i) an exact cap-optimal analytic Lorentz lift,
(ii) a treewidth-one and uniformly conditioned Newton point, (iii) one-query
exact central-state preparation, and (iv) the matched
\(B\sqrt{s}\)-versus-\(Bs\) classical-readout law.  The construction and
combination appear new, but priority is not established and specialist
review is still required.

## 8. Scope and open extensions

1. The cap-optimality statement uses the analytic/quasianalytic selected
   factor theorem.  The concrete SOCP, central-point formula, treewidth,
   conditioning, and oracle lower bounds do not require analyticity.
2. The lower bound is total over one requested path point.  It neither
   assigns fresh hidden data to iterations nor proves an IPM iteration lower
   bound.
3. A constant local-norm central-neighborhood guarantee alone does not
   preserve the amplified diagnostic (6).  A theorem for a standard
   constant-accuracy optimizer output would require a different encoding.
4. The conditioning bound is local to (13) and to the displayed public
   scaling.  No uniform bit-complexity theorem along an entire path is
   asserted.
5. The most useful next question is whether one can obtain the same output
   hierarchy for a bounded scalar diagnostic that is Lipschitz in the local
   barrier norm.  The phase-state geometry suggests a real obstruction:
   constant separation of one exceptional phase requires amplification of a
   \(1/\sqrt{s}\)-scale displacement.
