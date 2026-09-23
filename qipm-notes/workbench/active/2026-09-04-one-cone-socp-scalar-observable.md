# A matched classical-bit separation from one sparse Lorentz cone

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on novelty of the SOCP transfer  

## Result

The Grønlund--Larsen hard history state contains an efficiently measurable
public projector whose expectation has the Forrelation promise gap.  In the
one-cone SOCP of the companion note, only \(O(\log D)\) public three-sparse
accumulator equalities are needed to make the associated normalized overlap a
literal optimizer coordinate.

For every fixed sufficiently large \(r\), this gives a family with

\[
 \boxed{
 Q_{\rm quantum}=\operatorname{polylog}D,\qquad
 Q_{\rm classical}=\Omega(D^{1-1/r})}
\]

under the same classical-bit output contract: decide whether the magnitude
of one public optimizer coordinate lies in a low or high interval.  The
instance still has one high-dimensional Lorentz cone, constant hidden-data
sparsity, logarithmic condition number, and inverse-polylogarithmic required
objective accuracy.

## Exact history-state observable

In the \(k\)-Forrelation construction of
[Grønlund--Larsen](https://arxiv.org/abs/2411.02087), let

\[
 \gamma=e^{-1/T},\qquad A=I-\gamma U,\qquad
 M=\begin{pmatrix}0&A\\A^T&0\end{pmatrix},
\]

where \(U^{3T}=I\).  For \(x=M^{-1}e_1=[0;y]\),

\[
 y=\frac1{1-\gamma^{3T}}
 \sum_{t=0}^{3T-1}\gamma^t|t\rangle|\psi_t\rangle.
                                                               \tag{1}
\]

Throughout \(T\leq t<2T\), the work state is the final Forrelation state
\(|\psi_f\rangle\), with

\[
 \langle0^n|\psi_f\rangle=\phi_{n,k}(z).
\]

Put

\[
 S=\sum_{t=0}^{3T-1}\gamma^{2t},\qquad
 S_I=\sum_{t=T}^{2T-1}\gamma^{2t},\qquad
 q=\frac{S_I}{S}.
\]

Because \(\gamma^T=e^{-1}\),

\[
 \boxed{
 q=\frac{e^{-2}}{1+e^{-2}+e^{-4}}=0.11731\ldots.}              \tag{2}
\]

The public computational-basis projector

\[
 \Pi=\sum_{t=T}^{2T-1}
 |\mathrm{lower},t,0^n\rangle
 \langle\mathrm{lower},t,0^n|
\]

satisfies exactly

\[
 \boxed{
 \langle x/\|x\||\Pi|x/\|x\|\rangle
 =q\,\phi_{n,k}(z)^2.}                                       \tag{3}
\]

Equivalently, the public normalized vector

\[
 h=\frac1{\sqrt{S_I}}\sum_{t=T}^{2T-1}
 \gamma^t|\mathrm{lower},t,0^n\rangle
\]

obeys

\[
 \langle h|x/\|x\|\rangle=\sqrt q\,\phi_{n,k}(z).              \tag{4}
\]

For the source promise

\[
 \alpha=2^{-5k-1},\qquad \beta=2^{-5k},
\]

the magnitude and projector-probability gaps are

\[
 g=\sqrt q(\beta-\alpha)=\sqrt q\,2^{-5k-1},
\]

\[
 \Delta=q(\beta^2-\alpha^2)=3q\,2^{-10k-2}.                  \tag{5}
\]

## A literal sparse optimizer coordinate

Use the one-cone SOCP

\[
 \max_{x,u}\ 2e_1^Tu
 \quad\text{s.t.}\quad
 u=Mx,\quad(1,u)\in Q,
\]

whose unique optimizer has \(x^*=M^{-1}e_1\).  Its norm

\[
 R=\|x^*\|=\frac{\sqrt S}{1-\gamma^{3T}}
\]

is public.  For the selected coordinates
\(i_t=(\mathrm{lower},t,0^n)\), add free accumulator variables and equalities

\[
 a_t=\frac{\gamma^t}{R\sqrt{S_I}},
\]

\[
 r_T=a_Tx_{i_T},\qquad
 r_{t+1}=r_t+a_{t+1}x_{i_{t+1}},\qquad
 w=r_{2T-1}.                                                 \tag{6}
\]

Then (4) and telescoping give

\[
 \boxed{w^*=\sqrt q\,\phi_{n,k}(z).}                          \tag{7}
\]

Every new row has at most three nonzeros, every selected \(x\)-column gains
one incidence, only \(O(T)=O(\log D)\) public rows and variables are added,
and no cone is added.  The unequal new row and column norms are still public:
global SQ sampling is a public mixture of the original equal-norm rows and
the \(O(T)\) accumulator rows, while conditional samples need at most one
hidden-input query.  Thus the augmented SQ oracle is simulated with constant
hidden-query overhead and \(O(\log D)\) public preprocessing.

## Matched lower and upper bounds

Any classical SQ algorithm that estimates \(|w^*|\) to error below \(g/2\),
or directly decides

\[
 |w^*|\leq\sqrt q\,\alpha
 \quad\text{versus}\quad
 |w^*|\geq\sqrt q\,\beta,
\]

solves \(k\)-Forrelation.  Since the matrix dimension is
\(D=\Theta_k(n2^n)\), the randomized lower bound transfers as

\[
 \Omega\!\left(
 (D/\log^2D)^{1-1/k}
 \right).                                                     \tag{8}
\]

Setting the source parameter \(k=2r\) and weakening (8) absorbs logarithmic
factors and gives \(\Omega(D^{1-1/r})\) for every fixed sufficiently large
\(r\).

Quantumly, a sparse QLSA prepares \(|x^*\rangle\) in
\(\operatorname{polylog}D\) queries.  Amplitude estimation of the easy
projector \(\Pi\) resolves the Grover-angle gap in

\[
 O(g^{-1}\log(1/\zeta))=2^{O(k)}\log(1/\zeta)
\]

controlled state preparations.  For fixed \(k\), total complexity remains
\(\operatorname{polylog}D\).  State-preparation trace error must be
\(o(g)\), still a fixed constant for fixed \(k\).

The signed overlap (4) needs a phase-referenced controlled preparation.
The projector test, the magnitude decision, and (3) are phase invariant and
need no such convention.

## Objective-accuracy transfer

For an exactly feasible SOCP point with maximization gap \(\tau\), the
companion theorem gives

\[
 \frac{\|\widehat x-x^*\|}{R}\leq K\sqrt\tau,
\]

where, in the unscaled convention used here,

\[
 K_{\rm eff}=\frac{\|M^{-1}\|}{R}
 =\frac{1-\gamma^{3T}}{(1-\gamma)\sqrt S}
 =\Theta(\sqrt T)=\Theta(\sqrt{\log D}).
\]

The
coefficient vector in (6) has norm \(1/R\), so exact accumulator feasibility
implies

\[
 |\widehat w-w^*|\leq K_{\rm eff}\sqrt\tau.
\]

Therefore

\[
 \tau\leq\left(\frac{g}{3K_{\rm eff}}\right)^2
 =\Theta_k(1/\log D)
\]

suffices for the classical-bit decision.  Approximate cone or accumulator
feasibility must be added explicitly to this error ledger.

## Novelty boundary

The projector test is essentially implicit in the original
Grønlund--Larsen sampling reduction, so it is not itself new.  The apparent
new contribution is its access-preserving transfer to a one-cone SOCP and
the public sparse accumulator that produces a literal hard scalar optimizer
coordinate.  This removes the “quantum state versus classical sample”
asymmetry while preserving a near-linear-versus-polylogarithmic oracle gap.

The optimal objective value remains the public constant two.  The theorem is
about one optimizer coordinate or observable, not value-only optimization;
it also retains the coherent-data/QRAM setup caveat and one
high-dimensional Lorentz block.
