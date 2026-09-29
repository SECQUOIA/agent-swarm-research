# Independent review of minimum exact penalty hardness

Date: 2026-09-25. Scope: independent adversarial review of the graph and binary-box constructions proposed during the minimum-penalty investigation. This is a review record, not a novelty certification.

## Definition and a necessary distinction

For a finite native set \(X\), affine objective \(f\), and scalar affine residual \(r\), write

\[
L_\rho(\lambda)=\min_{z\in X}\{f(z)+\lambda r(z)+\rho|r(z)|\},
\qquad D_\rho=\sup_{\lambda\in\mathbb R}L_\rho(\lambda).
\]

The reviewed threshold is the least \(\rho\ge0\) for which \(D_\rho=p^*\), where \(p^*\) is the original optimum. Both constructions have a unique original feasible point, the origin, with known optimum zero.

This is exactness of the optimal value. At the threshold, infeasible native points attain the same augmented-Lagrangian value as the original optimizer. Requiring every augmented-Lagrangian minimizer to be originally feasible gives a strict inequality in these examples. The infimum of the latter parameters is the same threshold, but a smallest such parameter does not exist. The penalty convention is \(\rho|r|\); introducing a factor \(1/2\) changes numerical threshold statements.

## Graph construction

For a graph \(G=(V,E)\), let \(p,m,x_v\) be binary and impose

\[
p+m\le1,\qquad x_v\le p+m,\qquad x_u+x_v\le1\quad(uv\in E).
\]

Set \(f=-\sum_vx_v\) and \(r=p-m\). The zero-residual point has \(p=m=0\), hence \(x=0\). Each nonzero residual branch admits exactly the stable sets of \(G\). Consequently

\[
L_\rho(\lambda)=\min\{0,\rho-\alpha(G)-|\lambda|\},
\qquad D_\rho=\min\{0,\rho-\alpha(G)\},
\qquad\rho^*=\alpha(G).
\]

This calculation is correct and uses only coefficients in \(\{0,\pm1\}\). Exact computation is strongly NP-hard. Deciding exactness at an integer candidate \(k\) on this family is the coNP-complete question \(\alpha(G)\le k\). A stable set of size greater than \(k\) certifies nonexactness. An absolute error strictly below \(1/2\) permits rounding and is therefore NP-hard.

Two qualifications matter. First, this construction puts a hard stable-set problem inside the native set. Second, the coNP-completeness claim is immediately established for this restricted family with known primal value; it should not be extended without proof to a formulation that also asks an algorithm to determine an unknown primal optimum. Likewise, calling threshold minimization “APX-complete” would require an appropriate optimization-class definition: checking whether a candidate penalty is sufficient is already coNP-hard.

## Binary-box construction

Let \(a_1,\ldots,a_n\) and \(B\) be positive integers from SUBSET SUM. Append the item \(a_{n+1}=B+1\). For an integer \(K\ge2\), take the native set to be the binary box on \((x,q)\), and define

\[
f(x,q)=-q,\qquad
r(x,q)=K\sum_{i=1}^{n+1}a_ix_i-(KB+1)q.
\]

Modulo \(K\), a zero residual forces \(q=0\), and positivity of the items then forces \(x=0\). Thus the native linear optimization problem is trivial, and the original constrained problem has a known unique optimizer.

Let

\[
S^*=\max\left\{\sum_{i=1}^na_ix_i:\sum_{i=1}^na_ix_i\le B,\ x\in\{0,1\}^n\right\},
\quad d=K(B-S^*)+1,\quad e=K-1.
\]

Among points with \(q=1\), the negative residual nearest zero is \(-d\), and the positive residual nearest zero is \(e\). The appended item makes the latter value attainable. Every \(q=0\) point has nonnegative residual and objective zero.

For \(L_\rho(\lambda)=0\), the two nearest residuals require

\[
\rho-\lambda\ge1/d,\qquad \rho+\lambda\ge1/e.
\]

These inequalities also suffice: they make every farther residual branch nonnegative, and the second makes all \(q=0\) points nonnegative. Therefore

\[
\rho^*=\frac12\left(\frac1d+\frac1e\right).
\]

There is no issue concerning a nonattained dual supremum. For every \(\rho\ge0\), the explicit multiplier

\[
\lambda_\rho=\rho\frac{d-e}{d+e}
\]

attains

\[
D_\rho=\min\left\{0,-1+\frac{2\rho de}{d+e}\right\}.
\]

For the upper bound, take the minimum of the two affine functions from residuals \(-d\) and \(e\), and also use the feasible origin. Their intersection has the displayed multiplier and value. At this multiplier both coefficients \(\rho\pm\lambda_\rho\) are nonnegative, so farther residuals cannot worsen the value; the \(q=0\) points are nonnegative. This proves the matching lower bound.

The YES and NO thresholds satisfy

\[
B\text{ attainable}\implies \rho^*=\frac{K}{2(K-1)},
\qquad
B\text{ unattainable}\implies \rho^*\le\frac{K}{K^2-1}.
\]

The ratio of these bounds is \((K+1)/2\). The additive gap is \(K/[2(K+1)]\).

If the multiplier is fixed at zero, the least penalty giving the correct value is instead

\[
\rho^*_0=\max\{1/d,1/(K-1)\}.
\]

For \(K\ge3\), this equals 1 on a YES instance and \(1/(K-1)\) on a NO instance. Thus the same reduction also addresses the fixed-zero-multiplier exact-penalty interpretation, with an even simpler gap.

## Polynomial relative approximation

Let \(L_0\) be the binary encoding length of the SUBSET SUM input, and choose \(K=2^{L_0+2}\). Writing the new row explicitly takes \(L=O(L_0^2)\) bits: there are at most \(L_0+1\) item coefficients, each with \(O(L_0)\) bits.

Suppose a polynomial-time algorithm always returns a sufficient penalty \(\widehat\rho\) satisfying

\[
\rho^*\le\widehat\rho\le p(L)\rho^*
\]

for a fixed polynomial \(p\). In a YES instance, \(\widehat\rho>1/2\). In a NO instance,

\[
\widehat\rho\le p(L)\frac{K}{K^2-1}<\frac12
\]

for every sufficiently large \(L_0\), because \(K\) grows exponentially in \(L_0\) while \(p(L)\) grows polynomially. The finitely many shorter source inputs can be solved by a fixed brute-force procedure. This would decide SUBSET SUM in polynomial time. Thus no such polynomial-factor sufficient-penalty approximation exists unless P=NP. All thresholds here are strictly positive, so no zero-optimum convention is involved.

This is a bit-complexity result based on SUBSET SUM, not a strong-hardness claim for bounded numerical data. Uniform rational rescaling of the residual preserves the relative-approximation obstruction: replacing \(r\) by \(r/M\) multiplies both the threshold and the comparison cutoff by the known number \(M\). Such normalization replaces large integer magnitudes with fine rational residual spacing. It does not establish hardness for uniformly well-conditioned residual data.

The same proof can exclude a two-sided multiplicative estimate after accounting for two factors of \(p(L)\), because the exponential gap still dominates \(p(L)^2\). The sufficient-upper-approximation formulation above is the cleanest direct statement.

## Why the unit-residual graph restriction differs

An additional independent reviewer checked the following obstruction. If \(f\) and \(r\) are affine, \(r(X)\subseteq\{-1,0,1\}\), the original value is known, and exact linear optimization over a bounded native set is easy, then the threshold is easy. Choose a known objective-range bound and an \(M\) larger than that range. Minimizing \(f-Mr\) or \(f+Mr\) obtains the minimum objective on the \(+1\) or \(-1\) branch, if that branch exists. If both exist and their minimum values are \(f_+,f_-\), then

\[
\rho^*=\max\{0,p^*-(f_++f_-)/2\}.
\]

If one sign is absent, a multiplier suppresses the other sign without a penalty. Thus varying residual magnitudes are doing essential work in the binary-box construction.

## Verification performed

An exact-arithmetic Python heredoc was run using `fractions.Fraction`, `itertools.product`, and a random generator with seed 825031. It generated 40 positive-integer source instances with one through four items, and used \(K\in\{2,4,16\}\), for 120 box instances. For each instance it enumerated every native vertex and checked the unique zero-residual point, the YES/NO threshold bounds, and four penalties \(0,\rho^*/2,\rho^*,2\rho^*\). Independently of the proposed multiplier, it maximized the minimum of all affine Lagrangian functions over all pairwise line-intersection breakpoints. All 480 exact dual-value checks passed. The independent breakpoint check was then preserved in `check_minimum_penalty_review.py`, with an additional direct vertex check of the fixed-zero-multiplier threshold. The targeted command was `python research-20260925/check_minimum_penalty_review.py`. This tests the finite formula on small instances; it does not prove the complexity reduction or establish novelty.

An earlier, substantially larger exhaustive run was interrupted because direct breakpoint enumeration was unnecessarily costly. It did not report a failed assertion. The smaller targeted run above completed. No project-wide verification or CI inspection was performed.

The subordinate reviewer independently reported 420 small exact-rational checks for \(K=2\), and 240 checks with \(K=2^j\), \(2\le j\le25\). These are secondary reports; the 120-instance check described above was executed by the present reviewer.

## Literature and significance assessment

[Lefebvre and Schmidt, *Exact Augmented Lagrangian Duality for Nonconvex MINLP*](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf), Theorem 15, constructs a sufficient finite penalty for MILPs in polynomial time. Its conclusion explicitly asks whether the smallest parameter closing the duality gap can be computed in polynomial time and conjectures that it cannot. The constructions above separate computing some sufficient penalty from computing or approximating the smallest one. They do not contradict that theorem. The binary-box restriction strengthens the interpretation: neither hard native linear optimization nor an unknown original optimum is needed for the obstruction.

[Gu, Ahmed, and Dey, *Exact Augmented Lagrangian Duality for Mixed Integer Quadratic Programming*](https://arxiv.org/abs/1907.00920) establishes finite exactness with norm augmentation and a polynomial encoding-size bound on a sufficient penalty. [Bhardwaj, Narayanan, and Pathapati, *Exact Augmented Lagrangian Duality for Mixed Integer Convex Optimization*](https://arxiv.org/abs/2209.13326) develops constructive exactness results for mixed-integer convex programs. These results concern existence and sufficient parameters, so they are compatible with minimum-threshold hardness.

For the graph source problem, [Alimonti and Kann, *Hardness of Approximating Problems on Cubic Graphs*](https://www.cs.yale.edu/homes/aspnes/pinewiki/attachments/MarkovChains/alimanti-mis-cubic.pdf), Theorem 3.2, proves APX-completeness of maximum independent set for degree at most three. The binary-box result makes a separate APX-based consequence unnecessary for the main hardness statement.

The sources were inspected through targeted searches and the open papers. These searches do not establish novelty. Related formulations under exact-penalty calibration, smallest big-M constants, inverse optimization, and parametric optimization still need comparison before any priority claim. Even if original, the present result is a computational limitation, not a new solver improvement. Its potential value is to identify which penalty-calibration guarantees cannot hold uniformly and motivate structural or instance-dependent positive results.
