# Publication audit of the quadratic family and its exact gap

Date: 25 September 2026. Independent reviewer: `family_proof_audit`.

## Verdict

The mathematical claims in [the family SDP note](three-positive-family-sdp.md)
and [the disjoint-certificate counterexample](three-positive-disjoint-counterexample.md)
pass this audit. This includes the unrestricted scalar parameter, nonnegative
parameter boundary, exposed-ray statement under the strict contact assumptions,
the order-five LMI with six nonnegative variables, and strict separation from
both named relaxations. No unresolved proof gap was found in these claims.

This verdict does not establish publication priority, completeness after all
symmetries are imposed, minimality of the lift, or a practical advantage over
the classical exact tetrahedral formulation. Those are separate questions.
The claim ready for use is exact enforcement of this particular valid family
and the displayed strict separation.

## Parameter domains and the nonnegative identity

Write

\[
L=h-d_1x-d_2y+d_3z,\qquad D=d_1+d_2-h.
\]

The identity

\[
\begin{aligned}
L^2+2d_3kz(1-x-y)+k(2D+k)xy
={}&(L-kxy)^2+2d_3kz(1-x)(1-y)\\
&+k(2d_1+k)xy(1-x)+2kd_2xy(1-y)
+k^2x^2y(1-y)
\end{aligned}
\]

holds as a polynomial identity. Its right side is nonnegative on the cube
for every real `h` and every `d_1,d_2,d_3,k >= 0`. In particular, negative
`h`, zero coordinates of the parameter vector, and the zero vector require
no limiting argument. When `k=0` the polynomial is an affine square;
exclusion from the disjoint cone is not claimed on this boundary.

The nonnegative coefficient of each diagonal moment is `d_i^2`. Thus validity
extends to the positive-loop hull with upward diagonal slack. A coordinate
complement sends the diagonal moment to `1-2m_i+Y_ii` and leaves that slack
unchanged. This checks validity under the stated symmetries in both the compact
moment hull and the positive-loop hull.

## Exact lift, including closure and zero diagonal

With `b,B` exactly as displayed in the family note, direct expansion gives

\[
L_y(q_{h,d,k})=h^2+2h b^Tv+v^TBv,
\qquad v=(d_1,d_2,d_3,k)^T.
\]

For every fixed nonnegative `v`, minimizing over **all real** `h` gives
`v^T(B-bb^T)v`, attained at `h=-b^Tv`. Hence all family cuts hold exactly
when `B-bb^T` is copositive. This is an algebraic equivalence for arbitrary
normalized first and second moments; it does not assume that the candidate
already satisfies a baseline relaxation. Restricting `h` to be nonnegative
would change this argument and is not an allowed abbreviation.

The classical identity `COP_4 = S_+^4 + N_4`, where `N_4` is the symmetric
entrywise nonnegative cone, supplies an exact decomposition. There is no
unproved closure step: in a convergent sequence `P_j+N_j`, both nonnegative
diagonals are bounded, the PSD bound
`|(P_j)_ab|^2 <= (P_j)_aa(P_j)_bb` bounds `P_j`, and then `N_j` is bounded.
A convergent subsequence gives a decomposition of the limit.

If a decomposition has nonzero diagonal in `N`, move that diagonal into
the PSD summand. The resulting `N` has zero diagonal and six independent
nonnegative off-diagonal entries. The Schur complement of the fixed entry
one proves the exact order-five LMI. This reduction also applies when
the copositive matrix lies on its boundary. Neither strict feasibility nor
positive diagonal is required for the equivalence.

Setting `N=0` is generally invalid as a representation of the family.
For example, the actual cube point `(x,y,z)=(1/2,1/2,0)`, with its exact
moments, gives a matrix `B-bb^T` whose first diagonal entry is zero and whose
`(1,4)` entry is `1/8`. It is not PSD, although every family inequality is
valid at that point. This proves the need to retain a nonnegative summand;
it does not prove that six is the smallest possible auxiliary-variable count.

The normalized separation SDP is also exact. Its feasible set is compact,
and `(I+ee^T)/8` is strictly feasible. The identity `DNN_4=CP_4` implies that
its objective is a convex combination of normalized nonnegative rank-one
objectives. Consequently a negative optimum is equivalent to a violated
family member. Extracting that member from an arbitrary SDP solution still
requires a completely positive decomposition or a separate vector search.
The note states this limitation correctly.

## Contacts and exposed rays

The exposed-ray claim uses the strict conditions

\[
h,d_1,d_2,d_3,k>0,\quad h<\min(d_1,d_2),\quad d_1+d_2-h+k<d_3.
\]

These conditions place all five contacts in their stated edge interiors.
For any quadratic nonnegative on the cube and vanishing there, the edge
restrictions have double zeros, including the possibility of an identically
zero restriction. The two bottom edges therefore determine the common
nonnegative scale `lambda`, constant, and first two linear coefficients.
Comparison with the first vertical contact determines the third square
coefficient because `d_1-h>0`. The three vertical derivatives then determine
the third linear coefficient and its two mixed coefficients. The last
contact determines the remaining mixed coefficient. Every coefficient is
`lambda` times the displayed family coefficient.

This argument remains valid for `lambda=0`; it then forces the entire
quadratic to be zero. Since the sum of the five evaluations is nonnegative
on the cone, its zero face is exactly the asserted nonnegative ray.
No generic-rank assumption or unexamined exceptional strict parameter value
is used. The same contacts prove disjoint-cone exclusion: an affine factor
positive at the origin is forced to have value `alpha*k/h` at the fifth
contact, contradicting its required zero. The strict inequalities are used
at the denominators and the positive contact weights, and must be retained.

For the rational example, the independent edge check and all five zeros
also passed. The polynomial is nonnegative but has value `-1/40` at the
reported rational moment functional. The positive definite localizing
matrices make this a direct separation certificate, without an assumption
that the disjoint certificate cone is closed or that an SDP optimum is
attained. The shifted polynomial `p+1/80` gives the claimed strictly positive
counterexample by the same functional.

## Baseline constraints and the Anstreicher–Puges comparison

The unconditioned order-four localizing matrix is the ordinary PSD moment
constraint. The eight scalar blocks are the cube atom weights

\[
\lambda_s=L_y\!\left(\prod_{i:s_i=1}x_i
                         \prod_{i:s_i=0}(1-x_i)\right),
\qquad s\in\{0,1\}^3.
\]

They sum to one. Marginalizing these nonnegative weights gives the first
moments and off-diagonal second moments, so it gives all off-diagonal RLT
constraints. For example,

\[
m_i+Y_{jk}-Y_{ij}-Y_{ik}
=L_y\bigl(x_i(1-x_j)(1-x_k)+(1-x_i)x_jx_k\bigr)\ge0.
\]

The other triangle type follows from

\[
1-m_1-m_2-m_3+Y_{12}+Y_{13}+Y_{23}
=L_y\bigl((1-x_1)(1-x_2)(1-x_3)+x_1x_2x_3\bigr)\ge0.
\]

The 27 blocks do **not** themselves imply diagonal upper bounds
`Y_ii <= m_i`. Those are unnecessary for the positive-loop formulation,
but required by the compact moment baseline used in the comparison.
The witness satisfies them separately, with exact slacks
`649/10000, 649/10000, 87/1250`.

The primary [Anstreicher–Puges source, Section 4](https://arxiv.org/html/2501.09150v1#S4)
was inspected again. Equations (14)–(16) match the implemented scalar and
SOC constraints, and Lemmas 4–5 give the claimed ETRI implications. All
permutations and coordinate complements are covered by the checker.
The squared SOC inequalities also have nonnegative right-hand factors:
PSD gives the switched diagonal factors, and the nonnegative cube atoms
give the switched cross moments. The rational witness has strictly positive
factors, with minimum `22/625` over the factors checked.

The primary [Khajavirad source, Section 3](https://arxiv.org/html/2601.18545v2#S3)
was also inspected. Taking `P={1,2,3}`, `M` empty in equation (17) gives
the 27 blocks: counts `8,12,6,1` in orders `1,2,3,4`. The explicit
three-variable exactness question concerns this system. The comparison
uses these matrices, without relying on the later SOS degree convention.

Thus the same witness belongs to both named baseline relaxations and is
cut off by the proposed family. The strict-strengthening statement means
intersection with the family formulation. It does not mean that one family
block alone contains or dominates either baseline.

## Verification record and limits

The following targeted commands were run and passed in this audit:

```sh
python research-20260925/checks/three_positive_gap_certificate.py
python research-20260925/verify_three_positive_family_review.py
python research-20260925/verify_three_positive_disjoint_review.py
```

They respectively verify all 27 strict localizing matrices and the 24 plus
48 switched SOC inequalities; the symbolic family and moment identities;
and an independent rational matrix, edge, and zero calculation. The exact
SOC slack minima remain `2831/4000000` and `124813/12500000`.

An additional temporary `python - <<'PY'` check using `Fraction` and the
first script's moment evaluator enumerated all switched SOC factors,
off-diagonal RLT inequalities, and ordinary triangle inequalities. It found
minimum slacks `22/625` for off-diagonal RLT and `49/5000` for TRI, and
the separate diagonal slacks above. This is a supplementary arithmetic
check; the preceding atom identities are the independent implication proof.

The conic identity, Schur complement, contact argument, and source matching
were checked mathematically; these scripts do not formally verify them.
No project-wide checks, CI inspection, numerical optimization, or new
research extension was undertaken for this audit.

The older [family review](three-positive-family-lmi-review.md) describes the
pre-refinement lift with ten auxiliary entries in some passages. That
formulation remains correct but is superseded in size by the zero-diagonal
refinement audited here. A publication should use the six-variable version
consistently and should not claim that this count is minimal.
