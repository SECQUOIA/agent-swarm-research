# Unambiguous certificates for exact strongly convex quartic optimization

Date: 2026-09-28. Status: proved and passed
[fresh independent adversarial review](polyhedral-strong-quartic-unambiguous-upper-review.md),
including two additional focused reviews. Publication priority is
unestablished.

The full active set at a unique optimum is a unique certificate. The
point requiring care is how to check optimality without guessing a
possibly nonunique multiplier support. A rational LP with a circuit
objective supplies that check. This strengthens the
[active-support bound](polyhedral-strong-quartic-posslp-upper.md) to
\(\mathrm{UP}^{\mathrm{PosSLP}}\cap
\mathrm{coUP}^{\mathrm{PosSLP}}\).
It does not give a deterministic way to find the active set.

## 1. Statement and dependencies

Use the input and empty-polyhedron conventions of the active-support
note. In particular, \(f\in\mathbb Q[X_1,\ldots,X_n]\) is an
explicit polynomial of degree at most four, \(P=\{X:AX\le b\}\)
is an arbitrary explicit rational polyhedron, and a supplied rational
\(\mu>0\) satisfies
\[
                  \nabla^2 f(X)\succeq\mu I_n
                  \quad(X\in\mathbb R^n).                 \tag{1}
\]
For nonempty \(P\), let \(p_P\) be its unique minimizer.

**Theorem.** Every exact value comparison, and every comparison of a
specified coordinate of \(p_P\) with a rational threshold, in the
active-support note belongs to
\[
             \mathrm{UP}^{\mathrm{PosSLP}}\cap
             \mathrm{coUP}^{\mathrm{PosSLP}}.             \tag{2}
\]
With a bare supplied \(\mu\), this is a promise statement. With a
checked full rational positive definite Hessian Gram, it gives the
corresponding ordinary languages, rejecting invalid certificates.
There is no inactive-slack gap, multiplier gap, strict complementarity,
or ordinary Slater assumption.

Here \(\mathrm{UP}^{\mathrm{PosSLP}}\) means that a
nondeterministic polynomial-time machine with a PosSLP oracle has at
most one accepting computation on each input in scope. The two sides
of (2) have separate machines. They need not share the same final
comparison, but use the same unique certificate of optimality.

The proof uses the reviewed
[unconstrained polynomial-observable theorem](strong-convex-quartic-posslp-upper.md)
in two precise forms. For a supplied strongly convex quartic \(g\)
and explicit rational \(h\) of degree at most four, exact comparison
of \(h(p_g)\) uses one PosSLP instance per comparison. Also, its
proof supplies a uniform algebraic gap and a shared rational Newton
circuit, detailed in Section 3 below. Arbitrary circuit polynomials
evaluated at the algebraic point are not assumed to satisfy that
observable theorem.

## 2. A rational LP with a circuit objective

**Lemma 1.** Let \(D,e\) be explicit rational data and let
\(Q=\{v:Dv\le e\}\) be a nonempty bounded polyhedron in
\(\mathbb R^n\). Suppose the rational objective vector \(c\)
is supplied by rational arithmetic circuits with nonzero divisors.
An optimal vertex for \(\min_{v\in Q}c^{\mathsf T}v\) can be
printed as polynomial-bit rational coordinates in deterministic
\(\mathrm P^{\mathrm{PosSLP}}\). The running time is polynomial
in the explicit data and circuit encoding lengths.

**Proof.** Grötschel, Lovász, and Schrijver,
[*Geometric Algorithms and Combinatorial Optimization*](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf),
Theorem 6.6.3, printed pages 190--191, gives a rational LP algorithm
whose number of elementary arithmetic operations is polynomial in
the encoding length of the constraint matrix. It returns an optimal
vertex if one exists. On printed page 189 the elementary operations
are specified as addition, subtraction, comparison, multiplication,
and division. Their count is independent of the objective and
right-hand-side encoding lengths. Apply it to \(D,e,-c\).

Simulate each arithmetic value by a shared rational circuit. A
rational circuit can be represented by integer circuits \(N,D_0\)
with value \(N/D_0\) and \(D_0>0\). Addition and multiplication
use the usual fraction formulas; for division use
\[
 \frac{N_1/D_1}{N_2/D_2}
       =\frac{N_1D_2N_2}{D_1N_2^2}.                    \tag{3}
\]
Every division performed by the rational LP algorithm has nonzero
divisor. Each rational comparison is therefore decided by a constant
number of PosSLP queries on integer numerators. A polynomial number
of arithmetic operations adds only polynomially many shared gates.
All initial rational constants have polynomial encodings; build their
integer constants from binary digits. Thus the simulation takes
polynomial time with a PosSLP oracle, even though some represented
rationals may have very long binary expansions.

This initially returns a vertex \(v\) by circuits. A separate
recovery step is needed to print its coordinates. Use PosSLP to find
all exact equalities \(D_i v=e_i\). The active rows at a vertex
span \(\mathbb R^n\): otherwise a nonzero vector annihilated by
all active rows would give a sufficiently short feasible segment
through \(v\) in both directions, contradicting extremality.
This argument also applies to a lower-dimensional polytope. Choose
\(n\) independent active rows using ordinary rational rank
computation, and solve their explicit rational equation system.
Its unique solution is \(v\). Gaussian elimination, or Cramer's
rule, gives polynomial-bit output in the encoding of \(D,e\).
No circuit expansion or assumption about the LP algorithm's output
format is needed. The case \(n=0\) is immediate. \(\square\)

For clarity, the source's Frank--Tardos intermediate rounding does
not introduce an unrestricted floor oracle into this simulation.
Theorem 6.2.13 gives the required elementary-operation bound. Its
proof on printed page 168 explicitly implements its componentwise
round-down by a bounded number of comparisons after normalization;
subsequent integer computations have polynomial-size data. The
operation model in Theorem 6.6.3 is the relevant source claim.

## 3. Certifying a gradient inequality without algebraic-cost LP

Let \(g\in\mathbb Q[Y_1,\ldots,Y_d]\) be globally strongly
convex with the supplied curvature bound, and let \(y_*\) be its
unconstrained minimizer. Let
\(C(Y)\in\mathbb Q[Y]^n\) be an explicit vector of polynomials
of degree at most three. For an explicit rational matrix \(A_S\),
form the bounded nonempty polytope
\[
 Q_S=\{v\in\mathbb R^n:A_Sv\le0, -1\le v_j\le1
                                      \text{ for every }j\}.
                                                               \tag{4}
\]
The case \(d=0\) has a rational constant \(C\) and is just
ordinary rational LP. Assume \(d\ge1\) below.

**Lemma 2.** Whether
\[
                   C(y_*)^{\mathsf T}v\ge0
                   \quad\text{for all }v\in Q_S            \tag{5}
\]
holds is decidable in deterministic \(\mathrm P^{\mathrm{PosSLP}}\),
with time polynomial in these explicit inputs.

**Proof.** Every vertex of \(Q_S\) has polynomial-bit rational
coordinates, uniformly in the explicit encoding of (4). To see a
concrete uniform bound, clear all constraint denominators, using their
product if necessary. Each integer entry then has polynomial bit
length. A vertex solves an invertible \(n\)-row subsystem.
Hadamard's determinant bound and Cramer's rule bound all coordinate
numerators and denominators by \(2^{q(N)}\), for a fixed
computable polynomial \(q\) in the total input length \(N\).
No vertices need to be enumerated.

For every such vertex \(v\), put
\[
                       h_v(Y)=v^{\mathsf T}C(Y).         \tag{6}
\]
These are explicit polynomials of degree at most three. Their total
coefficient encoding lengths are uniformly bounded by a computable
polynomial in \(N\). Choose a polynomially bounded integer
\(M\ge2\) bounding the combined encoding length of
\(g,\mu,h_v\) for every vertex \(v\). This choice uses only
the preceding determinant bound and the printed coefficients of
\(C\), not the unknown vertices or their values.

Let \(a\) be the fixed effective polynomial in the companion
unconstrained proof, enlarged there so that \(a(M)\ge40M+10\).
Its singleton real-projection argument gives, uniformly over all
vertices,
\[
 h_v(y_*)\ne0\quad\Longrightarrow\quad
 |h_v(y_*)|\ge\gamma,
 \qquad \gamma=2^{-2^{a(M)+1}}.                         \tag{7}
\]
Neither quantifier elimination nor vertex enumeration is executed.
The bound does not assume a finite complex critical locus.

Use the companion Newton construction with the padded length bound
\(M\): set \(B=2^{20M}\), obtain an ordinary polynomial-bit
rational point of objective error at most
\(\mu^3/(32B^2)\), and take \(k=a(M)+2\) exact rational
Newton steps as a shared circuit. The proof of that construction
applies uniformly to each \(h_v\), since its encoding is bounded
by \(M\). In particular, if the circuit point is \(y_k\),
\[
                |h_v(y_k)-h_v(y_*)|\le\gamma/8
                   \quad\text{for every vertex }v.      \tag{8}
\]
This follows from the same common derivative bound \(B\) and
Newton error bound; no vertex-specific initialization or step count
is used. All preliminary precision has polynomially many printed
bits. Only the later circuits represent the much finer accuracy.

Set \(\widehat c=C(y_k)\), a rational circuit vector, and
apply Lemma 1 to minimize \(\widehat c^{\mathsf T}v\)
over \(Q_S\). Recover a printed polynomial-bit optimal vertex
\(w\) as in that lemma. Finally, compare the explicit cubic
observable \(h_w(y_*)\) with zero using the companion theorem.

If (5) holds, that final value is nonnegative. Conversely, if (5)
fails, some vertex \(v\) has \(h_v(y_*)<0\). Equations
(7)--(8) give
\[
               \widehat c^{\mathsf T}v\le-7\gamma/8.
\]
Every vertex \(u\) with \(h_u(y_*)\ge0\) instead has
\(\widehat c^{\mathsf T}u\ge-\gamma/8\). Hence the
optimal vertex \(w\) for the rational circuit objective must
satisfy \(h_w(y_*)<0\), which the last comparison detects.
Ties among zero values or among negative values cause no problem.
This proves the equivalence and the polynomial oracle bound.
\(\square\)

The LP objective in this proof is rational, represented by a Newton
circuit. It is not the algebraic vector \(C(y_*)\). Every oracle
query inside the LP simulation is an integer circuit sign query.
The only final algebraic observable is the explicit polynomial (6)
for the recovered rational vertex. Thus there is no implicit
extension of the observable theorem to nested circuit functions of
\(y_*\).

## 4. The unique active-set verifier

In the Hessian-certificate input format, first check that certificate.
An invalid certificate is rejected in the original language and
accepted in its complement, before any empty-polyhedron convention is
applied. Next check rational feasibility of \(P\), still before any
nondeterministic choice. Empty inputs have the truth values specified
in the active-support note. Zero-dimensional
ambient instances are rational and need no guess. For every remaining
input, guess exactly \(m\) bits, one for each row of \(A\),
encoding a subset \(S\).

Choose a row basis \(I\) of \(A_S\) deterministically, for
example by scanning rows in increasing order. Use the free-coordinate
chart from the active-support note:
\[
              X=\bar x+ZY,\qquad A_IX=b_I,\qquad
              Z^{\mathsf T}Z\succeq I.                 \tag{9}
\]
The basis equations are consistent because their left-hand rows
are independent. All chart coefficients have polynomial bit length.
The restricted quartic \(g_S(Y)=f(\bar x+ZY)\) has global
curvature at least \(\mu\). Let \(y_S\) be its unique
unconstrained minimizer, and write \(p_S=\bar x+Zy_S\).
If the basis has rank \(n\), the point is rational and all
following tests use ordinary rational arithmetic and LP.

Check, by the explicit linear slack observables, that
\[
 b_i-a_i^{\mathsf T}p_S=0\quad(i\in S),\qquad
 b_i-a_i^{\mathsf T}p_S>0\quad(i\notin S).              \tag{10}
\]
This checks both primal feasibility and that the entire active set
is exactly \(S\). Inconsistent additional equations among rows of
\(S\) therefore cause rejection, even though only a row basis was
used in (9). Zero normals and redundant inequalities require no
special convention.

Set
\[
                 C(Y)=\nabla f(\bar x+ZY),              \tag{11}
\]
an explicit cubic vector with polynomial coefficient encoding.
Apply Lemma 2 to this vector and the guessed set \(S\).
Accept the optimality certificate exactly when (10) holds and
\[
      \nabla f(p_S)^{\mathsf T}v\ge0
                      \quad(v\in Q_S).                 \tag{12}
\]
Every step after the \(m\)-bit guess is deterministic with a
polynomial number of PosSLP queries.

**Soundness.** Every feasible point \(x\in P\) has
\(A_S(x-p_S)\le0\), by (10). Any such direction can be
scaled by a positive factor to lie in the box in (4). Equation (12)
therefore implies \(\nabla f(p_S)^{\mathsf T}(x-p_S)\ge0\).
Convexity gives \(f(x)\ge f(p_S)\). Strong convexity then
identifies \(p_S\) with the unique optimum \(p_P\).

**Completeness.** Let \(S_*\) be all active rows at \(p_P\).
The polyhedral normal-cone argument proved in the active-support
note gives \(-\nabla f(p_P)\) in the cone of their normals.
In particular the gradient lies in their row space. Hence \(p_P\)
is stationary on the affine space defined by any row basis of those
active equations. It is the unique minimizer of that strongly convex
restriction, so the verifier constructs \(p_{S_*}=p_P\).
Conditions (10) and (12) both hold. This uses no strict-feasibility
condition or choice of nonnegative basis multipliers.

**Unambiguity.** If any guessed \(S\) passes, soundness gives
\(p_S=p_P\), and (10) forces \(S=S_*\). Conversely \(S_*\)
passes. There is thus exactly one valid \(m\)-bit optimality
certificate. All row-basis, LP, and arithmetic choices are fixed by
deterministic algorithms, and the oracle itself is deterministic.

Finally append the desired explicit degree-four value comparison
or degree-one coordinate comparison at \(y_S\). For the opposite
language append the logical complement of that comparison instead.
Both machines have at most one accepting computation, and completeness
gives the required accepting computation on the corresponding side.
The deterministic empty-input and invalid-certificate branches preserve
unambiguity. This proves (2). \(\square\)

## 5. Significance, sources, and remaining questions

The earlier active-support verifier may accept many multiplier
supports for the same optimum. The present argument checks the full
active set without guessing any support. The extra ingredient is a
deterministic oracle check of a gradient inequality on a rational
polytope. Its proof combines a uniform algebraic gap, rational Newton
circuits, and LP operation counts independent of objective bit length.

The result classifies the nondeterminism more precisely. It neither
computes the active set in deterministic polynomial oracle time nor
reduces the constrained problem to a single PosSLP instance. Ordinary
approximation cannot in general identify all active rows without a
quantitative gap. The separately reviewed
[supplied inactive-slack-gap refinement](polyhedral-strong-quartic-active-gap.md)
states a sufficient additional promise for a deterministic one-query
reduction. No practical optimization speedup is established here.

The primary LP source was examined directly at Theorem 6.6.3 and its
proof, together with the arithmetic model on printed page 189 and
Theorem 6.2.13 on printed pages 168--169. The source proves the LP
operation bound; it does not state the present nonlinear oracle
classification. The elementary circuit simulation and printed-vertex
recovery are provided above.

The other primary dependencies and their scope are recorded in the
[unconstrained source audit](strong-convex-quartic-posslp-upper-prior.md)
and the active-support note. In particular, Slot, Steurer, and Wiedmer,
[*Hesse's Redemption*](https://arxiv.org/html/2511.03440v1),
Corollary 1.2, supplies polynomial-bit approximation. Its Section 1.3
and Table 1 distinguish exact comparison from approximation in that
dated version; they do not by themselves establish current novelty.
Allender and coauthors' Boolean-part characterization supports generic
PosSLP simulation of polynomial real arithmetic, but does not supply
an exact convex-optimization algorithm. Here the precise LP operation
model and the separate Newton construction provide that simulation's
needed hypotheses.

The [narrow prior search](polyhedral-unambiguous-prior-search.md)
did not find this constrained unambiguous
classification. That is not evidence excluding an equivalent result
under another formulation. Publication priority remains unestablished.
Even if new, this is a complexity refinement built from substantial
known tools and the companion theorem, rather than an independent
general method for fast convex optimization.

## 6. Verification record

The main independent reviewer reconstructed the complete argument.
Two additional fresh reviewers separately audited the precise GLS
arithmetic model and the uniform-gap/unique-mask steps. Their findings
are recorded in the linked review. No substantive mathematical defect
was found. The final revision repairs two display errors and makes
invalid-certificate branch precedence explicit.

The author ran:

```text
python3 research-20260927/check_polyhedral_unambiguous_upper.py
```

The independent reviewer also reran this check successfully. It
enumerates 168 active masks across six rational quadratic special
cases, recovers 17 rational vertices from their active equations,
and checks 1466 optimal-vertex sign transfers, including all ties.
The cases include redundant and zero rows, zero gradients on proper
affine spaces, skew restrictions, vertex optima, and empty active
sets. These exact finite checks exercise the certificate and
sign-transfer mechanisms; they do not establish the asymptotic gap
or operation bound. No implementation of a PosSLP oracle or of the
strongly polynomial LP algorithm is claimed. No project-wide
verification or CI inspection was performed.
