# Independent review of the three-positive-variable SDP counterexample

Date: 2026-09-25. Reviewer: the `direction_audit` research agent, independently
of the construction. Scope: the displayed rational quadratic, the exact
27-block relaxation, its certificate interpretation, and the strict gap.

**Verdict:** the counterexample is correct. It answers negatively the
three-positive-loop exactness question stated in Section 3 of the inspected
version of Khajavirad's paper. The conclusion concerns that particular
relaxation. Exact SDP lifts of the three-variable quadratic box hull were
already known. The explicit rational feasible point proves a strict gap and
removes any need to infer a primal gap from unattainability of a dual
certificate.

The construction and its moment table are in
[the counterexample note](three-positive-disjoint-counterexample.md).
The broader comparison is in
[the exploration note](three-positive-exploration.md).

## 1. Exact match to the source relaxation

I inspected [Khajavirad, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2),
particularly Section 3, definitions (9)--(16), Theorem 3, equation (17), and
the open question after Example 3. For three positive-loop vertices, set
`P=V={1,2,3}` and `M=empty` in (17). Its indices are exactly

\[
A\mathbin{\dot\cup}B\mathbin{\dot\cup}R=V,
\qquad v_R=(1,(x_i)_{i\in R}),
\]

and its matrices are

\[
M_{A,B,R}(y)
=L_y\!\left[
 \left(\prod_{i\in A}x_i\prod_{j\in B}(1-x_j)\right)v_Rv_R^T
\right]\succeq0.
\tag{1}
\]

Here `L_y` replaces each monomial by its assigned moment. The required
monomials are the eight squarefree monomials, including `1`, and the twelve
monomials `x_i^2 prod_{j in S}x_j` with `S` contained in `V\{i}`.

There are `3^3=27` matrices: eight scalar blocks, twelve blocks of order two,
six of order three, and one of order four. No required block is omitted.
The constraint `y_000=1` gives the source's normalization. Smaller choices of
positive and conditioning sets add no strength beyond the full system: their
matrices follow by taking principal submatrices and summing the two
complementary choices for every unused coordinate.

The polynomial certificate cone dual to (1) is therefore

\[
\mathcal D_3=
\left\{\sum_{A\dot\cup B\dot\cup R=V}
 x_A(1-x)_B\,v_R^TQ_{A,B,R}v_R:
 Q_{A,B,R}\succeq0\right\}.
\tag{2}
\]

Each Gram matrix decomposes into affine squares involving only `R`.
This is the full disjoint-support affine-SOS cone in the candidate note.
Some matrix entries have degree four, such as `x_i^2 x_j x_k`. I used the
explicit Section 3 matrices to establish (1), rather than relying on the
degree labels in the separate Section 6 certificate discussion.

## 2. Nonnegativity of the quadratic

Consider

\[
p=x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+\tfrac14.
\]

Its quadratic coefficient matrix is

\[
Q=\begin{pmatrix}1&3&-6\\3&1&-6\\-6&-6&9\end{pmatrix}.
\]

The three principal determinants of order two are `-8,-27,-27`.
At any local minimum in the relative interior of a face, the principal
submatrix on that face's free coordinates must be positive semidefinite:
every sufficiently short displacement in those coordinates is feasible in
both directions, so the second directional derivative is nonnegative.
Any face with at least two free coordinates contains one of the displayed
indefinite principal submatrices. Hence **every global minimum lies on an
edge or vertex**. Compactness supplies a global minimum. This argument does
not assume that stationary points elsewhere are minima.

I independently minimized all twelve univariate restrictions over `[0,1]`
using exact rational arithmetic. The minima are as follows; each row for a
free `x` has a distinct symmetric row for a free `y`.

| Free coordinate | Fixed coordinates | Minimizer | Minimum |
|---|---|---:|---:|
| `x` | `y=0,z=0` | `1/2` | `0` |
| `x` | `y=0,z=1` | `1` | `25/4` |
| `x` | `y=1,z=0` | `0` | `1/4` |
| `x` | `y=1,z=1` | `1` | `1/4` |
| `z` | `x=0,y=0` | `0` | `1/4` |
| `z` | `x=0,y=1` | `1/6` | `0` |
| `z` | `x=1,y=0` | `1/6` | `0` |
| `z` | `x=1,y=1` | `5/6` | `0` |

Thus `p>=0` on the cube and its minimum is zero. Its zeros are precisely

\[
a=(\tfrac12,0,0),\quad b=(0,\tfrac12,0),\quad
c=(1,0,\tfrac16),\quad d=(0,1,\tfrac16),\quad
e=(1,1,\tfrac56).
\]

Indeed, a zero is itself a global minimum, so the same face argument places
it on an edge. The exact edge restrictions have only the listed zeros.

## 3. Independent proof that no disjoint certificate exists

Suppose `p` had a certificate (2). Since `p(0)=1/4`, some individual affine
square term has positive value at the origin. Its weight must have `A=empty`.
Write its affine factor as

\[
L=\alpha+\beta x+\gamma y+\delta z,
\qquad\alpha\ne0,
\]

where any variable belonging to `B` has coefficient zero in `L`.
Every term is nonnegative on the cube, so every term vanishes at every zero
of `p`.

The weight `(1-x)_B` is strictly positive at `a` and `b`, for every `B`.
Consequently `L(a)=L(b)=0`, giving `beta=gamma=-2 alpha`.
Thus neither `x` nor `y` can belong to `B`, and `B` is contained in `{z}`.
Its weight is then positive at `c` and `e` as well. The equation `L(c)=0`
gives `delta=6 alpha`. But

\[
L(e)=\alpha-2\alpha-2\alpha+5\alpha=2\alpha\ne0,
\]

a contradiction. The fifth zero `d` is unnecessary for this particular
exclusion argument. This proof also excludes certificates in any smaller
degree-truncated cone with the same support restriction.

The hidden assumption to avoid is that a variable may occur both in the box
factor and in its affine square. That is prohibited in the actual source
formulation. Allowing such overlap changes the certificate cone, and the
proof above would no longer apply without further work.

## 4. Strict primal gap: independent rational calculation

Nonmembership in a linear image of PSD cones does not, by itself, imply
a strict separation: such images can fail to be closed. The explicit moment
witness in the candidate note avoids that issue completely.

I independently entered its twenty rational moments with denominator
`10000`, expanded every factor `(1-x_j)` combinatorially, and formed all
27 matrices in (1). I used standard-library `Fraction` arithmetic and
symmetric Schur elimination, independently of the construction's numerical
search and its SymPy determinant checks. Every pivot is strictly positive.
The calculation returned:

```text
BLOCK COUNTS {1: 8, 2: 12, 3: 6, 4: 1}
POSITIVE PIVOTS 54 MIN 307/3855000
EXACT OBJECTIVE -1/40
```

Positive pivots prove positive definiteness of all 27 symmetric matrices.
The normalization moment is one. Therefore this is a feasible point of the
source's strongest relaxation, and

\[
\inf\{L_y(p):y_{000}=1,\ M_{A,B,R}(y)\succeq0\}
\le -\tfrac1{40}<0=\min_{[0,1]^3}p.
\tag{3}
\]

The witness also separates the source's joint quadratic hull: its three
diagonal coefficients `1,1,9` are positive, so adding the allowed
nonnegative diagonal slacks to a true point preserves the inequality
`L(p)>=0`.

No claim that `-1/40` is the relaxation's optimum is required or proved.
It is an explicit feasible objective value. The same witness gives
`L_y(p+1/80)=-1/80`, whereas `p+1/80>=1/80` on the cube. Thus the failure
also occurs for a strictly positive quadratic, rather than depending on
exact contact zeros in the final instance.

For completeness, the abstract strict-gap route can also be made sound.
Uniform cube moments give strict feasibility because the integral of a
nonzero affine square against any factor weight is positive. The relaxed
objective is bounded below by `-103/4`: full squarefree RLT bounds every
first and mixed second moment between zero and one, and the three diagonal
moments are nonnegative. Standard finite-dimensional conic Slater duality
then gives dual attainment. An optimal value zero would contradict the
proved exclusion from (2). This route is not needed for (3).

## 5. Significance, prior work, and limits

The source's three-positive-loop question concerns exactly the full
Section 3 relaxation checked above. Accordingly, the wording "a negative
answer to the question in arXiv:2601.18545v2, Section 3" is justified.
The latest version displayed at the [arXiv abstract page](https://arxiv.org/abs/2601.18545)
when inspected was v2. This is a version-specific conclusion, not a claim
that no later treatment exists anywhere.

[Anstreicher and Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf)
already provide an exact lift using a triangulation into six tetrahedra and
completely positive matrices of order four, which equal doubly nonnegative
matrices. The present result does not improve or disprove that
representability theorem. Its addition is a rational separating example for
a substantially stronger recent relaxation than the elementary SDP and RLT
systems, together with a short explanation of the support obstruction.

The example gives a useful test case for future relaxations and suggests
that certificates permitting overlapping supports, or selected simplex
blocks, may repair the missing inequalities. Establishing a useful general
repair, a separation algorithm, or an effective solver improvement requires
additional work. A single three-variable obstruction does not classify
graphs admitting exact formulations and does not establish practical
weakness across typical applications.

Targeted web searches included the exact arXiv identifier with
`counterexample`, `disjoint three Khajavirad SDP`, fragments of the
polynomial, and `box quadratic five zeros`. They did not locate an
equivalent earlier counterexample. That unsuccessful search does not
establish novelty or priority. The search did locate a later
[April 2026 manuscript by Khajavirad](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_007.pdf)
on sparse polynomial optimization; its inspected quadratic section does
not answer this relaxation question. Its separate use of a previously
identified incorrect treewidth lemma was referred to the graph-width
reviewer, rather than treated as evidence about this counterexample.

## 6. Verification scope

The targeted check actually run for this review was a separate inline
`python` program using only `fractions` and `itertools`. It checked all
27 localizing matrices, all 54 positive Schur pivots, the exact objective,
the three principal determinants of order two, every edge minimum, and all
five zeros. Its matrix construction and edge minimization were written
independently before reading the other verifier's implementation.

The durable companion check
[verify_three_positive_disjoint_review.py](verify_three_positive_disjoint_review.py)
was subsequently inspected; it performs the same exact tasks. The inline
run is the independent calculation reported above. These exact arithmetic
checks do not constitute a Lean formalization or a mechanical proof of the calculus and SOS
arguments. Those arguments were checked mathematically in Sections 2--3.
No project-wide verification or CI check was performed. The additional
parameterized family in the candidate note is outside this review's scope.
