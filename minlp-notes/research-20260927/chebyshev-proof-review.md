# Independent review of the Chebyshev path construction

Date: 2026-09-27. Review target: [structure-frontier.md](structure-frontier.md).
This review independently checks the mathematical argument and a stronger
decomposition sensitivity result. The literature screen is limited; it does
not establish novelty or publication readiness.

## Verdict and required scope

The exact threshold is correct for the explicitly specified edge-bag
hierarchy: with `N=2^m` and integer `r>=1`, its value is zero when `2r<N`
and two when `2r>=N`. Both the moment primal and the sparse SOS dual have
these values. The lower witness consists of actual locally feasible
probability measures, so it also defeats exact local convexification with
the same truncated overlap information.

The hierarchy convention matters. Every bag must have a full order-`r`
moment matrix, normalization, and all equality consequences `L(hp)=0`
with `deg(p)<=2r-2`. All overlap moments through degree `2r` are identified.
For quadratic `h`, this equality convention is equivalent to
`M_{r-1}(hy)=0`: products of two monomials of degree at most `r-1` span
all monomials of degree at most `2r-2`. It is also obtained by imposing
both signs of the equality as localizing inequalities at that order.

These are not claims about arbitrary algorithms, dense moment hierarchies,
all sparse decompositions, or intrinsic optimization difficulty. In fact,
bags of size three make order two exact, as proved below. Algebraic
presolve that identifies the duplicate chains also solves the instance.

## Lower witness and indexing audit

Let `q(t)=2t^2-1`. For uniform `k` in `0,...,N-1`, use

\[
X_+=\cos(2\pi k/N),\qquad X_-=\cos((2k+1)\pi/N).
\]

For each integer `0<=a<N`, expansion of `cos(theta)^a` into Fourier
frequencies gives equal moments: every nonzero frequency has magnitude
below `N`, and its average on either angular grid is zero. The constant
frequency agrees as well. Repeated cosine values retain their probability
multiplicities; deleting repeated atoms without combining weights would
change the law.

Push `X_+` through the entire `u` chain and `X_-` through the entire `v`
chain. Each edge measure satisfies its recurrence and every box inequality
pointwise. All within-chain overlaps agree as full probability laws. The
only cross-chain overlap is `x`, whose moments agree through degree `2r`
when `2r<N`. The terminal values are respectively `+1` and `-1`, giving
objective zero. The objective is a sum of two local squares, so zero is
also a valid sparse SOS lower bound.

A single global indexing vector for moments does not invalidate this
witness. With the edge-bag PSD architecture, the only monomials appearing
in two distinct bags are singleton monomials and the constant. These are
exactly the shared coordinates already checked. A global dense moment
matrix would introduce additional conditions and is a different relaxation.

The `m=1` case is harmless: the first valid order is already the exact
threshold `r=1`, so its below-threshold range is empty.

## Upper bound with an explicit sparse certificate

Put `P_j=T_{2^{m-j}}` for `0<=j<=m`. The Chebyshev composition identity gives
`P_{j-1}=P_j composed with q`. Define the polynomial

\[
R_j(a,b)=\frac{P_j(b)-P_j(q(a))}{b-q(a)}.
\]

This quotient is a polynomial by the difference-of-powers identity. If
`k=deg(P_j)=2^{m-j}`, its degree is at most `2k-2`, so
`deg((b-q(a))R_j)<=2k<=N`. In particular, the equality multiplier is
allowed at `r>=N/2`, including the endpoint case without an extra order.

Writing `h_j^u=u_j-q(u_{j-1})` and similarly for `v`, telescoping gives

\[
u_m-T_N(x)=\sum_{j=1}^m h_j^uR_j(u_{j-1},u_j),
\quad
v_m-T_N(x)=\sum_{j=1}^m h_j^vR_j(v_{j-1},v_j).
\]

Hence the following is an allowed edgewise sparse SOS certificate:

\[
F-2=u_m^2+v_m^2+
2\sum_{j=1}^m\bigl[h_j^vR_j(v_{j-1},v_j)
-h_j^uR_j(u_{j-1},u_j)\bigr].
\]

It proves the bound directly, without invoking Slater conditions or
strong duality. A feasible point with `T_N(x)=0` attains two, proving
both primal and dual values. The box localizers are unnecessary for this
upper certificate; they are satisfied by the lower witness.

## A width-two decomposition is exact at order two

This improves the first four-variable-bag repair. Use the path of bags

\[
C_1=\{x,u_1,v_1\},\qquad
B_j=\{u_{j-1},v_{j-1},u_j\},\quad
C_j=\{v_{j-1},u_j,v_j\}\quad(2\le j\le m),
\]

ordered `C_1,B_2,C_2,...,B_m,C_m`. Its consecutive separators are the
pairs `{u_{j-1},v_{j-1}}` and `{v_{j-1},u_j}`. Every variable occurs
consecutively, so the running intersection property holds. These are
`2m-1` bags of size three, and every original equation is supported in a
bag. Assign both first equations to `C_1`, and each later `u`/`v`
equation to `B_j`/`C_j` respectively.

Use `M_2` PSD, all local equality multiples through degree four, the
quadratic box localizers `M_1((1-z^2)y)>=0` for every bag variable, and
all pair-separator moments through degree four. Redundant copies of a
variable's box constraint can be placed in each containing bag.

**Base.** In `C_1`, both quadratic residuals
`h_u=u_1-q(x)` and `h_v=v_1-q(x)` have zero squared expectation: their
squares are equality multiples of degree four. The PSD form on
degree-at-most-two polynomials then gives
`L((u_1-v_1)^2)=L((h_u-h_v)^2)=0`.

**Induction in `B_j`.** Write `a=u_{j-1}`, `b=v_{j-1}`, `c=u_j`, and
`d=a-b`. The shared pair moments give `L(d^2)=0`. The exact identity

\[
4d^2-d^2(a+b)^2
=2d^2(1-a^2)+2d^2(1-b^2)+d^4
\tag{A}
\]

has nonnegative expectation on every right-hand term: the first two
use the quadratic box localizers with multiplier `d`, and the last is
an allowed square. The square `d^2(a+b)^2` also has nonnegative
expectation. Thus `L(d^2(a+b)^2)=0`.

Set `h=c-q(a)`. Another exact identity is

\[
(c-q(b))^2-4d^2(a+b)^2=h\,[h+4d(a+b)].\tag{B}
\]

The right side is an allowed equality multiple. Therefore
`L((c-q(b))^2)=0`. This polynomial depends only on the separator
`{b,c}` and has degree four, so its expectation transfers to `C_j`.

**Induction in `C_j`.** Put `e=v_j` and `k=e-q(b)`. The identity

\[
(c-e)^2-(c-q(b))^2=k\,[k-2(c-q(b))]\tag{C}
\]

is another equality multiple of degree at most four. It gives
`L((u_j-v_j)^2)=0`, completing induction.

At the terminal bag, PSD gives `L(u_m-v_m)=0`. Expanding the objective
now yields `L(F)=2+L(u_m^2)+L(v_m^2)>=2`. A true minimizing point is
feasible for the relaxation, so its optimum is two.

Quadratic boxes are material to this order-two proof. Replacing them
solely by linear bounds `1+/-z>=0` changes the relaxation and does not
automatically justify (A). Order three suffices without these quadratic
localizers: if `L(d^2)=0`, PSD `M_3` gives `L(dp)=0` for every polynomial
`p` of degree at most three, in particular `p=d(a+b)^2`; identities
(B)--(C) then finish the same induction.

## Literature screen and significance assessment

- Lasserre, [Convergent SDP-relaxations in polynomial optimization with
  sparsity](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf)
  (2006), especially Theorem 3.6 and its measure-gluing proof, supplies
  the convergent sparse hierarchy under running intersection and local
  compactness. The local repository full text was inspected. Its
  asymptotic convergence does not state the sharp order for this family.
- Korda, Magron, and Ríos-Zertuche,
  [Convergence rates for sums-of-squares hierarchies with correlative
  sparsity](https://d-nb.info/1330825241/34) (2024), Theorem 8, gives
  quantitative sparse Putinar bounds. Its constants depend on the
  constraint data and the collection of bags; its clique-size-dependent
  exponent is not a uniform fixed-order guarantee over growing instances.
  A full evaluation of its constants on the present family remains open
  in this review. The new example must not be described as contradicting
  that theorem.
- Balada Gaggioli, Henrion, and Korda,
  [Composition and tensor train structure in polynomial
  optimization](https://arxiv.org/abs/2604.17563) (April 2026), Sections
  4--5, develops state-lifting chordal and push-forward moment hierarchies.
  Equation (21) uses exactly the full equality-multiple convention
  reviewed here. Sections 4.3 and 5.2 describe the degree/bag-size
  tradeoff and fixed-order complexity; Section 6 numerically tests
  quadratic compositions. This is a close framework precedent, so
  composition lifting or a degree-versus-width tradeoff alone is not
  a new contribution. The inspected sections do not provide the present
  exact exponential order threshold or the width-two repair.
- Fawzi, Saunderson, and Parrilo,
  [Equivariant semidefinite lifts of regular
  polygons](https://arxiv.org/html/1409.4379v1) (2014 preprint), Theorems
  1 and 7, proves exact theta-rank `ceil(N/4)` for regular `N`-gons and
  gives logarithmic-size PSD lifts for powers of two. It is a substantial
  conceptual precursor: trigonometric degree can conceal a much smaller
  lifted certificate. Its hierarchy is over polygon vertices, rather
  than the edgewise quadratic-chain hierarchy here. No equivalence of
  the two constructions was proved in this review.

Queries examined included `sparse Lasserre hierarchy lower bound
treewidth continuous polynomial optimization degree exponential Chebyshev`,
`"sparse" "Lasserre" "exponential" lower bound`, and
`"treewidth" "sparse" "SOS" convergence lower bound`. Failure to find
an identical result is not evidence establishing novelty.

The strongest defensible candidate contribution is the explicit sharp
order separation between edge bags and these size-three bags for bounded
quadratic input on a path. It is an instructive obstruction to choosing
bags solely to minimize width. Its duplicate-computation structure limits
claims about solver importance: recognizing the duplicates already removes
the difficulty. Broader usefulness requires a structural condition or
an algorithm that identifies comparably useful bag enlargements beyond
this deliberately constructed family.

## Verification record

The targeted command `python - <<'PY' ... PY` was run from the repository
root using SymPy to expand the differences in (A)--(C), and a direct set
check to verify the stated bag path for `m=1,...,20`. Result:

```
PASS: 3 exact polynomial identities; width-two path RIP for m=1,...,20
```

The algebra checks use exact symbolic arithmetic. The finite bag checks
are supplementary; the consecutive-occurrence argument proves running
intersection for all `m`. The proof does not use a numerical SDP result.
No project-wide checks or CI inspection were performed, and this review
does not claim a Lean formalization.

## Follow-up: a rational perturbation preserves a fixed gap

The subsequent extension changes only the first equation of the `v`
chain to

\[
v_1=(1-\delta)q(x),\qquad \delta=4^{-m}.
\]

All later equations retain the map `q(t)=2t^2-1`. This extension is
correct, including the claimed constants. It removes literal duplicate
equations between the two branches, but uses a perturbation that decreases
exponentially with their length. It does not establish a gap robust to
a fixed perturbation independent of `m`.

Every state remains in `[-1,1]`: the first perturbed map has image
`[-1+delta,1-delta]`, and `q` preserves the box. On that box,

\[
|q(a)-q(b)|=2|a-b||a+b|\le4|a-b|.
\]

Thus every feasible point satisfies
`|u_m-v_m|<=4^{m-1}delta=1/4`. With `d=u_m-v_m` and
`s=(u_m+v_m)/2`, the objective is `2s^2+(d-2)^2/2`.
Consequently its true optimum is at least `49/32`.

Use the original angular-grid law on the `u` chain and the other grid
law on the perturbed `v` chain. The moments at `x` still agree below
degree `2^m`, and within each branch the laws are consistent. The `u`
terminal is one. The perturbed `v` terminal lies within `1/4` of its
unperturbed value minus one. Therefore the edge-bag relaxation has a
feasible point with objective at most `1/16` for `2r<2^m`. Its gap from
the true optimum is at least `47/32`. No assertion about its exact value
or exact convergence order follows from this argument.

### Width-two order-two certificate for the perturbed lower bound

The same size-three bags certify a lower bound of `49/32` at order two.
This need not equal the true perturbed optimum. A complete degree-four
sparse certificate follows, making the statement valid for the SOS dual
as well as the moment primal.

For the first bag put

\[
h_u=u_1-q(x),\quad h_v=v_1-(1-\delta)q(x),\quad
g=v_1-(1-\delta)u_1=h_v-(1-\delta)h_u.
\]

Writing `d_1=u_1-v_1`, the identity

\[
\delta^2-d_1^2
=\delta^2(1-u_1^2)+g(2\delta u_1-g)\tag{D}
\]

proves `L(d_1^2)<=delta^2`. The final term is an allowed combination of
the first two equality residuals with a linear multiplier. This avoids
any need to propagate fourth moments of `q(x)` for the base case.

For a later pair of bags use the variables from (A)--(C), and let
`d=a-b`, `h=c-q(a)`, and `k=e-q(b)`. Combining those identities gives

\[
\begin{aligned}
16d^2-(c-e)^2
={}&8d^2(1-a^2)+8d^2(1-b^2)+4d^4\\
&-h[h+4d(a+b)]-k[k-2(c-q(b))].\tag{E}
\end{aligned}
\]

Each term lies in one of the two bags and has degree at most four.
The first three terms belong to the local quadratic module; the last
two are allowed equality multiples. Thus
`L(d_j^2)<=16L(d_{j-1}^2)`. Equivalently, (E) is a degree-four sparse
certificate for this propagation bound.

Let `A_1=delta^2-d_1^2` and `A_j=16d_{j-1}^2-d_j^2` for `j>=2`.
The positive weighted sum

\[
16^{m-1}A_1+\sum_{j=2}^m16^{m-j}A_j
=16^{m-1}\delta^2-d_m^2=\tfrac1{16}-d_m^2\tag{F}
\]

cancels the intermediate separator polynomials. Finally, the terminal
bag supports the identity

\[
F-\tfrac{49}{32}
=\tfrac12(u_m+v_m)^2
+4(d_m-\tfrac14)^2
+\tfrac72(\tfrac1{16}-d_m^2).\tag{G}
\]

Substitution of (D)--(F) into (G) is the claimed order-two sparse SOS
certificate. In particular, no assumption that a truncated moment
sequence has a representing measure is used for the width-two bound.

### Encoding, limitations, and verification

The coefficient `1-delta=(4^m-1)/4^m` has `O(m)` binary digits. Only the
first perturbed equation requires coefficients of growing bit length;
the total ordinary sparse input remains `O(m log(m+1))` bits after
including variable indices. The perturbed family no longer has a fixed
finite coefficient alphabet. The weights in (F) have `O(m)` bits, as do
all coefficients in the expanded certificate; large numerical magnitude
is not exponential binary description length.

For `m=1`, the condition `2r<2^m` has no admissible integer order `r>=1`.
Nontrivial lower-order gaps therefore start at `m=2`. The result still
concerns the chosen edge-bag hierarchy. Recognizing and exploiting a
small discrepancy between the two chains is simple for this example,
and the extension does not itself establish a broad solver lower bound
or a practical bag-selection algorithm.

A second targeted inline Python/SymPy command checked the exact polynomial
identities (D), (E), and (G), the weighted telescope (F) for `m=1,...,20`,
and the rational gap subtraction. Result:

```
PASS: 3 exact perturbation certificates; weighted telescope m=1,...,20; gap=47/32
```

These are independent exact checks of the substantive extension. The
all-length telescoping formula and Lipschitz bound are proved above;
the finite computation is supporting verification.

The checks from both inline commands were then preserved in
[check_chebyshev_review.py](check_chebyshev_review.py). The reproducible
targeted command actually run was:

```
python research-20260927/check_chebyshev_review.py
```

It returned:

```
PASS: 6 exact identities; width-two RIP and weighted telescope m=1,...,20; gap=47/32
```
