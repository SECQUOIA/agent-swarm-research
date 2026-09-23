# Independent review of the PSD path approximation set

**The theorem and its stated corollaries pass independent mathematical review.**
For fixed matrix dimension, the construction in the
[author's note](research-20260912-dag-psd-approximation-set.md) produces a
polynomial-size set of actual feasible paths that approximates every feasible
PSD information sum from both sides, including singular sums with exactly the
same kernel. Its Turing bit complexity is polynomial in the explicit rational
DAG input size and inverse accuracy. No correction to the mathematical
statement or proof was required.

This review does not establish priority. The polynomial degree depends
strongly on the fixed matrix dimension. The construction is not a
dimension-independent fixed-parameter tractability result. An independent
checker now exercises every basis trial on small exact instances; this is
neither a production solver nor evidence of useful performance on realistic
graphs. The author's unresolved literature qualifications remain necessary.

The review treats the new range-enumeration argument independently of the
earlier determinant theorem. Its conclusions rest on the following checks.

1. **Every feasible range has an enumerated rational basis.** Rational
   pivoted PSD Schur elimination gives each input matrix at most `p` positive
   weighted rational rank-one factors. The residual stays PSD and its rank
   decreases at every positive pivot. A PSD matrix with all diagonal entries
   zero is zero. For a sum of PSD matrices, the kernel is the intersection of
   the summand kernels. Thus all factors of a rank-`r` feasible information
   matrix lie in its range and contain an independent set of `r` labels.
   Enumerating all `r<=p` therefore covers every possible range, even though
   the graph may contain exponentially many paths. The number of different
   nonzero feasible ranges cannot exceed the number of enumerated label bases.

2. **The rectangular normalization can be undone.** For the rational
   full-column-rank matrix `V`, the stated `L=(V^T V)^(-1)V^T` is a left
   inverse and `Pi=VL` is its range projector. The exact test `Pi Q=Q`
   means that the range of `Q` is contained in that basis range. Symmetry
   also gives `Q Pi=Q`. Consequently the proposed `T` and `K` satisfy
   `TK=I`, `KT=Pi`, and `K(TQT^T)K^T=Q` for every retained summand. This
   identity is the decisive new safeguard for singular matrices. Without
   the range test, closeness after multiplication by `T` would not control
   components outside the guessed range.

3. **A good basis trial exists for each path separately.** In the finite
   weighted-factor collection of any rank-`r` target path, a maximum-volume
   basis `B` exists. Replacing one of its columns by any factor multiplies
   its `r`-dimensional volume by that factor's corresponding coordinate
   magnitude, proving `|x_i|<=1`. This works in a proper subspace just as
   it does in the full space. Although the argument uses square roots,
   the algorithm enumerates labels and needs no irrational comparison.
   Its dyadic scales put each transformed selected factor's squared
   coordinate in `[1,4)`. Every target factor then has coordinate magnitude
   below 2. There are at most `p` factors in each matrix, so the prior and
   every target edge pass the diagonal threshold `4p`. The target also
   passes the exact range restrictions.

4. **Owner constraints are sufficient and do not assert compatibility.**
   Requiring every distinct selected edge owner includes all selected
   factors once; factors sharing an owner are distinct summands of that
   edge matrix. Prior factors are already present. A DAG cannot reuse an
   edge. Hence each accepted path obeys `A>=I_r`, while every original
   summand stays in the selected range. It therefore has exactly that
   range. An arbitrary enumerated basis can have mutually incompatible
   owners, or an owner removed by a filter. Such a trial simply has no
   complete terminal mask. The target's maximum-volume trial has compatible
   owners by construction. The mask needs at most `r` bits regardless of
   how many other edges occur on the path.

5. **Merging labels preserves paths and the required error bound.** Exact
   floor gives a remainder in `[0,h)` even for negative off-diagonal
   entries. A path of at most `N` edges has remainder in `[0,Nh)` for
   each coordinate. Different path lengths require no extra label: the
   difference of two such remainders has magnitude less than `Nh`, not
   `2Nh`. The unrounded common prior cancels. Thus two complete paths at
   the same integer-label state have a symmetric transformed difference
   satisfying `||Delta||_2 <= rNh = eta`. Since the target obeys `A>=I_r`,
   both inequalities follow:

   ```text
   Ahat >= A-eta I_r >= (1-eta) A,
   Ahat <= A+eta I_r <= (1+eta) A.
   ```

   Congruence by `K` and exact reconstruction give the claimed sandwich
   in the original space. In topological order, every continuation depends
   only on the vertex, owner mask, and label sum. Replacing a prefix by the
   retained prefix at that state cannot create a repeated-vertex conflict:
   all prefix vertices precede the current vertex and all suffix vertices
   follow it in the DAG order. Side constraints must already be encoded
   in the graph, as the theorem states.

6. **Rank zero and unknown rank need no positivity promise.** A feasible
   information sum is zero precisely when its prior and all traversed
   edge matrices are zero. Searching the zero-edge subgraph therefore
   covers the entire rank-zero family with one path. All nonzero ranks
   are enumerated, so the algorithm needs neither an optimal rank nor a
   positive eigenvalue lower bound. If `s=t`, acyclicity leaves only the
   empty path. If there is no feasible path, the empty output is correct.
   The two-sided sandwich with `eta<1` itself forces equal kernels; the
   exact range and owner arguments also establish this directly.

7. **The stated state count and bit bound are valid.** A signed edge
   label lies between `-4p/h-1` and `4p/h`. Thus every path-label coordinate
   lies in an interval of length at most `8pN/h+N`. The displayed bound
   `C_r=ceil(8prN^2/eta+N)+2` safely bounds the number of possible integers.
   There are `r(r+1)/2` coordinates, at most `2^r` masks, and at most
   `binom(M,r)` basis trials. Counting all terminal masks in the output
   bound is conservative because only the complete mask is accepted.
   Reconstructing a path multiplies the output bound by at most `N`.
   For fixed dimension, rational elimination, inverse Gram matrices,
   projectors, transforms, and floors have polynomial bit complexity.
   A tiny positive pivot increases rational bit length; it does not
   enlarge the normalized label interval. Dyadic exponent magnitude is
   bounded by the weight's encoding length, so storing the corresponding
   rational power of two also needs only polynomial space. No spectral
   oracle or square-root computation is needed by the set construction.

The scalar consequences are correct. A nonnegative Loewner-nondecreasing
function homogeneous of degree `q>0` inherits the factor `(1-eta)^q`
by evaluating the representative of an optimal path. No concavity is
needed, and the stated requirement for an objective comparison procedure
is material. For determinant, `eta=epsilon/p` and Bernoulli's inequality
give `1-epsilon`; determinant roots have factor `1-eta`. These do not
assert a multiplicative log-determinant guarantee. Minimum eigenvalue
has factor `1-eta`, with exact comparison possible through fixed-degree
rational characteristic polynomials and algebraic-number operations.
Its optimum is zero if every feasible matrix is singular.

For positive definite matrices, inversion reverses the sandwich, giving
an A-optimality cost at most `1/(1-eta)` times optimum. The suggested
`eta=epsilon/(1+epsilon)` gives the claimed minimization ratio. A feasible
positive definite matrix exists if and only if the output set contains
one. Assigning infinite cost to singular matrices therefore allows exact
detection of the no-finite-cost case; it is not a claim that an undefined
infinite-cost approximation ratio has numerical meaning.

For any target and its same-range representative, restrict both matrices
to an orthonormal basis of their common range. They become positive
definite, so the same inverse comparison applies there. Embedding back
gives

```text
(1+eta)^(-1) J(P)^dagger
  <=_PSD J(P_hat)^dagger
  <=_PSD (1-eta)^(-1) J(P)^dagger.
```

Their equal ranges preserve estimability of each specified contrast.
Thus minimizing its variance over the same output set has the stated
A-type bound with infinite cost assigned to nonestimable contrasts.
This argument does not use a false order-reversing rule for pseudoinverses
with different kernels. Adding a common PSD prior or applying a common
congruence preserves the original sandwich directly, so the corresponding
reuse claims are also valid.

The finite-memory transfer is a valid algebraic composition, conditional
on the separately established uniform matrix approximation and explicit
PSD graph construction. Apply the memory comparison once to the target
and once to its representative. The resulting true-matrix factors are
`(1-eta)(1-delta)/(1+delta)` and
`(1+eta)(1+delta)/(1-delta)`, exactly as stated. With `eta=epsilon/4`
and `delta<=epsilon/8`, the lower deficit is at most `epsilon/2` and
the upper excess is at most `17epsilon/28`, hence both satisfy the
requested `1±epsilon` bounds. The singular case remains valid because
each comparison preserves kernels. Obtaining an FPTAS in the original
design input still requires the stated polynomial graph construction,
fixed contraction and noise-ratio promises, and fixed information
dimension. This review does not extend those model assumptions.

The independent
[exact checker](../code/research_20260912/review_psd_approximation_set.py)
enumerates all factor bases and all feasible paths of its small fixtures.
It verifies maximum-volume witnesses for every nonzero-rank path, checks
every eligible same-label pair, and verifies coverage and equal kernels
directly using exact rational PSD tests. Unlike a solver, it deliberately
uses exhaustive path enumeration for verification. Its
[saved results](../code/research_20260912/results/psd-approximation-set-independent-review.json)
record 15 cases, 453 independent basis trials, and 38 feasible paths, all
covered by 32 output paths in total. The checks include:

- 35 maximum-volume witnesses and 42 same-label spectral sandwiches;
- 272 signed-floor residual checks and 19 actual state merges, including
  11 merges between paths of different lengths;
- 60 incompatible-owner trials, five trials with repeated basis owners,
  139 prior-range rejections, and 153 edge-range deletions;
- zero matrices, empty and infeasible path cases, mixed ranks from zero
  to three, distinct almost parallel rank-one ranges generated by
  `(1,0)` and `(1,2^-80)`, and a proper oblique rank-two range with a
  `2^-60` scale;
- three exact checks of the finite-memory accuracy constants.

All checks passed. They support the proof audit and exercise failure-prone
boundaries; they do not replace the symbolic argument or assess novelty.
Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_psd_approximation_set.py
```
