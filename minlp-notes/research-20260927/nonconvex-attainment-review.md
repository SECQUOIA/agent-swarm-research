# Adversarial review of attained optimizer bounds

Date: 2026-09-28. Status: the complete original manuscript, the revised
inactive-box proof, the final algorithm, and their dependencies were reviewed
independently. A fresh second reviewer also checked the inactive-box step.

The claim concerns rational quadratic inequalities, arbitrary affine rows,
an arbitrary rational quadratic objective, and no supplied box. The parameter
\(h\) is the dimension of the constraint-Hessian span; the objective Hessian
is excluded. If a finite minimum is attained, a global optimizer of minimum
Euclidean norm has a common algebraic description of size \(N^{O(h+1)}\).

**Finding.** No substantive gap was found in the
[main manuscript](nonconvex-attainment-and-optimizer.md). Its revised
inactive-box argument removes the original outer radius limit entirely.
The proof must still retain one nested vector sequence for all coordinate
outputs and exclude exceptional outer perturbation parameters.
The complexity consequences do not give an algorithm without an NP oracle
or establish publication priority.

## 1. Scope and independent checks

I read the generic perturbation, common-field, and rational univariate
representation arguments in
[the nonconvex certificate note](nonconvex-hessian-span-frontier.md), the
radius-dependent charts and ordered limits in
[the finite-infimum note](nonconvex-finite-infimum.md), and the determinant
factor argument in
[the finite-quotient lemma](explicit-span-separation.md). I then read the
complete first version of the attainment manuscript, Sections 1--10, the
replacement proof in Sections 2--6, and the final algorithms in Section 8.

A fresh subagent separately audited the original ordered-limit and
common-field kernel. Its
[written review](nonconvex-attainment-algebra-review.md) found no gap.
I reread that argument independently. Its three-limit conclusion remains
valid although the main proof no longer needs the radius limit. The
reviewer subsequently checked the revised two-limit proof and recorded that
assessment in the same file. That review did not independently verify the
generic-incidence degree estimates or novelty.

A different fresh subagent independently attacked the inactive-box
simplification. It confirmed the compactness contradiction, the parameter
quantifiers, the cases \(h=0\) and nonunique minimizers, and the two-limit
coefficient argument. It did not independently reprove every bound in the
foundational lemmas. I checked the replacement manuscript against these
findings.

## 2. Attainment supplies the required norm bound

Let \(\theta=\min_S q_0\) be finite and attained. The optimizer set
\[
 A=\{x\in S:q_0(x)=\theta\}
\]
is nonempty and closed. Intersect it with the closed norm ball of any one
optimizer and minimize the norm there. This proves the existence of a
minimum-norm optimizer \(x^*\), without assuming that \(A\) is bounded.
Put \(c=\|x^*\|\).

Lift the Hessian basis as \(w=(x,y)\), where each \(y_j\) is a fixed
quadratic function of \(x\). If a lifted box contains \(x^*\)'s lift, an
exact boxed minimizer \(x_\varepsilon\) of
\(q_0(x)+\varepsilon\|x\|^2\), for \(\varepsilon>0\), satisfies
\[
 \theta+\varepsilon\|x_\varepsilon\|^2
 \le q_0(x_\varepsilon)+\varepsilon\|x_\varepsilon\|^2
 \le\theta+\varepsilon c^2.
\]
Therefore
\[
 \|x_\varepsilon\|\le c,\qquad
 0\le q_0(x_\varepsilon)-\theta\le\varepsilon c^2.
\]
The exact lift bounds every \(y_j\) uniformly as well. Any limit as
\(\varepsilon\downarrow0\) is an optimizer of norm at most \(c\), and
hence has minimum norm. This uses attainment essentially.

The unknown \(c\) is only a compactness bound. It must not be inserted into
the rational coefficients from which the algebraic-size estimate is derived.

## 3. An unknown auxiliary box can become inactive

Choose one fixed radius \(R\) strictly larger than \(c\) and than all
lift-coordinate bounds obtained from \(\|x\|\le c\). Its value may be
unknown and nonrational. Let \(P_R=P\cap[-R,R]^{n+h}\). At fixed
\(\varepsilon>0\), perturb inside this compact polyhedron:
\[
 \min q_0(x)+\varepsilon\|x\|^2+\eta P_0(w),\qquad
 |F_j(w)+\eta^2P_j(w)|\le\eta.
\]
Every exact feasible point in the box remains feasible in the bands for
sufficiently small \(\eta\). Compactness and uniform convergence show that
every limiting perturbed minimizer is an exact boxed regularized minimizer.
The preceding norm bound places every such limit strictly inside the box.

Suppose artificial box rows were active at minimizers for arbitrarily small
positive \(\eta\). Choose such a sequence and a convergent subsequence.
Its limit belongs to the closed box boundary, but must be an exact regularized
minimizer and therefore strictly inside. This contradiction proves that
every perturbed minimizer is box-interior for all sufficiently small
\(\eta\), with \(\varepsilon\) fixed.

Thus the selected KKT affine charts use only rows of the original rational
polyhedron \(P\). Their coefficients do not contain \(R\). The box has
served only to obtain actual minimizers and compact inner limits. It can be
absent from the elimination equations without deleting an active constraint.

The perturbation coefficients can be chosen before the box is considered.
For fixed \(\varepsilon\) and nonzero \(\eta\), their restrictions to
each original affine chart range over all quadratics. The generic grid
argument therefore uses only the formal parameters
\((\varepsilon,\eta)\). Adding the fixed objective term
\(\varepsilon\|x\|^2\) does not affect this surjectivity.

## 4. Parameter exceptions and a common vector sequence

After the generic integer choice, each bad polynomial
\(b(\varepsilon,\eta)\) is nonzero. Exclude the finitely many
\(\varepsilon\) values for which it vanishes identically in \(\eta\).
At each retained positive \(\varepsilon\), sufficiently small positive
\(\eta\) avoids its roots. Intersect that tail with the tail on which
every artificial box row is inactive. Thresholds may depend on
\(\varepsilon\); no uniform rate is required.

Choose convergent leaf vectors as \(\eta\downarrow0\) for each retained
\(\varepsilon\). Their exact limits have the uniform norm bound in
Section 2. Choose a convergent sequence of these limits as
\(\varepsilon\downarrow0\). All outputs must use this same vector tree.

There are finitely many original affine charts and oriented band subsets.
Choose a constant label on each inner subsequence, then one constant label
on an outer subsequence. These restrictions preserve the vector limits.
At most one orientation of each band can be active, so the multiplier count
remains at most \(h\). A zero-dimensional retained chart is one rational
point and needs no elimination.

The original three-limit proof used the same argument at an additional
outer radius level. That proof is valid, but the inactive fixed box makes
that level unnecessary.

## 5. Elimination and common representation size

In a positive-dimensional chart, genericity gives an invertible multiplier
Hessian and an invertible bordered KKT matrix. Both are needed: an invertible
Hessian and independent gradients alone do not ensure the multiplier
Jacobian is nonsingular.

Eliminating the chart variables by the adjugate formula leaves \(s\le h\)
multiplier variables, multiplier degree \(O(N)\), and coefficient norm
logarithm polynomial in \(N\). Every coordinate is a rational output of
the same root system. All coefficients are rational functions of the input
and generic integer perturbations, with formal variables
\(\varepsilon,\eta\); the unknown radius contributes no coefficient.

The finite-quotient construction over \(\mathbb Z[\varepsilon,\eta]\)
gives a nonzero output polynomial after the auxiliary
\(\zeta,\delta\) extractions. Extract the lowest \(\eta\) coefficient
first, taking the inner limit at fixed \(\varepsilon\), then the lowest
\(\varepsilon\) coefficient. Coefficient extraction does not increase
degree or norm. Vanishing of a coefficient after specialization does not
invalidate the corresponding identity. An arbitrary diagonal limit is
neither justified nor needed.

Every rational linear combination of the same limiting coordinates has the
same degree bound, independently of its coefficient sizes. The primitive
element theorem therefore bounds the joint field degree. The
bounded-coefficient primitive combination and trace-matrix argument from
the certificate note give the common rational univariate representation.
Multiplying separate coordinate degrees would not prove the same bound.

With structural size \(S_0\) and coefficient bit size \(\tau_0\), the
degree bound has form \(S_0^{O(h+1)}\); coefficient bits and representation
length have form \((\tau_0+1)S_0^{O(h+1)}\). The additional rational norm
objective and one extra formal parameter preserve that dependence.

## 6. Exact attainment and minimum-norm recovery

Once the earlier value algorithm has supplied the exact finite infimum
\(\theta\), one NP query asks for a feasible rational univariate
certificate, within the proved optimizer length bound, with
\(q_0(x)=\theta\). The answer is yes exactly when the infimum is attained.
Prefix search on this language then recovers an optimizer.

Equality to a separately represented algebraic \(\theta\) does not require
a compositum. If \(f_\theta\) is its minimal polynomial and \((a,b)\)
isolates its real root, check
\[
 f_\theta(q_0(x))=0,\qquad a<q_0(x)<b
\]
in the candidate point's own representation. Univariate remainder and sign
computations perform these tests in polynomial time. Global optimality is
not verified from the feasible point alone: the value algorithm has already
supplied the correct \(\theta\).

The radius theorem gives an alternative attainment test by computing the
minimum on \(S\cap[-B,B]^n\). An empty bounded feasible set must be handled
as nonattainment unless \(B\) also dominates a separate feasibility radius.
If it is nonempty, equality of its compact minimum with \(\theta\) is
equivalent to attainment.

The theorem also supports recovery of a minimum-norm optimizer. Put
\[
 \rho=\min\{\|x\|^2:x\in S,\ q_0(x)=\theta\}.
\]
After attainment is established, an NP query for a certificate within the
same bound with \(q_0(x)=\theta\) and \(\|x\|^2\le t\) is equivalent
to \(\rho\le t\). A minimum-norm optimizer always has such a short
certificate, independently of \(t\). Its joint field and coordinate height
give degree and height bounds for \(\rho\). Bisection and algebraic
recognition recover \(\rho\); prefix search with both equalities recovers
a minimum-norm optimizer. This point is unique when the optimal set is
convex, but need not be unique in the general theorem.

## 7. Exact examples and the hardness check

An inline exact SymPy check used \(xy=1\), \(x,y\ge0\), objective
\(q_0=x^2\), and \(u=x^2\). The regularized objective is
\[
 (1+\varepsilon)u+\varepsilon/u.
\]
Its minimizer satisfies \(u=\sqrt{\varepsilon/(1+\varepsilon)}\), while
\(\|x,y\|^2=u+1/u\to\infty\). The infimum of \(q_0\) is zero and is
unattained. This confirms that Section 2 cannot assume merely a finite
infimum.

For the attained example \(xy=1\), \(x,y\ge0\),
\(q_0=(x-y)^2\), the exact identity
\[
 q_0+\varepsilon(x^2+y^2)-2\varepsilon
   =(1+\varepsilon)(u-1)^2/u
\]
shows that the regularized minimizer is \(x=y=1\), of squared norm two.
The check verified both stationary identities, the positive second
derivative in the unattained example, its divergence limit, and the last
identity. These finite checks do not prove the general theorem.

I independently verified the proposed hardness reduction. Given a 3SAT
instance, impose \(0\le x_i\le1\), the clause inequalities
\(L_C(x)\ge1\), \(t,y\ge0\), and one quadratic inequality
\[
 \sum_i x_i(1-x_i)-ty\le0,
\]
and minimize \(t\). Every \(t>0\) is feasible using \(x_i=1/2\) and
\(y=n/(4t)\), so every instance has known infimum zero. At \(t=0\),
each nonnegative summand must vanish, forcing a Boolean satisfying
assignment. Conversely any such assignment with \(t=y=0\) attains zero.
The sole Hessian is nonzero, so its span has dimension exactly one.
All input coefficients are bounded constants. This establishes strong
NP-hardness of attainment even on this promised-known-zero subclass.
Membership in NP there follows by adding the affine row \(t\le0\) and
using the fixed-span feasibility certificate theorem.

## 8. Prior-work boundary and verification scope

The primary statement of
[Grigoriev--Pasechnik, Theorem 1.2](https://arxiv.org/pdf/cs/0403008v3),
permits computable ordered coefficient subrings and bounds relative degrees
and arithmetic operations. Its stated bit bound is for integer coefficients.
Once the finite optimum is encoded, a proof over
\(\mathbb Q(\theta)\) is a plausible shorter route to an optimizer
bound, but its height dependence needs proof. A separate source audit is
examining this issue.

A simpler rational reduction already gives a weaker optimizer bound after
the finite-infimum theorem: lift \(t=q_0(x)\), restrict \(t\) to an
isolating interval for \(\theta\), and impose \(f_\theta(t)=0\).
Face sampling with \(h+2\) quadratic-map components and outer degree
\(O(\deg f_\theta)\) gives \(N^{O((h+1)^2)}\) representation length.
Thus the basic fixed-\(h\) attainment and recovery complexity consequence
does not require the sharper argument. Minimum-norm selection and the
linear dependence of the parameter exponent need their own prior comparison.

The general coefficient-ring statement also gives an arbitrary optimizer's
absolute field degree \(N^{O(h+1)}\), by applying the sampling theorem over
\(\mathbb Q(\theta)\) and multiplying relative degrees. This degree claim
does not require the unresolved coefficient-height extension. I checked
that distinction in the
[completed prior audit](nonconvex-attainment-prior-audit.md).

I independently inspected Definition 1.14, Theorem 1.15, and the adjacent
paragraph in the primary
[Kamminga--Rudolph ITCS 2026 paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf).
They concern approximation on a bounded quadratic-map zero set and report
that GP's announced unbounded optimization proof was unavailable to their
knowledge. The main manuscript's comparison respects those qualifications;
neither that report nor this review proves that an equivalent theorem does
not exist.

This is a correctness review, not a novelty certification. No Lean
formalization, project-wide verification, or CI inspection was performed.
The targeted local commands were the inline SymPy calculation described in
Section 7, an inline Python check of this review's final newline, control
characters, trailing whitespace, and local Markdown links, and a scoped
git diff whitespace check for this review alone.
