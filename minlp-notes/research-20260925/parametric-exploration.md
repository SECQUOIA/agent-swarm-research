# Parametric decomposition: a precision obstruction for exact penalties

Date: 2026-09-25. Status: complete elementary proofs checked by an independent
adversarial reviewer; bounded primary-literature comparison completed.
Originality of the precise adaptation remains provisional. See the
[proof review](parametric-penalty-review.md) and
[literature review](parametric-penalty-literature-review.md).

## Main finding

A bounded mixed-integer convex quadratically constrained problem with one
binary variable, a linear objective, and constant-size rational coefficients
can require a sharp augmented-Lagrangian penalty with exponentially many
binary digits. This remains true after optimizing over every real Lagrange
multiplier. It also holds when the requested dual bound has a fixed additive
accuracy, and when every feasible fixed-integer subproblem has a strict
Slater point with a uniform margin.

The obstruction is the distance of an **infeasible** integer assignment from
the relaxed linking equality. A chain of convex quadratic inequalities makes
this distance doubly exponentially small. Feasible-slice regularity does not
control this distance.

This addresses the general polynomial-encoding extension question posed in
the conclusion of Lefebvre and Schmidt's manuscript dated 15 December 2025,
with the qualifications in the comparison below. It does not rule
out better penalties for more restricted classes, symbolic representations
of large numbers, or formulations that change which constraints are relaxed.

## Main theorem: one binary variable

Fix \(n\geq1\), and define the compact convex quadratic chain

\[
 A_n=\{a\in[0,1]^n:a_1\geq1/4,\ a_{i+1}\geq a_i^2\ (1\leq i<n)\}.
\]

Its smallest possible final coordinate is
\(\delta_n=2^{-2^n}\), attained at \(\bar a_i=2^{-2^i}\).
Consider the native set

\[
 \widehat X_n=\{(a,y,q):a\in A_n,\ -1\leq y\leq1,
 q\in\{0,1\},\ y\geq a_n-2(1-q)\}.
\]

The original problem minimizes \(-q\) on \(\widehat X_n\) with the
additional equality \(y=0\). Define \(\widehat L_{n,\rho}(\lambda)\)
and \(\widehat D_{n,\rho}\) by minimizing
\(-q+\lambda y+\rho|y|\) over \(\widehat X_n\) and then maximizing over
\(\lambda\in\mathbb R\).

**Theorem 1.** The original optimum is zero, and, for all \(\rho\geq0\),

\[
 \widehat D_{n,\rho}
 =\min\left\{0,\frac{2\rho\delta_n-1}{1+\delta_n}\right\}.
\tag{A}
\]

Its least zero-gap penalty is

\[
 \widehat\rho_n^*=\frac1{2\delta_n}=2^{2^n-1},
\tag{B}
\]

an integer with exactly \(2^n\) binary digits, while the sparse model
encoding uses \(O(n\log n)\) bits and only one binary variable.

**Proof.** Projection onto \((q,y)\) gives exactly

\[
 (\{0\}\times[-1,1])\ \cup\ (\{1\}\times[\delta_n,1]).
\]

Indeed, the native inequality excludes \(y<\delta_n\) when \(q=1\),
and choosing \(a=\bar a\) realizes both displayed intervals. At \(q=0\),
the lower bound is \(\delta_n-2<-1\). In particular \(y=0\) forces
\(q=0\), proving the original optimum.

Evaluate any penalized subproblem at \((q,y)=(0,-1)\) and
\((q,y)=(1,\delta_n)\). Their objective values are
\(\rho-\lambda\) and \(-1+(\rho+\lambda)\delta_n\). Weighting these
values by \(\delta_n/(1+\delta_n)\) and \(1/(1+\delta_n)\) cancels the
multiplier. The minimum over the native set is no larger than this
weighted average or the value zero at \((0,0)\). This proves the upper
bound in (A), including after the unrestricted supremum over multipliers.

If \(0\leq\rho\leq1/(2\delta_n)\), set

\[
 \lambda_\rho=\frac{1+\rho(1-\delta_n)}{1+\delta_n}.
\]

Then \(\lambda_\rho\geq\rho\geq0\). On the \(q=0\) interval, the
minimum of \(\lambda_\rho y+\rho|y|\) is attained at \(y=-1\), and on
the \(q=1\) interval the minimum is attained at \(y=\delta_n\).
The two values coincide and equal \((2\rho\delta_n-1)/(1+\delta_n)\).
If \(\rho\geq1/(2\delta_n)\), take \(\lambda=\rho\). On \(q=0\),
the objective is nonnegative; on \(q=1\), it is at least
\(-1+2\rho\delta_n\geq0\). The value zero is attained at \((0,0)\).
This proves (A), hence (B). \(\square\)

At the minimum penalty, value exactness does not imply feasible penalized
minimizers: both displayed witnesses attain zero. For any strictly larger
penalty, taking \(\lambda=1/(2\delta_n)\) makes every native point with
\(y\ne0\) have strictly positive penalized objective, while every original
feasible point has objective zero. Thus solution-set exactness is also
available and has the same bit-length obstruction.

For every fixed \(0\leq\epsilon<1\), gap at most \(\epsilon\) requires

\[
 \rho\geq
 \max\left\{0,\frac{1-\epsilon(1+\delta_n)}{2\delta_n}\right\}.
\]

For example \(\epsilon=1/2\) requires
\(\rho\geq(1-\delta_n)/(4\delta_n)\), again exponentially many ordinary
binary digits. The normalized original objective range is one.

The only feasible fixed-integer slice is \(q=0\). It has the strict point
\(a_i=3/8,y=0\), with all continuous inequality slacks at least \(1/8\).
The native \(q=1\) slice has the equally strict point
\(a_i=3/8,y=1/2\), although it is infeasible after imposing \(y=0\).
This verifies the same source assumptions as the symmetric companion
below. All nonlinear native constraints are convex quadratic; every
coefficient belongs to a fixed finite set.

## Symmetric companion: definition and construction

Fix an integer \(n\geq1\). The continuous variables are
\(a=(a_1,\ldots,a_n)\) and \(y\); the binary variables are \(q,b\).
Define the compact native feasible set \(X_n\) by

\[
\begin{aligned}
 &0\leq a_i\leq1 &&(1\leq i\leq n),\\
 &a_1\geq\tfrac14,\\
 &a_{i+1}\geq a_i^2 &&(1\leq i<n),\\
 &-1\leq y\leq1,\qquad q,b\in\{0,1\},\\
 &y\geq a_n-(1-q)-2(1-b),\\
 &y\leq-a_n+(1-q)+2b.
\end{aligned}
\]

The original problem and its sharp augmented-Lagrangian dual are

\[
 P_n=\min\{-q:(a,y,q,b)\in X_n,\ y=0\},
\]

\[
 L_{n,\rho}(\lambda)
 =\min_{(a,y,q,b)\in X_n}
       \{-q+\lambda y+\rho|y|\},
 \qquad
 D_{n,\rho}=\sup_{\lambda\in\mathbb R}L_{n,\rho}(\lambda),
 \quad\rho\geq0.
\]

Only the scalar linear equality \(y=0\) is dualized. All standard scalar
\(\ell_p\) norms equal \(|y|\). Allowing arbitrary scaled norms would move
some of the numerical size into that norm's coefficient and is not the
encoding model asserted here.

The continuous relaxation of \(X_n\) is convex: the only nonlinear
constraints are \(a_i^2-a_{i+1}\leq0\), each a convex quadratic inequality.
All other native constraints are linear. The input uses \(n+3\) variables,
\(O(n)\) constraints, and coefficients in a fixed finite set. Its sparse
binary encoding length is \(O(n\log n)\); standard dense encoding also has
polynomial length in \(n\).

Write

\[
 \delta_n=2^{-2^n},\qquad
 \bar a_i=2^{-2^i}.
\]

Repeated induction gives \(a_i\geq\bar a_i\) at every point of \(X_n\).
The vector \(\bar a\) attains all these lower bounds.

## Symmetric companion: exact dual value

**Theorem 2.** For every \(n\geq1\) and \(\rho\geq0\),

\[
 P_n=0,
 \qquad
 D_{n,\rho}=\min\{0,-1+\rho\delta_n\}.
\tag{1}
\]

Consequently the least penalty giving zero duality gap is exactly

\[
 \rho_n^*=\delta_n^{-1}=2^{2^n}.
\tag{2}
\]

**Proof.** If \(q=1,b=1\), the lower linking inequality gives
\(y\geq a_n\geq\delta_n>0\). If \(q=1,b=0\), the upper inequality gives
\(y\leq-a_n\leq-\delta_n<0\). Thus \(y=0\) forces \(q=0\).
The point \((\bar a,0,0,0)\) belongs to \(X_n\), so \(P_n=0\).

For \(\lambda=0\), a native point with \(q=0\) has penalized objective
\(\rho|y|\geq0\). A native point with \(q=1\) has
\(|y|\geq\delta_n\), hence objective at least \(-1+\rho\delta_n\).
These bounds are attained by \((\bar a,0,0,0)\) and by either of

\[
 x^+=(\bar a,\delta_n,1,1),\qquad
 x^-=(\bar a,-\delta_n,1,0).
\]

Therefore
\(L_{n,\rho}(0)=\min\{0,-1+\rho\delta_n\}\).
For arbitrary \(\lambda\), evaluating at the feasible zero-objective point
and at \(x^+,x^-\) gives

\[
 L_{n,\rho}(\lambda)
 \leq\min\{0,-1+(\rho-|\lambda|)\delta_n\}
 \leq\min\{0,-1+\rho\delta_n\}.
\]

Taking the supremum in \(\lambda\) proves (1); (2) follows. In particular,
the supremum is attained at \(\lambda=0\), so nonattainment of the dual
supremum plays no role. \(\square\)

The proof establishes zero duality gap. At \(\rho=\rho_n^*\), the points
\(x^+,x^-\) also minimize the zero-multiplier penalized objective, despite
violating \(y=0\). To force every penalized optimizer to satisfy \(y=0\),
one can take \(\lambda=0\) and \(\rho>\rho_n^*\). These are different
notions of exactness.

For completeness, projecting \(X_n\) onto \((q,y)\) gives exactly

\[
 (\{0\}\times[-1,1])
 \ \cup\
 (\{1\}\times([-1,-\delta_n]\cup[\delta_n,1])).
\]

The inclusion from left to right follows from the sign constraints. For
the reverse inclusion, set \(a=\bar a\). When \(q=0\), the choices
\(b=0,1\) cover respectively \([-1,1-\delta_n]\) and
\([\delta_n-1,1]\), whose union is \([-1,1]\).
When \(q=1\), the two choices give the two displayed outer intervals.
Thus an optional full formula, writing \(c=\rho-|\lambda|\), is

\[
 L_{n,\rho}(\lambda)=\min\{0,-1+c\delta_n,-1+c\}.
\]

## Symmetric companion: encoding and approximation consequences

The integer \(2^{2^n}\) has \(2^n+1\) binary digits. More generally, any
nonnegative rational \(\rho\geq2^{2^n}\), written as an ordinary numerator
and positive denominator in binary, needs a numerator with at least
\(2^n+1\) digits. This is superpolynomial in the input length under either
sparse or dense ordinary encoding. Writing a power expression such as
\(2^{2^n}\) is a different, succinct representation model.

Equation (1) also gives the exact gap

\[
 P_n-D_{n,\rho}=\max\{0,1-\rho\delta_n\}.
\]

For any prescribed \(0\leq\epsilon<1\), obtaining dual gap at most
\(\epsilon\) requires and is sufficient for

\[
 \rho\geq(1-\epsilon)2^{2^n}.
\]

In particular, the fixed accuracy \(\epsilon=1/2\) already requires a
penalty at least \(2^{2^n-1}\), with exponentially many digits. The issue is
not confined to symbolic exact equality of primal and dual values.

The lower bound does not establish a running-time lower bound for solving
these optimization problems. The primal optimum and its feasibility
certificate are immediate from the displayed model. It establishes a
representation and regularization limitation for this prescribed
augmented-Lagrangian relaxation.

## Regularity and the source's assumptions

The objective is linear, the native set is nonempty and compact, and the
penalty is the absolute-value norm. The problem therefore satisfies
Assumptions 1--4 of Lefebvre--Schmidt in their stated roles.

For Assumption 5, fix the binary variables. For \(q=1\), the subproblem
including \(y=0\) is infeasible, which is an allowed alternative in that
assumption. For \(q=0\) and either value of \(b\), take

\[
 a_i=3/8\quad(1\leq i\leq n),\qquad y=0.
\]

Every continuous-variable native inequality is strictly satisfied. The
slack in \(a_1\geq1/4\) is \(1/8\); each nonlinear inequality has slack
\(3/8-(3/8)^2=15/64\); the smaller of the two sign-inequality slacks is
\(5/8\); the variable bounds have slack at least \(3/8\). Thus all these
slacks are at least \(1/8\), uniformly in \(n\). In particular the
source's requirement, strictness only for nonlinear constraints, holds.

The native slices with \(q=1\), before imposing \(y=0\), also have
uniform strict points: retain \(a_i=3/8\) and take \(y=1/2\) if \(b=1\),
or \(y=-1/2\) if \(b=0\). The minimum continuous inequality slack is again
at least \(1/8\). Nonetheless their distance in the relaxed equality is
exactly \(\delta_n\). Thus uniform strict feasibility of the native slices
and of all feasible original slices is insufficient to bound the penalty
with polynomially many digits.

## Literature examined and scope of the addition

1. Henri Lefebvre and Martin Schmidt, *Exact Augmented Lagrangian Duality for
   Nonconvex Mixed-Integer Nonlinear Optimization*, manuscript dated 15
   December 2025, [current open PDF](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf).
   The downloaded PDF and its extracted text are retained in
   [parametric-sources](parametric-sources/). Definition 1 uses zero duality
   gap after maximizing over the multiplier. Section 2 gives compactness,
   objective, and penalty assumptions. Assumption 5 and Theorem 14 cover
   mixed-integer convex problems with a Slater condition for every feasible
   fixed-integer slice. Section 6 asks whether the polynomial encoding
   guarantee known for MIQP extends to quadratically constrained problems.
   The proposed construction supplies a negative instance family inside
   the mixed-integer convex quadratically constrained class and satisfying
   that sufficient condition. It does not contradict their finite-penalty
   theorem.
2. Xiaoyi Gu, Shabbir Ahmed, and Santanu S. Dey, *Exact Augmented Lagrangian
   Duality for Mixed Integer Quadratic Programming*, SIAM J. Optim. 30
   (2020), 781--797, [primary preprint](https://arxiv.org/abs/1907.00920).
   The independent literature reviewer inspected Definition 8 and Theorem
   11 in full. They provide polynomial encoding for a convex quadratic
   objective over a rational mixed-integer polyhedron. The new family
   instead has a linear objective and convex quadratic **constraints**.
3. Avinash Bhardwaj, Vishnu Narayanan, and Abhishek Pathapati, *Exact
   augmented Lagrangian duality for mixed integer convex optimization*,
   SIAM J. Optim. 34 (2024), [primary preprint](https://arxiv.org/abs/2209.13326).
   The independent literature reviewer inspected Theorem 3.3 and Remark
   3.4 in full. Its linearly constrained setting and value-function
   approach are direct background; the proposed obstruction requires
   nonlinear native constraints.
4. The local scout
   [scout_area678_convex_decomp_new.md](../research-20260922/scouting/scout_area678_convex_decomp_new.md)
   identified the penalty-encoding question and existing nonconvex Benders
   and Lipschitz-cut methods. The existing
   [separator novelty review](../notes/research-20260922-separator-novelty.md)
   cautions that general feature matching and value approximation duality
   have substantial prior art. These sources motivated abandoning a
   generic new-cut claim in favor of the precise representation question.
5. Daniel Bienstock, Alberto Del Pia, and Roland Hildebrand,
   *Complexity, Exactness, and Rationality in Polynomial Optimization*,
   [open preprint](https://arxiv.org/pdf/2011.08347), Section 6. The
   independent reviewers directly inspected the convex large-coordinate
   chain and bounded nonconvex small-residual example. Their latter
   example already implies a large ordinary zero-multiplier norm penalty
   by dividing objective improvement by residual size. The theorem here
   retains convex native quadratic constraints and quantifies the
   optimized augmented dual, so a claim of discovering a generic QCQP
   penalty precision obstruction would overstate the addition. The
   source's small-residual vector has an apparent indexing issue; see the
   review before quoting its exact exponent. The qualitative comparison
   does not depend on that exponent.
6. Yasmine Beck, Daniel Bienstock, Martin Schmidt, and Johannes Thürauf,
   *On a Computationally Ill-Behaved Bilevel Problem with a Continuous and
   Nonconvex Lower Level*,
   [open manuscript](https://optimization-online.org/wp-content/uploads/2022/02/nearly-feasible-bilevel-preprint.pdf).
   Section 2 and Result 4 use a compact convex quadratic squaring chain
   with Slater regularity to demonstrate large sensitivity to extremely
   small feasibility errors. This is a close antecedent for both the
   mechanism and regularity qualification. Its conclusion concerns
   bilevel approximate feasibility rather than the optimized sharp
   augmented dual considered here.

No failed search establishes novelty. In particular, repeated squaring is
a standard small-number construction, and analogous precision phenomena
are known in conic optimization. The potentially new addition is their
use to settle the stated sharp-penalty encoding question, with optimized
multipliers, one binary (or two in the symmetric companion), convex quadratic constraints, uniform feasible
Slater margins, and the explicit fixed-accuracy gap formula. The exact
bounded prior-art comparison is recorded in the independent literature
review, which also discusses conic precision and alternative penalty
formulations. It is not an exhaustive novelty certificate.

The literature audit also found a distinction in Lefebvre--Schmidt's
Example 13: its supremum over multipliers equals the primal value even
though no finite multiplier attains it. The independent review records the
branch calculation, which the present author and root agent separately
rechecked from the source. Therefore that example is not used as evidence
of a positive optimized-dual gap. The present theorems directly bound the
supremum over all multipliers and attain their displayed dual values.

## Capabilities, limitations, and next questions

The theorem identifies a missing quantitative assumption in attempts to
make nonconvex Benders or dual dynamic programming penalties uniformly
small: feasible-slice regularity must be supplemented by control of
objective-improving infeasible slices. That is a proved obstruction to
such a conclusion from the stated assumptions alone. It is not yet a new
decomposition algorithm.

The completed [geometry note](penalty-geometry.md) separates the distance
of infeasible integer slices from sensitivity within feasible slices. The
[upper-bound companion](penalty-upper-bound.md) makes that split
quantitative: it proves an exponential encoding upper bound in continuous
dimension and a polynomial encoding bound when the number of nonlinear
quadratic inequalities is fixed. The
[right-hand-side perturbation result](smoothed-penalty.md) gives a different,
probabilistic route to short encodings. These are encoding results, not
algorithms for choosing useful coefficients in a solver. Recognizing
favorable structure, changing which constraints are relaxed, and obtaining
numerically reasonable penalties remain separate tasks.

There is also a concrete limitation to the obstruction. Set
\(p_n=2^{-n}\), a rational exponent with \(O(n)\) encoding length. Then
\(\delta_n^{p_n}=1/2\). For either construction, using the augmentation
\(2|y|^{p_n}\) and multiplier zero gives a nonnegative penalized objective
on \(q=0\), and gives at least \(-1+2\delta_n^{p_n}=0\) on \(q=1\).
It is therefore value-exact with a constant coefficient; a coefficient
strictly larger than two gives solution-set exactness. This elementary
observation does not refute the norm-penalty theorem: the augmentation
changes with the instance and is non-Lipschitz at zero. It illustrates why
allowing sufficiently sharp fractional penalties changes the encoding
question. Any general development must be compared with established
Hölder error bounds and non-Lipschitz exact penalty theory, and must assess
the added difficulty of minimizing the augmented objective.

## Verification record

The derivation above is exact and symbolic. Targeted checks so far:
`rg` reads of the named local notes and source; open primary-source web
searches; `curl` download and `pdftotext -layout` for the dated
Lefebvre--Schmidt source. The command
`python research-20260925/check_parametric_penalty.py` passed 72 exact
rational dual-envelope cases for dimensions 1 through 12, plus chain
identities, penalty bit lengths, and strict-point margins. This checks
finite cases and the independently implemented projected formulas; it
does not replace the symbolic proof, validate novelty, or test a solver.
The independent proof reviewer also ran
`python research-20260925/parametric-penalty-review-check.py`, checking 400
exact rational endpoint cases for each variant (800 total), and
independently rederived the one-binary formula. Those finite cases support arithmetic and indexing;
the proofs supply the general statements. No project-wide checks or CI
inspection were run.
