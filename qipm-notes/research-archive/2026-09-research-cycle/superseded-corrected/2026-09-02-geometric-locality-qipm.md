# A geometric-locality obstruction for sparse QIPM initialization

## Status and scope

This note gives a hardware-local circuit-depth lower bound for constructing a
locally readable central-point value from a sparse LP.  It is an end-to-end oracle
construction result, not a lower bound for an abstract QLSA supplied with a free
random-access oracle.  Its main point is a separation:

> A path-sparse LP can have a condition-one reduced barrier Hessian at every central
> point, while constructing one locally readable cell of an exact central-point
> oracle requires linear depth on a one-dimensional bounded-range architecture.

The causality argument is standard.  The potentially new conjunction is the exact
QIPM witness, strict primal-dual feasibility, condition-one reduced Newton geometry,
and the end-to-end physical-depth conclusion.

## 1. Sparse LP witness

Let hidden signs \(\sigma_1,\ldots,\sigma_N\in\{-1,+1\}\), and define

\[
 d_i=u_i-v_i,\qquad u_i,v_i\ge 0\quad(0\le i\le N).
\]

For a fixed \(\alpha\in(0,1)\), consider

\[
\begin{aligned}
 \min\quad& \sum_{i=0}^N(u_i+v_i)+\alpha(u_N-v_N),\\
 \text{s.t.}\quad&d_0=1,\\
 &d_i-\sigma_i d_{i-1}=0\quad(1\le i\le N).
\end{aligned}                                                    \tag{1}
\]

Every constraint row has at most four nonzeros, every column at most two, the
nonzero magnitudes are one, and the constraint-intersection graph is a path.  Set

\[
 p_0=1,\qquad p_i=\prod_{j=1}^i\sigma_j,\qquad q_i=u_i+v_i.
\]

Feasibility forces \(d_i=p_i\), hence

\[
 u_i=\frac{q_i+p_i}{2},\qquad v_i=\frac{q_i-p_i}{2},\qquad q_i\ge1. \tag{2}
\]

Taking every \(q_i=2\) gives strict primal feasibility.  With the dual convention
\(A^Ty+s=c\), the choice \(y=0\) gives \(s=c>0\), so the problem is also strictly
dual feasible.

On the feasible affine space, the primal logarithmic-barrier objective separates:

\[
 \Phi_\mu(q)=\sum_{i=0}^Nq_i+\alpha p_N
 -\mu\sum_{i=0}^N\log\frac{q_i^2-1}{4}.                         \tag{3}
\]

Every central coordinate is therefore

\[
 q(\mu)=\mu+\sqrt{\mu^2+1}.                                    \tag{4}
\]

At \(\mu=3/4\), \(q=2\), and consequently

\[
 (u_i,v_i)=
 \begin{cases}
  (3/2,1/2),&p_i=+1,\\
  (1/2,3/2),&p_i=-1.
 \end{cases}                                                    \tag{5}
\]

The fixed vectors

\[
 V_i=(e_{u_i}+e_{v_i})/\sqrt2
\]

form an orthonormal basis for the nullspace of the equality constraints.  If

\[
 H_x=\mu\operatorname{Diag}(u_0^{-2},\ldots,u_N^{-2},
                             v_0^{-2},\ldots,v_N^{-2})
\]

is the full-space primal barrier Hessian, then

\[
 V^TH_xV=
 2\mu\left[(q+1)^{-2}+(q-1)^{-2}\right]I.                      \tag{6}
\]

Thus the reduced primal-barrier Newton matrix has condition number exactly one for
every \(\mu>0\).  Equation (5), however, says that a locally readable central-point
cell at index \(N\) reveals the parity \(p_N\).

## 2. Geometrically local preprocessing model

Let \(\Gamma=(\mathcal V,\mathcal E)\) be a hardware graph.  The classical input
register holding \(\sigma_i\) is placed at a site \(v_i\in\mathcal V\).  These
registers begin in the computational-basis state encoding the signs.  Workspace
registers may start in an arbitrary state that is independent of the signs; in
particular, the workspace may contain input-independent long-range entanglement.

A range-\(r\), depth-\(T\) preprocessing circuit is a fixed circuit, independent of
the input values, with \(T\) layers.  Every gate in a layer is supported on a set of
hardware diameter at most \(r\), and gates within one layer have disjoint support.
Input dependence enters only through the input registers at their assigned sites.
This rules out a free global classical controller that first reads every sign and
then chooses the circuit.

An output at a site \(o\) is *locally parity-readable* if a measurement supported at
\(o\) returns \(p_N\) with probability at least \(2/3\) for every input.  This
includes a classical encoding of \((u_N,v_N)\) with coordinate error below \(1/2\),
because comparing the two coordinates recovers \(p_N\).

The same definition covers the combined cost of preprocessing and looking up cell
\(N\) at a local query port.  It does not cover an answer left only in a global
observable whose nonlocal measurement and classical aggregation are declared free.

## 3. Light-cone theorem

### Theorem 1 (central-oracle geometric depth)

For the LP family (1), every range-\(r\), depth-\(T\) circuit with a locally
parity-readable output at \(o\) satisfies

\[
 T\ \ge\ \frac{1}{r}\max_{1\le i\le N}\operatorname{dist}_\Gamma(o,v_i). \tag{7}
\]

In particular:

1. If the hardware is the path \(v_1,\ldots,v_N\) and the output is fixed at
   \(o=v_N\), then
   \[
   T\ge (N-1)/r.                                                \tag{8}
   \]
2. If the output location on that path may be chosen freely, then
   \[
   T\ge \lfloor(N-1)/2\rfloor/r.                               \tag{9}
   \]
3. If the signs occupy distinct sites of a \(d\)-dimensional nearest-neighbor grid,
   then any single locally readable output obeys
   \[
   T\ge \frac{N^{1/d}-1}{2r}=\Omega(N^{1/d}/r).                \tag{10}
   \]

These statements hold even with arbitrary input-independent entanglement in the
initial workspace.

#### Proof

Pull a measurement observable at \(o\) backwards through the circuit.  In one layer,
its support can grow by hardware distance at most \(r\).  After \(T\) layers, every
observable determining the output distribution is supported inside
\(B_\Gamma(o,rT)\), the radius-\(rT\) backward light cone of \(o\).

Suppose some input site \(v_j\) lies outside this ball.  Take two sign strings that
differ only in \(\sigma_j\).  Their input density operators have identical reduced
states on the backward light cone.  The initial workspace state is also the same for
the two inputs, even if it is entangled across the device.  Hence every local output
observable has the same expectation, and the entire output distribution at \(o\) is
identical for the two inputs.

Flipping one sign flips \(p_N\).  One identical output distribution cannot return
opposite signs with probability at least \(2/3\) on both inputs.  Therefore every
\(v_i\) must lie in \(B_\Gamma(o,rT)\), which proves (7).

For a path with \(o=v_N\), the farthest input is at distance \(N-1\), proving (8).
For a freely chosen path output, the minimum possible maximum distance to the two
ends is \(\lfloor(N-1)/2\rfloor\), proving (9).  Finally, a radius-\(R\) ball in the
\(d\)-dimensional grid contains at most \((2R+1)^d\) sites.  Containing all \(N\)
input sites requires \((2rT+1)^d\ge N\), which gives (10). \(\square\)

### Why pre-entanglement does not defeat the proof

Input-independent entanglement can create correlations, but it cannot transmit the
choice of \(\sigma_j\) outside its forward light cone.  The proof concerns the
reduced state of one locally measured output register, so it is exactly a
no-signalling statement.  Equivalently, in the Heisenberg picture every output
observable remains supported inside the backward light cone.

There are two important qualifications.

* Input-*dependent* pre-entanglement can already contain the parity.  Treating it as
  free merely moves the preprocessing cost into advice.
* A pre-shared GHZ state plus local sign-controlled phases can encode parity in a
  global observable without propagating it to one site.  Reading that observable
  requires a nonlocal measurement or aggregation.  The theorem charges this
  communication by requiring a locally readable answer.  It does not apply if global
  measurement and global classical postprocessing are free.

## 4. Consequence for sparse QIPMs

At \(\mu=3/4\), one locally readable cell of an exact or coordinate-error-below-
\(1/2\) primal central oracle solves parity.  Theorem 1 therefore gives an
end-to-end depth lower bound for constructing that oracle on bounded-range hardware.
At the same point, and in fact for every \(\mu>0\), equation (6) gives a scalar
reduced Newton matrix with condition number one.

The obstruction is consequently not captured by a QLSA cost expressed only through
the Newton-system condition number.  It is also different from the known
\(\Omega(\kappa)\) *query-depth* lower bound for quantum linear systems: here the
reduced system has \(\kappa=1\), and physical depth is spent propagating input
information needed to construct the feasible central representation.

This result applies to original-form feasible central-point access.  A homogeneous
self-dual embedding has a universal enlarged starting point and is not lower-bounded
by this initialization theorem.  For such a method, parity must instead appear in
the later evolution, recovery, or value readout.

## 5. Limitations and attempted stronger claim

The theorem is deliberately model-specific.

* It is not a lower bound in the standard all-to-all gate or sparse-query model.
  All-to-all bounded-fan-in gates can compute parity in logarithmic depth, and a free
  input-dependent QRAM can expose the answer immediately.
* It assumes the input is physically local and the circuit is fixed.  A free global
  controller that reads all signs has already paid or hidden the communication cost.
* It lower-bounds construction or lookup of a locally readable central cell.  It does
  not lower-bound every infeasible-start QIPM, every embedded formulation, or a purely
  global quantum state from which no local answer is required.
* The same geometric lower bound holds classically.  It is an obstruction to a
  claimed quantum depth advantage, not a quantum-versus-classical separation.

A tempting stronger statement is that every IPM iteration requires \(\Omega(N)\)
QRAM writes because all diagonal weights change.  That claim is false without a
strict materialized-array model.  For a fixed LP, a lazy value oracle may store the
input once and compute the current weight from the index and the scalar path parameter
on demand.  An \(\Omega(N)\) refresh theorem would therefore need either arbitrary
fresh information at each iteration, a cell-probe model that forbids lazy evaluation,
or a lower bound on evaluating the composed update oracle.  None follows merely from
the fact that \(N\) numerical weights have changed.  The geometric central-cell
theorem avoids this dead end because even one requested cell depends on a distant
input bit.

## 6. Literature and novelty audit

Light-cone arguments for geometrically local quantum circuits are standard.  For
example, Barak and Marwaha formalize how a depth-local quantum circuit restricts the
backward light cone of each measured output in
[*Classical Algorithms and Quantum Limitations for Maximum Cut on High-Girth
Graphs*](https://drops.dagstuhl.de/opus/volltexte/2022/15610/).  Dong, Ou, and Yao
prove much stronger parity-depth results for geometrically local QAC circuits,
including a nearly linear bound for contiguous one-dimensional inputs, in
[*On the Computational Complexity of Geometrically Local QAC0 Circuits*](https://arxiv.org/abs/2604.07178).
The depth exponent in Theorem 1 is therefore not a new circuit-complexity result.

Wang and Zhang prove an \(\Omega(\kappa)\) quantum query-depth lower bound for linear
systems in
[*Tight Quantum Depth Lower Bound for Solving Systems of Linear
Equations*](https://doi.org/10.1103/PhysRevA.110.012422).  That theorem concerns QLSA
query layers and becomes constant when \(\kappa=1\); it does not cover the geometric
construction cost isolated here.

End-to-end QIPM resource studies count circuit depth, tomography, and QRAM costs; see
Dalzell et al.,
[*End-To-End Resource Analysis for Quantum Interior-Point Methods and Portfolio
Optimization*](https://doi.org/10.1103/PRXQuantum.4.040325).  Targeted searches found
no prior QIPM theorem combining a path-local parity central point, condition-one
reduced Newton geometry, and a geometric-locality depth lower bound.  The defensible
novelty claim is this combination and its oracle-construction interpretation, not the
underlying parity or light-cone method.

## 7. Publication assessment

The result is rigorous and useful as a model-sensitive negative theorem in a broader
sparse-QIPM paper.  It closes one loophole left by condition-number-only analyses:
even a trivial Newton solve does not make a nonlocal feasible representation free on
bounded-range hardware.  It is not a standalone quantum lower-bound breakthrough,
because the causal proof is elementary, the conclusion is architecture-dependent,
and it supplies no quantum advantage over a classical local scan.
