# Second independent audit: noncommutative-rank integer precision law

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Source: `results/quadratic-system-noncommutative-rank-complexity.md`,
including the added elementary Hall/permanent lower proof.

## Verdict

The full theorem passes this second independent proof audit. I found no
substantive gap in the principal compression over the free skew field,
complex-to-real shrinking argument, symmetric coordinate conversion,
Hall/permanent covariance estimate, parity lower bound, or matching
compact binary upper construction. Both the full-rank case and arbitrary
rank deficiency are handled correctly.

This audit independently checked the mathematical derivations and the
needed primary algebraic sources. It does not establish publication
priority. The theorem is correctly stated as a fixed-data formulation
size and integer dimension result with real coefficients; it does not
claim polynomial bit-time construction of the coordinate system.

## Imported algebra and field conventions

I checked the open published paper of Garg, Gurvits, Oliveira, and
Wigderson. Theorem 1.4 gives the full-rank/shrunk-subspace equivalence
explicitly over the complex numbers. Theorem 1.17 characterizes rank `r`
by the largest zero rectangle after invertible constant row/column
changes, with its two sizes summing to `2n-r`. This yields exactly the
maximum deficiency formula used in the draft. Appendix A.3 also records
the rank-decrease formulation. [Primary source](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).

I also checked Volčič's Section 2.1: the complex free skew field has the
involution conjugating scalar coefficients and fixing its free
variables. Reversal of products and adjoint inversion are the usual
involution identities. Consequently the real symmetric coefficient
pencil here is Hermitian over the division ring. [Primary source](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1).

The zero-rectangle equivalence can be connected to the draft's exact
formula directly. A column subspace of dimension `j` sent into a row
space of dimension at most `n-i` has deficiency at least `i+j-n`.
Conversely, a subspace/image pair of deficiency `d` can be made
coordinate spaces by independent invertible changes, exposing a zero
rectangle with size sum `n+d`. Thus the maximum deficiency is `n-r`.
No identification of complex and real maximizing subspaces is silently
assumed at this stage; the later descent proof supplies it.

## Principal full-rank compression over the division ring

The Hermitian principal-pivot induction is valid in a noncommutative
division ring. A nonzero diagonal element has an inverse, and its
one-by-one pivot is Hermitian. If all diagonals vanish but the matrix
is nonzero, choose an off-diagonal `a!=0`. The stated two-by-two inverse
has its factors in the correct order: multiplying on either side gives
the identity using `a a^(-1)=a^(-1)a=1` and the corresponding identities
for `a*`.

For a Hermitian invertible pivot `D`, its inverse is also Hermitian.
Therefore `G-E*D^(-1)E` is Hermitian. Invertible block row/column
elimination gives rank additivity, which is valid over a division ring
without commutativity. When induction chooses principal indices `J`
in the Schur complement, restricting the original matrix to the pivot
indices together with `J` has exactly `S[J,J]` as its Schur complement.
Its invertibility follows from the two invertible blocks. The selected
principal order is the original rank, including the zero-rank empty
case.

Applying this argument to the Hermitian free-field pencil produces an
actual set of original coordinate indices. Its compressed coefficient
matrices remain real symmetric and its pencil has full noncommutative
rank. Fixing complementary real input coordinates inside their box
intervals gives a genuine full-dimensional box for the compressed
system. Graph containment and error remain valid under that affine
restriction, and no integer coordinate is added. This avoids any need
to realize a noncommutative basis change as a real input transformation.

## Full-rank energy estimate by Hall and the permanent

Let the compressed dimension be `s`. For each real orthogonal `O`,
`W_ab=sum_j (O^T G_j O)_ab^2` is nonnegative. A failed Hall condition
for a set of columns would put all images of the corresponding real
coordinate subspace into a strictly smaller row coordinate space.
Conjugating by `O` produces a real shrunk subspace, whose complexification
would contradict full complex noncommutative rank. Hence every such
support graph has a perfect matching.

The permanent is a sum of nonnegative products and contains a positive
matching product. It is therefore strictly positive at every orthogonal
matrix. Each entry, and hence the permanent, is a continuous function
of `O`. The orthogonal group is compact, so its minimum `mu` is attained
and strictly positive. Pointwise positive continuous functions would not
have this conclusion on a noncompact domain; compactness here is
precisely what makes the uniform constant legitimate.

One of the `s!` permutation products is at least `mu/s!`. In the
orthonormal eigenbasis of a positive definite covariance, the energy is

```
E = sum_(a,b) W_ab lambda_a lambda_b.
```

Symmetry of the Hessians is used here: the trace expansion contains
squares, not potentially signed products. Retaining that permutation's
`s` positive terms and using ordinary arithmetic-geometric mean gives

```
E >= s (mu/s!)^(1/s) (product_a lambda_a)^(2/s).
```

Both copies of the eigenvalue product occur because a permutation uses
every row and every column exactly once. Thus the determinant exponent
and the factorial factor are correct. This independently proves the
energy estimate required by the theorem from the shrunk-subspace
characterization alone. It does not assert that `mu/s!` equals operator
capacity or that it is efficiently computable.

As a separate exact finite check, I used the cross-product Hessians and
12 rational orthogonal Householder changes of basis. Exact rational
arithmetic verified permanent positivity, the best matching-product
bound by permanent divided by `6!`, and the resulting energy-determinant
inequality for positive diagonal eigenvalues varying over powers of two.
All checks passed. This finite exercise corroborates the formulas;
the Hall and compactness argument proves the universal assertion.

## Capacity variant and covariance factors

The optional capacity route is also algebraically correct. Positive
complex capacity bounds the determinant ratio at every real positive
definite matrix, since such matrices are among its admissible arguments.
For the real symmetric tuple, `T(Sigma)=sum_j G_j Sigma G_j` is positive
definite. Applying eigenvalue arithmetic-geometric mean to
`Sigma^(1/2) T(Sigma) Sigma^(1/2)` gives

```
tr(Sigma T(Sigma))
 >= s [det Sigma det T(Sigma)]^(1/s)
 >= s kappa^(1/s) (det Sigma)^(2/s).
```

No symmetry-preserving operator scaling is claimed or needed. The
qualitative main proof can use the independently justified permanent
constant instead, so it has no dependence on a quantitative capacity
algorithm or rational-coefficient lower bound.

The fourth-moment identity retains the factors verified in the earlier
vector audit. Pairwise midpoint error at most epsilon means
`|q_j(x-y)|<=4 epsilon` for `q_j(v)=v^T G_j v/2`. Centering independent
uniform samples gives

```
E[q_j(X-Y)^2]
 = (1/2)E[(X^T G_j X)^2]
   +(1/2)(E[X^T G_j X])^2 + tr(G_j Sigma G_j Sigma).
```

Thus total energy is at most `16m epsilon^2`. Combining it with either
energy lower estimate gives determinant at most
`[16m epsilon^2/(s kappa^(1/s))]^(s/2)`. The volume-covariance inequality
then yields the stated `C_s epsilon^(s/2)` with its displayed `C_s`.
Here `kappa` may mean the true positive capacity or the substitute
`mu/s!`, provided the same choice is used consistently.

## Parity cover and finite constant

For every parity support, two exact graph points have feasible integer
midpoint lifts. Their midpoint input lies in the original box, so the
error condition applies. Closing each support in that compact box
preserves all pair inequalities and coverage. Positive-volume supports
have positive definite covariance; zero-volume supports contribute zero
to the volume sum. There are at most `2^p` supports regardless of the
integer ranges and continuous lift dimension.

On the principal slice of dimension `r`, the cover gives
`V_I<=2^p C_r epsilon^(r/2)`. Rearranging yields exactly

```
epsilon >= sqrt(r kappa_I^(1/r)/m) V_I^(2/r)
           / [4(r+2) omega_r^(2/r)] * 2^(-2p/r).
```

The power `kappa_I^(1/r)` appears inside a square root, as required.
The affine coefficients of the restricted quadratics disappear from
midpoint differences. No closedness of the lifted convex set is needed.

## Real maximum-shrunk-space descent

For complex subspaces, `A(U+V)=A(U)+A(V)` and
`A(U intersect V)` is contained in `A(U) intersect A(V)`. The dimension
identity therefore gives supermodularity with the direction written in
the draft. The maximum deficiency is attained because its possible
integer values form a finite nonempty set.

Real Hessians preserve deficiency under conjugation. If `U` has maximum
deficiency `d`, both `U+conjugate(U)` and `U intersect conjugate(U)`
have deficiency at most `d`, while supermodularity says their sum is at
least `2d`. Each is consequently a maximizer. In particular the sum is
conjugation invariant. A conjugation-invariant complex vector space is
the complexification of its real part: real and imaginary parts of each
vector belong to it. Its image under real matrices is likewise the
complexification of the corresponding real image. This proves existence
of real `U,V=A(U)` with real dimension difference exactly `d`.

The argument is valid when `d=0`, and neither requires a unique
maximizer nor a rational maximizing subspace. It does not use a
genericity assumption or continuity of optimizing subspaces.

## Symmetric shrinking and the precision exponents

The projection maps `P_V:U->V` and `P_U:V->U` are adjoints under the
inherited real inner products, so they have equal rank. Their kernels
are the stated spaces `Z` and `W`; hence `dim Z-dim W=d`.
They are orthogonal because `Z subset U` and `W subset U^perp`.

For `z in Z`, every `H_j z` belongs to `V`. For every `u in U`,
symmetry gives `u^T H_j z=(H_j u)^T z=0`. Thus `H_j z` also belongs
to `U^perp` and lies in `W`. This proves the zero blocks in the proposed
orthogonal coordinate system. In particular, `Z` has no internal
quadratic terms and no quadratic coupling to the complementary `R`.

The only possibly nonzero quadratic blocks are `ZW`, `WW`, `WR`, and
`RR`. Exponents 0, 1, and 1/2 on `Z,W,R` respectively give endpoint
sums 1, 2, 3/2, and 1 for these blocks, including squares. The sum of
all coordinate exponents is

```
dim W+(dim R)/2 = [n-(dim Z-dim W)]/2 = r/2.
```

This is a simultaneous coordinate system for the entire Hessian family,
not a separate scalar diagonalization. The reasoning remains valid for
nontrivial overlap between the original `U,V`, zero-dimensional blocks,
and maximum deficiency coming from a common kernel.

## Anisotropic upper and its scope

The orthogonal image of a full-dimensional bounded box is contained in
a full-dimensional bounded coordinate box. Retaining the original linear
box constraints and the affine coordinate identities ensures that the
upper formulation remains a valid relaxation of the original domain.
Approximating uniformly on the larger box only strengthens its error
guarantee. Positive diagonal normalization preserves all quadratic zero
blocks; translations generate affine terms but do not create new
quadratic support.

With `L_i=ceil(alpha_i T)`, every required residual product has error
at most `h_i h_k/4<=2^(-T)/4`. The residual-square triangle has the
same bound with `h_i^2`; its validity was independently checked in the
vector audit. All binary prefix products are exactly linearizable,
including products involving an undiscretized `Z` coordinate. Such a
coordinate has no binary prefix, but its residual is a bounded continuous
factor and can be multiplied exactly by the other endpoint's bits.

Signed output assembly loses at most `C 2^(-T)/4<=epsilon`. Every exact
graph point has a lift with its actual residual products. Summing the
rounded depths adds at most `n` to `T sum_i alpha_i`, giving the claimed
`r/2` leading coefficient. The count of auxiliary products and rows is
linear in the total participating depths for fixed data. If `r=0`, the
pencil is identically zero, all Hessians vanish, and the affine graph is
exactly polyhedral without binaries; the separate case avoids dividing
by a quadratic coefficient bound of zero.

The lower bound counts arbitrary unrestricted integer coordinates,
while this upper uses binaries. Their common leading coefficient
therefore follows by the stated sandwich. The theorem appropriately
allows arbitrary real coordinate changes and coefficients. Rational
construction, coefficient encoding, and unequal vanishing accuracy
vectors would require additional results; they are not claimed here.
