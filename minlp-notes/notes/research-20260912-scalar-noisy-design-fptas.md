# Scalar noisy Markov design: approximation scheme and priority audit

Date: 2026-09-12. Status: mathematical corollary of the separately reviewed
[uniform finite-history theorem](research-20260912-noisy-markov-memory.md),
now checked in a [fresh independent review](research-20260912-scalar-fptas-independent-review.md).
For a scalar parameter (rank-one information target), FPTAS existence is
likely implied by a 2012 bounded-treewidth Gaussian algorithm; see the
[detailed prior-work reduction](research-20260912-scalar-gmrf-prior-reduction.md).
That reduction does not establish the same conclusion for input-sized rank
in the weighted-trace objective. The [full-block corollary and priority audit](research-20260912-full-block-design-fptas.md)
separately retain both observation and parameter dimensions as input.
This note concerns one scalar mean parameter,
or a fixed positive-semidefinite weighted trace of information. It does not
claim an approximation scheme for multi-parameter D-optimal design.

Das and Kempe (STOC 2008) studies the same scalar objective, gives an exact
algorithm for noiseless exponential covariance, and gives an FPTAS for
fixed-bandwidth covariance. Its displayed perturbation extension does not
directly give an FPTAS for positive nugget and dense exponential covariance.
However, for the rank-one target the later Gaussian message-passing algorithm
appears to give one after a target-variable augmentation and routine
recurrence adaptations.
The finite-history method remains a distinct specialized algorithm; its
dependence on correlation can make it impractical. No first-FPTAS claim is made.

## 1. Precisely defined input class

Fix rational constants `0<rho0<1` and `B0>0`. The input consists of rational
initial/process/noise variances, transitions, and mean sensitivities for

```text
Y_t = m_t(theta)+X_t+v_t,
X_t = a_t X_(t-1)+w_t,                 t=2,...,n.
```

Errors have the independence and Gaussian assumptions in the cited theorem.
The input is promised to satisfy

```text
|a_t| <= rho0,
0 <= Var(X_t) <= Pbar,
Var(v_t) >= rmin > 0,
Pbar/rmin <= B0.
```

The rational bounds `Pbar,rmin` can be supplied or computed from the input.
The promise is checkable by rational variance recursions and comparisons.
Zero process variances, signed transitions, and time-varying parameters are
allowed. The covariance is known and independent of the mean parameter.
There is one candidate at every calendar index, an integer `0<=k<=n`, and
only the requirement `|S|=k`. Prespecified mandatory or forbidden candidates
can also be included if the resulting family is nonempty.

For one mean parameter, write the rational sensitivity as `f_t` and define

```text
I(S) = I0+f_S^T R_SS^(-1) f_S,         I0>=0 rational.
```

Set the data term to zero when `S` is empty. A more general objective covered
by the same proof is

```text
I(S) = tr[W (J0+F_S^T R_SS^(-1) F_S)],
W >= 0, J0 >= 0,
```

with rational matrices. Here `W` is fixed across schedules; it may be supplied
as input. This is a weighted trace of information, not the A-optimal trace of
its inverse. Matrix dimension contributes polynomial arithmetic cost. No
sensitivity magnitude bound or strictly positive optimum is needed for the
multiplicative assertion. The logarithmic assertion requires a positive
optimum.

## 2. Algorithm and approximation ratio

Return the empty schedule immediately if `k=0`. For rational
`0<epsilon<1`, put `eta=epsilon/2` and

```text
C0 = 2 B0/(1-rho0)^2.
```

Choose the smallest integer `L>=0` with `C0 rho0^(L+1)<=eta`, unless
`L=n-1` is reached first; `L=n-1` makes every conditional exact. For `n=1`
use `L=0`, and for `n=0` return the empty schedule. If the actual transitions
are all zero, exact independent selection can instead be used directly.
Rational power comparisons suffice; rounded logarithms are unnecessary.

For every time `t` and subset `H` of its preceding `L` calendar indices,
calculate the true local conditional coefficients and variance

```text
b_(t,H) = R_(t,H) R_HH^(-1),
d_(t,H) = R_tt-R_(t,H) R_HH^(-1) R_(H,t),
g_(t,H) = f_t-sum_(j in H) b_(t,H),j f_j,
w_(t,H) = g_(t,H)^2/d_(t,H).
```

For the trace objective use instead
`w_(t,H)=tr[W G_(t,H)^T G_(t,H)]/d_(t,H)`, with
`G_(t,H)=F_t-sum_j b_(t,H),j F_j`.
All these quantities are rational and every weight is nonnegative.

Run one exact longest-path dynamic program. Its state records the calendar
index, the last `L` selection bits, and the number of selected candidates so
far. Skipping gives zero reward; selecting gives `w_(t,H)` for the recorded
history. Retain the best accumulated reward for each state and a predecessor
for reconstruction. Terminal states must have count `k`. The output `S_hat`
maximizes the finite-history objective `I_L(S)` over all feasible schedules.
The constant prior term need not be stored in the dynamic program.

**Corollary.** Under the stated fixed-parameter input class, this algorithm is
an FPTAS for maximizing `I(S)`. More precisely, when the certified local
precision bound is `delta<1`,

```text
I(S_hat) >= (1-delta)/(1+delta) max_(|S|=k) I(S).
```

With the above choice of `L`, this is at least `(1-epsilon)` times optimum.
When the optimum is positive,

```text
log I(S_star)-log I(S_hat)
 <= log[(1+delta)/(1-delta)].
```

**Proof.** The uniform theorem and positivity of the trace functional give

```text
(1-delta) I(S) <= I_L(S) <= (1+delta) I(S)
```

for every feasible `S`. Adding the nonnegative common prior preserves these
inequalities. If `S_star` maximizes the true objective, exact dynamic
programming gives

```text
I(S_hat) >= I_L(S_hat)/(1+delta)
         >= I_L(S_star)/(1+delta)
         >= [(1-delta)/(1+delta)] I(S_star).
```

For `delta<=epsilon/2`, the ratio is at least `1-epsilon`. The full-history
case has `delta=0` directly, even if the geometric upper bound at `n-1`
exceeds `eta`. A zero optimum causes no division in this proof. The log
claim follows only when the optimum is positive. QED.

The slightly less conservative choice `eta=epsilon/(2-epsilon)` gives the
same requested ratio. The stronger reviewed gain and conditional-variance
constants can reduce `L` in implementations; they are unnecessary for the
complexity result.

## 3. Arithmetic and bit complexity

Define `a0=log(2)/log(1/rho0)`. Before the full-history cap,

```text
L = max(0, ceil[log(C0/eta)/log(1/rho0)]-1),
2^L <= max(1,(C0/eta)^a0).
```

The graph has `O(n k 2^L)` states and arcs. Precomputing local conditionals by
ordinary rational linear algebra takes `n 2^L poly(L,p)` arithmetic
operations; the dynamic program takes `O(n k 2^L)` exact additions and
comparisons. A convenient overall bound is

```text
n (k+poly(L,p)) 2^L * poly(input bit length,n,L,p)
```

bit operations, with a deliberately unspecified polynomial for robust exact
linear algebra. All exponents other than `a0` are universal constants.

To justify that last factor, let `s` be the total rational input encoding
length. Calendar covariance entries are sums of products of input rationals,
and have bit length polynomial in `n,s`. Every local inverse has dimension
at most `L`; determinant bounds, or fraction-free elimination, bound its
rational entries by `poly(n,s,L)` bits. Local weights therefore have
polynomial bit length. A dynamic-programming value is the sum of at most `n`
such weights along one path, so its numerator and denominator also have
polynomial bit length. Exact comparison of competing path values is thus
polynomial. This argument does not assume fixed-precision arithmetic,
well-scaled sensitivities, or a lower bound on a nonzero sensitivity.

Because `rho0` and `B0` define fixed input-class bounds, `2^L` is polynomial
in `1/epsilon`. This establishes polynomial dependence on input length and
accuracy. The full-history cap cannot increase the stated graph-size bound.

The correlation exponent illustrates the limitation:

| `rho0` | exponent `a0` of `1/epsilon` |
|---:|---:|
| 0.2 | 0.431 |
| 0.4 | 0.756 |
| 0.6 | 1.357 |
| 0.8 | 3.106 |
| 0.9 | 6.579 |
| 0.95 | 13.513 |

These numbers describe the mask factor only; polynomial factors in `L`,
input size, and the constant `C0` still matter. As `rho0` approaches one,
`a0` grows like `log(2)/(1-rho0)`. If the correlation bound may approach one
arbitrarily with the input, this is not a uniform FPTAS. If `B0` is replaced
by an unbounded input ratio, the mask bound is polynomial in that ratio at
fixed `rho0`, but can be exponential in its binary encoding length. A
polynomially bounded ratio would suffice for a suitable promised input class;
an arbitrary binary-encoded ratio does not.

An arbitrary collection of installation or budget constraints is not covered
by the count-only dynamic program. The theorem also does not imply an
FPTAS for multi-parameter log determinant: maximizing that concave function
over the information hull can have a fractional relaxation gap.

## 4. Closest primary prior: Das and Kempe, STOC 2008

Source: [author PDF](https://david-kempe.com/publications/regression.pdf),
*Algorithms for Subset Selection in Linear Regression*, DOI
[10.1145/1374376.1374384](https://doi.org/10.1145/1374376.1374384).
Inspected §§2–4 and §7, especially Theorem 4.1, Corollary 4.2, and Lemma 7.1.
Their objective `b_S^T C_SS^(-1)b_S` is the same scalar quadratic form.
It is written as normalized regression variance reduction rather than mean
Fisher information. This change of statistical interpretation is not a new
optimization problem. Any positive-definite `R` and vector `f` can be embedded
in a valid joint observation/target covariance by choosing target variance
greater than `f^T R^(-1)f` and cross covariance `f`; normalizing only multiplies
the objective by a schedule-independent positive constant.

Section 7 gives `O(n^2 k)` exact dynamic programming when the observation
covariance has entries `a^|y_i-y_j|`, including diagonal one. Its proof uses
the tridiagonal inverse of every selected covariance. This already includes
nonsingular positive-transition noiseless scalar Markov errors after normalization.

For stationary AR errors with positive nugget, normalized off-diagonal
entries are `alpha rho^h`, where `alpha=P/(P+r)` lies strictly between zero
and one. For three consecutive candidates,

```text
C_13 = alpha rho^2 != alpha^2 rho^2 = C_12 C_23.
```

Thus this covariance is not in the paper's exact exponential-line subclass.
The fact that off-diagonal entries still decay exponentially is insufficient.
A generic covariance tree result also differs from a latent Markov precision
tree: marginal observed covariances remain dense.

Theorem 4.1 gives an FPTAS for fixed covariance bandwidth `beta` and
polynomially bounded condition number `kappa`. Its displayed runtime is

```text
O(n (k/epsilon)^(beta^2) beta^(2 beta^2) kappa^(2 beta^2)
     [1+2 log(1/rho_min)]^beta),
```

where `rho_min` is the smallest nonzero observation/target correlation.
Corollary 4.2 allows deleting covariance entries of size at most `tau`, with
`tau<=1/(4 kappa k)` and approximation factor

```text
[1-(8/3) kappa^2 k tau] (1-epsilon).
```

For fixed positive stationary AR correlation and fixed positive nugget,
`kappa` is uniformly bounded: eigenvalue bounds give
`kappa<=1+(P/r)(1+rho)/(1-rho)`. Achieving relative error of order `epsilon`
through that corollary still uses `tau=O(epsilon/k)`. Truncating the tail
`alpha rho^h` then requires `beta=Theta(log(k/epsilon))` in the nontrivial
large-instance regime. Substitution in the displayed runtime gives a
quasi-polynomial bound, not a polynomial bound in `k,1/epsilon`.
This is a consequence of that explicit construction; it is not a proof that
no improved implementation or other prior result can give an FPTAS.

The possible improvement here is therefore narrow but concrete: for a fixed
contraction and noise-ratio class, a relative error bound independent of
cardinality permits a history mask of length `O(log(1/epsilon))`, and the
surrogate scalar objective is exactly additive on that mask graph. It avoids
the continuous boundary-state discretization of the fixed-bandwidth method.

## 5. Other directly checked and adjacent prior

[Mahalanabis and Štefankovič (2012)](https://arxiv.org/pdf/1209.5991),
*Subset Selection for Gaussian Markov Random Fields*, §3.2 Theorem 43,
is the strongest algorithmic priority threat found. It approximates total
posterior variance on bounded-treewidth precision graphs, with runtime
polynomial in the matrix condition number. The
[separate reduction](research-20260912-scalar-gmrf-prior-reduction.md)
details why its matrix-order proof appears to permit zero node weights and
forbidden observations, and why scalar noisy Markov design can be normalized
and regularized into a well-conditioned model of treewidth at most three.
This is a proof-based implication, not a claim that the paper literally
states our scalar theorem. It presently prevents a first-FPTAS claim.

[Qian, Yu, and Zhou (NeurIPS 2015)](https://papers.nips.cc/paper/2015/file/b4d168b48157c623fbd095b4a565b5bb-Paper.pdf),
*Subset Selection by Pareto Optimization*, §4.2 Definition 4/Theorem 2,
gives an exact expected-polynomial algorithm for the same noiseless
exponential-line covariance subclass. Its proof cites the Das–Kempe
recurrence. The paper's ridge-regression experiment does not extend that
exactness theorem to covariance plus a positive diagonal nugget.

[Del Pia, Dey, and Weismantel (2020)](https://optimization-online.org/wp-content/uploads/2018/10/6842.pdf),
*Subset Selection in Sparse Matrices*, Theorem 1 in the final author
manuscript dated 2020-02-03, gives exact polynomial algorithms for a
block-diagonal data matrix with a fixed number of columns in each block and
a fixed number of additional columns. This concerns data-matrix sparsity;
the dense Gram matrices generated by a latent AR chain are not directly in
that class. The earlier author-hosted 2018 draft has different numbering.

[Levine and How (NeurIPS 2013)](https://proceedings.neurips.cc/paper_files/paper/2013/file/8a1e808b55fde9455cb3d8857ed88389-Paper.pdf),
*Sensor Selection in High-Dimensional Gaussian Trees with Nuisances*, §§5–7,
uses local Gaussian messages to accelerate focused-information greedy
selection. Proposition 7 gives an online bound through a larger latent
target set. It does not state an FPTAS for focused selection. Its explicit
distinction between target variables and nuisance variables is relevant to
the reduction above.

[Radovilsky and Shimony (UAI 2008)](https://raw.githubusercontent.com/mlresearch/r6/main/assets/radovilsky08a/radovilsky08a.pdf),
*Observation Subset Selection as Local Compilation of Performance
Profiles*, §4.2 Theorem 4, gives a polynomial approximation for a truncated
log-precision utility on a noisy Gaussian out-tree model, allowing designated
target variables. Its state discretization is additional strong prior for
noisy latent-tree observation optimization. A general sensitivity vector in
our model creates a global parameter connected across the latent chain, so
the augmented graph is not generally an out-tree.

[Krause and Guestrin (JAIR 2009)](https://arxiv.org/pdf/1401.3474),
*Optimal Value of Information in Graphical Models*, Theorem 1 and §8.2,
gives exact observed-chain dynamic programming and explicitly identifies
Radovilsky, Shattah, and Shimony's 2006 noisy-emission extension. The latter,
DOI 10.1109/ICSMC.2006.385249, was identified through its primary institutional
abstract but has not yet been retrieved and read in this audit; it was sent
to the literature agent for retrieval or a missing-source entry.

The earlier [localized-factor priority audit](research-20260912-noisy-markov-fsai-priority-audit.md)
records strong prior for inverse-factor decay and local conditional
approximations. The present optimization corollary must credit those ideas
as well as dynamic programming. Previously inspected Kalman scheduling
papers optimize state-estimation covariance and give pruning or approximation
bounds; a fixed-parameter mean-information FPTAS was not identified in the
inspected results. This bounded audit does not establish that one is absent.

## 6. Search record and remaining novelty risks

Search date: 2026-09-12. Searches used primary full texts where a relevant
result was identified. Representative query families were:

- `"sensor selection" "FPTAS" correlated`,
  `"sensor scheduling" "fully polynomial" approximation`;
- `"Fisher information" "FPTAS" selection`,
  `"correlated" "optimal design" "approximation scheme"`;
- `"Algorithms for subset selection in linear regression" FPTAS bandwidth`;
- `"subset selection" "exponential" "nugget" approximation`,
  `"subset selection" "exponential decay" approximation nugget`;
- `"FPTAS" "Kalman"`, `"FPTAS" "ridge regression"`;
- `"Gaussian" "FPTAS" "selection"`,
  `"subset selection" "treewidth" covariance`.

The follow-up queries included `Gaussian value information subset selection
bounded treewidth approximation Krause Guestrin`, `"sensor selection"
"treewidth"`, `"subset selection" "banded precision"`, and
`"Gaussian Free Fields" "FPTAS"`. They found the stronger 2012 result above.
All directly relevant identified works were submitted to the sole literature
maintenance agent for sequential inclusion, with primary full texts where
available. The 2006 noisy-emission paper remains unread pending retrieval.

The present status is a correct specialized algorithmic corollary whose
existence guarantee is likely already implied by prior methods. A useful
next comparison is the dependence on horizon, accuracy, and correlation in
the explicit mask algorithm versus covariance-message discretization.
Neither a new approximation formula nor a new hull theorem is claimed.

Dense physical-grid refinement creates a separate limit: with
`rho_n=exp(-lambda Delta_n)` and `Delta_n` decreasing to zero, the fixed
contraction class is violated. A fixed physical minimum sampling separation
may control the number of selected observations in a fixed physical history
window, but it changes the state count and requires a separate spacing
argument. No FPTAS uniform in grid refinement is asserted here.
