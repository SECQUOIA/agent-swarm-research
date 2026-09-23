# Box truncation of divergence base polyhedra: source and exact specialization

Date: 2026-09-05. This closes the formula and greedy-support attribution
question in
[the path-cut investigation](parametric-path-cut-clamp-investigation.md),
Section 2. The separate physical pooling reduction is not reviewed here.

The displayed box-truncation formula is established. Shioura,
Shakhlevich, and Strusevich, *A submodular optimization approach to
bicriteria scheduling problems with controllable processing times on
parallel machines*, SIAM Journal on Discrete Mathematics 27(1), 186–204
(2013), state it in Theorem 1, equation (11), printed page 192. Their
theorem identifies the maximal vectors of a nonempty submodular
polyhedron intersected with a box as a base polyhedron with this rank
function. Their Theorem 2 on the same page gives the greedy optimizer by
differences of rank values on sorted-cost prefixes. Both statements
were read in the
[primary manuscript](https://eprints.whiterose.ac.uk/id/eprint/78189/10/shakhlevich1.pdf).
The authors credit their 2009 paper and also cite Frank–Tardos (1988),
Proposition II.2.11, on generalized-polymatroid truncation. Those earlier
proofs were not independently inspected for this note.

Here is the exact specialization, including the total-sum condition.
Let `f` be finite submodular on `2^V`, with `f(empty)=0`, and define

```
B(f) = {d : d(S)<=f(S) for all S, d(V)=f(V)}.
Q = B(f) intersect {alpha<=d<=beta}.
g(S) = min_(T subset V) [f(T)+beta(S\T)-alpha(T\S)].
```

Assume `Q` is nonempty. Then `alpha<=beta`, `g(empty)=0`,
`g(V)=f(V)`, and `Q=B(g)`. In the flow application `f(V)=0`, but the
identity does not require that numerical normalization.

For completeness, these equalities also have a short direct check.
Any `d in Q` satisfies, for all `S,T`,

```
d(S) = d(T)+d(S\T)-d(T\S)
     <= f(T)+beta(S\T)-alpha(T\S).
```

Thus `d(S)<=g(S)`. For `S=empty,V`, combining this inequality with
the choices `T=empty,V`, respectively, gives the asserted normalizations.
Conversely, for `d in B(g)`, choosing `T=S` gives `d(S)<=f(S)`.
For `S={i}`, choosing `T=empty` gives `d_i<=beta_i`. For
`S=V\{i}`, choosing `T=V` gives
`d(V\{i})<=f(V)-alpha_i`, hence `d_i>=alpha_i`.

Submodularity of `g` follows by partial minimization on the product
lattice. The summand for each coordinate is
`beta_i s(1-t)-alpha_i t(1-s)`, for binary membership indicators
`s,t`. Its cross coefficient is `alpha_i-beta_i<=0`, so it is
submodular jointly in `s,t`; add the submodular term `f(T)`. Apply
the lattice inequality to minimizing sets for two choices of `S` and
then minimize on their union and intersection. This proves the needed
property without an assumption that `f` is monotone or nonnegative.

For a real cost vector `c`, sort indices so that
`c_(sigma1)>=...>=c_(sigman)` and set `S_k={sigma1,...,sigmak}`.
The greedy point has

```
d_(sigma k) = g(S_k)-g(S_(k-1)).
max_(d in Q) c.d
 = c_(sigma n) f(V)
   + sum_(k=1)^(n-1) (c_(sigma k)-c_(sigma(k+1))) g(S_k).
```

Ties cause no difficulty. Negative costs also cause no difficulty:
adding a common constant to all costs changes every feasible objective
by that constant times the fixed total `f(V)`. Minimum support is the
negative of maximum support for `-c`.

Nonemptiness must be established independently before using this
formula as a support value. The weaker condition
`P(f) intersect [alpha,beta]` nonempty alone need not preserve the
original total `f(V)`. This distinction is precisely why the base
intersection assumption belongs in the pooling argument. The formula,
box closure, and greedy rule are classical ingredients, with no novelty
claim here.
