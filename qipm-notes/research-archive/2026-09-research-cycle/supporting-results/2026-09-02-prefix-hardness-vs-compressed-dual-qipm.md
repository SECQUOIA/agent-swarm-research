# Compatibility of condition-one prefix hardness with the compressed-dual QIPM

Date: 2026-09-02

## Conclusion

The condition-one prefix family does not contradict the partition-free
compressed-dual theorem, and it cannot be used as a positive \(\kappa=1\)
example for that theorem without paying a linear factor.  There are three
separate reasons:

1. the hard one-step start is primal--dual infeasible, whereas the compressed
   dual method maintains the affine identity \(s=c-A^Ty\);
2. the advertised endpoint \(\mu_1=1/16\) is not in the active-separation tail
   uniformly in \(P\); that tail begins only at \(\mu=O(1/P)\); and
3. the retained dual dimension is
   \(m=3P+O(\log P)=\Theta(P)\), so the generic dense-tomography
   implementation in the compressed theorem budgets \(\widetilde\Theta(P)\)
   state-unitary calls for even one explicit constant-accuracy dual direction.

More strongly, a compiler that outputs the compressed primal-coordinate oracle
at a central point must spend \(\Omega(P)\) raw coefficient queries in either
setup or evaluation.  Otherwise constant-overhead value-to-amplitude loading
would violate the family's primal-state lower bound.  Thus the lower bound is
caught by a named loading/output factor, not by matrix conditioning.

## 1. Parameter map and applicability

The prefix family has

\[
 n=4P,
 \qquad
 m=3P+T_0,
 \qquad
 T_0=\left\lceil\tfrac12\log_2N\right\rceil,
 \qquad
 P=17N+1.
\tag{1}
\]

Its row and column sparsities are at most four, its coefficient magnitudes are
at most two, and \(\operatorname{nnz}(A)=\Theta(P)\).  Hence an ordinary
sparse-access block encoding can have \(\alpha_A=O(1)\) and use \(O(1)\) raw
coefficient queries per invocation.  If it is instead materialized in QRAM,
its input-dependent construction costs \(\Theta(P)\) words/queries and must be
included in \(C_{\rm build}(A)\).

The condition-one statement concerns the reduced *primal* barrier Hessian in
the public null basis \(W\):

\[
 W^T\nabla^2 f_\mu(x(\mu))W=\lambda(\mu)I.
\tag{2}
\]

It does not state that the dual normal matrix
\(AS^{-2}A^T\), the partition-free filtered matrix, the active singular gaps
\(\sigma_B,\sigma_N\), or their block-encoding normalizations equal one.
Substituting \(\kappa=1\) from (2) for any of
\(\mathcal K_M,\chi_Q,\Gamma_g\) in the compressed-dual ledger is therefore
invalid.

### Failure of the hard one-step start to meet the dual model

At the public start in the hardness theorem, \(y^0=0\), but the supplied
positive vector \(s^0\) is not the objective vector \(c\).  Hence

\[
 s^0\ne c-A^Ty^0=c.
\tag{3}
\]

The step is a standard infeasible-start KKT/Newton correction.  The compressed
dual algorithm cannot represent this \(s^0\) by its retained \(y^0\), so its
trajectory theorem does not apply to that step.  A Phase-I or self-dual
embedding could be added, but its loading, dimensions, and output would require
a new analysis.

### The constant endpoint is not uniformly in the partition tail

The limiting positive reduced cost on every free nonbasic coordinate is

\[
 \underline s_N=2w={7\over18H},
 \qquad H=\Theta(\sqrt P).
\tag{4}
\]

The automatic selector theorem requires, up to fixed neighborhood constants,

\[
 \mu\lesssim\underline s_N^2=\Theta(1/P).
\tag{5}
\]

At the advertised \(\mu_1=1/16\), every free-node central primal coordinate
is \(\Theta(H)\) and every slack is \(\Theta(1/H)\).  The comparison
\(x_i\ge s_i\) therefore marks both members of a hidden \((u_i,v_i)\) pair;
it does not recover the limiting basic/nonbasic partition.  The
partition-free tail theorem begins only after (5), not at the hard one-step
endpoint.

The robust approximate-feasibility corollary remains relevant at smaller
\(\mu\): it applies to a central primal state at any prescribed parameter.
That tail use is addressed below.

## 2. Exact charges in the compressed-dual ledger

For this family, the path-query term from the compressed-dual theorem is

\[
 Q_{\rm path}
 =\widetilde O\!\left(
  \sum_t {mJ_t\rho_t\over\eta}
  \Gamma_{g,t}\mathcal K_{M,t}\chi_{Q,t}
 \right).
\tag{6}
\]

The accuracy conversion parameters satisfy, for a nonzero solve,

\[
 J_t\ge1,
 \qquad
 \rho_t={\alpha_{M,t}\|z_t\|\over\|\widetilde g_t\|}\ge1,
 \qquad
 \mathcal K_{M,t}=\alpha_{M,t}\|M_t^{-1}\|\ge1,
\tag{7}
\]

and valid amplitude-amplification and projector-query costs cannot be below
one invocation.  Since \(m=\Theta(P)\), the generic coherent-tomography
subroutine specified in the compressed theorem, run at
\(\xi=\Theta(\eta/(J\rho))\), budgets

\[
 \widetilde\Theta(mJ\rho/\eta)
 =\widetilde\Omega(P)
\tag{8}
\]

controlled state-preparation/inverse invocations at constant \(\eta\).  When
the state-preparation circuit calls the raw sparse oracle, those calls expand
into raw coefficient queries; if it uses compiled data, that compilation must
be charged instead.  Equation (8) is the cost of the stated generic
tomography implementation, not a proof that this family's *dual* direction is
a worst-case tomography state.  The family-specific raw-query lower bound is
the aggregate compiler theorem in Section 3.  This family is balanced, not
tall, so retaining an \(m\)-vector provides no dimensional compression.

The remaining ledger entries are separate and cannot be omitted:

- **Static input.** Loading the explicit sparse matrix costs
  \(C_{\rm build}(A)=\Theta(P)\).  Direct oracle access avoids that load but
  charges the raw coefficient query inside every block-encoding call.
- **Retained iterate.** Loading or updating explicit \(y_t\) costs
  \(\widetilde O(mB_t)=\widetilde O(PB_t)\) memory operations per materialized
  direction.
- **Bit precision.** The dynamic range \(H=\Theta(\sqrt P)\), the objective
  slope \(w=\Theta(P^{-1/2})\), and a polynomially small tail parameter require
  \(B_t=\Theta(\log P+\log(1/\eta))\) bits even though \(\mu_1\) itself is
  constant.
- **Active access.** The hidden parity determines which member of every free
  pair is limiting nonbasic.  A free preloaded selector would be
  input-dependent advice.  The allowed coherent comparator constructs it on
  demand from current values and charges the underlying coefficient/iterate
  reads.
- **Spectral constants.** Primal nondegeneracy proves that \(A_B\) is
  nonsingular; it supplies no dimension-independent lower bound on
  \(\sigma_{\min}(A_B)\).  Likewise, (2) gives no bound on \(\chi_Q\) or the
  dual forcing factors.  The tail bounds contain
  \(\underline s_N^{-2}=\Theta(H^2)=\Theta(P)\), although matching global
  scaling may cancel this factor in \(\alpha_M\|M^{-1}\|\).  Such cancellation
  must be proved rather than inferred from (2).
- **RHS.** The hardness theorem does not prove that normalized RHS preparation
  alone is difficult.  It allows the parity information to enter through
  feasibility translation and output recovery.  Therefore the correct audit
  retains \(\Gamma_g\) but does not falsely assign the entire lower bound to
  it.

## 3. Coordinate-oracle compatibility theorem

The strongest compatibility statement does not rely on tomography dimension.
It applies to any proposed compiler for the compressed output.

### Theorem 1 (setup--query lower bound for the compressed primal oracle)

Fix a central parameter for the prefix family at which the primal point
\(x(\mu)\) is feasible and has the padded plateau described in the hardness
construction.  Suppose an algorithm makes \(S\) raw sparse coefficient
queries and outputs classical data together with a coherent value oracle

\[
 O_x:|j,0\rangle\longmapsto|j,x_j(\mu)\rangle.
\tag{9}
\]

Suppose one controlled invocation of \(O_x\) or \(O_x^\dagger\) makes at most
\(q\) additional raw coefficient queries.  Then

\[
 \boxed{S+q=\Omega(P).}
\tag{10}
\]

The same conclusion holds for a coherent value oracle for the exact Newton
direction (21) in the hardness note, with a fixed real sign convention.

#### Proof

On the \(K=16N=\Theta(P)\) plateau nodes, every central primal block has
coordinates equal, up to the hidden pair swap, to fixed positive constants
times \(H\).  Hence

\[
 \|x(\mu)\|_2=\Theta(H\sqrt P),
 \qquad
 \|x(\mu)\|_\infty=\Theta(H).
\tag{11}
\]

Prepare a uniform index, query (9), and rotate an ancilla by
\(x_j/(C H)\) for a public constant \(C\).  Equation (11) makes the success
probability

\[
 {\|x(\mu)\|_2^2\over 4P(C H)^2}=\Theta(1).
\tag{12}
\]

Constant-round amplitude amplification and uncomputation therefore prepare
\(|x(\mu)/\|x(\mu)\|\rangle\) using \(O(1)\) calls to
\(O_x,O_x^\dagger\).  The robust approximate-feasibility corollary in the
hardness note requires \(\Omega(P)\) raw coefficient queries for this state.
Expanding the compiler and oracle calls gives \(S+O(q)=\Omega(P)\), proving
(10).  The Newton direction has the same \(\Theta(P)\)-coordinate plateau,
\(\ell_2\) norm \(\Theta(H\sqrt P)\), and \(\ell_\infty\) norm \(\Theta(H)\),
so the direction-state lower bound gives the second statement.

The constants in (10) absorb the \(O(1)\) oracle invocations.  More generally,
if state preparation has amplification cost \(a\), the conclusion is
\(S+aq=\Omega(P)\).

### Corollary 2 (where the affine compressed implementation pays)

The compressed-dual oracle computes a primal coordinate from an explicit
\(m\)-vector \(y\), the final direction, and at most \(d_c\le4\) entries of the
queried column.  Thus its online evaluation cost is \(q=O(1)\) raw coefficient
queries, apart from polylogarithmic arithmetic and coherent reads of retained
vectors.  Theorem 1 forces

\[
 S=\Omega(P).
\tag{13}
\]

In the stated algorithm this setup cost appears concretely as the
\(m=\Theta(P)\) tomography/load term (8), or as
\(C_{\rm build}(A)=\Theta(P)\) if the input-dependent data are materialized.
It cannot be hidden by declaring the returned coordinate oracle to have unit
cost.

If the output contract is weakened to an explicit dual vector with no primal
coordinate oracle and no requirement that it induce a robust approximately
feasible primal state, the prefix theorem does not directly apply.  The hard
result is explicitly about original-primal states and feasibility.  This is a
real oracle boundary, not a loophole in either theorem.

## 4. Implications for positive QIPM claims

The compatibility theorem imposes the following referee rules:

1. A \(\kappa=1\) reduced Hessian does not make original-coordinate loading or
   recovery free.  Positive complexity statements must expand all block
   encodings and output compilers into raw input queries.
2. The partition-free stable theorem is useful only after a data-dependent
   tail threshold.  Strict complementarity without a uniform margin can make
   that threshold scale as \(1/P\) or worse.
3. Compressed dual output yields a dimensional advantage only when \(m=o(n)\).
   Here \(m=\Theta(n)\), and its own tomography term already matches the
   lower bound.
4. A returned primal coordinate oracle is substantive output.  On a
   well-spread vector it is equivalent, up to constant amplification, to a
   primal state preparer and inherits the same setup--query lower bound.
5. A genuinely dual-only certificate can lie outside the prefix theorem's
   scope.  Any claimed contradiction must first give a low-query reduction
   from that certificate to one of the hard primal outputs.

Status: **proved exact compatibility.  On the hard family, the compressed-dual
ledger charges \(\Omega(P)\) through retained dimension/loading, and any
purported unit-cost primal-coordinate output must have \(\Omega(P)\) compiler
setup.  The condition-one claim affects neither charge.**
