# Integer-query convex feasibility: a stronger applicable predecessor

Date: 2026-09-28. Status: focused primary-source audit, with independent
inspection by a second agent. This updates the source map in
[the fixed-dimension audit](fixed-integer-quartic-oracle-prior.md).
It identifies an FPT oracle theorem that may simplify the proposed
quartic extension. It does not claim that the general integer-query
method or its optimization variant is new.

## 1. Exact oracle contract and complexity

[Hildebrand--Göß, *Complexity of Integer Programming in Reverse Convex
Sets via Boundary Hyperplane Cover*](https://arxiv.org/html/2409.05308v2),
Theorem 9 and Appendix B, give integer feasibility for a convex set
\(S\subseteq[-R,R]^k\), using separation queries only at integer
points. The stated time is

\[
 2^{O(k\log k)}\operatorname{poly}
       (\langle R\rangle,\Phi_{\rm sep}(k\langle R\rangle)).
\tag{1}
\]

The oracle answers exact membership or returns a rational separating
inequality. Its time and output-length bounds are part of the model.
Appendix B uses closest and shortest lattice vectors and ellipsoid
dimension reduction. Theorem 9 does not require the intersection-inradius
assumption used for the paper's separate continuous feasibility results.
The inspected version is **v2, dated 13 September 2026**. Theorem 9
should be cited with that version rather than inferred from the 2024
submission date. The paper itself restricts its main treatment to pure
integer problems and flags mixed-integer oracle issues.

[Ari--Hildebrand, *Hidden Convexity via Symmetric Displacement Covers:
Mixed-Integer Quadratic Programming and Integer Cubic Programming in
Fixed Dimension*](https://arxiv.org/html/2609.18266v2), Definition 3.4
and Theorem 3.5, restate the precise interface: for closed convex
\(S\subseteq[-R,R]^k\), each rejected integer query is strictly
separated by a rational inequality valid on \(S\). The polynomial
degree in (1) is absolute; their formula includes a constant multiple
of the total query-coordinate encoding. Queries outside the known box
are separated by box rows, and recursive queries are mapped back to
the original integer coordinates. The paper cites Hildebrand--Göß and
Basu for this theorem. Its Lemma 3.6 separately develops objective
sublevel hulls and rational-valued supporting inequalities.

The separation target must be a fixed convex set. A cut valid merely
for some integer points is insufficient until one specifies their
convex hull and verifies the integer membership equivalence.

## 2. The older underlying algorithm

[Basu, *Complexity of optimizing over the integers*](https://arxiv.org/html/2110.06172v6),
Theorem 5.7, is initially a mixed-integer approximate feasibility result.
Remark 5.11 removes strict-feasibility assumptions in the pure integer
case and states exact optimization with
\(2^{O(k\log k)}\operatorname{poly}(\log(kR))\) overall oracle
complexity. The test points in this specialization are integer closest
lattice vectors. Its proof discusses rational rounding and bit control
through the standard ellipsoid literature. Remark 5.9 already describes
optimization without value bisection: cut at visited feasible points and
select the best visited value. Remark 5.12 expressly warns that extending
projection oracles to arbitrary continuous blocks requires careful
approximation details. These passages were read directly by both agents.

Thus a general algorithm that searches using integer cuts and retains the
best visited candidate has substantial existing precedent. The proposed
quartic work must be positioned through its implementation of these
oracles for a large continuous block and its exact arithmetic comparisons.

## 3. Application to algebraic fiber values: the interface deduction

Let \(P\subseteq[-R,R]^k\) be a bounded rational polytope. Suppose
\(G:\mathbb R^k\to\mathbb R\) is differentiable and globally
\(\mu\)-strongly convex, with a known rational \(\mu>0\).
For a threshold \(t\), define

\[
 Z_t=\{z\in P\cap\mathbb Z^k:G(z)\le t\},
 \qquad S_t=\operatorname{conv}(Z_t).
\tag{2}
\]

The set \(Z_t\) is finite, so \(S_t\) is closed and bounded;
the empty hull is permitted. Convexity of \(P\) and \(G\) gives

\[
                           S_t\cap\mathbb Z^k=Z_t.       \tag{3}
\]

At an integer query \(z\notin P\), return a violated row of \(P\).
At \(z\in P\), an exact comparison with \(t\) decides membership
in (2)--(3). If the query is rejected, compute a rational \(q\) with
\(\|q-\nabla G(z)\|_2\le\mu/4\). For every \(w\in Z_t\),
we have \(w\ne z\), hence \(r=\|w-z\|_2\ge1\), and

\[
 \begin{split}
 q^{\mathsf T}(w-z)
 &\le G(w)-G(z)-\frac\mu2r^2+\frac\mu4r\\
 &\le-\frac\mu4.
 \end{split}
\tag{4}
\]

Therefore

\[
                  q^{\mathsf T}(x-z)\le-\mu/4             \tag{5}
\]

strictly excludes \(z\) and is valid on the whole convex hull \(S_t\).
When \(q=0\), it is a valid empty-set certificate. This proof does not
need a lower bound on \(G(z)-t\), and it never requires separation of
the continuous sublevel \(\{x:G(x)\le t\}\).

For \(G(z)=\min_y f(z,y)\), with globally strongly convex rational
quartic \(f\), the separate continuous theory is needed to implement
the exact comparison. Ordinary polynomial-accuracy fiber minimization
can provide the rational gradient approximation. The application must
prove uniform time and output-length bounds in the original-coordinate
queries specified by the source theorem. Once supplied, (2)--(5) give
the precise integer-query separation interface required by (1).

The rational-valued hypothesis in Ari--Hildebrand's Lemma 3.6 cannot be
silently imposed on \(G\): fiber values may be irrational algebraic
numbers. The relevant import is their feasibility Theorem 3.5, together
with the separately proved comparison and rational-cut implementation.

## 4. Why the recent nonconvex results do not settle this application

The overall theorem of Ari--Hildebrand v2 fixes the **total** dimension
\(N=k+n\); its coefficient-encoding exponents depend on \(N\).
Its nonlinear extension includes cubics and a concave homogeneous
quartic part in a pure integer problem. It does not give a
fixed-parameter bound in the integer dimension alone for the present
globally strongly convex quartic with an arbitrary continuous block.
Those restrictions concern the application theorem, rather than its
stronger reusable oracle interface above.

The v2 paper expressly supersedes
[arXiv:2609.17889](https://arxiv.org/abs/2609.17889). That predecessor's
abstract page uses the title *Bounded Integer Quadratic Programming
through Parallelepiped Covers and Discrete Convic Optimization*, while
its HTML displays *Bounded Integer Quadratic Programming via Symmetric
Displacement Covers*. The versioned superseding paper is the clearer
primary reference for the shared oracle argument. The exact arXiv
identifiers and version histories were checked directly.

## 5. Verification and limits

The author and a separate agent independently read the three decisive
primary sources: Hildebrand--Göß v2 Theorem 9 and Appendix B;
Ari--Hildebrand v2 Definition 3.4, Theorem 3.5, and Lemma 3.6; and Basu
Theorem 5.7 with Remarks 5.9--5.12. Both checked the distinction between
separation of the continuous sublevel and separation of its integer
sublevel hull. The elementary margin calculation (4) was independently
reconstructed.

This note does not reproduce or independently formalize all ellipsoid
rounding and lattice-bit arguments of the cited algorithms. It is a
source audit and interface proof, not a complete independent verification
of their complexity theorems. The full quartic FPT application and its
exact-optimization variant need their own proof and fresh review.

Targeted verification: Python checks of local Markdown links, final
newline, trailing whitespace, and the exact integer margin for
\(1\le r\le32\); `git diff --check --
research-20260927/integer-query-convex-oracle-prior.md`. Both passed.
No project-wide checks or CI inspection were performed.
