# Implicit PSD fiber recentering is linear with norms—and Grover-hard without them

Status: Independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated implicit, scale-aware access and output contracts

## Result

The off-center PSD obstruction can be removed at packing-independent cost,
but only in a scale-aware implicit representation.

For the column-packed lift of \(C=(B_2^s)^b\), let every source ball have
\(h\) coordinate columns. At a projected interior point \(x\), put

\[
       \rho_a=1-\|x_a\|^2,\qquad
       d_\gamma={\rho_a\over h}\quad(\gamma\in\Gamma_a).  \tag{1}
\]

Do not materialize the dense Gram matrices. Store the centered PSD lift as
the pair \((W,d)\), with semantics

\[
 D_\ell=\operatorname{Diag}(d_\gamma:\gamma\in\ell),
 \qquad
 S_\ell=W_\ell^TW_\ell+D_\ell.                            \tag{2}
\]

### Implicit recentering theorem

Given explicit projected coordinates, (1)--(2) can be built in
\(O(bs)\) arithmetic and \(O(bs)\) storage, independently of the PSD
packing arity and layout. It is the exact unique fiber analytic center,
satisfies every affine source equation, and restores the exact
PSD--Lorentz reduced-oracle equivalence.

For \(B\)-bit fixed-point (equivalently, common-denominator dyadic)
coordinates it can be represented without
cancellation in

\[
 \widetilde O\!\left(bs\,\mathsf M(B+\log(bs))\right)      \tag{3}
\]

bit operations, where \(\mathsf M(q)\) is the cost of \(q\)-bit integer
multiplication. The representation is backward exact for the stored
rational iterate. Dependence on the inverse interior margin enters only
when barrier inverses or target numerical accuracy are requested, not in
forming the symbolic center.

If an approximate representation obeys the certified fiber residual

\[
 \max_\ell\left\|
 (D_\ell^0)^{-1/2}(\widehat D_\ell-D_\ell^0)
 (D_\ell^0)^{-1/2}\right\|_2\leq\delta<1,                 \tag{4}
\]

then the centered Lorentz Hessian preconditions its projected Newton
system within

\[
                     \left({1+\delta\over1-\delta}\right)^2. \tag{5}
\]

Thus recentering before each call gives \(\delta=0\); certified approximate
recentering gives a robust off-center equivalence.

### Access dichotomy

In a quantum/SQ interface that supplies reversible scale access to every
\(\rho_a\), one query to the scale oracle plus
\(\operatorname{poly}(B,\log h)\) reversible gates returns any requested
centered diagonal \(d_\gamma\). Together with coherent access to \(x\),
the common rank-one reduced-Hessian compiler has packing-independent
oracle cost. A fiber-centered state-only QIPM therefore pays no additional
cone-factor or packing-arity factor for recentering.

This positive statement is conditional on maintaining the scale oracle.
It cannot be removed:

1. A normalized state oracle for \(x\) contains no radial scale. Two
   different radii give the identical state oracle but different
   \(\rho_a\), centered completions, and Newton Hessians. Recentring from
   normalized state access alone is information-theoretically impossible.
2. From a coordinate bit oracle with no norm metadata, producing a
   scale-aware center within any fixed \(\delta<1/3\) needs
   \[
              \Omega(\sqrt s)\ \text{quantum queries},\qquad
              \Omega(s)\ \text{randomized queries}        \tag{6}
   \]
   even for one ball. Producing all \(b\) independent source scales as a
   jointly correct classical record, or as a standalone value oracle that
   makes no further coordinate-input queries, has the direct-sum lower
   bounds
   \[
              \Omega(b\sqrt s)\ \text{quantum},\qquad
              \Omega(bs)\ \text{randomized}.              \tag{7}
   \]

   More generally, for \(k\mid s\) and \(1\leq k\leq s/2\), a
   replicated-block promise with centered slack \(\rho=k/s\) gives the
   tight one-source laws
   \[
       \Theta(\sqrt{s/k})=\Theta(\rho^{-1/2})\ \text{quantum},
       \qquad
       \Theta(s/k)=\Theta(\rho^{-1})\ \text{randomized}.   \tag{7a}
   \]

The quantum lower bound is matched on the Boolean promise by Grover
search/counting. Hence norm metadata is a genuine input resource, not a
minor implementation detail.

Finally, if the output contract requires explicit dense \(S_\ell\), any
algorithm must write

\[
                     \Omega\!\left(\sum_\ell c_\ell^2\right) \tag{8}
\]

auxiliary entries, and ordinary Gram formation costs
\(O(\sum_\ell p c_\ell^2)\) arithmetic. The packing-independent theorem is
therefore exactly an implicit/reduced theorem; it does not make dense
ambient output free.

## 1. Exact implicit compiler

The centered PSD block factors as

\[
 Z_\ell=
 \begin{pmatrix}W_\ell^TW_\ell+D_\ell&W_\ell^T\\
                 W_\ell&I_p\end{pmatrix}
 =
 \begin{pmatrix}W_\ell^T\\I_p\end{pmatrix}
 \begin{pmatrix}W_\ell&I_p\end{pmatrix}
 +\begin{pmatrix}D_\ell&0\\0&0\end{pmatrix}.              \tag{9}
\]

Thus (2) specifies \(Z_\ell\) exactly without storing \(W_\ell^TW_\ell\).
Because \(D_\ell\succ0\), the Schur complement proves \(Z_\ell\succ0\).
For each source \(a\),

\[
 \sum_{\gamma\in\Gamma_a}(S_{\ell(\gamma)})_{\gamma\gamma}
 =\sum_{\gamma\in\Gamma_a}\|x_\gamma\|^2
   +\sum_{\gamma\in\Gamma_a}d_\gamma
=\|x_a\|^2+\rho_a=1.                                    \tag{10}
\]

There is an analogous coherent representation. Let
\(K_\ell=(W_\ell\ I_p)\), so (9) is
\(Z_\ell=K_\ell^TK_\ell+\operatorname{Diag}(d_\ell,0)\).
Given a projected-unitary \(\alpha_K\)-block encoding of \(K_\ell\), the
standard product construction uses one call and one inverse call to encode
\(K_\ell^TK_\ell\) with normalization \(\alpha_K^2\). Let
\(\alpha_d\geq\|d_\ell\|_\infty\) be a supplied normalization for the
diagonal encoding compiled from (14). One may use the public bound
\(\alpha_d=1/h\); using the exact maximum instead requires that maximum as
metadata or charged preprocessing. An LCU then encodes \(Z_\ell\) with
normalization
\[
                           \alpha_K^2+\alpha_d.             \tag{10a}
\]
Thus Gram materialization is unnecessary even for a centered ambient
block encoding. The query count is constant *relative to the supplied
\(K_\ell\) encoding*; constructing that encoding, its normalization, and
using \(Z_\ell^{-1}\) remain charged and may depend on block size and
conditioning.

Hadamard equality and AM--GM show that this is the unique minimizer of the
restricted standard log-determinant on the auxiliary fiber.

Computing all \(\rho_a\) is one pass over the \(bs\) coordinates.
Writing the \(H=bh\leq bs\) diagonal labels is another linear pass. The
packing map is used only to route labels; no inner product between packed
columns is evaluated.

If the stored coordinates are \(B\)-bit fixed-point numbers with a common
dyadic denominator, their squared norms and (1) are exact rationals with
numerator/denominator length \(O(B+\log(bs))\), up to the standard constant
factor from squaring and the public divisor \(h\). Fast integer arithmetic
gives the conservative bit ledger (3). For unrelated rational
denominators, their common-denominator growth must instead be charged.
One may store \(S_\ell\) as the symbolic expression in (2), so subtracting
two rounded Gram matrices never occurs.

## 2. Approximate recentering and the robust QIPM ledger

Condition (4) is precisely the relative fiber-eccentricity condition from
the off-center quotient theorem with

\[
              (1-\delta)D_\ell^0
                 \preceq\widehat D_\ell
                 \preceq(1+\delta)D_\ell^0.               \tag{11}
\]

Substitution of \(\mu=1-\delta\), \(L=1+\delta\) proves (5).
If diagonal slack values obey

\[
                   |\widehat d_\gamma-d_\gamma|
                        \leq\delta d_\gamma,               \tag{12}
\]

then (4) holds immediately. Approximate values in (12) need not satisfy
the original affine equations exactly. Exact feasibility is recovered by
computing (1) from the stored rational \(x\), or else affine residuals must
be included in the inexact-IPM analysis; this note does not silently treat
approximate norm metadata as exact feasibility.

Let \(n=bs\) and \(H=bh\). A classical fiber-centered short-step
implementation using the common reduced Hessian has the ledger

\[
 \begin{array}{c|c|c}
  &\text{per outer call}&\text{standard upper certificate}\\ \hline
  \text{recenter and projected solve}
     &O(n)&O(n\sqrt H\log(\Delta/\epsilon)).
 \end{array}                                               \tag{13}
\]

This is an upper bound, not an iteration lower bound. With extra sparse
constraints, replace the linear solve term by the charged augmented
incidence-treewidth solver; the recentering pass remains \(O(n)\).

For a quantum reduced-state implementation, suppose a complete canonical
oracle provides, at the requested precision,

\[
 O_\rho:\ |a,z\rangle\longmapsto|a,z\oplus\rho_a\rangle.  \tag{14}
\]

Reversible division by public \(h\) compiles the diagonal-center oracle
with one use of \(O_\rho\). The centered reduced Hessian

\[
 (H_0)_a={2h\over\rho_a}I
   +{4h\over\rho_a^2}x_ax_a^T                            \tag{15}
\]

then has the same block encoding, normalization, condition, and
inverse-state target as the grouped Lorentz formulation. With approximate
fiber data satisfying (4), the spectral condition overhead is bounded by
(5), in addition to the separately charged block-encoding normalization
and success amplitude.

Maintaining (14) after a dense quantum update is not automatic. The exact
identity

\[
 \rho_a(x+\alpha u)
  =\rho_a(x)-2\alpha x_a^Tu_a-\alpha^2\|u_a\|^2           \tag{16}
\]

shows that an update needs blockwise inner products and direction norms.
If these are supplied by a dynamic SQ structure, they are part of its
update cost. If not, Section 3 applies. The companion
[dynamic scale-maintenance theorem](2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md)
gives the exact invocation--compilation query tradeoff for fresh
hidden-support update batches, and explains why that direct sum does not
automatically compose along a fixed QIPM trajectory.

## 3. Scale is necessary

### 3.1 Normalized-state impossibility

Fix a unit vector \(v\) and two radii \(0<r_0<r_1<1\). The normalized
state-preparation oracle for \(x^{(j)}=r_jv\) may be the same complete
unitary on both inputs:

\[
                         |x^{(j)}\rangle=|v\rangle.        \tag{17}
\]

But its centered slack is
\(d^{(j)}=(1-r_j^2)/h\). Choosing the radii so that these two values differ
by more than a factor \((1+\delta)/(1-\delta)\) makes their admissible
relative-\(\delta\) output intervals disjoint. No algorithm seeing the
same oracle can succeed on both. A norm or scale oracle is therefore
necessary even with unlimited computation.

This is also why arbitrary unitary completions must be matched. If a
state-preparation oracle is permitted to encode \(r_j\) in an unused
subspace, it has silently become a scale oracle.

### 3.2 Coordinate-query lower bound

Take one ball, \(h=1\), and let a bit string
\(z\in\{0,1\}^s\) have \(z_1=0\). Promise either:

\[
 \begin{array}{ll}
 {\cal P}_0:&z_i=1\quad(2\leq i\leq s),\\
 {\cal P}_1:&\text{exactly one hidden }j\geq2
                       \text{ also has }z_j=0.
 \end{array}                                               \tag{18}
\]

Set \(x_i=z_i/\sqrt s\). Both points are strictly interior, and

\[
 \rho=
 \begin{cases}
 1/s,&{\cal P}_0,\\
 2/s,&{\cal P}_1.
 \end{cases}                                               \tag{19}
\]

A **scale-aware \(\delta\)-recenterer** outputs a classical value or
reversible fixed-point value oracle for a diagonal \(\widehat d\) satisfying

\[
                         |\widehat d-\rho|\leq\delta\rho.  \tag{20}
\]

For \(\delta<1/3\), the two output intervals in (20) are disjoint, so one
call to the output value oracle distinguishes \({\cal P}_0\) from
\({\cal P}_1\). This is unstructured search on \(s-1\) locations. The
standard Grover and randomized search lower bounds prove (6).

For \(b\) disjoint strings, require all \(b\) diagonal scales with joint
success probability at least \(2/3\), materialized as a classical record
or compiled into a standalone value oracle that makes no subsequent
coordinate-input queries. Here is a direct adversary proof.
For one block, index the promise inputs by
\(\{\varnothing\}\cup\{\{j\}:2\leq j\leq s\}\), and let
\(\Gamma_1\) be the adjacency matrix of the star centered at
\(\varnothing\). Then
\[
                         \|\Gamma_1\|=\sqrt{s-1},
\]
while filtering by any input-bit query leaves norm at most one. For the
\(b\)-fold output function, use the Kronecker sum
\[
 \Gamma_b=\sum_{a=1}^b
  I^{\otimes(a-1)}\otimes\Gamma_1\otimes I^{\otimes(b-a)}.
\]
It vanishes between inputs with the same output vector,
\(\|\Gamma_b\|=b\sqrt{s-1}\), and a query in block \(a\) kills every
summand except the \(a\)-th, whose filtered norm is one. The general
adversary theorem proves the quantum lower bound in (7). A product hard
distribution and Yao's principle give the classical randomized direct
sum. Running Grover separately on every block matches the quantum scale
on this promise.

This direct-sum statement is not the cost of one *online* coherent scale
evaluation. If the evaluator may query the coordinate input each time it
is used, Grover search can be controlled by the source label, so one
superposed evaluation
\(|a,z\rangle\mapsto|a,z\oplus\rho_a\rangle\) costs
\(O(\sqrt s)\) input queries on this promise, independently of \(b\).
Those per-use queries must remain in the QIPM ledger; they have not
materialized the maintained scale oracle assumed in (14).

The lower bound concerns a value-bearing output. A normalized quantum
state of the one-dimensional diagonal is always \(|1\rangle\) and is not a
usable centered completion without normalization metadata.

### 3.3 Margin-sensitive strengthening

The same search reduction exposes the inverse-margin cost hidden by the
special case \(\rho=1/s\). Let \(k\) divide \(s\), with
\(1\leq k\leq s/2\), put \(N=s/k-1\), and partition the coordinates
into one public block and
\(N\) candidate blocks of size \(k\). The public block is identically zero.
Every candidate block is identically one, except that under the marked
promise exactly one candidate block is identically zero. Set again
\(x_i=z_i/\sqrt s\). Then
\[
 \rho=
 \begin{cases}
   k/s,&\text{no candidate block is marked},\\
   2k/s,&\text{one candidate block is marked}.
 \end{cases}                                               \tag{20a}
\]
For \(\delta<1/3\), a relative-\(\delta\) recenterer distinguishes these
cases. Each coordinate query is simulated by at most one query to the mark
bit of its candidate-block label (and no query for the public block), so
unstructured-search lower bounds on the \(N\) candidate labels give
\[
   \Omega(\sqrt N)=\Omega(\sqrt{s/k})\quad\text{quantum},
   \qquad
   \Omega(N)=\Omega(s/k)\quad\text{randomized}.            \tag{20b}
\]
Conversely, use one fixed representative coordinate from each candidate
block as the Grover search domain, or scan those representatives
classically. This proves the matching upper bounds in (7a). Since the
smaller slack in (20a) is \(\rho=k/s\),
the laws are exactly \(\Theta(\rho^{-1/2})\) and
\(\Theta(\rho^{-1})\) on this family.

This is a per-snapshot scale-compilation theorem. It shows that missing
radial metadata can introduce inverse-margin overhead near a boundary, but
does not multiply that overhead by an IPM iteration count: iterates may be
correlated, and a maintained scale data structure can reuse information.

## 4. Explicit-output boundary

In the implicit representation, off-diagonal entries of \(S_\ell\) are
not stored. An explicit symmetric \(c_\ell\times c_\ell\) matrix has
\(c_\ell(c_\ell+1)/2\) scalar entries. Therefore classical
materialization has the unconditional write lower bound
\[
                         \Omega\!\left(\sum_\ell c_\ell^2\right).
                                                                    \tag{21}
\]

Ordinary multiplication of a \(p\times c_\ell\) matrix gives
\(W_\ell^TW_\ell\) in \(O(pc_\ell^2)\) arithmetic, leading to the upper
ledger stated in (8). Fast rectangular multiplication may improve the
arithmetic exponent but cannot remove the output-size bound.

A quantum state of the flattened Gram matrix is a different output
contract. Preparing it requires a specified access model, normalization,
and error metric; the reduced-state theorem does not imply such a compiler.

## 5. Scope and literature boundary

The positive compiler applies to the explicit PSD column-packed Schur lift
and objectives/additional constraints depending only on projected
coordinates. It uses the restricted standard log-determinant and exact
fiber analytic centers. It does not prove stability of a generic
primal-dual SDP update that insists on ambient variables.

The quantum upper statement assumes scale-aware access (14). The lower
bound shows this assumption is necessary for packing-independent
polylogarithmic oracle overhead near the boundary; it does not rule out
Grover-scale norm estimation or problem-specific maintained norms.

Quantum norm estimation, amplitude estimation, and Grover search are
standard. General adversary composition/direct-sum results justify the
all-block form of (7); see Belovs and Lee,
[*The quantum query complexity of composition with a
relation*](https://arxiv.org/abs/2004.06439). A targeted search did not
locate the exact implicit PSD-fiber compiler, its connection to the
PSD--Lorentz oracle equivalence, or the scale-aware recentering lower bound
(18)--(20). Novelty is plausible subject to specialist review.
