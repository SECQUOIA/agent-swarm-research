# Finite-history design bounds for partial observations of a latent process

Date: 2026-09-12. Status: the original bound below passed
[fresh independent review](research-20260912-partial-observation-independent-review.md).
The normalized refinement and its intrinsic covariance promises also passed
the review addendum, including exact coordinate-change checks.
This extends the measurement model used by the earlier
[full-state result](research-20260912-noisy-markov-memory.md). It uses classical
Kalman covariance identities; no new filtering identity or publication priority
is claimed. The potential contribution is a useful explicit error bound and its
consequence for discrete measurement design.

At each time, selecting a measurement acquires a fixed observation packet.
The packet may observe only part of a larger latent state. Its channels are
acquired together. The observation matrix is fixed before optimization; selecting
arbitrary individual channels within a packet is a different problem.

## Model and promises

For centered errors, let

```text
X_t = A_t X_(t-1)+w_t,
Y_t = H_t X_t+v_t.
```

The initial state, process errors and measurement errors are independent
Gaussian vectors. Their covariances are known and independent of the mean
parameters. The latent dimension and packet dimensions may be part of the input.
Write `P_t=Cov(X_t)`, `Q_t=Cov(w_t)`, and `V_t=Cov(v_t)`. Suppose

```text
P_t <= Pbar I,       Q_t >= q I   (t>=2),
V_t >= r I,         ||H_t||_2 <= hbar,
Pbar>0, 0<q<=Pbar, r>0.
```

The initial covariance may be singular. There is no lower bound on it and no
separate Euclidean norm bound on `A_t`. These conditions concern the supplied
finite horizon. In particular, the process-noise lower bound is a substantive
assumption; the earlier full-state theorem allows zero process noise.

Put `gamma=sqrt(1-q/Pbar)`, `C=hbar^2 Pbar`, and
`B=hbar sqrt(Pbar/r)`. The nontrivial case is `0<gamma<1` and `hbar>0`.

For a selected set `S`, use exactly the preceding selected observations within
`L` calendar positions to predict `Y_t`. Denote this history by `Hcal_t` to
distinguish it from the observation matrix. Let `Z_t` be the true local
regression residual, `D_t=Cov(Z_t)`, and `beta_(t,j)` its regression blocks.
These are fresh local conditionals, not truncated full-history coefficients.

## A covariance contraction that tolerates partial observation

Consider any fresh filter and any pattern of selected updates. Its prediction
and posterior covariances satisfy `P_t^-<=P_t<=Pbar I` and
`P_t^+<=P_t^-`. At an unobserved time, set the update matrix to identity and
the posterior equal to the prediction covariance. At an observed time write

```text
K_t = P_t^- H_t^T (H_t P_t^- H_t^T+V_t)^(-1),
E_t = I-K_t H_t,
P_t^+ = E_t P_t^- E_t^T+K_t V_t K_t^T.
```

Each transition obeys

```text
A_t P_(t-1)^+ A_t^T = P_t^- - Q_t
                    <= (1-q/Pbar) P_t^- = gamma^2 P_t^-.
```

Multiplying this inequality by update matrices and using
`E_t P_t^- E_t^T<=P_t^+` telescopes. If `T_(t,j)` propagates a state error
just after the update at `j` to the prediction at `t`, including intermediate
updates but no update at `t`, then

```text
T_(t,j) P_j^+ T_(t,j)^T <= gamma^(2(t-j)) P_t^-.
```

The same statement holds when starting at an unconditioned time with covariance
`P_j`. This proof uses only positive semidefinite inequalities, so it needs no
inverse of an initial or posterior state covariance.

Since `K_j V_j K_j^T<=P_j^+` and `V_j>=r I`, the coefficient by which
an observation at `j` influences the predicted packet at `t` satisfies

```text
beta_(t,j) = H_t T_(t,j) K_j,
||beta_(t,j)||_2 <= B gamma^(t-j).
```

This is the step that permits a partial observation matrix: it avoids assuming
that `I-K_j H_j` is a Euclidean contraction.

## Residual-pair bounds

If `j<t-L`, every update in the fresh history of `t` is later than `j`.
Start that filter at unconditional covariance `P_j`. Independence of later
process and observation errors gives

```text
Cov(Z_t,Y_j) = H_t T_(t,j) P_j H_j^T,
||Cov(Z_t,Y_j)||_2 <= C gamma^(t-j).
```

For a far selected pair `s<t` with `t-s>L`, write
`U=Cov(X_s,Z_s)=P_s^-(Hcal_s) H_s^T`. The two local histories need not be
equal. Nevertheless, conditional covariance monotonicity yields

```text
U U^T <= hbar^2 Pbar P_s^-(Hcal_s) <= hbar^2 Pbar P_s.
```

The `t`-local filter can start from unconditional `P_s`, because all its
updates are strictly later than `s`. Propagating `U` with the same contraction
therefore gives the direct bound

```text
||Cov(Z_t,Z_s)||_2 <= C gamma^(t-s),       t-s>L.
```

For a near pair, `h=t-s<=L`, regression orthogonality removes `Y_s` and
every observation shared with the `t`-local history. Only `j` in the
`s`-local history with `j<t-L` remains. With `d=s-j`,

```text
||Cov(Z_t,Z_s)||_2
 <= C B gamma^h sum_(d=L+1-h)^L gamma^(2d),       1<=h<=L.
```

These estimates are uniform over all selected sets and do not multiply by
either the latent dimension or the packet dimension.

## Spectral bound and design consequence

Every `D_t>=r I`. A block row-sum bound on the normalized residual covariance
therefore gives

```text
|| D^(-1/2) Cov(Z_S) D^(-1/2)-I ||_2 <= delta_L,

delta_L = (2C/r) [ gamma^(L+1)/(1-gamma)
                  + B gamma^(L+2)(1-gamma^L)(1-gamma^(L+1))
                    / ((1-gamma)(1-gamma^2)) ].
```

The finite near sum uses the independently checked geometric identity in the
[pair-refinement review](research-20260912-pair-refinements-independent-review.md).
For a complete-history window `L>=n-1`, use the exact bound zero. If `hbar=0`,
the observations are independent. If `q=Pbar`, each transition carries zero
unconditional covariance from the past, so the observations are also independent
and the error bound is zero. An empty selection is exact.

When `delta_L<1`, congruence and inversion give the same relative precision
and Fisher-information sandwiches as the earlier theorem. For rational mean
sensitivities, a positive semidefinite fixed trace weight, and a nonnegative
fixed prior, one exact count-and-history dynamic program maximizes the local
weighted-trace information. Its chosen schedule achieves at least
`(1-delta_L)/(1+delta_L)` of the true optimum.

Consequently, if `q/Pbar` is bounded below by a fixed positive constant and
`hbar^2 Pbar/r` is bounded above by a fixed constant, choosing
`L=O(log(1/epsilon))` gives an FPTAS for the weighted-trace objective with
an exact cardinality constraint. Latent, packet and parameter dimensions enter
polynomial matrix computations, and do not enter the history-state exponent.
One may choose fixed rational upper bounds on `gamma` and `B` when evaluating
the accuracy bound. Covariances and local conditionals are computed directly
with rational arithmetic; no irrational whitening is required.

For example, an isotropic stationary latent process with `P_t=I` and
`Q_t=I-A_t A_t^T`, `||A_t||<=rho<1`, permits `q=1-rho^2` and hence
`gamma=rho`, even with changing fixed partial observation matrices. This
preserves the original correlation rate. It is potentially more useful than
the conservative rate from a general covariance-decay theorem. No application
comparison or exact certificate using this new bound has yet been produced.

Prior-art assessment remains necessary before treating this as a
new research result. In particular, finite-memory filtering and Riccati
contraction are established subjects. The proposed statement concerns a uniform
measurement-design guarantee built from those identities.

## A sharper bound from normalized residuals

The preceding proof can retain the signal-to-noise contraction at both ends
of each covariance transport. This yields a stronger bound and more general,
coordinate-invariant assumptions. This section passed the independent
review addendum; the earlier statement and its artifacts remain available separately.

Fix `0<=gamma<1` and `s>=0`. It suffices to assume

```text
V_t > 0,
Q_t >= (1-gamma^2) P_t,             t>=2,
H_t P_t H_t^T <= s V_t,            every t.
```

Here `P_t` is still the unconditional state covariance. No separate bound on
its Euclidean norm, the observation matrix, or the smallest eigenvalue of
`V_t` is needed. The process inequality says that new process noise supplies
a fixed fraction of each marginal state covariance. The observation inequality
bounds the signal covariance relative to measurement noise. The earlier
Euclidean assumptions imply these promises with
`gamma^2=1-q/Pbar` and `s=hbar^2 Pbar/r`.

Put `kappa=s/(1+s)`. For any fresh prediction covariance `P<=P_t`, define
`D=H_t P H_t^T+V_t` and the Kalman gain `K`. Then

```text
|| D^(-1/2) H_t P^(1/2) ||_2 <= sqrt(kappa),
K V_t K^T <= kappa Ppost.
```

Both statements hold for singular `P`. To see the second, put
`M=P^(1/2) H_t^T V_t^(-1) H_t P^(1/2)<=s I` and use

```text
Ppost = P^(1/2)(I+M)^(-1)P^(1/2),
K V_t K^T = P^(1/2) M(I+M)^(-2) P^(1/2).
```

The scalar inequality `a/(1+a)<=kappa` for `0<=a<=s` proves the required
Loewner comparison. The covariance transport still contracts at rate `gamma`
because every fresh prediction is bounded above by unconditional `P_t`.

For a far pair, normalization at the earlier residual gives
`U D_s^(-1) U^T<=kappa P_s`. Normalization at the later residual supplies
another square-root factor. For the near-pair expansion, use the measurement
noise covariance at each surviving old observation between the two factors.
The resulting bounds are

```text
||D_t^(-1/2) Cov(Z_t,Z_s) D_s^(-1/2)||_2
  <= kappa gamma^(t-s),                                      t-s>L,

||D_t^(-1/2) Cov(Z_t,Y_j) V_j^(-1/2)||_2
  <= sqrt(kappa*s) gamma^(t-j),                              j<t-L,

||D_s^(-1/2) beta_(s,j) V_j^(1/2)||_2
  <= kappa gamma^(s-j),                                     j in Hcal_s.
```

Thus the uniform normalized residual error has the stronger upper bound

```text
delta_normalized = 2 kappa [ gamma^(L+1)/(1-gamma)
                  + sqrt(kappa*s)
                    * gamma^(L+2)(1-gamma^L)(1-gamma^(L+1))
                    / ((1-gamma)(1-gamma^2)) ].
```

Use zero at complete history, `gamma=0`, or `s=0`. This is a relative
precision bound for genuine local conditionals under the intrinsic promises.
With fixed `gamma,s`, the same exact-rational dynamic program gives the
weighted-trace FPTAS. Both promises can be checked as rational positive
semidefinite inequalities when the model and constants are rational. Fixed
rational upper bounds may replace the square roots in the accuracy calculation.
The statement continues to require acquisition of whole fixed packets.

At `s=1`, the original bound has prefactor two and near coefficient one.
The normalized bound has prefactor one and near coefficient `1/sqrt(2)`.
This improvement concerns the guarantee. A separate exact trace-certificate
implementation is undergoing review for the two-mode drift application.

## Initial primary-source comparison

[Kozdoba, Marecek, Tchrakian and Mannor (2019)](https://arxiv.org/abs/1809.05870)
is direct contraction and finite-memory prior. Its Theorem 1 contracts the
limiting filter in its covariance norm using a positive process-noise
contribution. Theorem 2 and Lemma 3 approximate forecasts of an observable,
time-invariant system by finitely many recent scalar observations. The inspected
proof uses convergence of the filter coefficients and a covariance-norm
equivalence constant. Our telescoping calculation makes the same established
noise-dissipation mechanism explicit for each finite, time-varying local
history, using the stated unconditional covariance bound. The objective here is
uniform selected-covariance information, whereas that paper studies prediction
and online regret. This distinction identifies the present task; it does not
prove the design corollary is new.

[Bougerol (1993)](https://doi.org/10.1137/0331041), Theorem 1.7 and Section 2.3,
provides earlier contraction and exponential-stability theory for Kalman
filtering, including random coefficient systems. The matrix metric and
observability/controllability hypotheses differ from the direct covariance
inequalities above. This is additional evidence that contraction itself is
established prior, and must be credited in any later presentation.
