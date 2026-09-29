# One negative Hessian eigenvalue does not control convex-cover complexity

Status: a proved obstruction to an inertia-only approximation bound. The proof
has received an independent adversarial audit, recorded below. The
[bounded primary-source comparison](branching-curvature-prior.md) is complete;
publication priority remains unestablished.

## Motivation and scope

A tempting solver principle is that a function with at most \(k\) negative
Hessian eigenvalues should require only \(O(\varepsilon^{-k/2})\) convex
pieces for a uniform epigraph approximation of vertical accuracy
\(\varepsilon\). A fixed subspace containing every negative direction can
support such a principle, and a uniform positive spectral gap can support
local reductions. Pointwise negative inertia alone cannot.

We construct one fixed \(C^2\) function on \([0,1]^n\), for every \(n\ge2\),
whose Hessian has at most one negative eigenvalue everywhere, but whose
convex epigraph cover complexity has the full ambient exponent \(n/2\).
The construction places many shallow, disjoint wells in successively smaller
slabs. Each well has nonnegative tangential curvature and can have negative
curvature only in its radial direction.

This is a lower bound for uniform approximation by convex disjuncts. It is
not a running-time lower bound for unrestricted optimization algorithms, nor
for branch-and-bound stopped after proving one scalar objective bound.

## Approximation model

Let \(D=[0,1]^n\), and use epigraphs relative to \(D\). Define
\(N_f(\varepsilon)\) as the least positive integer \(N\) for which there are
convex sets \(K_1,\ldots,K_N\subseteq D\times\mathbb R\) satisfying
\[
 \operatorname{epi}_D f
 \subseteq \bigcup_{i=1}^N K_i
 \subseteq \operatorname{epi}_D(f-\varepsilon).
 \tag{1}
\]
Set \(N_f(\varepsilon)=\infty\) if no finite cover exists. Closure and
polyhedrality are not required. Thus a lower bound in this model applies to
convex relaxation epigraphs on convex branch cells, including overlapping
cells. It also applies if only the graph of \(f\), rather than its full
epigraph, is required on the left of (1).

For example, if convex cells cover \(D\) and each cell carries a convex
underestimator \(g\) satisfying \(f-\varepsilon\le g\le f\), their
restricted epigraphs satisfy (1).

## The theorem

**Theorem.** For each integer \(n\ge2\), there is a function
\(f\in C^2(\mathbb R^n)\), supported in \([0,1]^n\), such that:

1. \(\nabla^2 f(x)\) has at most one strictly negative eigenvalue at every
   \(x\in\mathbb R^n\).
2. \(\sup_x\|\nabla^2 f(x)\|\le 3/8\).
3. For some constants \(c_n,C_n>0\) and all sufficiently small
   \(\varepsilon>0\),
   \[
   c_n\frac{\varepsilon^{-n/2}}
             {(\log(1/\varepsilon))^{n/2+2}}
   \le N_f(\varepsilon)
   \le C_n\varepsilon^{-n/2}.
   \tag{2}
   \]

Consequently,
\[
 \lim_{\varepsilon\downarrow0}
 \frac{\log N_f(\varepsilon)}{\log(1/\varepsilon)}=\frac n2.
 \tag{3}
\]
In particular, for this one fixed function and every \(\beta<n/2\), there
is no constant \(C_f\) with
\(N_f(\varepsilon)\le C_f\varepsilon^{-\beta}\) for all sufficiently
small \(\varepsilon\).

### 1. One radial well

For \(a,r>0\) and \(c\in\mathbb R^n\), put
\[
 w_{a,r,c}(x)=-a\left(1-\frac{\|x-c\|^2}{r^2}\right)_+^3.
 \tag{4}
\]
Here \(t_+=\max\{t,0\}\). This function is \(C^2\) on all of
\(\mathbb R^n\), is negative exactly on \(B(c,r)\), and is zero with its
first two derivatives on the ball boundary. Write \(u=x-c\) and
\(s=\|u\|^2/r^2\). For \(s<1\),
\[
 \nabla w=\frac{6a}{r^2}(1-s)^2u,
 \qquad
 \nabla^2 w=
 \frac{6a}{r^2}(1-s)^2I-
 \frac{24a}{r^4}(1-s)uu^\top.
 \tag{5}
\]
Its tangential eigenvalue, with multiplicity \(n-1\) away from the center,
and its radial eigenvalue are respectively
\[
 \lambda_T=\frac{6a}{r^2}(1-s)^2\ge0,
 \qquad
 \lambda_R=\frac{6a}{r^2}(1-s)(1-5s).
 \tag{6}
\]
At the center all eigenvalues equal \(6a/r^2\). Hence there is at most one
negative eigenvalue, occurring exactly when \(1/5<s<1\). In addition,
\[
 |w|\le a,\qquad \|\nabla w\|\le6a/r,
 \qquad \|\nabla^2w\|\le6a/r^2.
 \tag{7}
\]
For the last bound, \((1-s)(1-5s)\) ranges between \(-4/5\) and \(1\)
on \([0,1]\).

### 2. Explicit packing

For integers \(m\ge16\), define
\[
 L_m=\frac1{16m^2},\quad
 t_m=\sum_{j=m}^{\infty}L_j,\quad
 r_m=2^{-m},\quad
 a_m=\frac{r_m^2}{m}.
 \tag{8}
\]
The slabs
\[
 S_m=(t_{m+1},t_m)\times(0,1)^{n-1}
\]
are pairwise disjoint and lie in \((0,1)^n\). In slab \(m\), take the
Cartesian grid of centers
\[
 c_1=t_{m+1}+2r_m+4r_mj_1,
 \qquad c_i=2r_m+4r_mj_i\quad (2\le i\le n),
 \tag{9}
\]
where
\[
 0\le j_1<q_{m,1}:=\left\lfloor\frac{L_m}{4r_m}\right\rfloor,
 \qquad
 0\le j_i<q_m:=\left\lfloor\frac1{4r_m}\right\rfloor.
\]
All these balls of radius \(r_m\) have closures inside their slabs and
have pairwise disjoint closures, also across different slabs. Since
\(L_m\ge8r_m\) for \(m\ge16\), their number \(M_m\) satisfies
\[
 M_m=q_{m,1}q_m^{n-1}
 \ge\frac{L_m}{8^nr_m^n}
 =\frac{2^{mn}}{16\cdot8^nm^2}.
 \tag{10}
\]
For completeness, \(L_{16}/r_{16}=16\), and
\((L_{m+1}/r_{m+1})/(L_m/r_m)=2m^2/(m+1)^2>1\) for \(m\ge16\).

Define \(f\) as the sum of (4) over all these balls with parameters
\((a_m,r_m,c)\), and set it to zero off the balls. At most one summand is
nonzero at any point.

### 3. Global regularity and inertia

Away from the plane \(x_1=0\), a sufficiently small neighborhood meets
only finitely many slabs and balls, so \(f\) is \(C^2\) there. Within
slab \(m\), bounds (7) become
\[
 |f|\le\frac{4^{-m}}m,\qquad
 \|\nabla f\|\le\frac{6\,2^{-m}}m,\qquad
 \|\nabla^2f\|\le\frac6m.
 \tag{11}
\]
We check regularity at the accumulation plane directly. If \(p_1=0\)
and \(x\) lies in a ball of slab \(m\), then
\[
 \|x-p\|\ge x_1>t_{m+1}
 \ge\frac1{16(m+1)}.
 \tag{12}
\]
As \(x\to p\) through these balls, \(m\to\infty\). Equations
(11)--(12) give
\[
 \frac{|f(x)|}{\|x-p\|}\to0,
 \qquad
 \frac{\|\nabla f(x)\|}{\|x-p\|}\to0.
\]
Off the balls both numerators vanish. Thus \(f\) is differentiable at
\(p\) with gradient zero, and this gradient is differentiable at \(p\)
with derivative zero. The Hessian is continuous there by (11). This proves
\(f\in C^2(\mathbb R^n)\).

The Hessian is zero off the ball interiors, and (6) gives the asserted
inertia within each ball. Its norm is at most \(6/16=3/8\).

### 4. A general disjoint-well lower bound

**Lemma.** Suppose \(f\) is zero off pairwise disjoint open balls
\(B(c_j,r_j)\subseteq D\), is zero on their boundaries, and
\(f(c_j)=-a_j\). Every cover satisfying (1) has at least
\(\#\{j:a_j\ge2\varepsilon\}\) members.

**Proof.** Each graph point \((c_j,-a_j)\) with
\(a_j\ge2\varepsilon\) belongs to a cover member. Suppose that two
such graph points belong to one convex member. The line segment between
their centers exits the first ball at a point \(z\) strictly between the
centers. This boundary point lies in no other open ball: if another open
ball contained it, its neighborhood would intersect the first ball's
interior, contradicting disjointness. Hence \(f(z)=0\), even if infinitely
many balls accumulate nearby. The corresponding point of the graph-space
chord has height at most \(-2\varepsilon\), and belongs to that convex
member. It is outside \(\operatorname{epi}_D(f-\varepsilon)\), whose
minimum height at \(z\) is \(-\varepsilon\). This contradicts (1).
Thus each member contains at most one selected graph point. \(\square\)

Apply the lemma to the balls in slab \(m\). Whenever
\(a_m\ge2\varepsilon\),
\[
 N_f(\varepsilon)\ge M_m
 \ge\frac{2^{mn}}{16\cdot8^nm^2}.
 \tag{13}
\]
For all sufficiently small \(\varepsilon\), choose the largest such
\(m\). The adjacent-depth ratio
\[
 \frac{a_m}{a_{m+1}}=4\frac{m+1}{m}\le8
\]
implies
\(2\varepsilon\le a_m<16\varepsilon\). Since
\(2^{mn}=(a_mm)^{-n/2}\), (13) gives
\[
 N_f(\varepsilon)
 \ge c_n\varepsilon^{-n/2}m^{-n/2-2}.
\]
Also \(4^{-m}\ge2m\varepsilon\ge2\varepsilon\), so
\(m\le\log(1/(2\varepsilon))/\log4\). This proves the lower bound
in (2) for every sufficiently small tolerance, not just a subsequence.

### 5. Matching ambient exponent

The elementary upper bound uses only a bounded Hessian. Suppose
\(\nabla^2f\succeq-LI\) on \(D\), for some \(L>0\). Partition
\(D\) into cubes of side at most \(h\). On one such cube \(Q\) with
center \(c\), let \(R_Q=\max_{x\in Q}\|x-c\|\), and define
\[
 g_Q(x)=f(x)+\frac L2\|x-c\|^2-\frac L2R_Q^2.
 \tag{14}
\]
The function \(g_Q\) is convex and obeys
\[
 f(x)-\frac{Ln h^2}{8}\le g_Q(x)\le f(x)
 \quad (x\in Q).
\]
Taking \(h\le\sqrt{8\varepsilon/(Ln)}\) produces (1) with
\(O(\varepsilon^{-n/2})\) convex epigraphs. The construction above has
\(L=3/8\). This proves the upper bound in (2), and (3) follows.

## What the obstruction establishes

- A pointwise bound of one negative eigenvalue does not imply a smaller
  uniform convex-cover exponent than the general bounded-Hessian case.
  The counterexample is one fixed function with a bounded Hessian, so
  allowing a function-dependent constant does not rescue a smaller power.
- If an affine branching scheme ends with convex epigraph relaxations of
  uniform vertical error at most \(\varepsilon\), it needs at least the
  number of leaves in (2). The lower bound permits arbitrary convex pieces,
  so the choice of affine branch directions cannot evade it.
- A finite binary disjunctive convex model with \(b\) binary variables has
  at most \(2^b\) fixed-binary convex projections. If its continuous
  projection satisfies (1), then
  \[
   b\ge\frac n2\log_2(1/\varepsilon)
        -\left(\frac n2+2\right)\log_2\log(1/\varepsilon)-O_n(1).
  \]
  This assertion requires that fixing every binary variable leaves a
  convex feasible set. It does not cover formulations with residual
  general integer variables.

The last argument does **not** give a lower bound on the number of
unrestricted integer variables. Our incompatible pairs need not be
midpoint-incompatible, which would be needed for a parity argument.

The construction leaves room for positive results based on more information:
a common low-dimensional subspace, quantitative spectral gaps, controlled
variation of eigenspaces, or geometric restrictions on the number and sizes
of nonconvex regions. Determining a useful condition that is both weaker than
a uniform positive gap and strong enough to reduce the approximation
exponent remains open in this investigation.

## Literature comparison

Ma, Chen, Jin, Flammarion, and Jordan,
[“Sampling Can Be Faster Than Optimization” (2019)](https://arxiv.org/pdf/1811.08413),
Theorem 2 and Appendix C, prove a derivative-oracle global-optimization
lower bound of order \(\varepsilon^{-n/2}\), with the smoothness and region
size parameters fixed. Their equation (45) places a negative radial well
at a hidden member of a ball packing and uses a flat background inside the
region. The radial profile is increasing, so nonnegative tangential
curvature follows by the same radial-Hessian calculation used here. This is
our observation about their construction, not an inertia claim quoted from
their theorem. Their regularity assumption is a Lipschitz gradient.

Thus the radial well and ambient ball-packing mechanism are established
antecedents. The statement proved here differs in its quantifiers and
approximation model: one fixed globally \(C^2\) function contains all scales,
and every uniform convex epigraph cover requires the ambient exponent. Their
oracle lower bound uses a hidden well chosen for the requested tolerance;
it is not itself a convex-cover lower bound. These distinctions do not
establish novelty. We examined the paper's Theorem 2 and Appendix C,
especially equation (45).

The completed [convex-cover comparison](branching-curvature-prior.md)
identifies the segment argument as the classical invisibility-clique
lower bound on convex-cover size. It also checks real q-convexity as
the established name for the smooth negative-inertia hypothesis, and
compares binary convex disjuncts with general-integer midpoint
obstructions. The specific result retained here is the explicit fixed
C² construction with bounded Hessian, its everywhere bounded negative
inertia, and its all-tolerances approximation exponent. The audit did
not identify an equivalent theorem among the statements examined;
that does not establish novelty.

## Verification and limits

An independent child agent (`rankone_counterexample`) independently found
the disjoint-well idea and then audited the stated construction. The audit
specifically checked the segment argument against other and accumulating
balls, the all-tolerances conversion from adjacent depths, and regularity at
the accumulation plane. Its positive assessment is evidence, not a
substitute for the proofs above.

A second fresh reviewer (`barrier_full_audit`) independently checked the
complete proof, including exact finite packing/depth computations for
\(m=16,\ldots,199\), and reported no substantive error. That reviewer
identified one missing scope condition in the standalone disjoint-well
lemma: the balls must lie in \(D\), so their center graph points are covered
by (1). The lemma now states that condition explicitly; the construction
already satisfies it. This correction does not change the theorem.

Targeted symbolic and numerical checks are recorded in
`branching-degeneracy-checks.py`. The script checks the two-dimensional
Hessian formula symbolically, samples its eigenvalues, and checks the finite
packing/depth inequalities. These checks do not prove the infinite packing,
global \(C^2\) extension, or the covering lower bound; the arguments above
do. Commands actually run:

```text
python research-20260928/solver/branching-degeneracy-checks.py
  PASS: symbolic Hessian and radial/tangential eigenvectors
  PASS: 1,001 exact rational eigenvalue samples
  PASS: packing and depth inequalities for m=16..300, n=2,3,5,10
git diff --check -- research-20260928/solver/branching-degeneracy-barrier.md research-20260928/solver/branching-degeneracy-checks.py
  exit 0; this does not inspect new untracked files
python - [inline pathlib check of final newlines and trailing whitespace in both new files]
  PASS: both new files end with newline and have no trailing whitespace
```

No project-wide checks or CI checks were run for this note.

The bounded literature audit and its limitations are recorded in
[branching-curvature-prior.md](branching-curvature-prior.md). It is complete
at the stated scope and supports the qualified assessment above. The upper
bound is elementary quadratic convexification and is included for comparison,
not presented as new.
