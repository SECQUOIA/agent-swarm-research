# Follow-up review: full separators and squared-width model error

Date: 2026-10-02. This is an independent follow-up to the reviews of
[regridded certificates](../regridded-certificates/note.md), their
[inexact oracles](../regridded-certificates/inexact-oracles.md), and the
[affine-repair extension](../new-direction/affine-repair-exploration.md).

Both extensions are valid. The supplied tree decomposition can be retained
without merging bags, including when an adjacent pair has a full-bag
separator. The proof also permits continuous convex aggregate bag models
with a uniform squared-width error bound; endpoint exactness is unnecessary.
The revised main note states these broader hypotheses and uses the
appropriate uniform counts.

## 1. Separator dimensions and counts

The original certificate model assumes that no bag is contained in its
parent. Under that convention, every separator has dimension at most
\(w=p-1\), and the original \(3^w\) count is justified. The earlier
adversarial review explicitly recorded this convention. This follow-up
broadens the supplied-decomposition scope; it does not invalidate that
historical scoped result.

For an arbitrary supplied decomposition, define

\[
q=\max\bigl(\{0\}\cup\{|S_t|:t\ne r\}\bigr)\le p.
\]

Adjacent identical bags of size \(p\) can have \(q=p\). The existing
shell argument already proves, for a bag of dimension \(d\) and an
incident separator of dimension \(q_t\), at most
\(3^{q_t}m^d(j+1)^2\) touching pairs at stage \(j\), where
\(m=4/\theta\). Consequently the local-oracle count is bounded by

\[
N3^q m^p\frac{(J+1)(J+2)(2J+3)}6,
\]

and \(3^p\) is a valid uniform replacement. The same replacement
applies to child-incidence processing, inexact local-oracle counts,
general affine-repair counts, and counted-work budgets. The final and
total box counts do not change. The difference between \(3^p\) and
\(3^w\) is only a factor of three in a big-O statement, but explicit
upper bounds should use the stated separator hypothesis.

The review found one further affected estimate: naive dense comparison
of every bag leaf with every separator cell takes
\(O(Nm^{p+q}(j+1)^2)\) pair tests, uniformly
\(O(Nm^{2p}(j+1)^2)\). The old exponent \(2w+1=p+w\) depended on
the reduced-bag convention. The main note now uses the valid uniform
\(2p\) exponent. Coordinate processing has the additional factor
already specified there.

No other part of the regridding argument needs a proper separator.
Running intersection, occurrence-tree depth bounds, aggregate copy drift,
subtree-gradient telescoping, grading absorption, and the inexact slope
bound remain valid when \(V_t\setminus S_t\) is empty. So do the
local dynamic program, backtracking, and touching-face reconstruction.
The relevant multiplicity remains the supplied occurrence bound \(k\).

There is no implicit bag merging. Moving factors between bags can change
the bag-gradient constant \(M\) and other bagwise constants. Keeping
the supplied factor assignment avoids that change. For the stable-state
path with \(S_t=\{s_t\}\), the actual separator dimension is one, so
the sharper incidence factor remains three.

## 2. The weaker lower-model contract is sufficient

For each bag leaf \(B\), it is sufficient to supply a continuous convex
function \(\ell_{t,B}\) such that

\[
0\le a_t(v)-\ell_{t,B}(v)
\le A_0\operatorname{width}(B)^2/4
\qquad(v\in B).
\]

Certificate validity uses only underestimation. Local convex optimization
uses convexity and attainment. Telescoping introduces the aggregate model
error only through its sign and the displayed bound. The entire
contraction proof then proceeds with the same constants involving
\(A_0\). The geometry and counting arguments are independent of the
models' endpoint values. The same conclusion holds for the inexact
residual induction and the affine-repair cancellation argument.

The original factorwise vertex-vanishing condition implies this contract
with \(A_0=\alpha' A\), but is stronger. Under the generalized contract,
\(A_0\) is the supplied aggregate bound. The revised note makes that
distinction explicit and limits its unchanged-factor-rule statement to
the original-model application.

## 3. Midpoint Taylor models and the bag-gradient caveat

Suppose \(a_t\) has an \(M\)-Lipschitz gradient. Let \(m_B\) be
the local bag-box midpoint and let its side lengths be \(s_i\). Set

\[
\rho_B=\frac M8\sum_i s_i^2,\qquad
\ell_{t,B}(v)=a_t(m_B)+\nabla a_t(m_B)^T(v-m_B)-\rho_B.
\]

The two-sided Taylor remainder is at most \(\rho_B\) in absolute
value, so

\[
0\le a_t(v)-\ell_{t,B}(v)
\le2\rho_B\le\frac{Mp}{4}\operatorname{width}(B)^2.
\]

Thus \(A_0=Mp\) suffices for this affine, continuous, convex aggregate
model. The midpoint is local to the leaf; expansion at a distant stage
center does not give the same squared-width bound.

For separately constructed factor models with gradient constants
\(L_a\), the corresponding safe aggregate constant is
\(\max_t\sum_{a\text{ assigned to }t}L_a|a|\). A curvature bound
on the bag sum does not bound those individual factor constants:
cancellation can make \(M\) small. Using the aggregate bag model avoids
that unjustified transfer of constants.

These Taylor models generally fail literal endpoint exactness. For
example, on \([0,1]\), the construction for \(a(x)=x^2\), \(M=2\),
gives \(\ell(x)=x-1/2\), with positive error at both endpoints.
It satisfies the squared-width contract but cannot satisfy a finite
vertex-vanishing upper-error bound there. The generalized hypothesis must
therefore be stated, as the revised note now does.

Exact rational polynomial values and gradients at rational midpoints,
with rational curvature bounds, give rational affine models. Approximate
Taylor coefficients need their own certified downward correction and a
preserved squared-width error bound. The inexact theorem's slope budget
does not automatically cover model-construction errors. This review
does not certify a new LP/QP bit-complexity theorem; that implementation
requires its own arithmetic and oracle analysis.

## 4. Verification record

The reviewer re-read the revised main note and checked the updated
inexact, affine, and synthesis count statements. A delegated independent
reviewer checked every use of the lower-model hypothesis and derived the
midpoint Taylor error bound. Verification used targeted `rg`, `cat`, and
`sed` reads. No new executable checks, external research, project-wide
verification, or CI inspection were performed.
