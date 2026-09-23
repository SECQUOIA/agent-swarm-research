# Second independent audit: smooth-map integer precision

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.
Target:
[the smooth-map result](../results/smooth-map-local-rank-integer-complexity.md).

**Verdict: PASS.** The local noncommutative-rank lower bound, global
Hessian-span upper bound, and compact fixed-degree polynomial upper
construction are correct under the stated assumptions. This review
found no substantive proof defect. It independently checks the analytic
step, rather than inferring it from the earlier quadratic result.

The result remains a novelty candidate; this audit does not establish
publication priority. The imported matrix-evaluation characterization,
Hörmander estimate, and parity argument are established results.

## Analytic theorem and its precise use

Hörmander's 1973 Theorem 1.1 states the needed mixed-Hessian operator
estimate: for a real smooth phase and smooth compact amplitude, a
nonvanishing mixed-Hessian determinant gives `L2 -> L2` norm
`O(lambda^(-N/2))`. Its assumptions do not require positive curvature
or a symmetric mixed Hessian. I checked the theorem and the beginning
of its proof in the
[original paper's primary-source text](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7179-11512_2006_Article_BF02388505.pdf).
Direct PDF opening timed out in this audit, but the search service returned
the actual theorem and proof text from that primary document.

I also read Theorem A and its proof on printed pages 50–51 in the
[editor-hosted Wolff notes](https://personal.math.ubc.ca/~ilaba/wolff/notes_march2002.pdf),
using the previously downloaded local PDF text. That source independently
confirms the hypotheses, norm exponent, and small-support localization.

For the candidate's application, the neighborhood and cutoff are chosen
once, before the contact set or accuracy parameter. Thus derivative,
support, and inverse-Hessian bounds are fixed. The phase can be extended
smoothly outside a slightly larger neighborhood if a globally defined
phase is desired; it is unchanged near the amplitude support.

No regularity of the contact set's boundary is required. Its indicator
belongs to `L2`; the operator estimate extends from smooth functions
by density and applies to the actual compactly supported integral kernel.

## Direct check of local nondegeneracy

At the repeated base point let the mixed-Hessian matrix be `A_0`,
with smallest singular value `sigma>0`. The neighborhood can be made
a convex product neighborhood on which

```
||Phi_XY(X,Y)-A_0|| <= sigma/2.
```

For two output-side points `X,Z`, integration along their segment gives

```
grad_Y[Phi(X,Y)-Phi(Z,Y)]
 = integral_0^1 Phi_XY(Z+t(X-Z),Y)^T (X-Z) dt.
```

Its difference from `A_0^T(X-Z)` has norm at most
`(sigma/2)|X-Z|`. Therefore its norm is at least
`(sigma/2)|X-Z|`. This verifies the key nonstationary-phase
condition without assuming that arbitrary averages of invertible
matrices remain invertible.

Smoothness gives uniform bounds for the normalized phase difference
and its derivatives. Repeated integration by parts in the `TT*`
kernel then produces the required off-diagonal decay; choosing more
than `N` integrations makes both Schur integrals finite and of order
`lambda^(-N)`. The square root yields the stated operator exponent.
This is a check of the established local argument, not a new analytic
theorem. The candidate conservatively assumes `C^infinity`; this
audit does not assert that `C^2` would suffice.

## Matrix evaluation and the midpoint phase

For full pointwise noncommutative rank, a finite complex matrix evaluation
of the Hessian pencil is invertible. Its determinant, at that fixed
evaluation dimension, is a real-coefficient polynomial in the matrix
entries. Nonvanishing at a complex tuple implies that polynomial is
nonzero, and hence that it is nonzero at some real tuple. This gives
fixed real matrices `B_j`. They need not be symmetric.

The full midpoint defect is

```
D_j(x,y)=f_j(x)+f_j(y)-2f_j((x+y)/2).
```

Differentiating once in each input gives

```
(D_j)_xy=-(1/2) Hess f_j((x+y)/2).
```

For the Cartesian-power phase in the result, the block in row `a`
and column `b` of its mixed Hessian is therefore

```
-(1/2) sum_j (B_j)_ab Hess f_j((x_a+y_b)/2).
```

At the repeated base point this is exactly the matrix evaluation
`-(1/2)sum_j B_j tensor Hess f_j(x_0)`. The Kronecker block order and
factor are correct. Continuity lets one choose the common small box
`Q` so that the whole `Q^d times Q^d`, together with a neighborhood
supporting the cutoff, lies within the nondegenerate region. All
midpoints remain in the original smooth domain.

## Contact volume and arbitrary integer lifts

Let `v=vol_n(S)` and `K=sum_(a,b,j)|(B_j)_ab|>0`. Pairwise contact
defects bounded by `2epsilon` give `|Phi|<=2Kepsilon` on
`S^d times S^d`. For

```
lambda=1/(4Kepsilon),
```

the phase angle has absolute value at most one half. For sufficiently
small accuracy, `lambda>=1`. The cutoff equals one on the entire
integration set, and its exponential has real part at least one half.

The measure of the product is `v^(2d)`, whereas the squared `L2`
norm of `1_(S^d)` is `v^d`. Consequently

```
(1/2) v^(2d) <= C (4Kepsilon)^(nd/2) v^d.
```

For positive volume, division by `v^d` and the `d`th root yield
`v<=C'epsilon^(n/2)`. Zero volume is immediate. The evaluation
dimension cancels from the precision exponent, though it remains in
fixed constants. In particular no missing factor of `d` survives.

At an integer midpoint of two exact graph lifts, the visible error is
`D_j/2`, so convex feasibility implies exactly the contact condition
`|D_j|<=2epsilon`. Parity classes therefore satisfy the volume lemma.
Their closures inside `Q` remain contact sets by continuity, are
compact and measurable, and still cover `Q`. The cover argument does
not require bounded integer coordinates, measurable projections, closed
lifts, or regular contact geometry.

For pointwise rank `r<n`, the independently reviewed Hermitian
principal-compression lemma selects `r` original coordinates.
Fixing the others at the interior base point gives an actual
`r`-dimensional box and the correct compressed Hessians. Applying
the preceding volume argument in that dimension yields the stated
`r/2` coefficient. The largest occurring rank on the nonempty
interior occurs at some point because ranks take only finitely many
integer values; compactness of the interior is not needed.

## Fixed global structure and the smooth upper bound

The span of all Hessians is a finite-dimensional real matrix space.
A single shrinking witness for this space gives a single decomposition
`Z,W,R` working at every input in the original domain. In its
coordinates, only Hessian entries with endpoint exponent sum at least
one can be nonzero, for exponents `0,1,1/2` on `Z,W,R`.
Their sum is `r_all/2`.

For arbitrary smooth functions the forbidden blocks need only vanish
on the original transformed parallelepiped. The proof correctly
intersects its grid with this domain and chooses every Taylor center
inside the resulting convex cell. Each Taylor segment stays inside
that cell. Therefore no derivative bound or structural zero is
silently used outside the domain.

If side widths are `b_i 2^(-alpha_i T)`, every contributing remainder
term has magnitude at most a fixed coefficient times `2^(-T)`.
The finitely many Hessian entries and outputs have one uniform bound
on the compact domain. With remainder at most `epsilon/2), an
affine output band of radius `epsilon/2` contains the whole graph
on its cell and remains within `epsilon` of it.

Each band over a compact cell is a bounded polyhedron. A convex-hull
disjunctive formulation with distinct binary codes represents their
union exactly at integral codes: a convex combination of zero-one
codes is integral only when every positively weighted code is the
same. Boundedness excludes nonzero recession contributions from
inactive members. Hence the logarithm of the number of cells, rather
than the number of cells itself, bounds the required binaries.

The construction may have polynomially many rows in `1/epsilon`.
That limitation is correctly stated. If every Hessian vanishes, the
functions are affine on the connected box and need no binaries.

## Compact polynomial formulation

For polynomials, each forbidden Hessian entry vanishes on a nonempty
open subset and thus vanishes identically. This validates the same
Taylor estimate on the larger normalized enclosing box, including
at prefix points outside the transformed original domain.

The dyadic prefix `A` and point `y=A+rho` both lie in that box;
their joining segment lies there as well. The expression

```
f_j(A)+sum_i partial_i f_j(A) rho_i
```

is the exact first-order Taylor polynomial at `A`. Its approximation
error comes solely from the bounded remainder.

After expansion, terms are products of at most `D` input bits or
products of at most `D-1` input bits and one bounded residual.
The displayed AND constraints force an auxiliary continuous variable
to equal the zero-one product whenever the existing input bits are
integral. Thus the subsequent four-row bounded-product formulation
with a residual is exact even though this auxiliary variable is not
declared integer. Empty products are constants; repeated bits can
be removed. No new integer coordinate is introduced.

With fixed `n,m,D`, the number of expanded terms is at most
`O((1+sum_i L_i)^D)`, and each requires `O(D)` rows.
All coefficient-weighted expressions are exact and may have either
sign. The error band and binary count therefore remain correct,
and the claimed polynomial-in-depth total size follows.

## Material limits retained by the theorem

- The lower bound uses local pointwise noncommutative rank; the upper
  bound uses the span of Hessians over the whole domain.
- Equality of those ranks gives the matching law. When they differ,
  the result is a sandwich and does not claim a characterization.
- All exact graph points must be admitted, with two-sided vertical
  error for every admitted output.
- Polynomial compactness requires fixed degree; the result does not
  assert a comparable row bound for an arbitrary smooth map.
- Coefficients are allowed to be real and this result itself makes no
  preprocessing bit-complexity claim.
- Neither an exact graph representation nor a bound for a graph on an
  arbitrary lower-dimensional feasible set follows without further work.

