# A fixed-parameter bit bound for regridded box quadratic certificates

Date: 2026-10-02. Status: complete derivation with a
[fresh adversarial review](../reviews/regridded-qp-bit-adversary.md)
finding no substantive mathematical gap, and targeted exact-arithmetic checks.
This note specializes the aggregate contraction in
[`regridded-certificates/note.md`](../regridded-certificates/note.md) to
affine Taylor lower models. It replaces the real convex-optimization oracle
by exact corner minimization and proves a common-denominator invariant.
The rational-height arguments are from
[`exact-box-qp.md`](exact-box-qp.md). No external novelty claim is made here.

## 1. Result and scope

Consider a continuous rational box quadratic program

\[
\min_{x\in X} F(x)=\sum_{t\in T}a_t(x_{V_t}),\qquad
X=\prod_{i=1}^n[l_i,u_i].
\]

The input supplies rational quadratic bag functions, a rooted tree
decomposition with the running-intersection property, and a rational
\(M\ge0\) such that every bag Hessian has Euclidean operator norm at most
\(M\). Let \(N=|T|\), let \(p\ge1\) bound bag size, and let \(k\ge1\)
bound the number of bags containing any one coordinate. The total binary
input length \(I\) includes the factorization, decomposition, box, and
\(M\). A rational bound on the absolute row sums of every symmetric bag
Hessian supplies such an \(M\) directly. The parameter below refers to
the actual supplied bound and factorization.

For quadratics, the supplied bound can be checked exactly by testing
\(MI+\nabla^2a_t\succeq0\) and \(MI-\nabla^2a_t\succeq0\) for every
bag. Rational positive-semidefiniteness tests have uniform polynomial bit
cost. Alternatively, computing the absolute-row-sum bound above provides
a directly verifiable bound. This curvature check is separate from the
growth promise, which the algorithm never needs to verify.

Assume a unique optimizer \(x^*\) and a constant \(g>0\) satisfying

\[
F(x)-F(x^*)\ge g\|x-x^*\|_2^2\quad(x\in X).
\tag{1}
\]

The algorithm need not know \(g\). If \(M>0\), put
\(\kappa=\max\{1,M/g\}\). Empty boxes are rejected, fixed coordinates
can be substituted out, and a zero-dimensional domain is immediate.
Substitution preserves the bag Hessian bound and cannot increase \(p\)
or \(k\).

**Theorem.** There is a deterministic algorithm that, for dyadic accuracy
\(\varepsilon=2^{-q}\), where \(q\) is a nonnegative integer, returns a rational feasible point and an exact
rational decomposition certificate whose upper-minus-lower gap is at most
\(\varepsilon\), in

\[
f(p,k,\kappa)\,(I+q+1)^{C}
\tag{2}
\]

bit operations. Here \(C\) is an absolute constant independent of all
three parameters. There is also an exact algorithm for the unique
optimizer and optimum value in \(f_1(p,k,\kappa)(I+1)^{C_1}\) bit
operations, with an absolute \(C_1\). Both algorithms can run without a
supplied growth constant or a supplied bound on \(\kappa\).

Thus this is fixed-parameter tractability in \((p,k,\kappa)\), with
numerical conditioning treated as a numerical parameter. It is not FPT
in width alone. Its full-bag Hessian ratio is stronger than the
coordinate upper-curvature ratio used by the shared-coordinate-grid
algorithm, and its occurrence parameter \(k\) is explicit. The point
of this result is that the accuracy and input-length exponents do not
grow with bag dimension.

For \(M=0\), every bag is affine and so is \(F\). Sum the rational
linear coefficients and choose a minimizing endpoint for each coordinate.
This solves the problem exactly in polynomial bit time without (1).
The rest of the note assumes \(M>0\).

## 2. An affine lower model with a uniform box error

For a bag box \(B\), let \(m_B\) be its midpoint and \(W_B\) its
largest side length. Define

\[
\ell_{t,B}(z)=a_t(m_B)+\nabla a_t(m_B)^T(z-m_B)
                  -\frac{MpW_B^2}{8}.
\tag{3}
\]

Since \(\|z-m_B\|^2\le pW_B^2/4\), the two-sided Taylor estimate gives

\[
0\le a_t(z)-\ell_{t,B}(z)\le\frac{MpW_B^2}{4}
\qquad(z\in B).
\tag{4}
\]

This uses the **full absolute Hessian norm bound**, not merely an upper
bound on coordinate curvature. For quadratics the Taylor expansion is
exact, and (4) also follows immediately by bounding its quadratic term.
The model is affine, continuous, and convex.

Equation (4) is the uniform bag error needed in the regridded proof, with
\(A_0=pM\). It does not imply the original pointwise condition
\((U^q)\) in the older certificate note: the model's error can be positive
at a box vertex. Accordingly this note uses (4) in place of that stronger
condition. In the aggregate argument, the only relaxation-error step is
\(\sum_t\mathrm{err}_t\le(A_0/4)\sum_tW_{B_t}^2\), so the substitution
is sufficient. The validity of the decomposition certificate itself needs
only valid convex lower models.

Use one slope per separator, equal to the sum of the relevant bag
gradients at the current common center \(c\):

\[
\lambda_{t,i}(c)=\sum_{s\in\mathrm{sub}(t):\,i\in V_s}
                         \partial_i a_s(c_{V_s}),\qquad i\in S_t.
\tag{5}
\]

For a bag leaf \(B\), the child contribution is
\(\lambda_u^Tz_{S_u}+\min\{\beta_{u,D}:D\cap B_{S_u}\ne\varnothing\}\).
Thus each own-separator subproblem defining \(\beta_{t,D}\) minimizes
an affine function over

\[
\{z\in B:z_{S_t}\in D\}.
\tag{6}
\]

This set is an axis-aligned box, possibly of lower dimension. Empty
intersections are omitted. An exact minimizer chooses the lower endpoint
of a coordinate interval when its affine coefficient is nonnegative and
the upper endpoint when it is negative. In particular, **zero coefficients
also select an endpoint**. Root problems use the same rule. There is no
nonlinear optimization or real-comparison oracle.

Store the minimizing bag, corner, and child choices. Backtracking gives a
configuration, and selecting coordinate \(i\) from its highest bag gives
the next consistent feasible center. Every selected coordinate is therefore
an endpoint of a leaf or separator interval from that stage.

## 3. Contraction and parameter dependence

Replace \(g\) by \(\bar g=\min\{g,M\}\). This preserves (1), and now
\(M/\bar g=\kappa\ge1\). Define the constants from the aggregate proof:

\[
\begin{aligned}
C_0&=k(k-1)p, & B_0&=\frac M4(2C_0+p),\\
\eta&=\bar g/20, &
C&=12B_0+120kC_0M^2/\bar g,\\
B&=\max\{p,2C/\bar g\}.
\end{aligned}
\tag{7}
\]

Choose \(\theta=2^{-\mu}\), \(\mu\ge1\), satisfying

\[
12C_0\theta^2\le1,\qquad
\sqrt{12}\,k\sqrt{C_0}M\theta\le\bar g/80,\qquad
12kB_0\theta^2\le\bar g/80.
\tag{8}
\]

A dyadic inverse between \(1024k^2p\kappa\) and
\(2048k^2p\kappa\) satisfies all three inequalities. To see this, use
\(C_0\le k^2p\); the three required lower bounds on \(1/\theta\)
are at most

\[
4k\sqrt p,\qquad
278k^2\sqrt p\,\kappa,\qquad
27k^{3/2}\sqrt{p\kappa},
\]

respectively. The chosen bound also enforces \(\mu\ge1\). Moreover

\[
C/\bar g=3\kappa(2C_0+p)+120kC_0\kappa^2,
\qquad B\le259k^3p\kappa^2.
\tag{9}
\]

Let \(s_0=\max_i(u_i-l_i)>0\), set \(h_j=s_0 2^{-j}\), and construct
fresh shell partitions about the previous common center. Apply the exact
affine DP above and update the best feasible incumbent. The aggregate
copy-drift and telescoping proof, with (4), gives

\[
\|x^{(j)}-x^*\|^2\le BN h_j^2,
\qquad
0\le\mathrm{UBD}-\mathrm{LB}_j\le\bar g BN h_j^2.
\tag{10}
\]

It therefore suffices to reach

\[
J=\max\left\{0,\left\lceil
\log_2\bigl(s_0\sqrt{\bar g BN/\varepsilon}\bigr)
\right\rceil\right\}.
\tag{11}
\]

For \(\varepsilon=2^{-q}\), input magnitude bounds and (9) imply
\(J=O(I+q+\log\kappa)\). There is no factor \(\varepsilon^{-p/2}\)
or \((\log(1/\varepsilon))^p\) in this stage bound or the partition count.
Large linear coefficients affect rational bit length, but do not enter
\(\theta\) or \(\kappa\).

At each stage every certificate is valid, even if (8) fails; (8) is used
for convergence and complexity, not for soundness of the stopping test.

## 4. Dyadic shell corners do not accumulate new denominators

Write each bag quadratic as \(a_t(z)=z^TQ_tz+d_t^Tz+e_t\), with
\(Q_t\) symmetric. Let \(D\) be a common positive denominator for every
entry of \(Q_t,d_t,e_t\), all box endpoints, and \(M\). Its binary length
is \(O(I)\). Choose the initial center to be the lower box corner.
Then \(s_0\) and every initial coordinate also have denominator dividing
\(D\).

Fix a run with \(\theta=2^{-\mu}\). Put

\[
A_j=D\,2^{j+\mu}.
\tag{12}
\]

**Lattice lemma.** At stage \(j\), every bag-leaf and separator endpoint,
every chosen local minimizer coordinate, and every next-center coordinate
lies in \(A_j^{-1}\mathbb Z\).

*Proof.* The central part of the shell partition is cut at coordinates
\(c_i-h_j,c_i,c_i+h_j\). At shell level \(\ell=1,\ldots,j\), the mesh
is

\[
\theta\,2^{\ell-1}h_j
        =s_0\,2^{\ell-1-j-\mu}.
\]

Its coordinate lines are the current center plus integer multiples of
this mesh. All such increments belong to \(A_j^{-1}\mathbb Z\).
At stage zero the old center has denominator dividing \(D\); subsequently
its denominator divides \(A_{j-1}\), which divides \(A_j\). Clipping
chooses between a mesh boundary and an original endpoint. Intersecting
boxes chooses maxima of lower endpoints and minima of upper endpoints.
Neither operation introduces division. The affine minimization rule
chooses those intersection endpoints, and consistency extraction chooses
one of the resulting coordinates. This closes the induction. QED.

This is the actual dyadic shell construction from Lemma 3.1 of the older
certificate note. It is not the coordinate grid obtained by repeatedly
adding \(h+\theta t\); the latter has a different denominator analysis.
Midpoints are used to form lower models but are never needed as returned
minimizers, even when an affine coefficient vanishes.

**Arithmetic lemma.** At stage \(j\), all local affine values evaluated
at the chosen corners, all message intercepts, the root lower bound, and
the objective values of stage corners have denominators dividing

\[
T_j=8D A_j^2=8D^3 2^{2(j+\mu)}.
\tag{13}
\]

*Proof.* Box widths have denominator dividing \(A_j\), and their midpoints
have denominator dividing \(2A_j\). The quadratic value at a midpoint,
the gradient at a midpoint dotted with a corner-minus-midpoint, and
\(MpW_B^2/8\) all have denominators dividing \(8DA_j^2\).
The center gradients in (5) have denominators dividing \(DA_j\); their
dot products with corner coordinates divide \(DA_j^2\). A DP intercept
is obtained only by adding or subtracting these numbers and child
intercepts and then selecting a minimum. Induction through the tree
therefore preserves the same \(T_j\). There is no division by a slope,
determinant, or message coefficient. Values of \(F\) at corners divide
\(DA_j^2\). Earlier incumbent denominators also divide \(T_j\), since
the lattices are nested in denominator. QED.

Input coordinate magnitudes and coefficient magnitudes have logarithms
\(O(I)\). Every primitive quadratic or affine expression has magnitude
bounded by a polynomial in \(p,N\) times such input magnitudes; a subtree
intercept is a sum of at most \(N\) bag terms and at most \(N-1\) slope
terms. Consequently numerator and denominator lengths are
\(O(I+j+\mu+\log N+\log p)\). An exact rational implementation can
instead scale all stage values to the common denominator \(T_j\).
Either representation uses polynomial bit time per arithmetic operation,
with a polynomial degree independent of \(p\). Tree depth and the number
of preceding stages do not multiply denominators.

## 5. Counting all bit operations

Let \(m=4/\theta\). The shell-incidence proof gives at most

\[
O\bigl(N3^p m^p(j+1)^2\bigr)
\]

bag/own-separator and parent-bag/child-separator incidences at stage \(j\).
We use \(3^p\) because the supplied decomposition may have a separator
of size \(p\). If every separator has size at most \(p-1\), it may be
replaced by \(3^{p-1}\). Merging bags merely to obtain that form could
increase \(M\), so no such transformation is assumed.

Each incidence needs polynomially many operations in \(p\) to intersect
boxes, evaluate an affine corner minimum, and update a minimum. Subtree
gradient accumulation and construction of the affine models also take
polynomially many operations per bag or leaf. Incidences can be generated
by shell-level pairs and grid indices as in the source proof; a dense
all-pairs scan is unnecessary. Across stages \(0,\ldots,J\), the
arithmetic-operation count is therefore

\[
O\bigl(\operatorname{poly}(p)\,N3^p(4/\theta)^p(J+1)^3\bigr).
\tag{14}
\]

The integer bit length per operation is polynomial in \(I+J+\mu\),
by (12)--(13), and comparisons, multiplication, exact division, and gcd
computations on such integers have uniform polynomial bit cost. Substituting
\(\theta^{-1}\le2048k^2p\kappa\), \(\mu=O(\log(kp\kappa))\),
and (11) proves (2). For example, the exponential state-count factor is
bounded by \((24576k^2p\kappa)^p\); polynomial factors in the parameters
can be absorbed in \(f\).

Reading and writing the certificate and its rational data is covered by
the same bound. No supplied real-function oracle, hidden exact nonlinear
solve, or arithmetic unit-cost assumption remains.

## 6. Unknown growth constants: budget bit operations, not stages

For a fixed target accuracy, start a run for each \(\mu=1,2,\ldots\),
with \(\theta=2^{-\mu}\). In round \(r\), restart each run with
\(\mu\le r\) from the same initial corner and allow at most \(2^r\)
Turing-machine bit operations. Stop as soon as a run returns a valid
gap certificate. The budget applies to reading and constructing numbers,
partition construction, all rational operations, and output. A run may
be suspended mid-operation; this is a standard bit-step simulation, not
a unit-cost arithmetic budget. No extra stage cap is imposed.

Let \(\mu_*\) be a sufficient index from (8) and let \(T_*\) be its
total bit work from the preceding section. A round

\[
r_*\ge\max\{1,\mu_*,\lceil\log_2T_*\rceil\}
\]

is sufficient. Total simulated work through that round is
\(O(r_*2^{r_*})\), plus polynomial scheduling overhead. Since
\(2^{\mu_*}\le2048k^2p\kappa\) and
\(T_*\le f(p,k,\kappa)(I+q+1)^C\), this is again an FPT bound with
an absolute input exponent. Budgeting stages through a requirement such
as \(r\ge J\) would instead risk a factor \(2^J\); that schedule is
deliberately not used here.

Validity of a returned certificate does not rely on (1) or on guessing
the conditioning correctly. The growth assumption supplies the work bound.

## 7. Exact rational optimization

Aggregate the rational quadratic into \(F(x)=x^TQx+d^Tx+e\). Clearing
all coefficients and endpoints gives a positive integer \(D_0\) with
\(H=D_0Q\) integral. Define

\[
C_H=\max\{1,\max_{i,j}|H_{ij}|\},\quad
\Delta=(2nC_H)^n,\quad R=D_0\Delta,\quad V=D_0R^2.
\tag{15}
\]

The height lemma in `exact-box-qp.md` proves that the unique optimizer has
coordinate denominators at most \(R\), and that the optimum value has
denominator at most \(V\). The value bound holds even without uniqueness.
The binary lengths of \(R,V\) are \(O(n(I+\log n))\), hence polynomial
in \(I\) with an absolute degree. The proof uses stationarity on the
minimal continuous face and Cramer's rule; it does not enumerate faces.

An exact run at index \(\mu\) uses the target

\[
\varepsilon_\mu=
\min\left\{\frac1{4V^2},\frac{M\theta^2}{16R^4}\right\}.
\tag{16}
\]

At a stage reaching this gap, reconstruct the unique rational of
denominator at most \(V\) in the certified objective interval. For
each coordinate of the incumbent \(y\), look for a rational of
denominator at most \(R\) in

\[
[y_i-1/(4R^2),\ y_i+1/(4R^2)].
\tag{17}
\]

Each such interval contains at most one candidate, because distinct
denominator-at-most-\(R\) rationals differ by at least \(1/R^2\).
Use continued-fraction or Euclidean interval reconstruction, then verify
the candidate point's box feasibility and exact objective equality with
the reconstructed optimum value. Return only if these checks pass.
Every returned result is sound independently of the growth promise.
A run whose reconstruction fails can be discarded.

For an admissible \(\theta\), the last inequality in (8), together with
\(B_0\ge pM/4\), gives

\[
M\theta^2\le\bar g/(240kp).
\]

Thus (1) and (16) imply

\[
\|y-x^*\|^2\le\varepsilon_\mu/\bar g
       \le1/(3840kpR^4)<1/(16R^4).
\]

The true coordinate therefore belongs to every interval (17), and the
reconstruction succeeds. The precision needed in (16) is
\(O(I^2+\mu)\), including the binary length of \(M\). Equations
(11)--(14) and the bit-budget dovetail then give
\(f_1(p,k,\kappa)\operatorname{poly}(I)\) exact bit complexity.

A continuous rational quadratic on a compact box with a unique global
optimizer has some positive global quadratic-growth constant, by the
qualitative growth lemma in `exact-box-qp.md`. Consequently this exact
algorithm terminates on every such unique-optimum input; the parameter
\(\kappa\) describes its running-time guarantee. It does not provide
uniform polynomial time at arbitrarily poor conditioning.

## 8. Approximation extends to explicit rational polynomial bags

The affine lower model (3), corner rule, shell lattice lemma, and aggregate
contraction only use the bag gradient's known Lipschitz bound \(M\),
not the fact that the function is quadratic. For rational polynomial bags
in explicit monomial-list encoding, of total degree at most \(d\), assume the same
known rational full-gradient Lipschitz bound on each bag box and the same
global growth condition. The model remains valid with \(A_0=pM\).

If \(d\) is fixed, or if the encoding guarantees \(d\) is bounded by a
fixed polynomial in the input length, exact polynomial and gradient
evaluation has bit cost polynomial in \(I+\bar d(I+J+\mu)\), where
\(\bar d=\max\{d,2\}\). A valid common stage denominator is
\(D^{\bar d+1}2^{\bar d(j+\mu+1)+3}\), with \(D\) now also clearing
all monomial coefficients. Affine intercept accumulation again only adds
numbers. The certified approximation theorem therefore retains an
absolute input/accuracy exponent independent of \(p\), with the stated
degree-encoding assumption and without changing the three parameters.

This statement does not cover sparse polynomials whose binary exponents
allow exponentially large numerical degree without charging for that
degree. It also does not extend the exact rational-output conclusion:
polynomial optimizers can be algebraic with large exact output, as discussed
in [`algebraic-output.md`](algebraic-output.md). Obtaining a valid \(M\)
is a separate task; its bound and encoding are part of this theorem's input.

## 9. Verification record

The [fresh independent adversarial review](../reviews/regridded-qp-bit-adversary.md)
checked the lower models, parameter constants, denominator bound, uniform
bit complexity, adaptive schedule, and exact reconstruction. It found no
substantive correction needed; its encoding and curvature-validation
clarifications are included above.
The targeted command

```
python research-20261002/geometric-dp/checks/regridded_affine_checks.py > research-20261002/geometric-dp/checks/regridded-affine-results.json
```

passed in exact rational arithmetic. It checks 20,340 shell boxes across
ten successive centers, 494 bag/separator intersections, 714 affine minima
against corner enumeration, and 40 endpoint-selected ties. A further
4,185 shell boundary coordinates exercise several dyadic grading ratios.
Six quadratic Taylor cases use 310 probes, including sharp indefinite
Hessians. Coordinate and model-value denominators obey (12)--(13).

The [script](checks/regridded_affine_checks.py) and
[recorded output](checks/regridded-affine-results.json) test local
invariants; they are not a full regridded-DP implementation. These finite
checks do not replace the contraction proof or establish a novelty claim.
No project-wide verification or CI inspection was run.
