# Independent review of the three-variable parameter-family SDP

Date: 25 September 2026.

The proposed nonnegative family and its exact semidefinite lift pass this
review. The lift enforces this particular family of cuts; it has not been
shown to describe the full quadratic moment hull. The main qualifications
are that the scalar parameter must be unrestricted, a dual matrix does not
automatically give one parameter vector, and compactness per orientation
does not establish a computational advantage over the known exact hull.

## Family and parameter domain

Let (h\in\mathbb R) and (d_1,d_2,d_3,k\ge0). Define

\[
p_{h,d,k}(x,y,z)=(h-d_1x-d_2y+d_3z)^2
 +2d_3kz(1-x-y)+k\bigl(2(d_1+d_2-h)+k\bigr)xy.
\]

The identity

\[
\begin{aligned}
p_{h,d,k}={}&(h-d_1x-d_2y+d_3z-kxy)^2\\
 &+2d_3kz(1-x)(1-y)+k(2d_1+k)xy(1-x)\\
 &+2kd_2xy(1-y)+k^2x^2y(1-y)
\end{aligned}
\]

is exact. Every term on its right is nonnegative on the cube. This proves
validity for the entire stated parameter domain, including zero parameters
and negative (h). It does not require the five-contact assumptions in
[the counterexample note](three-positive-disjoint-counterexample.md).
Those stronger assumptions remain necessary for that note's particular
contact and exclusion proof; not every member of the enlarged family lies
outside the disjoint affine-SOS cone. For example, (k=0) gives an affine
square.

The displayed decomposition uses a bilinear polynomial inside a square,
and multipliers that overlap variables in other factors. It is therefore
not a certificate in the disjoint affine-SOS cone and does not contradict
the counterexample.

## Exact moment formulation

Let a normalized linear functional on quadratics have moments

\[
L(1)=1,\quad L(x_i)=m_i,\quad L(x_ix_j)=Y_{ij}.
\]

No feasibility assumptions on these nine numbers are needed for the
following algebraic equivalence. Set

\[
b=\begin{pmatrix}-m_x\\-m_y\\m_z\\-Y_{xy}\end{pmatrix},\qquad
B=\begin{pmatrix}
Y_{xx}&Y_{xy}&-Y_{xz}&Y_{xy}\\
Y_{xy}&Y_{yy}&-Y_{yz}&Y_{xy}\\
-Y_{xz}&-Y_{yz}&Y_{zz}&m_z-Y_{xz}-Y_{yz}\\
Y_{xy}&Y_{xy}&m_z-Y_{xz}-Y_{yz}&Y_{xy}
\end{pmatrix}.
\]

Writing (v=(d_1,d_2,d_3,k)^T), direct expansion gives

\[
L(p_{h,d,k})=h^2+2hb^Tv+v^TBv.
\]

For each fixed (v\ge0), its minimum over (h\in\mathbb R) is

\[
v^T(B-bb^T)v,\qquad h=-b^Tv.
\]

Consequently, all family cuts hold if and only if

\[
S:=B-bb^T\in\operatorname{COP}_4.
\]

The classical order-four identity is

\[
\operatorname{COP}_4=\mathbb S^4_++\mathcal N_4,
\]

where \(\mathcal N_4\) means symmetric entrywise nonnegative matrices,
not PSD matrices. Its dual form is
\(\operatorname{CP}_4=\operatorname{DNN}_4\). These facts are explicitly
recalled in Section 2, pp. 3–4, of the local primary-source manuscript of
[Anstreicher and Burer](../literature/papers/anstreicher2010-computable-representations-for-convex-hulls/fulltext.md);
the original decomposition theorem is due to
[Diananda (1962)](https://doi.org/10.1017/S0305004100036185).
The Diananda publisher record was inspected, but its full article was not
retrieved in this review.

It follows, by the Schur complement of the fixed positive top-left entry,
that all family cuts hold exactly when there exists (N\in\mathcal N_4)
such that

\[
\boxed{\begin{pmatrix}1&b^T\\b&B-N\end{pmatrix}\succeq0.}
\]

This is affine in the original moments and the ten independent entries of
(N). It needs no moments of degree three or four. This statement should
be called a formulation **using original first and second moments with
auxiliary matrix variables**, rather than an unlifted LMI.

There is no hidden closure assumption. More generally,
\(\mathbb S^n_++\mathcal N_n\) is closed: if (P_j+N_j\to A), each
diagonal of (P_j,N_j) is nonnegative and bounded. PSD implies
\(|(P_j)_{ab}|^2\le(P_j)_{aa}(P_j)_{bb}\), so (P_j) is bounded, as is
\(N_j\). A convergent subsequence gives an exact decomposition of (A).

The unrestricted domain of (h) is essential to the derivation. Do not
abbreviate the condition as “all (h,v\ge0).” With (h\ge0), the
minimizer instead is \(\max\{0,-b^Tv\}\), and the copositivity condition
need not be necessary.

## Diagonal epigraphs, bounds, and symmetry

For any cube point, keep (Y_{ij}=x_ix_j) off the diagonal and allow
(Y_{ii}\ge x_i^2). The lifted cut's value becomes

\[
p_{h,d,k}(x)+\sum_{i=1}^3 d_i^2(Y_{ii}-x_i^2)\ge0.
\]

Thus the same family is valid on the convex hull of this set and on its
closure. No diagonal upper bound is required for this validity statement.
This does not mean arbitrary first and off-diagonal moments are valid;
it describes a specific generating set and its convex hull.

Coordinate permutations and switches (x_i\mapsto1-x_i) preserve validity.
A switch sends a diagonal moment to (1-2m_i+Y_{ii}), so it also preserves
the nonnegative diagonal surplus. Bounded nonunit intervals can be handled
by the usual affine rescaling when their widths are positive.

The (x,y) symmetry leaves at most three choices of distinguished
coordinate and eight switches: at most 24 orientations per triple. One
orientation uses one order-five PSD block and ten scalar nonnegative
variables. Imposing all orientations can therefore use more PSD blocks
than the classical exact six-tetrahedron construction. No overall size or
runtime advantage has been proved.

## Separation and extraction

At a fixed candidate moment point, form (S=B-bb^T) and solve

\[
\mu=\min\{\langle S,W\rangle:W\succeq0,
\ W\ge0\text{ entrywise},\ \operatorname{tr}W=1\}.
\]

The feasible set is compact. It is strictly feasible, for example at
\(W=(I+ee^T)/8\) in dimension four. Since
\(\operatorname{DNN}_4=\operatorname{CP}_4\),

\[
\mu=\min\{v^TSv:v\ge0,\ \|v\|_2=1\}.
\]

To see this directly, write a feasible matrix as
\(W=\sum_r u_ru_r^T\), with (u_r\ge0). Its trace is
\(\sum_r\|u_r\|^2=1\), so its objective is a convex combination of
the normalized rank-one objectives. Conversely every such rank-one
matrix is feasible. Thus the lift is infeasible exactly when \(\mu<0\).

If a negative objective matrix is returned, a completely positive
factorization contains at least one factor with (u_r^TSu_r<0). That
factor, with (h=-b^Tu_r), gives a violated family cut. Alternatively,
one may solve the stated four-dimensional nonnegative quadratic problem.
A rank-one optimal solution exists, but a general SDP solver need not
return one. Claiming automatic extraction from an arbitrary numerical
dual matrix would omit a real algorithmic step. Numerical negativity and
factorization need their own tolerances or exact certification.

For the rational moment witness from the counterexample note,
(v=(1,1,3,1)^T) and (h=1/2) give \(-1/40\). Keeping (v) fixed and
minimizing (h) gives the stronger exact violation

\[
h=\frac{2361}{5000},\qquad
L(p_{h,d,k})=-\frac{644321}{25000000}.
\]

## Prior results and significance

[Anstreicher and Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf)
already give an exact SDP description of the entire three-variable box
quadratic hull through a triangulation, using six DNN blocks of order four
for the displayed triangulation. They also mention a five-tetrahedron
triangulation. Their result implies every member of this family.
Consequently, the new item under review is a restricted family with a
small lift per chosen orientation, not a new general tractability theorem
for three-variable box quadratic optimization.

[Anstreicher and Puges, Section 4](https://arxiv.org/html/2501.09150v1#S4)
use a trilinear variable, its eight RLT inequalities (14), and SOC
inequalities (15)–(16) under permutations and switches. Lemmas 4–5 show
that this system implies ETRI1/2/3. The counterexample's exact witness
satisfies that system but violates a member of the proposed family.
Adding this family to their system therefore strictly strengthens that
system. The single new orientation alone has not been proved to dominate
their system. Their exact disjunctive comparator already enforces the cut.

The cone identity, Schur complement, and CP-based separation are classical
ingredients. Any originality claim must concern the explicit family, its
geometric derivation, and the value of its selective enforcement. This
review has not established priority for those components. A broader
search for equivalent parameterizations and overlapping-multiplier
certificates remains necessary. A further mathematical question is whether
all symmetry copies, combined with an appropriate baseline, characterize
any useful class more fully; no such completeness claim has been proved
here.

## Verification record

The independent exact command run for the new assertions was

```sh
python research-20260925/verify_three_positive_family_review.py
```

It checks both symbolic identities, the elimination of (h), and the two
rational separating values. It does not mechanize the classical cone
identity, compactness, Schur-complement argument, or global nonnegativity
inference; those are justified above. The existing targeted command

```sh
python research-20260925/checks/three_positive_gap_certificate.py
```

was also rerun and passed its 27 localizing-matrix checks and all 24 and
48 switched SOC checks. Its code was read against equations (14)–(16),
including the nonnegative factors needed for rotated SOC validity.
The eight scalar localizing blocks give (14); the base PSD block and
diagonal upper-bound checks supply the remaining baseline conditions.
No project-wide checks, CI checks, or Lean verification were performed.

## Final normalization check

The final formulation reduces the ten nonnegative entries to six by
requiring `diag(N)=0`. The root independently checked this step: from
`S=P+N`, replace `P` by `P+diag(N)` and `N` by `N-diag(N)`.
The former remains PSD and the latter remains entrywise nonnegative.
The reverse implication is immediate. Thus the final six-variable
formulation has exactly the same projection as the version reviewed above.
