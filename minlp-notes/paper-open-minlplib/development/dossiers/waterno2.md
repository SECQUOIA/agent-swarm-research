# Dossier: waterno2_06, _09, _12, _18, _24 (family key `waterno2`)

Prepared 2026-10-04 for the MPC paper. `R/` means `research-20260929/`.
Authoritative numbers come from `R/open-instances-summary.md`; every
disagreement found is flagged. This version supersedes the earlier draft of
the same date. It re-checks that draft against the sources and adds four new
checks:
- an exact GAMS ≡ OSIL comparison for all five instances;
- exact consistency of the exactly feasible points with every implied-bound
  file and every period bound;
- a deterministic replay of saved vbb2 runs;
- the binary64 residual signs.

Scripts and logs are in `paper-open-minlplib/development/dossiers/waterno2-checks/`
(`run_all.sh`, `replay_vbb2.sh`, `logs/`). Everything ran in scratch copies
under `/tmp` on at most 2 cores. Nothing under `R/` or `literature/` was edited
or executed in place, and no file there changed during this work.

## 0. Summary for the author

- **Result.** For all five instances we have rigorous dual bounds far above
  every MINLPLib-listed bound, and exactly feasible primal points. None is
  closed.

  | instance | best listed dual | our dual | primal (exactly feasible) | gap ≤ |
  |---|---|---|---|---|
  | waterno2_06 | 165.1902989 (SCIP) | 278.230573 | 282.888038 | 1.68% |
  | waterno2_09 | 273.8958303 (SCIP) | 824.834692 | 914.012 | 10.82% |
  | waterno2_12 | 479.5051427 (GUROBI) | 2089.754565 | 2233.821346 | 6.90% |
  | waterno2_18 | 770.7361733 (SCIP) | 4790.820715 | 5023.983 | 4.87% |
  | waterno2_24 | 1095.126488 (SCIP) | 6576.151388 | 6963.795181 | 5.90% |

  Gaps are (primal − dual)/dual, rounded up. Duals are truncated and primals
  rounded up.
- **Mechanism.** The model splits exactly into T hourly periods. They are
  coupled only by 3(T − 1) tank-level copy rows and one horizon row, and the
  horizon row is equivalent to a terminal-volume row.
  - 09–24: the bound is a period Lagrangian. Each of the T period values is
    bounded by rigorous spatial branch and bound (B&B).
  - 06: the tank-level separators are split into cells, and each cell has its
    own Lagrange slope vector. Every (entry cell, exit cell) pair of every
    period is bounded by rigorous B&B, and an exact shortest path combines
    the pair bounds.
- **Proof status.**
  - The combination steps are short theorems, proved in Section 3.
  - The period and pair bounds are computer-assisted. Each was established
    twice, by two separately written B&B codes: `rbb.py` in outward-rounded
    binary64, and `vbb.py`/`vbb2.py` with exact rational node bounds. Either
    code alone yields every claimed value.
  - Coverage, slope corrections, sums and the shortest path were recomputed
    in exact rational arithmetic by three implementations.
- **Critical examination (Section 8).** Nothing found invalidates a claimed
  bound or point.
  - Resolved here: the shared OSIL reader (W3); one coverage bound obtained
    by bound tightening, now proved by hand (W4); GAMS ≡ OSIL for 09–24, now
    exact (W8); consistency of the 09–24 period bounds with exactly feasible
    points (W12).
  - What remains is wording, plus one structural limitation (W1): the B&B
    trees are not stored. The pair and period bounds can be re-established
    only by re-running B&B, which is deterministic (replayed here bit for
    bit on 21 saved runs). The full replay costs tens of CPU-hours.

## 1. Instances and models

### 1.1 Source and physical meaning

- **MINLPLib.** Application "Water Network Operation", added 2014-08-12. The
  instance pages cite two sources:
  - "Huang, Wei, Operative Planning of Water Supply Networks by Mixed Integer
    Nonlinear Programming, Masters thesis, FU Berlin, 2011";
  - Gleixner, Held, Huang and Vigerske, NACO 2(4) (2012)
    [[gleixner2012-towards-globally-optimal-operation-of]].
- **The two cited sources.**
  - The FU Berlin catalog lists the 2011 work as a *Diplom* thesis
    [[huang2011-operative-planning-of-water-supply]]. Its text was not
    obtained.
  - The NACO paper treats stationary problems on two other networks.
- **Source network.** The network is the Tsinghua University network n9p3a11
  of Huang's 2019 TU Darmstadt dissertation (Section 5.5)
  [[huang2019-optimal-operation-of-water-supply]]: 1 reservoir, 3 tanks and
  9 variable-speed pumps.
  - The pump-power coefficients of the dissertation's Example 5.41
    (25.92674585, 18.13482123, 22.12766012, −42.68950769) occur exactly 2T
    times in each waterno2_T file. They are the station-B2 power
    coefficients in the table below.
  - Source: `R/publication/literature/network/report.md` §5.1 and its
    `checks/waterno2_huang_match.py`.
- **Physical layout** (derived from the rows):
  - source → station A (3 pumps) → tank 1 (area 1800) → stations B1 ∥ B2
    (2 pumps each) → tank 2 (area 720) → station D (2 pumps) → tank 3 (area
    1600) → demand;
  - the pumps of one station share one speed and one head;
  - a period is one hour (3600 s);
  - the objective is total pumping cost: each pump's cost is at least a
    cubic power polynomial divided by an hourly tariff factor;
  - the horizon row requires total station-A flow to be at least total
    demand.
- **Horizon.** waterno2_T is the first T hours. Huang's 1- and 2-period
  optima equal waterno2_01/02's. From 3 periods on, Huang's multi-period
  models differ from MINLPLib's: Huang's 3-period optimum is 215, while
  waterno2_03 has a listed feasible point of value 115.0045167.

### 1.2 Size, sense, bounds

| instance | variables (binary) | rows | per period: vars, binaries, rows | link rows | horizon row |
|---|---|---|---|---|---|
| waterno2_06 | 996 (54) | 1234 | 166, 9, 203 | 15 | 1 |
| waterno2_09 | 1494 (81) | 1852 | 166, 9, 203 | 24 | 1 |
| waterno2_12 | 1992 (108) | 2470 | 166, 9, 203 | 33 | 1 |
| waterno2_18 | 2988 (162) | 3706 | 166, 9, 203 | 51 | 1 |
| waterno2_24 | 3984 (216) | 4942 | 166, 9, 203 | 69 | 1 |

- All five are minimization problems.
- The OSIL objective is the sum of the 9T cost variables, with coefficient 1
  and no constant. The GAMS file defines `objvar` by row e1 instead.
- Every row is a polynomial of degree at most 3.
- All variables are bounded, except the monomial auxiliaries, which their
  defining rows bound.

### 1.3 The model in clean notation

Read from the OSIL rows; checked row by row against the period-0 dump
`R/open-instances-wave2/waterno2/logs/period0_dump.txt` for this dossier.

**Indices.**
- periods t = 0, …, T − 1;
- tanks k = 1, 2, 3, with areas A = (1800, 720, 1600) and w := A/3600 =
  (1/2, 1/5, 4/9);
- stations S ∈ {A, B1, B2, D}, with pumps p ∈ S (3, 2, 2 and 2 pumps).

**Period-t variables.**
- y_{t,p} ∈ {0,1}: pump on;
- q_{t,p} ≥ 0: pump flow;
- Q_{t,S} = Σ_{p∈S} q_{t,p}, and Q_{t,B} = Q_{t,B1} + Q_{t,B2};
- ω_{t,S}: station speed;
- η_{t,p}: pump head; H_{t,S}: station head;
- L_{t,k}, E_{t,k}: start and end levels;
- γ_{t,p} ≥ 0: cost;
- every monomial (q², q³, ω², ω³, qω, qω², q²ω, yω³, Q²) is an auxiliary
  variable with a defining equality row;
- redundant auxiliaries: per pump a "virtual flow" that equals q when the
  pump runs and the station minimum flow when it is off, and the slack x548.

```
(P_T)  min  Σ_t Σ_p γ_{t,p}
 s.t.  q^min_S y_{t,p} ≤ q_{t,p} ≤ q^max_S y_{t,p}
       ω^min_S ≤ ω_{t,S} ≤ ω^min_S + (1 − ω^min_S) y_{t,p_1(S)},  ω_{t,S} ≤ 1
       y_{t,p_1} ≥ y_{t,p_2} (≥ y_{t,p_3})                              (symmetry)
       η_{t,p} = a_S ω_{t,S}² + b_S q_{t,p} ω_{t,S} + c_S q_{t,p}²      (pump curve)
       −2000 (1 − y_{t,p}) ≤ η_{t,p} − H_{t,S} ≤ M_S (1 − y_{t,p})       (running pump: η = H)
       H_{t,A} = L_{t,1} + 11 + 5 Q_{t,A}²
       H_{t,B} = π_t + 4 Q_{t,B}² − L_{t,1} − 60,   π_t ≥ L_{t,2} + 90   (one head for B1 and B2)
       H_{t,D} = L_{t,3} − L_{t,2} + 13 + 5 Q_{t,D}²
       κ_t γ_{t,p} ≥ e_S y_{t,p} ω³ + f_S q ω² + g_S q² ω + h_S q³,   γ_{t,p} ≤ γ̄_{S,t}
       1800 (E_{t,1} − L_{t,1}) = 3600 (Q_{t,A} − Q_{t,B})
        720 (E_{t,2} − L_{t,2}) = 3600 (Q_{t,B} − Q_{t,D})
       1600 (E_{t,3} − L_{t,3}) = 3600 (Q_{t,D} − d_t)
       L_{t,·}, E_{t,·} ∈ [2,5] × [2.5,5] × [2,6],   L_{0,·} = σ := (3.5, 4.1, 4)
       L_{t+1,k} = E_{t,k}                     (link rows, t = 0..T−2)
       Σ_t h_t ≥ c_T,   h_t = Q_{t,A}          (horizon row; h_t is a copy variable)
```

**Station data** (exact OSIL decimals):

| S | (q^min, q^max) | ω^min | (a, b, c) head | (e, f, g, h) power | M_S |
|---|---|---|---|---|---|
| A | (0.2, 0.8) | 0.6 | (57.2814121, −37.5407324, −27.42831624) | (13.94696158, 24.46510819, −7.28623839, −23.57687014) | 1049 |
| B1 | (0.25, 0.5) | 0.8 | (76.45219958, −43.14087708, −50.37356589) | (29.29404529, −108.39408287, 442.21990639, −454.58448169) | 1065 |
| B2 | (0.4, 0.7) | 0.85 | (69.39622571, −58.31011875, 25.39911174) | (25.92674585, 18.13482123, 22.12766012, −42.68950769) | 1065 |
| D | (0.24, 0.58) | 0.7 | (34.92732674, 2.03724124, −63.61644904) | (17.4714791, −39.98407808, 134.55943082, −135.88441782) | 1095 |

Example rows for station D in period 0: pump curve e44, big-M rows
e564/e618, head row via e264/e282/e720/e721, speed row e468, symmetry row
e498, balance row e105.

**Data facts** (`logs/data_facts.log`, exact):
- Tariff κ_t:
  - waterno2_06: 0.309838295393634 in every period;
  - waterno2_09: two values, 0.309838295393634 and 0.132557606221724;
  - waterno2_12–24: three values, adding 0.0826068064704259.
- Demands of waterno2_06 in period order: d = (0.296666667, 0.294444444,
  0.283888889, 0.277222222, 0.293333333, 0.306944444). Over 09–24 the
  demands range from 0.277222222 to 0.733888889; they roughly double after
  hour 6.
- Horizon constant: c_T = Σ_t d_t exactly for every T (c_6 = 1.752499999).
- In waterno2_06 the periods differ only in the demand row. In 09–24 they
  also differ in the tariff of the 9 cost rows.

### 1.4 The structure that matters

1. **Exact period decomposition.** Removing the horizon row and the
   3(T − 1) link rows leaves exactly T components. Each is a period of 166
   variables, 9 binaries and 203 rows, and each cost variable lies in one
   period.
   - Shown by the authors' `wmodel.structure`.
   - Shown by a different recovery rule (first verifier, `vstruct.py`;
     T ∈ {1, 2, 3, 4, 6, 9, 12, 18, 24}).
   - Shown again by this dossier's own recovery (`point_consistency.py`): it
     orients the link rows by the sign of the area coefficient and orders the
     periods along the link chain.
   - waterno2_06: link rows e111–e125 (e111: −x243 + x244 = 0); horizon row
     e56: x188 + … + x193 ≥ 1.752499999.
2. **Heads depend on start levels.** Pump heads, and hence costs, depend on
   the period's start levels through H_{t,S}. Pumps are on/off with minimum
   flows. So a period's value function is nonconvex in its boundary levels.
   This causes the Lagrangian duality gap: linear prices cannot stop a period
   from ending at one level and the next from starting at another.
3. **The horizon row carries no real coupling.** Modulo the linear equality
   rows, it is a terminal-volume row on the last period (Lemma 2).
4. **Implied level bounds.** Tank 3 cannot drain faster than the demand.
   This gives start-level bounds at links 0–2 that periods 1–3 of the wave-2
   bound need: without them, 06 gives 262.701963972 instead of
   263.735099441. The only bounds that the cell cover needs have hand proofs
   (Lemma 5).

### 1.5 Provenance and semantics

- **GAMS ≡ OSIL, exactly, for all five instances (new).**
  `gms_vs_osil.py` parses the GAMS text and the OSIL XML separately. With
  every decimal read as a rational, it compares every row as a polynomial,
  every bound and type, and the objective after eliminating `objvar`.
  - Result: 0 differing rows and 0 differing variables for T = 6, 9, 12, 18
    and 24 (`logs/gms_vs_osil.log`).
  - GAMS files: `R/publication/minlplib-status/pages/models/gms/`, fetched
    2026-10-02; 06 is byte-identical to `R/open-instances-wave2/waterno2/data/`.
  - Negative controls: a 10⁻⁸ change in one coefficient and a change in one
    bound are both detected. The GAMS equation counts equal OSIL rows + 1
    (row e1).
  - This supersedes the earlier "6 random points at 60 digits" evidence
    for 09–24.
- **History.**
  - The MINLPLib.jl copy of 2017-11-23 agrees numerically with today's
    model, and statistics are equal from 2014-12-09 on
    (`R/publication/minlplib-status/`).
  - The cached OSIL files are sha256-identical to the files fetched on
    2026-10-02.
- **Semantics (must be stated in the paper).** Every decimal is the exact
  rational it denotes, and "feasible" means exactly feasible. This matters
  here:
  - At an off station, the speed is ω^min and its square and cube variables
    sit at their lower bounds (ω^min)² and (ω^min)³. These identities hold
    for decimals (0.7³ = 0.343).
  - In binary64 the square and cube residuals are negative for stations A
    (0.6), B2 (0.85) and D (0.7): for example fl(0.7)³ − fl(0.343) =
    −9.24·10⁻¹⁷. They are positive for B1 (0.8)
    (`logs/binary64_residuals.log`).
  - So under a binary64 reading of the data, every point with station A, B2
    or D off in some period is infeasible.
  - The exactly feasible points use these identities. Cube rows with both
    variables at lower bounds whose identity fails in binary64: 15, 18, 18,
    24 and 33 for 06, 09, 12, 18 and 24 (`logs/point_consistency.log`).
  - The same residual triggers SCIP's wrong answers (Section 7.4).
  - No claim is made for a binary64 reading.

## 2. Listed status (MINLPLib)

The pages were fetched 2026-09-29/30 (`R/bound-audit/pages.json`). The status
refresh of 2026-10-02 found them unchanged
(`R/publication/minlplib-status/`). None of the five is marked solved.

| instance | best listed dual (solver, date) | other listed duals | 3-solver listing dual | listed primal (point, added, page infeas.) |
|---|---|---|---|---|
| 06 | 165.1902989 (SCIP, 2025-07-31) | GUROBI 162.1927701, XPRESS 108.4043018, BARON 107.9508883, COUENNE 94.21252965, ANTIGONE 89.07175449, LINDO 34.03436054, SHOT 0 | 108.4043 | 282.8880374 (p4, 2025-07-31, 2e-12) |
| 09 | 273.8958303 (SCIP, 2025-07-31) | GUROBI 226.8256323, XPRESS 134.2240446, ANTIGONE 127.7681346, BARON 122.906804, COUENNE 36.93519535, LINDO 22.04414019, SHOT 0 | 134.224 | 922.5952898 (p4, 2025-07-31, 1e-10) |
| 12 | 479.5051427 (GUROBI, 2025-07-31) | SCIP 426.3836029, XPRESS 280.5539705, ANTIGONE 219.8390107, BARON 198.7666059, COUENNE 34.76707503, LINDO 9.39261594, SHOT 0 | 280.554 | 2263.358374 (p9, 2025-07-31, 2e-12) |
| 18 | 770.7361733 (SCIP, 2022-02-15) | GUROBI 751.6532797, ANTIGONE 383.6649097, XPRESS 348.3640233, BARON 214.0851043, COUENNE 28.12743573, LINDO 0, SHOT 0 | 383.6649 | 5269.638815 (p6, 2018-08-04, 7e-11) |
| 24 | 1095.126488 (SCIP, 2022-03-17) | GUROBI 834.4213941, ANTIGONE 474.8317637, XPRESS 309.5105715, BARON 131.191737, COUENNE 0, LINDO 0, SHOT 0 | 474.8318 | 7332.721691 (p5, 2025-07-31, 2e-12) |

Relative gaps of the listed bounds, (p − d)/d: 71.25%, 236.84%, 372.02%,
583.71% and 569.58%.

**Family context.** MINLPLib marks an instance solved when at least three
solvers claim optimality within relative tolerance 10⁻⁶. Only waterno2_01
and _02 carry the mark.
- waterno2_03: SCIP's dual equals the listed primal 115.0045167, and LINDO's
  dual (115.0044602) is within 4.9·10⁻⁷ relative. BARON (115.0017607),
  COUENNE and ANTIGONE are within 1.3·10⁻⁴. No mark.
- waterno2_04: SCIP's dual equals the primal 145.4397918; the next best
  (BARON 145.4394212) is 2.5·10⁻⁶ away. No mark.

So "solved up to 4 periods" (`R/SYNTHESIS.md`), "optima known" (wave-2
report) and "closed by several solvers" (network literature report, §5.1)
are all imprecise (W6).

## 3. The certificates

### 3.1 The idea in plain words

1. Put a price on water at every period boundary, separately for each tank.
   Each hour can then be optimized alone: it pays for the water it leaves in
   the tanks and is paid for the water it receives. The sum of the hourly
   optima is a lower bound (Lagrangian relaxation; used for waterno2_09–24).
2. The weakness of this bound is "level jumps". Pump costs depend
   nonconvexly on tank levels. So under linear prices an hour may end at one
   level vector while the next hour starts at a different one.
3. For waterno2_06 the possible level vectors at each boundary are split
   into small boxes (cells). The two hours on either side of a boundary must
   use the same cell, so a jump stays inside one cell. Each cell gets its own
   price vector, tuned to make jumps inside it unprofitable.
4. Every (entry cell, exit cell) pair of every hour is bounded rigorously.
   The cheapest chain of cells through the hours is a lower bound.
5. The horizon row needs no price. Summed over the hours, it says the final
   stored volume is at least the initial one.

### 3.2 Setting

Write x = (x_0, …, x_{T−1}) with x_t ∈ R^{166} the variables of period t.
For period t:
- s_t(x_t), e_t(x_t) ∈ R³: the start and end levels (L_t, E_t);
- h_t(x_t): the horizon copy variable;
- c_t(x_t): the sum of the period's 9 cost variables;
- X_t: the set of x_t satisfying the 203 period rows, the OSIL bounds and
  binary integrality.

**Fact 1 (structure).** Every row other than the horizon row and the link
rows involves variables of one period only. The objective is Σ_t c_t(x_t).
So (P_T) reads

    min Σ_t c_t(x_t)  s.t.  x_t ∈ X_t;  s_{t+1}(x_{t+1}) = e_t(x_t) (t ≤ T−2);  Σ_t h_t(x_t) ≥ c_T.

(Code evidence: Section 1.4, item 1, and `R/reviews/waterno2-sepbranch-review-checks/check_rows.py`.)

**Fact 2 (implied bounds).** Let I_t be boxes with x_t ∈ I_t for every
feasible x, and put X'_t = X_t ∩ I_t. Adding such boxes does not change the
feasible set.
- The certificates use machine-proved boxes:
  - authors: `R/open-instances-wave2/waterno2/logs/implied_TT.json`;
  - first verifier: exact-rational FBBT and OBBT,
    `R/reviews/waterno2-verification/logs/my_implied_06.json`;
  - recheck: `R/reviews/waterno2-recheck/logs/my_implied_TT.json`.
- The first verifier reproduced or beat every authors' bound by exact FBBT
  and OBBT on the full model without the horizon row (`vimplied.py`).
- The bounds the cell cover needs also have hand proofs (Lemma 5).

### 3.3 Proposition 1 (period Lagrangian)

For any λ_0, …, λ_{T−2} ∈ R³ and μ ≥ 0, put λ_{−1} = λ_{T−1} = 0 and

    φ_t(λ, μ) = inf { c_t(x_t) + λ_{t−1}ᵀ s_t(x_t) − λ_tᵀ e_t(x_t) − μ h_t(x_t) : x_t ∈ X'_t }.

Then OPT(P_T) ≥ μ c_T + Σ_t φ_t(λ, μ). Hence OPT(P_T) ≥ μ c_T + Σ_t B_t for
any numbers B_t ≤ φ_t(λ, μ).

*Proof.* Let x be feasible. The link rows give Σ_t λ_tᵀ(s_{t+1} − e_t) = 0.
The horizon row with μ ≥ 0 gives μ(c_T − Σ_t h_t) ≤ 0. So

    f(x) ≥ f(x) + Σ_t λ_tᵀ(s_{t+1}(x) − e_t(x)) + μ(c_T − Σ_t h_t(x))
         = μ c_T + Σ_t [c_t + λ_{t−1}ᵀ s_t − λ_tᵀ e_t − μ h_t](x_t) ≥ μ c_T + Σ_t φ_t(λ, μ),

because x_t ∈ X'_t (Facts 1 and 2). □

The multipliers are binary64 numbers, taken as exact rationals. They came
from a bundle method that used SCIP as an untrusted oracle, so their quality
affects only the strength of the bound. Each variable of a period objective
receives at most one Lagrangian term, so every objective coefficient is an
exact float.

### 3.4 Lemma 2 (the horizon row is a terminal-volume row)

Let w = (1/2, 1/5, 4/9) and σ = (3.5, 4.1, 4). Every x that satisfies the
linear equality rows of (P_T) (balance, copy, link and demand rows)
satisfies

    Σ_t h_t(x) − Σ_t d_t = wᵀ(e_{T−1}(x) − σ).

Since c_T = Σ_t d_t exactly, such an x satisfies the horizon row if and only if

    ½ E_{T−1,1} + ⅕ E_{T−1,2} + 4/9 E_{T−1,3} ≥ 3913/900   (⇔ 1800 E1 + 720 E2 + 1600 E3 ≥ 15652 = 1800·3.5 + 720·4.1 + 1600·4).

*Proof.* Merge variables joined by copy rows. Period t's three balance rows,
divided by 3600, read:
- ½(e_{t,1} − s_{t,1}) = h_t − Q_{t,B};
- ⅕(e_{t,2} − s_{t,2}) = Q_{t,B} − Q_{t,D};
- 4/9 (e_{t,3} − s_{t,3}) = Q_{t,D} − d_t,

where d_t is fixed by a single-variable equality row. Their sum is
wᵀ(e_t − s_t) = h_t − d_t. Summing over t and using s_{t+1} = e_t and
s_0 = σ telescopes to the identity. □

The data fact c_T = Σ_t d_t was checked exactly for T ∈ {2, 3, 4, 6, 9, 12,
18, 24} by three separate derivations:
- the authors' `sepbranch/terminal.py` (least squares, then an exact check);
- the review's structural `terminal_allT.py`;
- this dossier's `terminal_check.py` (`logs/terminal_check.log`).

At all five exact points the horizon row is active, Σ_t h_t = c_T
(`logs/point_consistency.log`).

**Folding.** For feasible x,
μ(c_T − Σ h_t) = μ wᵀσ − μ wᵀe_{T−1} + Σ_t μ wᵀ(s_{t+1} − e_t). So a horizon
multiplier equals a shift of every link slope by μw, plus a price on the
final volume that the hard terminal row dominates. The cell certificates
therefore use μ = 0 and start from the folded slopes λ_t + μw. The review
checked the stored folded slopes bit for bit.

### 3.5 Theorem 3 (cell decomposition with one slope vector per cell)

Let Y_l = {e_l(x) : x feasible} ⊂ R³ for l = 0, …, T − 2. Assume:

- **(H1) Cover.** P_l is a finite family of closed boxes (cells) with
  Y_l ⊆ ∪P_l.
- **(H2) One slope per cell.** Each D ∈ P_l carries a vector λ_{l,D} ∈ R³.
- **(H3) Pair bounds.** For every t, D ∈ P_{t−1} and D′ ∈ P_t, the number
  B_t(D, D′) ∈ R ∪ {+∞} satisfies B_t(D, D′) ≤ φ_t(D, D′), where

      φ_t(D, D′) = inf { c_t(x_t) + λ_{t−1,D}ᵀ s_t(x_t) − λ_{t,D′}ᵀ e_t(x_t) :
                         x_t ∈ X'_t, s_t(x_t) ∈ D, e_t(x_t) ∈ D′,
                         and wᵀ e_{T−1}(x_t) ≥ 3913/900 if t = T − 1 }

  and inf ∅ = +∞. Period 0 has no entry cell or entry term; period T − 1
  has no exit cell or exit term.

Then OPT(P_T) ≥ V, where

    V := min over (D_0, …, D_{T−2}) ∈ P_0 × … × P_{T−2} of Σ_{t=0}^{T−1} B_t(D_{t−1}, D_t).

V is computed by the shortest-path recursion:
- F_0(D) = B_0(D);
- F_t(D′) = min_{D∈P_{t−1}} [F_{t−1}(D) + B_t(D, D′)] for 1 ≤ t ≤ T − 2;
- V = min_{D∈P_{T−2}} [F_{T−2}(D) + B_{T−1}(D)].

*Proof.* Let x be feasible and y_l = e_l(x) = s_{l+1}(x) ∈ Y_l. By (H1),
choose one D_l ∈ P_l with y_l ∈ D_l; on a shared face, choose either cell,
and both adjacent periods then use the chosen cell. The link rows give
Σ_l λ_{l,D_l}ᵀ(s_{l+1}(x) − e_l(x)) = 0. Adding this to f(x) and grouping by
period:

    f(x) = Σ_t [c_t(x_t) + λ_{t−1,D_{t−1}}ᵀ s_t(x_t) − λ_{t,D_t}ᵀ e_t(x_t)].

For each t, x_t ∈ X'_t (Fact 2), s_t(x_t) ∈ D_{t−1} and e_t(x_t) ∈ D_t. For
t = T − 1 the terminal row holds by Lemma 2. So the t-th bracket is at least
φ_t(D_{t−1}, D_t) ≥ B_t(D_{t−1}, D_t), and f(x) ≥ V. The recursion is the
shortest path in the layered graph with arc weights B_t. □

*Remarks.*
- The only coupling condition is (H2): the exit term of period l and the
  entry term of period l + 1 use the same λ_{l,D}.
- Slopes may jump across faces.
- Offsets would cancel along every path, so they are useless.
- Pair-dependent slopes are not allowed unless the DP state becomes a pair
  of cells.
- With one cell per link and slopes λ_l + μw, Theorem 3 reproduces
  Proposition 1, with the terminal row in place of the horizon term. For
  waterno2_06 this gives +0.0008 (263.735935 vs 263.735099).
- Theorem 3 is the path case of Definition 1.2 / Lemma 1.5 of
  `R/theory-decomposition/decomposition-certificates.md`, with
  cell-dependent minorants. The direct proof above does not need that
  note's "touching pairs" remark.

### 3.6 Lemma 4 (reusing a bound after a slope change)

Let a record r of period t consist of boxes A_in, A_out, slopes a, a′, and a
number B_r with

    B_r ≤ inf { c_t + aᵀs_t − a′ᵀe_t : x_t ∈ X'_t, s_t ∈ A_in, e_t ∈ A_out (+ terminal row if t = T−1) }.

Let D = [lo, hi] ⊆ A_in and D′ = [lo′, hi′] ⊆ A_out carry slopes
l = λ_{t−1,D} and l′ = λ_{t,D′}. Then

    φ_t(D, D′) ≥ B_r + Σ_k min{(l_k − a_k) lo_k, (l_k − a_k) hi_k} + Σ_k min{−(l′_k − a′_k) lo′_k, −(l′_k − a′_k) hi′_k},

and B_r = +∞ (record box empty) implies φ_t(D, D′) = +∞.

*Proof.* The feasible set of (D, D′) is contained in that of
(A_in, A_out). On it, the pair objective equals the record objective plus
(l − a)ᵀs_t − (l′ − a′)ᵀe_t. A linear function on a box attains its minimum
coordinatewise at endpoints. □

If both records at link l used the same old slope a, the exit and entry
corrections at one cell sum to −Σ_k |l_k − a_k|(hi_k − lo_k). In waterno2_06,
certA's slopes with only cert3's records gave 243.10.

### 3.7 Lemma 5 (level ranges at the links of waterno2_06, hand proofs)

For every feasible x of waterno2_06:
- (a) E_{0,3} ≥ 3.33249999925, E_{1,3} ≥ 2.67000000025, E_{2,3} ≥ 2.03125;
- (b) E_{0,3} ≤ 5.6976271;
- (c) all other link coordinates lie in the OSIL boxes [2,5] × [2.5,5] × [2,6].

*Proof.*
- (c) This is the OSIL box.
- (a) The tank-3 balance gives E_{t,3} = L_{t,3} + 2.25(Q_{t,D} − d_t) with
  Q_{t,D} ≥ 0. Start from L_{0,3} = 4 and use L_{t+1,3} = E_{t,3}:
  - E_{0,3} ≥ 4 − 2.25·0.296666667 = 3.33249999925;
  - E_{1,3} ≥ 3.33249999925 − 2.25·0.294444444 = 2.67000000025;
  - E_{2,3} ≥ 2.67000000025 − 2.25·0.283888889 = 2.03125.
  The next step gives 1.4075 < 2, so it adds nothing.
- (b) Setup. In period 0, L_{0,2} = 4.1 and L_{0,3} = 4, so H_D = 12.9 + 5Q_D².
  Each running D pump satisfies 63.61644904 q² − 2.03724124 ωq +
  (H_D − 34.92732674 ω²) = 0 with 0.7 ≤ ω ≤ 1. Both D pumps share ω and H_D.
  Cases:
  - *No pump on.* If the first D pump is off, the second is off by
    symmetry, and Q_D = 0.
  - *One pump on.* Q_D = q ≤ 0.58.
  - *Two pumps on, different flows.* The flows are the two roots of one
    quadratic, so their sum is 2.03724124ω/63.61644904 ≤ 0.0321 < 0.48, the
    sum of the minimum flows. This is impossible.
  - *Two pumps on, equal flows q.* Then Q_D = 2q and H_D = 12.9 + 20q², so
    83.61644904 q² = 34.92732674 ω² + 2.03724124 qω − 12.9
    ≤ 22.02732674 + 2.03724124 q. Hence q ≤ 0.5255838 and Q_D ≤ 1.0511676.
  In all cases E_{0,3} = 4 + 2.25(Q_D − 0.296666667) ≤ 5.6976271. □

The rows used are e44, e75, e105, e168/e174, e222/e228, e240/e246, e264,
e282, e468, e498, e564/e570, e618/e624 and e720/e721; all were checked for
this dossier against the period-0 dump. The arithmetic is in
`logs/tank3_hand_bound.log`.

**Coverage consequence.** certB's root cells are, for links 0–4:
- tank 1: [2, 5] on every link;
- tank 2: [2.5, 5] on every link;
- tank 3: [3.3324999992334576, 5.936197237759838], [2.6700000002022537, 6],
  [2.0312499999222715, 6], [2, 6] and [2, 6].

By Lemma 5 each root contains Y_l. This needs no machine-proved bound.
Before Lemma 5(b), link 0's upper end 5.936… rested on OBBT, because the
trivial bound from q ≤ 0.58 is 5.9425.

### 3.8 Lemma 6 (soundness of the per-period and per-pair B&B)

Let S be the feasible set of a period or pair problem (one of the sets in
Proposition 1, Theorem 3 or Lemma 4, with its linear objective cᵀz). Let
τ ∈ R be a target. Suppose a procedure keeps a finite list N of boxes with
this invariant:

> every z ∈ S with cᵀz < τ lies in some box of N,

and each box β ∈ N carries a number b(β) ≤ inf{cᵀz : z ∈ S ∩ β}. Then
inf_S cᵀz ≥ min(τ, min_{β∈N} b(β)), with min ∅ = +∞.

*Proof.* A point z ∈ S either has cᵀz ≥ τ, or lies in a box β ∈ N and has
cᵀz ≥ b(β). □

The invariant holds initially, with N = {root box ⊇ S}. These operations
keep it:
1. splitting a box into two closed boxes whose union is the box (binaries
   into {0} and {1}; continuous variables at a point);
2. shrinking β to a box containing {z ∈ S ∩ β : cᵀz < τ}. This covers
   outward-rounded FBBT, OBBT with or without the cutoff cᵀz ≤ τ, and
   reduced-cost tightening;
3. deleting β when b(β) ≥ τ, or when S ∩ β = ∅ has been proved.

The value +∞ is returned only when propagation *without* cutoff proves the
root box empty, so then S = ∅.

**Node bounds.** Each monomial gets an auxiliary variable. On a box, the
relaxation uses these valid inequalities:
- w = x²: tangents w ≥ 2px − p²; secant w ≤ (l + u)x − lu;
- w = x³ with x ≥ 0 (asserted; flows and speeds): tangents
  w ≥ 3p²x − 2p³ with p ≥ 0, valid because
  x³ − 3p²x + 2p³ = (x − p)²(x + 2p) ≥ 0; secant
  w ≤ (l² + lu + u²)x − lu(l + u), valid because
  x³ − [(l² + lu + u²)x − lu(l + u)] = (x − l)(x − u)(x + l + u) ≤ 0 on [l, u];
- w = xy, including binary × variable: the four McCormick inequalities
  (exact for a binary factor at 0/1).

For relaxation rows A_I z ≤ b_I, A_E z = b_E on a box [l, u], and *any*
y with y_I ≥ 0 (Neumaier–Shcherbina [[neumaier2004-safe-bounds-in-linear-and]]):

    min { cᵀz : rows, l ≤ z ≤ u } ≥ −yᵀb + Σ_j min{(c + Aᵀy)_j l_j, (c + Aᵀy)_j u_j}.

*Proof.* cᵀz ≥ cᵀz + yᵀ(Az − b) = (c + Aᵀy)ᵀz − yᵀb. □

HiGHS supplies y. A wrong y only weakens b(β).

### 3.9 The computer-assisted part: what is computed and what must be trusted

**Statements established by computation.**
- For each period t of 09–24 (and of 06 wave 2): S_t := "B_t ≤ φ_t(λ, μ)"
  at the stored multipliers.
- For each record r of 06: S_r := the inequality of Lemma 4 at the record's
  stored boxes and slopes, or "the record box is empty" when B_r = +∞.

Each statement was established by two separately written B&B codes, both
instances of Lemma 6.

| code | written by | data | propagation | relaxation constants | node bound |
|---|---|---|---|---|---|
| `rbb.py` (`R/open-instances-wave2/waterno2/`) | authors | decimals enclosed in [down(v), up(v)] | binary64, outward via `nextafter`; sums get margin 10⁻¹²·Σ\|terms\| (> γ_{n−1}Σ\|terms\| for n ≤ 9000) | rigorous float constants | interval coefficients, outward rounded |
| `vbb.py` (`R/reviews/waterno2-verification/`) | first verifier | exact rationals | exact (`Fraction`), outward-rounded to floats | exact rational | exact (`Fraction`) |
| `vbb2.py` (`R/reviews/waterno2-recheck/`) | recheck | exact rationals | binary64, one ulp outward per ×, ÷, √; `fsum` + 2 ulp; cubes and cube roots exact | exact rational (from vbb) | exact (`Fraction`) |

Other differences:
- rbb also uses reduced-cost tightening and root OBBT with cutoff (valid by
  Lemma 6, item 2).
- vbb and vbb2 use neither, only root OBBT without cutoff.
- vbb2 = vbb with float propagation. It was tested against vbb's exact
  propagation (3000 pass comparisons, 0 violations) but not proved.

**Coverage of the runs.**

| item | rbb (authors) | second code | result |
|---|---|---|---|
| 06 wave 2: 6 periods | certified at the stored B_t | `vbb.py`, exact propagation; periods 1–3 with the verifier's own implied bounds | all 6 certified at the authors' values |
| 09–24 wave 2: 63 periods | certified | `vbb2.py` with the recheck's implied bounds | all 63 certified; exact sums equal bit for bit |
| 06 cert3: 8,958 used records | 9,631 runs | `vbb2.py` through the review's own driver, model and terminal row | 6,827 certified at the rbb bound, 2,131 boxes proved empty, 0 failed |
| 06 certB: 49,315 used records | 77,249 records (cert3, certA, certB runs) | `vbb2.py` through a second review's own driver | 33,899 certified, 15,416 proved empty (all 12,298 +∞ records and 3,118 finite ones), 0 failed; 556 corrected leaf pairs re-bounded directly at the leaf slopes: 436 certified, 120 empty |

The exact DP from the vbb2 values alone equals the certificate value (both
reviews). So each line, rbb or vbb/vbb2, yields every claimed bound by
itself.

**Exact combination.**
- 09–24: μc_T + Σ_t B_t in `Fraction`, by three implementations
  (`vsum.py`, `vsum2.py`, this dossier's `wave2_sums.py`).
- 06 certB: three implementations (authors' `verify_cs.py`, review's
  `ind_verify_cs.py`, this dossier's `dp_check.py`). Each:
  - checks that the leaves partition each root box (`dp_check.py`: leaves
    inside the root, pairwise disjoint interiors by exact float comparison,
    exact volume sum);
  - checks that each root contains the proven level box;
  - picks a containing record for each of the 117,736 leaf pairs (exact
    float comparison of boxes);
  - adds the Lemma-4 corrections in `Fraction`;
  - runs the shortest path in `Fraction`.

**What must be trusted.**
1. **Record and period statements.** For each statement S, at least one of
   the two executions (rbb, or vbb/vbb2) is correct, together with the
   implied-bound file that execution used:
   - rbb: the authors' files, reproduced by exact FBBT/OBBT;
   - vbb for 06: the first verifier's exact file;
   - vbb2 for 09–24: the recheck's file, made with vbb2's propagation plus
     exactly evaluated OBBT;
   - vbb2 for 06: the first verifier's file.
2. **Platform.** IEEE-754 binary64 in CPython/NumPy (round to nearest,
   correctly rounded `sqrt`, `nextafter`, `fsum` within the margin), and
   Python's `fractions`.
3. **Model reading.** All B&B pipelines read the OSIL through `osilx.py`.
   It agrees exactly with a separately written parser on all rows, bounds
   and objectives of all five instances (`logs/osilx_cmp.log`), and the
   OSIL equals the GAMS text exactly (Section 1.5).
4. **Untrusted inputs.** HiGHS and SCIP supply hints only: dual vectors,
   branching points, targets and multipliers.

There are no eg-style A1/A2 assumptions and no mpmath-interval assumptions
in this family.

**What is not stored.** The B&B trees (leaf boxes, dual vectors, emptiness
proofs) were not saved. A record stores its boxes, slopes, bound, status,
node count and time. So the computed statements are reproducible by re-run
but cannot be checked from a stored proof object (W1).

**Replay costs.**
- Exact DP replay: seconds.
- vbb2 replay is deterministic: 20 certB records and waterno2_09 period 6
  give the identical status, exact bound and node count on re-run
  (`logs/replay_compare.log`).
- Full vbb2 re-bounding of certB: 214,979 CPU-s on a loaded machine. The
  replay sample ran 2.4× faster (69 s vs 166 s), so expect roughly 25–60
  CPU-hours.
- The 63 periods of 09–24: 30,516 s of vbb2 B&B time.

### 3.10 Instantiation

**Corollary 7 (waterno2_06, certificate certB).**
- **Data.** `R/open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz`
  (6.2 MB):
  - five split trees with 228, 154, 148, 153 and 240 leaves;
  - one binary64 slope vector per leaf (101, 130, 135, 139 and 174 distinct
    vectors per link);
  - 77,249 records, of which 49,315 are used.
- **Pair bounds.** B_t(D, D′) is the largest Lemma-4 bound over records of
  period t whose boxes contain D and D′. Then:
  - (H1) holds by Lemma 5 and the partition check;
  - (H2) holds by construction (one array per link serves both adjacent
    periods);
  - (H3) holds by Lemma 4, given the record statements of Section 3.9.
- **Value.** V = 39157472136693483/140737488355328 (denominator 2⁴⁷)
  = 278.2305737745608…, so OPT(waterno2_06) ≥ 278.230573774.
- **Pair table.** 79,919 finite leaf-pair bounds and 37,817 leaf pairs
  proved empty. 52,826 finite pair bounds use a nonzero correction.
- **Minimizing path.** Records 52772, 52771, 52856, 53013, 52936 and 53069.
  All are certB runs at the leaf boxes and slopes, so they need no
  correction.

| period | pair bound | exit cell (tank 1 × tank 2 × tank 3) | exit-cell slope | folded wave-2 slope |
|---|---|---|---|---|
| 0 | −615.3962 | [4.175, 4.183] × [4.099, 4.108] × [3.332, 3.338] | (33.16, 37.58, 103.55) | (32.78, 34.19, 101.91) |
| 1 | 59.5099 | [3.980, 4.240] × [3.333, 4.167] × [2.670, 2.762] | (34.44, 34.50, 109.66) | (33.70, 34.50, 102.54) |
| 2 | 68.8988 | [4.430, 5.000] × [2.500, 3.009] × [2.612, 2.861] | (35.86, 35.67, 104.08) | (34.89, 35.31, 103.03) |
| 3 | 59.8840 | [2.000, 5.000] × [4.167, 5.000] × [2.500, 3.000] | (36.05, 37.35, 101.19) | (36.49, 35.49, 103.73) |
| 4 | 60.3246 | [4.092, 5.000] × [2.500, 3.333] × [2.500, 3.000] | (38.06, 36.13, 102.12) | (38.50, 37.17, 103.73) |
| 5 | 645.0095 | free end, terminal row | – | – |

Successive certificates for waterno2_06 (all superseded by certB; gaps
against the exact primal, rounded up; `logs/ratios.log`):

| certificate | exact value | display | gap ≤ | cells per link | slopes |
|---|---|---|---|---|---|
| wave 2 (Prop. 1) | 148469661946242564611253309/562949953421312000000000 | 263.735099441 | 7.27% | 1 | λ, μ |
| cert2 (Thm. 3) | 38164240025509421/140737488355328 | 271.173235159 | 4.33% | 77–101 | one per link |
| cert3 (Thm. 3) | 19181443079783745/70368744177664 | 272.584700834 | 3.78% | 113–162 | one per link |
| certA (Thm. 3) | 2437338627747397/8796093022208 | 277.093321045 | 2.10% | 148–240 | 91–152 per link |
| **certB (Thm. 3)** | **39157472136693483/140737488355328** | **278.230573774** | **1.68%** | 148–240 | 101–174 per link |

Wave-2 details for 06:
- μ = 185.86682755574702 and μc_6 = 325.7316151055798;
- B_t = 158.44542021914268, 3.3200165915325814, 0.05585209119252331,
  0.011863658606134687, −5.762328864166388, −218.06733936023628.

**Corollary 8 (waterno2_09–24, Proposition 1).** The stored float
multipliers λ, μ ≥ 0 and the period bounds B_t are in
`R/open-instances-wave2/waterno2/logs/cert_TT_w1_impl.json`.

| T | μ | μ c_T | exact μ c_T + Σ B_t | display | rbb nodes |
|---|---|---|---|---|---|
| 9 | 430.70076424644117 | 1603.6425120673491 | 3627661341387654598825371/4398046511104000000000 | 824.834692454 | 108,519 |
| 12 | 688.8500140339286 | 3895.255481293818 | 9190837775594918144252281/4398046511104000000000 | 2089.754565439 | 140,952 |
| 18 | 759.5351463046937 | 7197.017474025643 | 5267563083146225483626937/1099511627776000000000 | 4790.820715376 | 381,084 |
| 24 | 170.79839472283007 | 2187.310663925092 | 115688878681251187594323079/17592186044416000000000 | 6576.151388415 | 525,224 |

- The per-period values are listed in `R/reviews/waterno2-recheck.md` §2.
- The bundles for T = 6, 9, 12 and 18 started from least-squares KKT
  multipliers at the best MINLPLib point. For T = 24 the dense KKT solve did
  not finish, so it started from zero.
- The bundles for T = 18 and 24 were stopped with a predicted further gain
  of about 1–2.

## 4. Exactly feasible primal points

Source: `R/publication/primal/water-ann-kan/report.md`; points in
`points/waterno2_TT.exact.json`.

**Construction.** It starts from MINLPLib's p4 for 06, and from the
authors' window-reoptimized points for 09–24. Those came from SCIP on
2-period windows with the true objective, accepted at row violation ≤ 10⁻⁸.

1. Fix the binaries. Pin variables that single rows force (an off pump has
   flow 0 and speed ω^min). Turn the pairs of big-M rows of running pumps
   into η = H.
2. Alias the flows of the running pumps of one station: the shared speed and
   head force equal flows. Two distinct flows would be the two roots of one
   pump quadratic, whose sum is −b_Sω/c_S. That sum is negative for A and B1,
   above 2·0.7 for B2 (2.296ω ≥ 1.95), and below 2·0.24 for D
   (0.032ω). The station flows are the free "seeds".
3. Solve the linear rows exactly. Active level bounds and the horizon row
   are imposed as equalities by a minimum-norm exact rational correction of
   the seeds. The largest corrections are 3.0e-16 (06), 1.1e-10 (09),
   8.8e-9 (12), 1.0e-9 (18) and 6.1e-10 (24).
4. Each running station's pump-curve row is then a quadratic in its speed
   with rational coefficients.
   - The speed is the root nearest the numerical speed, isolated in a
     rational interval of width 2·10⁻⁴⁵ by a sign change.
   - The discriminant is not a rational square, so every coordinate lies
     in Q or in one quadratic field Q(w_k). The points have 9, 18, 28, 48
     and 63 irrational speeds.
   - In waterno2_18 three stations needed a 10⁻⁹ flow shift to keep the
     speed ≥ 0.8.
5. Costs are set to rational upper bounds of the power expression on a
   10⁻³⁰ grid, so the objective is an exact rational number.

**Proof of feasibility.** Every row, bound and integrality requirement is
decided exactly. The construction steps only propose a point; validity rests
on the checks. Three exact checkers ran:
- the author's `qfield` check;
- the author's second checker, which writes w_k = (−B + s√d)/(2A) and
  decides signs by comparing a² with b²d;
- the independent reviewer's multi-quadratic-field evaluator, with its own
  OSIL reader (`R/publication/reviews/primal-water-ann-kan-review-r1.md`,
  verdict "verified"). Its mutation tests catch perturbations of 10⁻³⁰.

The points were also evaluated at 60 digits with `osilx.py` (residual
≤ 1.3e-57).

**New checks for this dossier** (`logs/point_consistency.log`, `logs/gaps.log`):
- each stored objective equals the exact sum of the point's cost
  coordinates;
- each point satisfies every implied-bound file used by any certificate:
  228, 48, 66, 102 and 138 bounded variables in the authors' files; 627
  (first verifier, 06) and 806, 1070, 1598 and 2129 (recheck, 09–24). This
  is a necessary condition for those files to be valid.

**Objective values (exact rationals).**

| instance | exact objective | earlier point (violation) | listed primal |
|---|---|---|---|
| 06 | 282888037386904807969455615812871/10³⁰ = 282.888037386904807969… | MINLPLib p4: 282.8880373869047 (row 1.08e-11, e94) | 282.8880374 |
| 09 | 228502993809271497947655151104763/(2.5·10²⁹) = 914.011975237085991… | 914.011970349935 (rows 1.0e-9; bounds 5.7e-11) | 922.5952898 |
| 12 | 69806917050256726053529840094123/(3.125·10²⁸) = 2233.821345608215233… | 2233.821335281894 (1.0e-9; 3.1e-10) | 2263.358374 |
| 18 | 502398276046066187107521965865629/10²⁹ = 5023.982760460661871… | 5023.982735142767 (4.4e-9; 8.9e-10) | 5269.638815 |
| 24 | 278551807206256780512771353023449/(4·10²⁸) = 6963.795180156419512… | 6963.795154460378 (1.0e-9; 9.0e-10) | 7332.721691 |

- **06.** The point lies within 3.1·10⁻¹³ of p4. Its objective is
  2.0·10⁻¹³ below p4's objvar 282.888037386905012. So it is MINLPLib's p4
  made exact: credit p4, added 2025-07-31. MINLPLib's page lists p4's
  infeasibility as 2e-12; the exact maximum row violation is 1.08e-11.
- **09–24.** These points are ours. They improve the listed primals by
  8.58, 29.54, 245.66 and 368.93. They are also better than every point
  returned in the one-hour solver runs: GUROBI's 919.99, 2262.23 and
  7295.02, all with row violations near 10⁻⁶.

## 5. Numbers table

Displays follow the summary: duals truncated, primals rounded up, gaps
rounded up. All cells agree with `R/open-instances-summary.md`.

Sources:
- duals: `R/open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json`
  (`bound_exact`) for 06, and `R/open-instances-wave2/waterno2/logs/cert_TT_w1_impl.json`
  (`certified_bound_exact`) for 09–24;
- primals: `R/publication/primal/water-ann-kan/points/waterno2_TT.exact.json`;
- gaps: `R/publication/integration/gap-values.json`, recomputed in
  `logs/gaps.log`;
- listed values: `R/bound-audit/pages.json`.

| instance | best listed dual | our dual | primal | abs. gap ≤ | gap/dual ≤ (exact) | gap/primal | ours ÷ listed dual | listed gap/dual |
|---|---|---|---|---|---|---|---|---|
| 06 | 165.1902989 | 278.230573 | 282.888038 | 4.6575 | **1.68%** (1.673958%) | 1.646398% | 1.68 | 71.25% |
| 09 | 273.8958303 | 824.834692 | 914.012 | 89.1773 | **10.82%** (10.811534%) | 9.756686% | 3.01 | 236.84% |
| 12 | 479.5051427 | 2089.754565 | 2233.821346 | 144.0668 | **6.90%** (6.893957%) | 6.449342% | 4.36 | 372.02% |
| 18 | 770.7361733 | 4790.820715 | 5023.983 | 233.1621 | **4.87%** (4.866850%) | 4.640980% | 6.22 | 583.71% |
| 24 | 1095.126488 | 6576.151388 | 6963.795181 | 387.6438 | **5.90%** (5.894691%) | 5.566559% | 6.00 | 569.58% |

The ratios are 1.6843, 3.0115, 4.3581, 6.2159 and 6.0049. For waterno2_06,
certB closes 96.04% of the absolute gap between the best listed dual and the
best primal, and 75.68% of the wave-2 gap.

**Disagreements found (displays only; no wrong bound).**
- "1.67%" (nearest rounding) appears in `R/SYNTHESIS.md`, `cell-slopes.md`
  and `closing-research-results.md`. The safe upward display is ≤ 1.68%.
- `R/publication/literature/network/report.md` §5 (table) gives "≤ 4.90%"
  for waterno2_18. The summary and `gap-values.json` give ≤ 4.87%; both are
  valid upper bounds. Use 4.87%.
- `R/publication/solver-runs/report.md` lines 206–210 still quote the
  tolerance-feasible primals (914.011970350, …).
- The wave-2 report quotes nearest-rounded gaps (7.26%, 10.81%, 6.89%,
  5.89%).
- `R/SYNTHESIS.md` says the duals rose "by factors of 1.6–6.2". With certB
  the factors are 1.68–6.22; 1.6 is the wave-2 factor for 06.

**One-hour solver comparison.** BARON 26.5.27, GUROBI 13.0.2 and SCIP
10.0.3 ran single-threaded with a 3600 s limit
(`R/publication/solver-runs/results_table.md`).
- Best final duals: 142.83 (GUROBI, 06), 220.68 (GUROBI, 09), 454.56
  (GUROBI, 12), 891.93 (SCIP, 18) and 1074.44 (SCIP, 24). All are far below
  ours, and no run closed.
- SCIP returned no primal point on any of the five.
- The waterno2_24 runs were in the overloaded first batch.
- The solver-analysis review r1 has verdict "issues" (two major: six BARON
  values without a globality guarantee, and the overloaded first batch).
  The author's response was not re-reviewed
  (`R/publication/reviews/integration-review-r1.md`). The duals quoted
  above are GUROBI and SCIP final bounds; quote them as one-hour
  floating-point solver outputs only.

## 6. Verification record

| review | scope | what it checked | verdict |
|---|---|---|---|
| `R/reviews/waterno2-verification/verification-report.md` (first verifier) | wave 2, all T | structure by a different rule; Lagrangian signs; implied bounds by exact FBBT/OBBT, with hand proofs for tank 3; code review of `rbb.py`; all 6 periods of 06 plus 09 p6 and 24 p19 re-certified with `vbb.py`; exact sums; negative controls; SCIP wrong answers with exactly feasible witnesses; MINLPLib status | confirmed |
| `R/reviews/waterno2-recheck.md` | 09–24 | all 63 periods re-certified with `vbb2.py` and its own implied bounds; exact sums bit for bit; propagation tested against exact propagation; negative controls on 09 p8 and 24 p19; objective coefficients compared | all certified; independent of the authors, not of the first verifier |
| `R/reviews/waterno2-sepbranch-review.md` | 06 cert2/cert3 | validity argument; independent terminal-row derivation for all T; coverage; record containment and slopes for all 62,088 and 28,858 leaf pairs; exact DP; all 8,958 used cert3 records re-bounded with vbb2 through its own driver; negative control; p1–p4 margins | confirmed; 6 minor wording issues, fixed |
| `R/reviews/waterno2-cellslopes-review.md` | 06 certA/certB | Proposition 1 (= Thm. 3) and Lemma 2 (= Lemma 4) re-derived; one vector per cell on both sides; coverage; all 117,736 leaf pairs mapped by containment; own exact DP; all 49,315 used records re-bounded; 556 leaf-level Lemma-4 checks; negative control at p4 + 0.01; p1–p4 | verified; 7 minor issues, fixed |
| `R/reviews/waterno2-cellslopes-confirm-r1.md` | the 7 fixes | recounts | verified |
| `R/publication/reviews/primal-water-ann-kan-review-r1.md` | exact points | own multi-quadratic-field evaluator and OSIL reader; all five points exactly feasible; objectives; gaps; mutation tests | verified. Note: the report text it received was cut off at §2 step 2, so it checked every number but not the rest of the method text (W14) |
| `R/publication/reviews/integration-review-r1.md` | displays | recomputed every gap cell; all water percentages are valid upper bounds | issues, none blocking; water cells confirmed |
| `R/publication/scip-bug/report.md` + `R/publication/reviews/scip-bug-review-r1.md` | SCIP side finding | reproduction across versions; exact witnesses checked by four separate checkers; root-cause traces | verified |
| this dossier (`waterno2-checks/`) | combination, data, consistency | see below | consistent; no error found |

**Checks run for this dossier** (all exact unless stated; `logs/`):
1. `terminal_check.py`: own structural derivation of the terminal row and of
   c_T = Σd_t for T ∈ {2, 3, 4, 6, 9, 12, 18, 24}.
2. `wave2_sums.py`: μc_T + ΣB_t in `Fraction` for T = 6–24. All equal the
   stored exact values and their truncations. The certificate and
   multiplier files agree.
3. `dp_check.py`: certB. It checks:
   - the leaf partition of each root;
   - one finite slope per leaf;
   - μ = 0 and zero slopes on missing sides;
   - +∞ only with status `infeasible`;
   - containment, then the exact Lemma-4 corrections and the exact shortest
     path.
   Result: 39157472136693483/140737488355328, with 49,315 records used.
4. `rootbox_check.py`: each root contains the box given by the OSIL bounds
   and the first verifier's implied bounds.
5. `tank3_hand_bound.py`: Lemma 5(b); I re-derived it against the rows.
6. `gms_vs_osil.py` + `gms_mutation_control.py` (**new**): GAMS ≡ OSIL for
   all five instances; negative controls detected.
7. `osilx_cmp.py`: the shared reader `osilx.py` agrees exactly with a
   separate parse on all five instances.
8. `point_dp_check.py`: the exact 06 point lies in one leaf per link, every
   period value is ≥ its pair bound (smallest margin 0.0104), and the path
   sum is 280.436037.
9. `point_consistency.py` (**new**), for each T:
   - own period-structure recovery;
   - the exact point satisfies every implied-bound file;
   - every one of the 69 period-Lagrangian values at the exact point is
     ≥ its stored B_t;
   - the exact identity f(x) − (μc + ΣB_t) = Σ_t margin_t + μ(Σh − c).
   Smallest margins:
   - 06: 0.0376 (period 5);
   - 09: 0.00072 (period 7);
   - 12: 0.1150 (period 5);
   - 18: 0.0640 (period 5);
   - 24: 1.896 (period 14).
10. `gaps.py`, `ratios.py`, `data_facts.py`, `binary64_residuals.py`: the
    displays, the intermediate certificates, the data facts of Section 1.3,
    and the residual signs of Section 1.5.
11. `replay_vbb2.sh` (**new**; 2 cores, 81 s wall): the reviewers' vbb2 runs
    replayed bit for bit (status, exact bound, nodes) on certB's 6
    minimizing-path records, 14 seeded random used records, and
    waterno2_09 period 6.

## 7. Relation to prior work

### 7.1 These instances

Status of the search: "new as far as found"
(`R/publication/literature/network/report.md` §5).

- **Huang 2019** [[huang2019-optimal-operation-of-water-supply]], Table 5.2.
  - SCIP 5.0.1 ran for 1 h on related multi-period models of the same
    network; none with ≥ 5 periods closed.
  - Huang's 3-period optimum is 215, against waterno2_03's feasible 115.0045,
    so the models differ.
  - The extended-model 6-period dual 343.41 lies above our 06 primal. It
    concerns a different model and must not be compared.
- **Huang 2011** (FU Berlin; "Masters thesis" on MINLPLib, "Diplom" in the
  FU catalog, [[huang2011-operative-planning-of-water-supply]]) was not
  obtained. It may contain multi-period results on these models. This is
  the remaining caveat behind "new as far as found".
- **D'Ambrosio, Lodi, Wiese and Bragalli, EJOR 2015**
  [[ambrosio2015-mathematical-programming-techniques-in-water]], §5.2:
  "there is no successful solution for this complete [time-discretized]
  form in the literature".
- **SCIP Optimization Suite 8.0** [[bestuzheva2021-the-scip-optimization-suite-8]],
  App. A: SCIP 7 / SCIP 8 time-limit gaps of 326%/128% (06), >1000%/321%
  (09), >1000%/571% (12), >1000%/638% (18) and >1000%/750% (24).
- **Müller, Serrano and Gleixner**, SIOPT 30(2) 2020: waterno2_04–24 at the
  time limit (not in `literature/`; cited from the network report).
- **The JOGO SCIP 8 paper** [[bestuzheva2025-global-optimization-of-mixed-integer]]
  and Mittelmann's benchmark contain only waterno2_02/03.
- **Geißler, Morsi, Schewe and Schmidt**, SIOPT 27(3) 2017: heuristic
  primals of 442.50, 1422.16, 3119.55, 7359.11 and 9711.81, all worse than
  the listed ones.

### 7.2 Mechanisms (no method novelty claimed)

- **Lagrangian relaxation of state copies, branching on the copied
  variables, and DP across stages.**
  - Dual decomposition for stochastic integer programs (Carøe and Schultz,
    ORL 24, 1999; only the ZIB preprint page was seen; not in
    `literature/`).
  - Branching on tender variables [[ahmed2004-a-finite-branch-and-bound]].
  - Nested decomposition with local state copies and Lagrangian cuts
    (SDDiP, Zou, Ahmed and Sun, Math. Program. 175, 2019; not in
    `literature/`).
  - Nonconvex nested Benders [[fullner2022-non-convex-nested-benders-decomposition]],
    with refined binary state expansions whose Lagrangian cuts project to
    nonconvex piecewise-linear value-function approximations; SDDP review
    [[fullner2025-stochastic-dual-dynamic-programming-and]].
- **Cell-dependent multipliers.** The closest relative found is Yang and
  Yang [[yang2025-globally-converging-algorithm-for-multistage]].
  - SDDP-L partitions state intervals and generates Lagrangian cuts in the
    lifted space, so the cut coefficients depend on the active partition
    element.
  - Their setting is sampled MILP stages. Ours is a deterministic chain of
    nonconvex MINLP periods, with rigorous spatial B&B per cell pair and an
    exact DP.
- **Lagrangian decomposition for multi-period pump scheduling.** Ghaddar,
  Naoum-Sawaya, Kishimoto, Taheri and Eck, EJOR 241(2) 2015
  [[ghaddar2015-a-lagrangian-decomposition-approach-for]]; *not read*
  (local status: access none, unread). It must be read before submission.
- **Copy relaxation of subfunctions that share variables.** Berenguel,
  Casado, García, Hendrix and Messine, JOGO 56(3) 2013. Not in
  `literature/`, and its read status conflicts between `R/SYNTHESIS.md` and
  `R/literature/decomposition-bb-prior.md`.
- **Rigorous LP bounds and relaxations.** Neumaier–Shcherbina
  [[neumaier2004-safe-bounds-in-linear-and]];
  [[mccormick1976-computability-of-global-solutions-to]].
- **Value-function relaxation order.** [[robertson2025-on-the-convergence-order-of]];
  internal decomposition note, Proposition 2.6 and Theorem 3.4.
- **Solver and library.** [[hojny2025-the-scip-optimization-suite-10]];
  [[vigerske2026-minlplib-a-library-of-mixed]].

### 7.3 Relation to the internal theory notes

Theorem 3 is the path case of the decomposition-certificate framework. The
recipe of Theorem 3.4 there (slopes = gradients at the minimizer) does not
apply: its quadratic-growth and unique-minimizer assumptions fail.
- Along p4's trajectory, KKT slopes nearly close the gap: SCIP estimates of
  282.53 with 0.5-wide cells, against 282.89.
- On a uniform grid the same slopes gave an estimated 223.0, far below the
  one-cell bound.
- The tuned cell slopes vary widely from cell to cell (Section 5.2 of
  `cell-slopes.md`). They are an empirical substitute for that recipe.

### 7.4 SCIP wrong optimal values (side finding)

Source: `R/publication/scip-bug/report.md` and its review r1 (verified).
- SCIP 10.0.2, 10.0.3, 10.1.0 and master a01de2c report wrong "optimal"
  values, through PySCIPOpt and through GAMS:
  - on three single-period Lagrangian subproblems of waterno2_06 (periods 0,
    4 and 5);
  - on one cell-pair subproblem, depending on the random seed. The 65.12
    and 56.49 claims are refuted; the claims near 55.69 are not.
- Exactly feasible rational witnesses refute the claims, checked by four
  separate exact checkers.
- In the instrumented wrong runs, the default nonlinear handler's reverse
  propagation declares a node infeasible, because
  fl(0.7)³ − fl(0.343) = −9.24·10⁻¹⁷ once both variables are fixed.
- A 15-variable reproducer fails with default settings in every version.
- The upstream report is drafted and **not submitted**.
- Our bounds never use SCIP values.
- The listed SCIP duals for waterno2 lie far below ours. They are neither
  contradicted nor examined.

## 8. Critical examination

I re-derived Proposition 1, Lemma 2, Theorem 3, Lemma 4, Lemma 6 and the
relaxation inequalities. I re-derived Lemma 5 against the OSIL rows. I
reviewed the exact DP code `dp_check.py`:
- its partition test is sufficient: leaves inside the root with pairwise
  disjoint interiors and equal total volume cover the root, since the union
  is closed and of full measure;
- choosing a record by float value and then evaluating it exactly is sound,
  because any containing record gives a valid bound;
- the correction signs are right.

**No finding invalidates a claimed bound or point.** Every check that could
have exposed an error passed:
- three exact DP implementations agree;
- coverage now rests on hand proofs;
- the terminal row was derived three ways;
- GAMS ≡ OSIL exactly;
- the shared reader was cross-checked;
- the exact points satisfy every implied-bound file and lie above all 69
  wave-2 period bounds and all certB pair bounds on their cells;
- replays are deterministic.

The findings and their resolutions follow.

**W1 (minor; structural). The computed bounds are not checkable proof
objects.** B&B trees were not stored, so a reader can re-establish the
period and pair bounds only by re-running B&B.
- *Resolution (wording).* Write "computed by a rigorous B&B and recomputed
  by a second, separately written B&B with exact rational node bounds; the
  runs are deterministic and replayable". Do not write "verified
  certificate file".
- *Replay costs:*
  - exact DP: seconds;
  - certB re-bounding: about 25–60 CPU-hours (Section 3.9);
  - 09–24: about 8.5 CPU-hours;
  - this dossier replayed 21 saved runs bit for bit.
- *Optional strengthening.* Have vbb2 emit per-leaf proof data (box, dual
  vector y, or an emptiness witness), and write an exact checker that
  verifies the leaf cover and each node bound. Cost: a few days of coding;
  a full re-run (≈ 25–60 CPU-h for certB, ≈ 9 for 09–24); a checker pass of
  perhaps 10–20% of that. Not needed for the claims as worded.

**W2 (minor; trust base). Two B&B lines, not three.**
- vbb and vbb2 share the first verifier's model builder `vmodel`,
  relaxation and node-bound code. vbb2's float propagation is tested, not
  proved. The recheck's implied bounds for 09–24 come from that same
  propagation.
- rbb is a separate code base with its own model builder (`wmodel`), and
  its implied bounds were reproduced by exact FBBT/OBBT.
- A wrong claimed value would need an error in both lines on the same
  statement.
- *Resolution.* State exactly this.
- *Optional.* Re-run the 09–24 periods and certB's records with `vbb.py`'s
  fully exact propagation, at about 3–4× vbb2 time (≈ 25–35 CPU-h for 09–24,
  ≈ 75–240 CPU-h for certB). Not needed for the claim as worded.

**W3 (resolved). Shared OSIL reader.** `osilx_cmp.py` shows that `osilx.py`
agrees exactly with a separate parse on every row, bound and objective of
all five instances. Together with W8, two formats and two parsers agree.

**W4 (resolved). Coverage used an OBBT bound.** Link 0's root has tank-3
upper end 5.936197237759838, which needed OBBT; the trivial bound is
5.9425. Lemma 5(b) proves E_{0,3} ≤ 5.6976271 by hand. All coverage facts
are now hand-proved. The other implied bounds enter only inside the pair
and period problems, and both lines use machine-proved, valid versions.

**W5 (minor; displays and wording).**
- Use the summary's upward displays (≤ 1.68%, ≤ 4.87%), not "1.67%"
  (SYNTHESIS, cell-slopes note, closing results) or "≤ 4.90%" (network
  report).
- Use the exact-point primals, not the tolerance points in the
  solver-runs table.
- "49,315 pair bounds" or "every cell-pair bound" (summary, READINESS)
  actually means *records*: bounds on ancestor pair boxes at the record's
  own slopes. The 79,919 finite leaf-pair bounds follow from them by the
  exact Lemma-4 correction, and 556 leaf pairs were also re-bounded
  directly. *Suggested wording:* "all 49,315 pair-box bounds used by the
  certificate were recomputed with a second B&B code; the leaf-pair bounds
  follow by an exact linear correction".
- "Factors of 1.6–6.2" (SYNTHESIS) → 1.68–6.22.
- The wave-2 report's §4 still says `rbb.py` "has not been independently
  reviewed"; the first verifier reviewed it.

**W6 (minor; wording).** Do not say "solved up to 4 periods", "optima
known" (03/04) or "closed by several solvers" (03). MINLPLib marks only
waterno2_01/02 solved. For 03, SCIP's dual equals the primal and LINDO's is
within 4.9·10⁻⁷ relative; for 04, only SCIP's matches. Neither has the
mark. Huang's model-mismatch argument survives, because it only needs
waterno2_03's feasible point of value 115.0045 < 215.

**W7 (minor; semantics).** All bounds and points are for decimal-exact data.
Under a binary64 reading, no feasible point has station A, B2 or D off
(Section 1.5). That would be a different problem.
- *Resolution:* one sentence in the paper's conventions, linked to the SCIP
  finding.
- rbb encloses each decimal in [down(v), up(v)], but the implied bounds and
  vbb2 are decimal-exact, so no claim is made for the binary64 reading.

**W8 (resolved here). GAMS ≡ OSIL for 09–24 was only numerical.**
`gms_vs_osil.py` now shows exact equality for all five instances, with
negative controls. The GAMS files were already saved locally; no fetch was
needed.

**W9 (minor; scope).** waterno2_09–24 rest on the wave-2 period Lagrangian
only.
- The 18 and 24 bundles were stopped early (predicted gain about 1–2), and
  24 started from zero multipliers.
- Separator branching and cell slopes were not attempted on 09–24.
- *Resolution:* say so.
- *Cost estimates for extending separator branching to waterno2_09:*
  - for 06, the cert3 pipeline took about 22 CPU-hours and certA/certB about
    101;
  - 09 has 8 links instead of 5, and its period B&B is 2–4× harder (up to
    30k nodes per period against 8k);
  - so expect several hundred CPU-hours to reach about 3–5%, plus a similar
    amount for independent re-bounding.
- For 06 the last slope cycle gained +1.14 for about 9,500 SCIP evaluations
  and 24,478 rbb runs. Closing the remaining 4.66 would need splits in the
  wide cells at links 3 and 4 plus more slope cycles: tens to hundreds of
  CPU-hours, with falling returns and no guarantee.
- The per-period margins at the exact points (`logs/point_consistency.log`)
  show where the 09–24 gaps sit. For example, in 24 periods 8–10 and 17
  account for 166 of 388.

**W10 (minor; literature).**
- Huang 2011 is not obtained. The FU catalog calls it a Diplom thesis, and
  MINLPLib a Masters thesis; the paper should not say "MSc" without
  qualification.
- Ghaddar et al. 2015 (multi-period pump scheduling by Lagrangian
  decomposition) is listed but unread. It is the most direct mechanism
  relative and must be read before submission.
- Carøe–Schultz, SDDiP and Berenguel et al. are not in `literature/`, and
  Berenguel's read status conflicts between documents.
- *Resolution:* "new as far as found" for the instance results; no method
  novelty; read Ghaddar et al. and Carøe–Schultz, and confirm Berenguel,
  before submission. Reading only; no computation.

**W11 (minor; timings).** The wave-2 report's timings (06: 151 s wall,
550 s summed) differ from READINESS's command-index wall times (221.25 s).
They measure different things.
- *Resolution:* one source per table, with a defined measure (wall vs
  summed CPU, workers, shared machine).

**W12 (resolved here). The consistency evidence for 09–24 was thin.**
Before this dossier, only two 09–24 periods had negative controls against
near-feasible points. Now:
- all 63 period bounds (and the 6 of 06) lie below the exact period values
  of exactly feasible points;
- every implied-bound file is satisfied by those points;
- the gap decomposes exactly into per-period margins, because the horizon
  row is active at the points.

**W13 (minor; model description).** waterno2_09 has two tariff values, not
three; 12–24 have three. The earlier dossier draft said "three" for 09–24.

**W14 (minor; review coverage).** The primal review r1 received a report
text truncated in §2 step 2. It verified every numerical claim with its own
evaluator, but did not read the rest of the method text. Validity rests on
the exact checks alone, which r1 reproduced.
- *Resolution:* say so in the verification table. Optionally, a reader pass
  of report §2 (reading only).

## 9. What the paper may and must not claim

**May claim (suggested wording).**
- "For waterno2_06 we prove 278.230573 ≤ OPT ≤ 282.888038, a relative gap
  (primal − dual)/dual of at most 1.68% (absolute gap at most 4.6575). The
  best dual bound listed on MINLPLib is 165.1902989 (SCIP), a listed gap of
  71.25%."
- "For waterno2_09, _12, _18 and _24 we prove dual bounds 824.834692,
  2089.754565, 4790.820715 and 6576.151388, 3.0–6.2 times the best listed
  dual bounds. We give exactly feasible points of value at most 914.012,
  2233.821346, 5023.983 and 6963.795181, which improve the listed primal
  values. The remaining gaps are at most 10.82%, 6.90%, 4.87% and 5.90%.
  No instance is closed."
- "All bounds are valid for every exactly feasible point of the MINLPLib
  models, with decimal data read as exact rationals. The OSIL and GAMS
  files define identical models."
- "Each period or pair bound was computed by a rigorous branch and bound in
  outward-rounded floating point. It was recomputed by a second, separately
  written branch and bound whose node bounds are evaluated in exact
  rational arithmetic; either computation alone yields the stated values.
  Coverage, slope corrections, sums and the shortest path were computed in
  exact rational arithmetic and recomputed by two further implementations."
- "To the best of our knowledge, no closure and no dual bound above the
  MINLPLib-listed bounds has been published for these models." Add the
  caveats: the 2011 thesis cited by MINLPLib was not available to us, and
  the multi-period models in Huang (2019) differ from the MINLPLib
  instances.
- On the method: "The certificate combines classical ingredients:
  Lagrangian relaxation of state copies, branching on the copied
  (separator) variables, and dynamic programming over stages. Its
  cell-dependent multipliers are related to partition-dependent Lagrangian
  cuts (Yang and Yang 2025). The only coupling condition is that both
  periods adjacent to a link use the same multiplier vector for the same
  cell."
- "The listed point p4 of waterno2_06 violates a row by 1.1·10⁻¹¹; an
  exactly feasible point within 3.1·10⁻¹³ of it exists."
- The SCIP finding, worded as in `R/publication/scip-bug/report.md` §7:
  wrong optimal values up to 3.8 above exactly feasible points on period
  subproblems, a 15-variable reproducer, and a report not submitted
  unless the user files it.

**Must not claim.**
- That any waterno2 instance is solved or closed; "1.67%" as an upper
  bound.
- Novelty of the decomposition method, of cell slopes, or of Lemma 4.
- That cell slopes beat further splitting. This is "not established", and
  certification cost would weigh against slopes.
- That the bounds are checkable from stored certificate files (W1), or
  that three independent codes verified the pair bounds (W2).
- That the listed SCIP (or other) duals for waterno2 are invalid. They were
  not examined, and they are below ours.
- That the SCIP defect is confirmed upstream or explains every SCIP result.
- Any comparison with Huang's 343.41 dual or other numbers from Huang
  2019, which concern different models.
- That waterno2_03/04 are solved; "solved up to 4 periods".
- Any result for a binary64 reading of the data.
- That the waterno2_06 primal is ours (it is MINLPLib's p4, made exact).
- "MSc thesis" for Huang 2011 without qualification.

## 10. Candidate figures and tables

1. **Main table.** Section 5: listed dual, our dual, exact primal, absolute
   and relative gaps before and after, and the factor over the listed dual.
2. **Model and decomposition figure.** Network schematic (source → A → tank
   1 → B1 ∥ B2 → tank 2 → D → tank 3 → demand) above a time line of T
   periods. Show the three level copies at each boundary and the terminal
   row on the last period.
3. **Cells and paths figure.** A 2-D slice (tank 1 × tank 2 at fixed tank 3)
   of one link's partition, coloured by cell slope. Overlay p4's levels and
   certB's minimizing cells: the minimizing path leaves p4's trajectory and
   runs through wide cells at links 3 and 4.
4. **waterno2_06 progression table.** Wave 2 → cert2 → cert3 → certA →
   certB: value, gap, cells per link, distinct slopes, records used, new
   rbb runs, CPU.
5. **Where the gap sits (new data).** Per-period margins L_t(x*) − B_t at
   the exact best points, which sum exactly to f(x*) − bound; bar charts for
   06 and 24. From `logs/point_consistency.log`:
   - 06: 0.127, 2.871, 1.346, 14.083, 0.689 and 0.038;
   - 24: largest in periods 8–10 and 17.
6. **Verification table.** Who checked what, with which code, and the
   counts: 6 + 63 periods; 8,958 and 49,315 records; 556 leaf checks; 3 DP
   implementations; 21 replayed runs.
7. **Small wave-2 table for waterno2_06.** Per-period B_t, showing that
   periods 1–3 need the implied tank-3 bounds: 262.702 without them,
   263.735 with them.
8. **Optional figure.** Planning value against SCIP evaluations during the
   cell-slope phase, with the certified values marked, showing the falling
   returns per cycle.

## Appendix: commands run for this dossier

From `paper-open-minlplib/development/dossiers/waterno2-checks/`, with
`OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`:

```
bash run_all.sh /tmp/wn2d3/run         # 28 s, one core: all exact checks; logs copied to logs/
bash replay_vbb2.sh /tmp/wn2d3/replay  # 81 s wall, two workers: vbb2 replay; logs/replay_compare.log, replay_09_p06.log
```

- `run_all.sh` copies these inputs into the scratch directory:
  - OSIL files from `~/.cache/minlplib/minlplib/osil/`;
  - GAMS files from `R/publication/minlplib-status/pages/models/gms/`;
  - certificate, multiplier and implied-bound JSON files;
  - the certB pickle, the exact points, `osilx.py` and the stub loader
    `load_cs.py`.
- `replay_vbb2.sh` copies the reviewers' `vrebound_cs.py`, `run_period.py`,
  `vbb.py`, `vbb2.py`, `vmodel.py`, `vstruct.py`, `osilx.py` and their input
  files into a mirror of the `R/` layout under the scratch directory. Their
  relative paths resolve there, and nothing runs in the repository tree.
- Environment: Python 3.13.11, NumPy 2.5.1.
- No solver campaign, no long computation, no project-wide check and no CI
  was run. Nothing under `R/` or `literature/` was edited.
