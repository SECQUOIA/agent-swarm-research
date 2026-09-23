# Independent review of the partial-observation memory bound

Date: 2026-09-12. Reviewer: `/root/noisy_markov_review`.

**Verdict: the stated bound is correct under the stated assumptions.** The
proof permits singular initial covariance, partial observation matrices,
changing packet sizes, and Euclidean transition or update norms above one.
The process-noise lower bound must hold at every calendar transition,
including times at which no packet is selected. Selection acquires a whole
fixed packet. This review establishes correctness, not publication priority.

The reviewed draft is
[the partial-observation bound](research-20260912-partial-observation-memory-bound.md).
I derived its transport and residual-pair estimates independently before
reading the completed draft. The accompanying checks use dense covariance
conditionals and a separately computed Kalman recursion; they do not import
the author implementation or previous review implementations.

## 1. Covariance transport and the regression coefficients

Use the author's constants

```text
gamma^2 = 1-q/Pbar,
C = hbar^2 Pbar,
B = hbar sqrt(Pbar/r).
```

For one fixed local history, let `Sigma_t^-` and `Sigma_t^+` denote its
prediction and posterior state covariances. Conditioning gives
`Sigma_t^- <= P_t <= Pbar I`, irrespective of the observation pattern. At
an unobserved time the update is the identity and the two covariances agree.
At an observed time the Joseph covariance identity gives both

```text
E_t Sigma_t^- E_t^T <= Sigma_t^+,
K_t V_t K_t^T <= Sigma_t^+,
```

where `E_t=I-K_t H_t`. There is no assertion that `E_t` contracts the
Euclidean norm.

At the next transition,

```text
A_(t+1) Sigma_t^+ A_(t+1)^T
 = Sigma_(t+1)^- - Q_(t+1)
 <= gamma^2 Sigma_(t+1)^-.
```

The last inequality follows because
`Q_(t+1) >= q I >= (q/Pbar) Sigma_(t+1)^-`. Congruence preserves each
inequality, so induction yields

```text
T_(t,j) Sigma_j^+ T_(t,j)^T
 <= gamma^(2(t-j)) Sigma_t^-.
```

Here the ordered product is

```text
T_(t,j) = A_t E_(t-1) A_(t-1) ... E_(j+1) A_(j+1).
```

It starts after the update at `j`, contains exactly `t-j` transitions,
and ends before an update at `t`. Missing updates contribute identity
matrices. All these inequalities remain valid for singular state
covariances: the only inverse used in forming a Kalman gain is the positive
definite observation innovation covariance.

The coefficient of observation `Y_j` in the local prediction of `Y_t` is
exactly `beta_(t,j)=H_t T_(t,j) K_j`. Since
`r K_j K_j^T <= K_j V_j K_j^T <= Sigma_j^+`,

```text
beta_(t,j) beta_(t,j)^T
 <= (gamma^(2(t-j))/r) H_t Sigma_t^- H_t^T
 <= B^2 gamma^(2(t-j)) I.
```

This verifies the coefficient bound and its endpoints without changing the
order of noncommuting matrices.

## 2. Excluded observations and the two different local filters

If `j<t-L`, every observation used by the `t`-local filter occurs strictly
after `j`. It is therefore legitimate to initialize that filter at time
`j` with unconditional covariance `P_j` and no update at `j`. This statement
does not replace a conditional covariance by an unconditional covariance
inside a filter that already used earlier observations.

Later process and measurement errors are independent of `Y_j`. Cross
covariance thus follows the same transition and update product:

```text
Cov(Z_t,Y_j) = H_t T_(t,j) P_j H_j^T.
```

For `U_j=P_j H_j^T`,

```text
U_j U_j^T <= hbar^2 P_j^2 <= hbar^2 Pbar P_j.
```

Applying the transport inequality and then `Sigma_t^- <= Pbar I` gives
`||Cov(Z_t,Y_j)||_2 <= C gamma^(t-j)`.

For a far selected pair `s<t`, `t-s>L`, the earlier residual comes from a
different local filter. Orthogonality of its regression nevertheless gives

```text
Cov(X_s,Z_s) = Sigma_s^-(history at s) H_s^T = U.
```

The needed comparison is

```text
U U^T <= hbar^2 Pbar Sigma_s^-(history at s)
      <= hbar^2 Pbar P_s.
```

All updates of the `t`-local filter occur after `s`, so that filter can
again start with unconditional `P_s`. Future process and observation
errors are independent of `Z_s`. Consequently,

```text
Cov(Z_t,Z_s) = H_t T_(t,s) U,
||Cov(Z_t,Z_s)||_2 <= C gamma^(t-s).
```

No identity between the two local filters is required. This is the key
point that avoids an unnecessary extra history term for far pairs.

## 3. Overlap, both row sums, and the relative precision bound

For a near pair with `h=t-s<=L`, the selected time `s` belongs to the
`t`-local history. Expanding the other residual in its own history gives

```text
Cov(Z_t,Z_s)
 = -sum_(j in history at s, j<t-L) Cov(Z_t,Y_j) beta_(s,j)^T.
```

The term involving `Y_s` and every shared-history term are zero by local
regression orthogonality. Writing `d=s-j`, a surviving term satisfies
`L+1-h <= d <= L`, and its norm is at most
`C B gamma^(h+2d)`. This confirms the proposed near-pair estimate, including
the transpose and the strict endpoint `j<t-L`. Overlapping windows need
not produce uncorrelated residuals.

Let `D_t=Cov(Z_t)`. The observation noise at `t` is independent of its
history, so `D_t>=V_t>=r I`. Normalizing a residual covariance block
therefore multiplies its norm by at most `1/r`. There is at most one
calendar time at each positive lag on either side of a given time. Using
the same majorant on each side yields the factor two. The finite sum is

```text
sum_(h=1)^L sum_(d=L+1-h)^L gamma^(h+2d)
 = gamma^(L+2)(1-gamma^L)(1-gamma^(L+1))
   / [(1-gamma)(1-gamma^2)].
```

It follows that the author's displayed `delta_L` bounds every block row
sum. This also works for unequal packet sizes: the symmetric comparison
matrix whose entries are block operator norms bounds the full operator
norm by Cauchy--Schwarz on block norms. No dimension factor appears.

For clarity, the passage to relative precision can be shown without
guessing the direction of an inverse inequality. Let `Acal` be the unit
lower triangular residual map and let `R` be the selected true covariance.
Then

```text
M = D^(-1/2) Acal R^(1/2),
M M^T = normalized residual covariance,
M^T M = R^(1/2) Q_local R^(1/2).
```

The two matrices have the same eigenvalues. Thus, for `delta_L<1`,

```text
(1-delta_L) R^(-1) <= Q_local <= (1+delta_L) R^(-1).
```

The previously reviewed Fisher-information and positive semidefinite
weighted-trace conclusions follow by congruence and positive linear
functionals. An additive nonnegative prior preserves the relative bound.

## 4. Degenerate cases and the algorithmic consequence

The following cases need no limiting interpretation of the formula.

- If `hbar=0`, all observations consist only of independent noise.
- If `q=Pbar`, each transition satisfies `A_t P_(t-1) A_t^T=0` and
  `Q_t=P_t=Pbar I`. The state carries no random component of the past,
  even if `A_t` is nonzero on a nullspace of the initial covariance.
  Observation packets at different times are independent.
- If `L>=n-1`, the selected residuals are the exact sequential innovations.
- An empty selection has no approximation error.

For `0<gamma<1`, a useful monotone envelope is

```text
delta_L <= K gamma^(L+1),
K = (2C/[r(1-gamma)]) [1+B gamma/(1-gamma^2)].
```

Since `B=sqrt(C/r)`, fixed bounds on `gamma<1` and `C/r` fix `K`.
Choosing `delta_L<=epsilon/2` yields an approximation ratio at least
`1-epsilon`. One may use fixed rational upper bounds on `gamma`, `B`,
and `C/r` in this envelope to choose the window entirely with rational
comparisons. The precision bound need not be evaluated through an
irrational matrix square root.

The existing count-and-history dynamic program uses one selection bit per
calendar packet. Its state count is `O(n(k+1)2^L)`, and `2^L` is polynomial
in `1/epsilon` for the stated fixed input class. The latent dimension,
packet dimensions, and mean-parameter dimension occur in rational matrix
computations of polynomial size; they do not enter this state exponent.
Direct covariance recursions and finite-dimensional rational inverses have
polynomial bit complexity in these sizes and the input encoding length.
Neither small state eigenvalues nor large Euclidean transition norms
invalidate that exact-arithmetic statement.

These observations verify the claimed weighted-trace FPTAS consequence.
They do not establish an FPTAS for general multiparameter log determinant,
nor allow arbitrary coordinate selection within a packet. They also do
not claim the algorithm is numerically efficient under every permitted
conditioning pattern.

## 5. Independent computational checks

The reproducible script is
[review_partial_latent_memory.py](../code/research_20260912/review_partial_latent_memory.py),
with results in
[partial-latent-memory-independent-validation.json](../code/research_20260912/partial-latent-memory-independent-validation.json).
Run it using the existing isolated environment:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_partial_latent_memory.py
```

The exact rational check uses a four-time, two-dimensional latent model
with singular initial covariance, changing scalar partial observations,
unequal measurement noise, and a transition of Euclidean norm two. It
checks all 15 nonempty selected subsets and all five windows: 75 models,
80 regression coefficients, 40 excluded-observation covariances, and 120
residual pairs. Squared pair and coefficient inequalities are rational,
so these comparisons use exact SymPy arithmetic.

The numerical suite uses 24 noncommuting models with latent dimensions
two, three, and five, six calendar times, changing packet sizes, zero or
rank-deficient observation matrices, singular or anisotropic initial
covariances, and multiple process-noise floors. It enumerates all 63
nonempty selections and seven windows for each model. Its 10,584 models
check the separate filter transport, dense local regression coefficients,
excluded covariance bounds, the exact far-pair transport identity,
near-pair bounds, block row sums, normalized residual spectra, and the
relative precision sandwich. A separate `gamma=0` example retains a
nonzero transition acting only on the initial covariance's nullspace and
checks exact independence.

All checks passed. There were 3,024 models with `delta_L<1`, 26,880
regression-block checks, 13,440 excluded-observation checks, and 40,320
checks each of transport and residual pairs. The largest transition norm
was about 9.878, the largest update norm was 1.191, and the largest
transition/marginal commutator norm was 6.643. Thus the tested models
include both noncommuting matrices and operators that expand Euclidean
norms. The largest identity discrepancy was about `7.12e-15`, in the
comparison of innovation covariances from the two computations. No tested
bound had a positive excess. These floating-point checks supplement the
proof; they are not interval certificates or evidence of novelty.

## 6. Addendum: sharper normalization

The root researcher subsequently proposed a sharper bound. **This
refinement is also correct.** Write

```text
s = hbar^2 Pbar/r,
kappa = s/(1+s).
```

For any local prediction covariance `Pi`, observation matrix `H`, and
noise covariance `V`, let `D=H Pi H^T+V`. The hypotheses imply
`H Pi H^T<=sV`, hence

```text
D^(-1/2) H Pi H^T D^(-1/2) <= kappa I.
```

For example, `D<=(1+s)V` directly gives
`D^(-1/2)V D^(-1/2)>=I/(1+s)`, which proves this assertion by subtraction.
No assertion about an inverse of `Pi` is needed.

The sharper gain inequality also holds with singular `Pi`. Define

```text
M = Pi^(1/2) H^T V^(-1) H Pi^(1/2),       0<=M<=sI.
```

The exact identities

```text
Pi_post = Pi^(1/2) (I+M)^(-1) Pi^(1/2),
K V K^T = Pi^(1/2) M(I+M)^(-2) Pi^(1/2)
```

follow from the observation-space inverse identity. On each eigenspace
of `M`, `lambda/(1+lambda)<=kappa`. Congruence therefore gives
`K V K^T<=kappa Pi_post`. This is stronger than the Joseph inequality
used in the baseline proof, and is valid without an inverse or
pseudoinverse of a state covariance.

For a far pair, with `U=Pi_s^- H_s^T`, endpoint normalization gives

```text
U D_s^(-1) U^T <= kappa Pi_s^- <= kappa P_s.
```

Transport from unconditional `P_s`, followed by the normalized terminal
bound at `t`, thus supplies two factors of `sqrt(kappa)`:

```text
||D_t^(-1/2) Cov(Z_t,Z_s) D_s^(-1/2)||_2
 <= kappa gamma^(t-s),                 t-s>L.
```

For an excluded old observation `j`, use its measurement covariance
`V_j` to normalize the middle factor. The unconditional signal-to-noise
bound gives

```text
P_j H_j^T V_j^(-1) H_j P_j <= s P_j.
```

The same transport then gives

```text
||D_t^(-1/2) Cov(Z_t,Y_j) V_j^(-1/2)||_2
 <= sqrt(kappa s) gamma^(t-j).
```

For a coefficient of the `s`-local regression, the sharper gain bound
and terminal normalization give

```text
||D_s^(-1/2) beta_(s,j) V_j^(1/2)||_2
 <= kappa gamma^(s-j).
```

Multiplying these two inequalities is legitimate: the middle
`V_j^(-1/2)` and `V_j^(1/2)` cancel in the near-pair expansion, with the
second normalized expression transposed. Consequently,

```text
||D_t^(-1/2) Cov(Z_t,Z_s) D_s^(-1/2)||_2
 <= kappa sqrt(kappa s) gamma^h
    sum_(d=L+1-h)^L gamma^(2d),         1<=h=t-s<=L.
```

The sharper dimension-free bound is therefore

```text
delta_normalized = 2 kappa [ gamma^(L+1)/(1-gamma)
                    + sqrt(kappa s)
                      gamma^(L+2)(1-gamma^L)(1-gamma^(L+1))
                      / ((1-gamma)(1-gamma^2)) ].
```

It improves both coefficients of the baseline bound whenever `s>0`.
For `s=1`, the leading factor decreases from two to one, and the near
coefficient inside the brackets decreases from one to `1/sqrt(2)`.
The geometric rate remains `gamma`.

## 7. Addendum: intrinsic covariance assumptions

The reviewer observed, and the root researcher independently agreed,
that the normalized proof requires only the following assumptions:

```text
V_t > 0,
Q_t >= (1-gamma^2) P_t,          t>=2,
H_t P_t H_t^T <= s V_t,         all t,
0<=gamma<1, s>=0.
```

Here `P_t` remains the unconditional state covariance. These statements
may replace the separate Euclidean bounds in the baseline theorem.
Indeed,

```text
Q_t >= (1-gamma^2) P_t >= (1-gamma^2) Pi_t^-
```

proves exactly the same transport contraction, and
`H_t Pi_t^- H_t^T<=sV_t` proves every normalized endpoint and gain bound
above. The old-observation step uses the stated unconditional
signal-to-noise bound directly. The state covariance may be singular at
any time under these intrinsic assumptions, since the proof uses no
state-covariance inverse.

These assumptions are preserved by arbitrary invertible, time-dependent
changes of state coordinates `X'_t=M_t X_t` and packet coordinates
`Y'_t=N_t Y_t`. In particular,

```text
P'_t=M_t P_t M_t^T,  Q'_t=M_t Q_t M_t^T,
A'_t=M_t A_t M_(t-1)^(-1),
H'_t=N_t H_t M_t^(-1),  V'_t=N_t V_t N_t^T.
```

Both promises transform by congruence. A normalized residual changes
only by a block orthogonal map, because
`(D'_t)^(-1/2) N_t D_t^(1/2)` is orthogonal. Thus the normalized block
norms, relative precision spectra, and displayed bound are independent
of these coordinate choices. This invariance is stronger than merely
allowing large Euclidean transition norms.

For fixed rational class constants `gamma<1` and `s`, these promises
are exactly checkable through rational positive semidefinite tests.
The weighted-trace FPTAS argument carries over. If a completely rational
window bound is preferred, use
`sqrt(kappa s)=s/sqrt(1+s)<=s` in the monotone envelope. This supplies a
fixed rational constant multiplying `gamma^(L+1)`; it requires no
irrational computation. The trivial cases `gamma=0` or `s=0` give
independent packets, including when latent covariances are singular.

This establishes the intrinsic variant as a direct consequence of the
same proof. It does not establish that this formulation or its design
consequence is absent from prior work.

## 8. Addendum checks

The same independent script now also checks the stronger gain
inequality, both normalized factors in the near-pair proof, normalized
far and near pairs, and the sharper row and spectral bounds. The
24-model suite passes these checks. It includes 4,536 subset/window
models with the sharper bound below one. The largest positive numerical
excess is about `1.91e-17`, in the gain covariance inequality at a
singular boundary; all normalized pair, row, and spectral inequalities
have nonpositive excess. The exact rational suite also checks squared
normalized coefficient, old-covariance, and pair inequalities.

To check coordinate invariance without adding a large suite, the exact
four-time model additionally undergoes changing rational state and
packet coordinates. The state changes include `diag(100,1/100)`, a
nonorthogonal triangular matrix, and other unequal scalings; the packet
scalings are `2, 1/3, 5, 1/7`. The script reconstructs the transformed
joint covariance from the transformed transitions and innovations,
checks both intrinsic promises exactly, and compares all 75 transformed
local residual maps and residual covariances with their predicted
congruences. These identities establish invariance of all the scalar
normalized inequalities in that exact suite.
