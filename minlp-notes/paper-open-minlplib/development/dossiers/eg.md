# Dossier: eg_int_s, eg_disc_s, eg_disc2_s (family key `eg`)

Date: 2026-10-04 (second pass; it replaces the first draft of this file written
earlier the same day, and corrects it where noted in Section 8.5). Paths are
relative to `research-20260929/` (called R/) unless stated otherwise. Checks
of this pass are in `paper-open-minlplib/development/dossiers/checks/eg/r2/`
(scripts, `logs/`, `README.txt`); checks of the first pass are in
`checks/eg/`. All of them ran on copies under `/tmp`, never inside R/.

## Bottom line

- **Nothing found invalidates a claimed result.** I re-derived every proof
  step, re-read the bounding code of all three certificate routes, and
  recomputed the displays, gaps, primal enclosures, interval-exp constants
  and margin statistics.
- **Three certificate routes exist, and each part of each instance has at
  least two of them, computed by different code** (Section 3.4):
  - **S-I**, the search itself in outward-rounded interval mode: complete for
    eg_int_s (run H), eg_disc_s (run I) and the optimum-containing part of
    eg_disc2_s (the review's replay). It uses no library exp.
  - **S-F**, the search in fast mode: complete for all parts (runs C, E, G).
    It uses its own exp (`fexp`, no libm) and a hand-derived floating-point
    error analysis ("Lemma S").
  - **R**, the independent re-certification of every leaf (all 33,385 +
    86,796 + 1,114,361 leaves). It uses exact rational final tests, padded
    float enclosures (A1) and numpy's exp (A2).
- **The summary's qualifier "under A1/A2" describes route R only.** For
  eg_int_s, eg_disc_s and eg_disc2_s part 1, route S-I gives a certificate
  that needs neither A1 nor A2. For eg_disc2_s parts 0 and 2–7 (979,044
  leaves), the A2-free certificate is S-F, which needs Lemma S instead.
- **A1 can be removed by a written proof.** Section 3.6 gives the error
  lemma of the independent certifier ("Lemma A1"); I derived it from the code
  line by line.
- **A2 can be weakened for free and removed cheaply.**
  - Weakened, by a proof given here: the padding slack tolerates a relative
    exp error of 9.9e-14 (at least 446 ulp), against an observed 1.3e-16
    (Proposition A2′).
  - The exp actually run is Intel SVML `__svml_exp8_ha`, called by NumPy
    2.5.1's `DOUBLE_exp_X86_V4` loop. I confirmed this from the source, the
    disassembled binary and an experiment.
  - No margin argument removes A2.
  - The cheapest removal is an exp-audited rerun of route R. Measured
    inputs: 10,864 exp arguments per certified piece, and 178 ns per argument
    for a tight rigorous enclosure.
  - Cost of the audit: about 3.1–4.8 CPU-h for eg_disc2_s parts 0 and 2–7,
    or 4.3–6.4 CPU-h for every leaf, including regenerating the deleted
    eg_int_s/eg_disc_s recordings. That is 1.6–3.2 h wall time on 2 quiet
    cores (Section 8.3).
- **Display caveat.** eg_disc_s's summary display 5.760539610694994 is
  2.38e-16 above the binary64 number that routes S certify. Only route R
  certified that decimal. Print 5.760539610694993 if S routes carry the
  claim.

---

## 1. Instances and models

### 1.1 Source and provenance

- MINLPLib source: "Bram Schoonen's Model Collection", added 25 Jul 2002, no
  reference (literature report small, §9.1). No document on the origin or
  physical meaning of the models was found, so the **physical meaning is
  unknown**. The paper must not invent one.
- File dates: OSIL Last-Modified 2019-06-25, GAMS 2020-12-11
  (`publication/minlplib-status/data/tables.md`, Table A). The 2026-10-02
  refresh found the pages, points, bounds and OSIL files unchanged.
- History (`minlplib-status/data/tables.md`, rows 136–138; literature small
  §9.1):
  - The GAMS text is identical to the MINLPLib 1 copies (2001) and to the
    MINLPLib.jl copies (2017).
  - The 2001 header and table say 26 equations and 206 nonzeros, but the
    archived text has 28 rows. The 2008 GAMSlinks logs show the current size
    (28 rows, 8 columns, 220 nonzeros, 196 nonlinear). Why two rows appear in
    the record is unknown.
  - Our claims concern the current OSIL files only.
- **Model files agree exactly.** I know of four checks:
  - first review: author's OSIL decoding = independent GAMS reader, as
    Fractions, for all three instances (`reviews/eg-retry-review.md` §2);
  - review r1: OSIL = the independent certifier's data for eg_disc2_s, "MODEL
    DATA IDENTICAL" (`publication/reviews/eg-recheck-review-r1.md` §1.1);
  - literature round 2: the AMPL `.mod` rows are numerically identical to the
    OSIL rows;
  - **this pass:** my own generic OSIL parser (`r2/osil_iv.py`) decompresses
    the linear-coefficient block. It confirms that it holds exactly the 24
    objvar coefficients (value 1) of rows e1–e24, that the e25/e26 linear
    terms sit inside the nonlinear trees, and the structure claims below.
- Related instance eg_all_s (both grids at once) is solved on MINLPLib (SCIP,
  7.65775209). It is not a target.

### 1.2 The model

Write $y=s\circ x$ with an instance-specific scaling $s\in\{1,\tfrac1{10}\}^7$
(exact decimals). All three instances share **the same 28 functions** of $y$
and the same box

$$Y=[0.3,0.6]\times[0.4,1]\times[0.4,1]\times[0.7,1.5]\times[1,2]\times[3,4]\times[2,5].$$

For $k=1,\dots,28$ let

$$G_k(y)=\sum_{m=1}^{97}a_{km}\exp\Big(\sum_{i=1}^{7}\gamma_{ki}(y_i-z_{mi})^2\Big),\qquad\gamma_{ki}<0 .$$

Each instance is

$$\begin{aligned}
\min\ &\ \text{objvar}\\
\text{s.t. }&\ \text{objvar}\ \ge\ c_k+G_k(y), && k=1,\dots,24\quad(\text{e1–e24})\\
&\ G_{25}(y)-0.45\,y_3\ \le\ -0.350268824 && (\text{e25})\\
&\ G_{26}(y)-0.45\,y_2\ \le\ -0.374014485 && (\text{e26})\\
&\ -346.198237\ \le\ G_{27}(y)\ \le\ 53.8017630000004 && (\text{e27, e28};\ G_{27}\equiv G_{28})\\
&\ y=s\circ x,\quad x\ \text{in its box, integrality as below}.
\end{aligned}$$

In the OSIL, row $k$ reads $\text{objvar}+\text{nl}_k(x)\ge c_k$ (k ≤ 24) with
$\text{nl}_k=-(G_k-\text{linear part})$. Each term is stored as the product of
a weight and seven factors $\exp(\gamma_{ki}(-z_{mi}+s_ix_i)^2)$, which equals
the exponential of the sum. In eg_disc_s the e25/e26 linear terms read
$-0.045\,i_3$ and $-0.045\,i_2$, that is, $-0.45\cdot(0.1\,i)$ exactly. The
constants are $c_k\in[1.291143688,\,13.56829208]$.

| instance | variables (OSIL order) | scaling $s$ | integer part | integer combinations |
|---|---|---|---|---|
| eg_int_s | x1–x4 cont., i5, i6, i7 int. | all 1 | i5 ∈ {1,2}, i6 ∈ {3,4}, i7 ∈ {2..5} | 16 |
| eg_disc_s | i1–i4 int., x5–x7 cont. | (0.1,0.1,0.1,0.1,1,1,1) | i1 ∈ {3..6}, i2, i3 ∈ {4..10}, i4 ∈ {7..15} | 1,764 |
| eg_disc2_s | x1–x4 cont., i5–i7 int. | (1,1,1,1,0.1,0.1,0.1) | i5 ∈ {10..20}, i6 ∈ {30..40}, i7 ∈ {20..50} | 3,751 |

Each instance has 8 variables (objvar has lb −INF and no ub), 28 rows and 220
nonzeros (196 nonlinear). The objective sense is min.

**Minimax form.** objvar appears only in e1–e24, with coefficient 1, so the
problem is the minimisation of $F(x)=\max_{k\le24}(c_k+G_k(s\circ x))$ over
the $x$ that satisfy e25–e28, the bounds and integrality.

### 1.3 Structure that matters

Checked in `r2/logs/osil_iv.log` and `r2/logs/struct2.log`, and in the
review's `check_structure.log`.

- **Common centres.** All 28 rows use the same 97 centres $z_m$.
- **Common length scale per row.** Within row $k$, $\gamma_{ki}$ is the same
  for all 97 terms. Ranges over rows, per coordinate: [−46.35, −1.913],
  [−12.79, −6.148], [−12.78, −0.517], [−3.714, −0.0523], [−4.595, −0.0039],
  [−4.042, −0.0010], [−0.511, −0.0118].
- Each row therefore has the form of a Gaussian-kernel expansion on a common
  97-point design, as in an RBF network or the posterior mean of a Gaussian
  process with an anisotropic squared-exponential kernel. This is a
  **structural reading, not documented provenance.**
- **Signed weights and cancellation.**
  - $\sum_m|a_{km}|$ is 27.8–667.5 on the objective rows, 336.5 (e25), 156.8
    (e26) and 39,666.8 (e27 = e28; max $|a|=1711.4$).
  - At the eg_int_s optimum, the active row e12 has
    $\sum_m|a_{km}e^{E_{km}}|=61.4$ against $|G_{12}|=7.115$.
  - The active side row e26 has $\sum|w|=78.4$ against a Gaussian part of
    $-0.0829$.
  - So any bound that adds up term ranges loses a factor of about 8.6 to 900
    here. This explains why the wave-3 natural/mean-value interval search
    failed (eg_int_s: bound 2.43 after 603 s).
- **Active sets at the best points** (mpmath iv, `r2/logs/osil_iv.log`,
  `struct2.log`):
  - eg_int_s: objective row e12 alone; side row e26 (slack 1.49e-11, from
    the push into the interior); bound $x_3=1$.
  - eg_disc_s: e8 and e12 (within 6.5e-15).
  - eg_disc2_s: e8, e10 and e12 (within 6.1e-15); bound $x_2=1$.
- **Flat landscape** (heuristic local solves; evidence only).
  - eg_disc2_s: 75 integer combinations with a local minimum below 6.0, and
    507 below 7.0 (optimum 5.642).
  - eg_disc_s: 10 combinations below 6.0.
  - Part 0 of eg_disc2_s holds feasible points with $F-\theta^*\approx0.0066$
    (r1 `local_min.log`).

### 1.4 Point and value issues

- The listed MINLPLib points p1 are only tolerance-feasible, except for
  eg_disc2_s (review `check_primal.log`):
  - eg_int_s p1 violates e26 by 2.89e-16, and with its listed objvar it
    violates e12 by 4.57e-15;
  - eg_disc_s p1 violates e12 by 1.66e-14;
  - eg_disc2_s p1 is exactly feasible.
- Two published values lie *below* our certified duals. Both are tolerance
  artifacts (literature small §9.1, §11.1):
  - the old GAMS World point of eg_int_s, objvar 6.4531031527, violates e12
    by 6.37e-9 (interval-proved);
  - CAMINO's S-B-MIQP value 5.642100351878204 for eg_disc2_s is 2.2e-7 below
    our bound.

## 2. Listed status (MINLPLib pages, unchanged at the 2026-10-02 refresh)

| | eg_int_s | eg_disc_s | eg_disc2_s |
|---|---|---|---|
| best listed dual (instance page) | **6.32629896 (SCIP, 2025-07-31)** | **3.36596129 (SCIP, 2025-07-31)** | **0 (SHOT, 2022-02-15)** |
| other page duals | ANTIGONE −6.82078456, BARON 0.14309125, COUENNE −6.39393306, GUROBI −1.54105206, LINDO −1.20527282, SHOT 0 | ANTIGONE −5.89996559, BARON −0.2567667, COUENNE −8.08686, GUROBI −5.01379636, LINDO −4.0246301, SHOT 0 | ANTIGONE −5.22577638, BARON −5.53779193, COUENNE −8.0869773, GUROBI −5.74731082, LINDO −7.56589692, SCIP −1.48945961 |
| dual in the instance list (instances.html) | 0. | −0.2568 | −5.2258 |
| listed primal p1 (infeasibility shown) | 6.45310316 (2e-16) | 5.76053962 (9e-15) | 5.64210058 (0) |
| solved mark | no | no | no |

Sources: `publication/minlplib-status/data/part_a.json` (parsed pages; bold
marks as on the pages), `open-instances-wave3/eg/retry/logs/minlplib_pages_20260930.txt`,
`reviews/eg-retry-review-checks/data/minlplib_pages_extract.txt` and
`minlplib-status/logs/bounddates.log`. The instance-list dual differs from the
best page dual; I did not establish why. The paper should quote the page
values and say so.

## 3. The certificate

### 3.1 Idea in plain words

We branch on the 7 inputs, splitting integer coordinates at integers. On each
box, a second-order Taylor model around the box centre (with a third-order
alternative) bounds every row between two affine functions.

- The model's constant, gradient and Hessian are **signed** sums over the 97
  kernel terms. The cancellation between large positive and negative terms
  is therefore kept, and only a small Taylor remainder is bounded in absolute
  value.
- The affine bounds of the 24 objective rows and 4 side rows form a small LP:
  minimise $t$ subject to $t\ge$ every objective minorant and the relaxed
  side rows. Its dual multipliers are re-evaluated rigorously by weak duality,
  so the LP solver need not be trusted. Near the eg_int_s optimum the LP
  combines objective row e12 with side row e26 (multiplier 22.27); no single
  row gives the bound there.
- Domain reduction, a side-row infeasibility test and a Farkas test remove
  the rest.
- The search stops when every box is closed at the cutoff
  $\theta=U-\text{tol}$, $\text{tol}=10^{-9}U_0$. Then every feasible point
  has $F\ge\theta$.
- Independently, a second program takes the search tree only as a proposed
  partition. It checks exactly that the leaves cover the domain, then
  re-certifies every leaf against the claimed value, with its own enclosures
  and exact rational final tests.

### 3.2 Theorem

**Theorem (computer-assisted).** Let $P_I$ be the MINLPLib OSIL model of
$I\in\{$eg_int_s, eg_disc_s, eg_disc2_s$\}$ (files of 2019-06-25).

1. Every point $(x,\text{objvar})$ that satisfies all rows, bounds and
   integrality of $P_I$ exactly has $\text{objvar}\ge L_I$.
2. The point $x_I^*$ of Section 4 is feasible, and its optimal objvar
   $F(x_I^*)$ is at most $U_I$.

| $I$ | $L_I$ | $U_I$ | $(U_I-L_I)/L_I$ |
|---|---|---|---|
| eg_int_s | 6.4531031529331155 | 6.4531031593842275 | 9.9969e-10 |
| eg_disc_s | 5.760539610694993 (route R also certifies …994) | 5.7605396164535107 | 9.9965e-10 |
| eg_disc2_s | 5.642100574331458 | 5.6421005799711068 | 9.9957e-10 |

**Hypotheses.**

- **(H0), all routes.**
  - numpy float64 arithmetic is IEEE-754 binary64 with round-to-nearest and
    gradual underflow (numpy's default). Route R would also tolerate
    flush-to-zero, because of its absolute $10^{-300}$ pads.
  - `np.nextafter` is exact, and `np.ldexp` is exact for normal results.
  - Python `Fraction` arithmetic is exact, and `float(Fraction)` rounds
    correctly.
  - The programs do what is described here. They were reviewed, not formally
    verified.
- **Part 1 of the theorem**, per part of the domain:
  - eg_int_s, eg_disc_s, and eg_disc2_s with $i_7\in[24,27]$: **(H0) only**
    (route S-I). Independently re-verified by route R under Lemma A1 and A2′.
  - eg_disc2_s with $i_7\in[20,23]\cup[28,50]$: **(H0) and Lemma S** (route
    S-F, the authors' float error analysis; Section 3.7). Independently
    re-verified by route R under Lemma A1 and **Assumption A2′**: the vector
    exp used (`__svml_exp8_ha`) has relative error at most 9.9e-14 on the
    arguments used. Additionally certified with outward-rounded interval
    arithmetic and no libm on a sample of 10,404 leaves, including the 300
    tightest per part.
- **Part 2:** mpmath `iv` (200 bits) is correctly outward-rounded. With (H0)
  alone, the interval path of the search proves the weaker upper values
  $U'$ = 6.4531031593862185, 5.760539616455533 and 5.642100579973559
  (Section 4).

**The current summary's framing.** It states all three duals "under A1/A2";
this is route R alone. That is conservative but correct. If the paper adopts
the route structure above, it can drop A2 from the claim and keep it only as
a qualifier on the independent re-verification of eg_disc2_s parts 0 and 2–7
(Section 9).

### 3.3 Lemmas

Notation for a box $X=\{x:|x_i-c_i|\le r_i\}$ with float centre $c$: $d=x-c$.
For term $m$ of a row (row index dropped), with $t_{mi}=s_ic_i-z_{mi}$:

$$E_m(c+d)=E_{0m}+L_m(d)+Q(d),\quad L_m(d)=\sum_iv_{mi}d_i,\ v_{mi}=2\gamma_is_it_{mi},\quad Q(d)=\sum_i\gamma_is_i^2d_i^2\le0 .$$

$Q$ does not depend on $m$, because $\gamma$ is common to the row. Set
$w_m=a_me^{E_{0m}}$, $\ell_m=\sum_i|v_{mi}|r_i$ and $q=\sum_i|\gamma_i|s_i^2r_i^2$,
so $|L_m|\le\ell_m$ and $Q\in[-q,0]$. Over the root box, $\ell_m\le16.97$
(exact computation, `retry/check_ell_bound.py`).

**Lemma 1 (minimax).** $(x,\text{objvar})$ is feasible iff $x$ satisfies
e25–e28, the bounds and integrality, and $\text{objvar}\ge F(x)$.
*Proof.* Rows e1–e24 are exactly $\text{objvar}\ge c_k+G_k$, and objvar
occurs nowhere else (checked on the decompressed OSIL coefficient block). ∎

**Lemma 2 (second-order Taylor model with signed moments).** For all
$|d_i|\le r_i$,
$$G(c+d)=\underbrace{\sum_mw_m}_{G_0}+\underbrace{\sum_mw_mv_m}_{\nabla}\cdot d+\tfrac12d^\top Hd+\rho,\qquad H=\sum_mw_mv_mv_m^\top+\operatorname{diag}(2\gamma s^2)\sum_mw_m,$$
with $|\rho|\le\sum_m|w_m|R_2(\ell_m,q)$. Two valid choices are
$R_2^{\rm S}=\ell q+q^2/2+(\ell+q)^3e^{\ell}/6$ (search) and
$R_2^{\rm R}=e^{\ell}[(\ell+2q)^3/6+q(\ell+2q)]$ (independent certifier).
Linear terms of e25/e26 enter $G_0$ and $\nabla$ exactly.

*Proof (S).* With $u=L+Q$, Taylor's theorem gives
$e^u=1+u+u^2/2+u^3e^{\vartheta u}/6$ for some $\vartheta\in(0,1)$. Since
$u^2/2=L^2/2+LQ+Q^2/2$,
$$e^u=1+L+Q+L^2/2+R,\qquad R=LQ+Q^2/2+u^3e^{\vartheta u}/6 .$$
$Q\le0$ gives $u\le L\le\ell$, so $e^{\vartheta u}\le e^{\ell}$; also
$|u|\le\ell+q$. Multiply by $w_m$ and sum over $m$. The quadratic part is
$$\sum_mw_m\big(L_m^2/2+Q\big)=\tfrac12d^\top\Big(\sum_mw_mv_mv_m^\top\Big)d+\Big(\sum_mw_m\Big)\sum_i\gamma_is_i^2d_i^2 .$$

*Proof (R).* Put $\varphi(\tau)=\exp(\tau a+\tau^2b)$ with $a=L$ and
$b=Q\in[-q,0]$, and $p=a+2b\tau$. Then $\varphi'=\varphi p$,
$\varphi''=\varphi(p^2+2b)$ and $\varphi'''=\varphi p(p^2+6b)$. On $[0,1]$,
$|p|\le\ell+2q$ and $0<\varphi\le e^{\tau|a|}\le e^{\ell}$. Taylor's theorem at
$\tau=0$ gives $\varphi(1)=1+a+b+a^2/2+\varphi'''(\xi)/6$. ∎

**Lemma 3 (third-order alternative).** Also
$G(c+d)=G_0+\nabla\cdot d+\tfrac12d^\top Hd+C_3+\rho_4$ with the signed cubic
$C_3=\sum_mw_m(L_m^3/6+L_mQ)$. It satisfies

$$|C_3|\le\tfrac16\sum_{ijk}|T_{ijk}|r_ir_jr_k+\Big(\sum_i|\nabla^0_i|r_i\Big)q,\qquad T_{ijk}=\sum_mw_mv_{mi}v_{mj}v_{mk},$$

where $\nabla^0_i=\sum_mw_mv_{mi}$ excludes the linear terms. Also
$|\rho_4|\le\sum_m|w_m|R_4$, with $R_4^{\rm S}=q^2/2+\ell^2q/2+\ell q^2/2+q^3/6+(\ell+q)^4e^{\ell}/24$
or $R_4^{\rm R}=e^{\ell}[(\ell+2q)^4+12q(\ell+2q)^2+12q^2]/24$.

*Proof.* Expand to fourth order:
$u^3/6=L^3/6+L^2Q/2+LQ^2/2+Q^3/6$. Keep $L^3/6+LQ$ signed; bound the other
terms as listed. For (R), $\varphi''''=\varphi(p^4+12bp^2+12b^2)$ and
$\varphi'''(0)/6=a^3/6+ab$. Finally,
$\sum_mw_mL_m^3=\sum_{ijk}T_{ijk}d_id_jd_k$ and
$\sum_mw_mL_mQ=(\nabla^0\cdot d)\,Q$. ∎

Per row, both programs use the smaller of the two totals; both are valid.

**Lemma 4 (affine bounds).** For $|d_i|\le r_i$:
$$\tfrac12d^\top Hd\ \ge\ -\tfrac12\sum_i\max(-H_{ii},0)r_i^2-\sum_{i<j}|H_{ij}|r_ir_j .$$
If the computed gradient is $\beta$ with $|\nabla_i-\beta_i|\le\delta_i$, then
$\nabla\cdot d\ge\beta\cdot d-\delta\cdot r$. Hence
$G(c+d)\ge aL+\beta\cdot d$ with
$aL=G_0^{\rm lo}-P+Q_L-\delta\cdot r$, where $P$ is the remainder bound of
Lemma 2 or 3. The upper bound $aU+\beta\cdot d$ is symmetric. ∎

**Lemma 5 (natural enclosure).** Each exponent
$\sum_i\gamma_i(s_ix_i-z_{mi})^2$ is separable. Over a box its range is
$[\sum_i\gamma_i\max t_i^2,\ \sum_i\gamma_i\min t_i^2]$, with $\min t_i^2=0$
when $0\in[t_i^{\rm lo},t_i^{\rm hi}]$. exp is monotone, so each term's range
follows, and the row lies in the sum of the term ranges. ∎

**Lemma 6 (per-box certificates).** On a box $X$, let every row satisfy
$aL_k+\beta_k\cdot d\le g_k\le aU_k+\beta_k\cdot d$, possibly intersected with
$[n_k^{\rm lo},n_k^{\rm hi}]$. Let $\underline g_k,\overline g_k$ be the
resulting bounds over $X$, and $h_s^\pm$ the side bounds.

1. *(row)* If $c_k+\underline g_k\ge\theta$ for some $k\le24$, then $F\ge\theta$
   on $X$.
2. *(side)* If $\underline g_s>h_s^+$ or $\overline g_s<h_s^-$, then $X$ holds
   no feasible point.
3. *(LP weak duality)* For $y\in\mathbb R^{24}_+$ with $\sum y>0$ and
   $z^\pm\in\mathbb R^4_+$, every feasible $x\in X$ satisfies
   $$\Big(\sum_ky_k\Big)F(x)\ \ge\ \sum_ky_k(c_k+aL_k)+\sum_sz_s^+(aL_s-h_s^+)+\sum_sz_s^-(h_s^--aU_s)+\min_{d\in X-c}\Big(\sum_ky_k\beta_k+\sum_s(z_s^+-z_s^-)\beta_s\Big)\cdot d .$$
4. *(Farkas)* Take nonnegative multipliers on the cut rows
   $c_k+aL_k+\beta_k\cdot d-\theta\le0$ and on the side rows. If the combined
   affine function is $>0$ on all of $X$, no feasible $x\in X$ has
   $F(x)\le\theta$.

*Proof.* At a feasible $x$, $F(x)\ge c_k+g_k(x)\ge c_k+aL_k+\beta_k\cdot d$,
and the side-row expressions are $\le0$. Multiply by the multipliers, add, and
minimise the affine right-hand side over the box; the minimum is taken at a
vertex. For item 4, every combined row is $\le0$ at a feasible point with
$F\le\theta$. ∎

The multipliers may come from any LP solver. This is the safe-bound argument
of Neumaier–Shcherbina (`neumaier2004-safe-bounds-in-linear-and`). In route R
all four tests run in exact `Fraction` arithmetic on the float data; in
routes S they run in outward-rounded interval arithmetic.

**Lemma 7 (coverage, tree-free form; route R).** Suppose finitely many boxes
(leaves) contain every point of the domain: every continuous point at every
integer assignment in range. Suppose each leaf satisfies a test of Lemma 6
at level $\theta^*$, or is split into finitely many covering pieces that each
do. Then no feasible point has $F<\theta^*$. Relaxing integer coordinates to
intervals inside a leaf only enlarges the set being bounded. ∎

**Lemma 8 (invariant of the search; routes S).** In `egbb.BB.run`, every
feasible point at every moment lies in one of these:

- (a) an open box, whose key is a valid lower bound on it;
- (b) a box closed with key or bound $\ge$ the cutoff in force at its
  closure;
- (c) a domain-reduction slab or a Farkas-excluded box, where $F>\theta_t$;
- (d) a box proved infeasible.

Hence the final value $\min(\theta_{\min},\ U_{\rm fin}-\text{tol},\ \text{open keys},\ \text{forced keys})$
is a valid bound.

*Proof.*

- Children lie in the reduced box, and the reduced box keeps every feasible
  point with $F\le\theta_t$. So a parent's bound is valid for its children.
- $\theta_{\min}$ is updated before any closure at level $\theta_t$.
- When the incumbent improves inside an iteration, boxes are closed against
  the new, lower level $U_{\rm new}-\text{tol}$. Since
  $U_{\rm fin}\le U_{\rm new}$, the final term $U_{\rm fin}-\text{tol}$ covers
  them.
- Integer splits $[a,\lfloor m\rfloor]\cup[\lfloor m\rfloor+1,b]$ act on
  integral ends (domain reduction rounds them inward).
- A NaN bound is replaced by $-\infty$.
- In the reported runs, no box was open or forced closed at the end, so the
  value is $U_{\rm fin}-\text{tol}$.
- Validity does not need the incumbent to be feasible; only the gap claim
  does. ∎

**Lemma 9 (interval exp of route S-I; `kan_iv.iexp_pt_fast`).** For a float
$x$ with $|x|\le700$ (asserted): $m=\mathrm{rint}(64x/\ln2)$ and
$r\in R:=x-m\cdot[\mathrm{LN2}/64]$ in outward interval arithmetic, with
$|r|\le0.0055$ asserted. Then
$$e^x\in2^k\,[T_j^{\rm lo},T_j^{\rm hi}]\cdot\Big(\mathrm{Horner}_{\rm NI}\Big(\sum_{j\le8}R^j/j!\Big)\pm10^{-25}\Big),\qquad m=64k+j .$$

- The remainder satisfies $0.0055^9/9!\cdot e^{0.0055}=1.28\cdot10^{-26}\le10^{-25}$.
- The table satisfies $(T_j^{\rm lo})^{64}\le2^j\le(T_j^{\rm hi})^{64}$, and
  the ln 2 bracket contains $\sum_{k\le300}1/(k2^k)$ and that sum plus its
  tail bound.
- Both are **checked exactly with Fractions, without trusting mpmath**
  (`r2/logs/table_exact.log`).
- The $2^k$ scaling is exact for normal results. ∎

### 3.4 Routes: what is computed, in what arithmetic, and what must be trusted

| | route S-I (interval search) | route S-F (fast search) | route R (independent leaf re-certification) |
|---|---|---|---|
| runs | H (eg_int_s); I (eg_disc_s, 2 parts); the review's replay of run G part 1 (`reviews/eg-retry-review-checks/logs/disc2_9_ni_p1.log`) | C, E, G (all parts) | `verify_tree.py` + `indep_cert.py` on all leaves (review: eg_int_s, eg_disc_s, eg_disc2_s part 1; eg-recheck: all 8 parts of eg_disc2_s) |
| model data | OSIL via `eg_model`/`egdata`, decimals enclosed by `frac_iv` | same, midpoint floats | GAMS via own reader `gms_model.py`, floats of the decimals |
| partition | built by the search; Lemma 8 | built by the search; Lemma 8 | author's trees, recorded by replay; coverage re-proved exactly (bookkeeping; tree-free guillotine proof for eg_disc2_s) |
| enclosures | outward-rounded intervals (`ia.NI`: round to nearest, then one ulp outward); 97-term sums by float sum ± (n+2)·2u Σ\|·\|; exp by Lemma 9 | float64 with explicit error bounds (Lemma S, `egfast.py` docstring); exp by `fexp` (Cody–Waite with exact $mL_1$, degree-6 Taylor, exact table; no libm) | float64 with a-posteriori padding (Lemma A1); exp = numpy (A2/A2′) |
| per-box tests | row, side, domain reduction, LP weak duality, Farkas; all outward-rounded | same | row, side, LP weak duality, Farkas, all in exact `Fraction`; failing leaves bisected to depth 24 |
| LP | HiGHS (highspy) proposes multipliers only | same | scipy-HiGHS proposes multipliers only |
| must be trusted | (H0); the code | (H0); Lemma S; the code | (H0); Lemma A1 (proved in 3.6); A2′; the code |
| complete for | eg_int_s, eg_disc_s, eg_disc2_s part 1 | all three instances | all three instances |

What is shared between the routes:

- Route R shares only the tree shapes and the model source with the search;
  the LP multipliers are its own.
- Routes S-I and S-F share the search loop, the data loading, the LP/Farkas
  evaluation code and the exactly checked $2^{j/64}$ table. They do not
  share the enclosure arithmetic or the exp evaluation.

Hence every part has at least two certificates computed by different
enclosure and exp code, and eg_int_s, eg_disc_s and eg_disc2_s part 1 have
three.

### 3.5 Algorithm summary and runs (for the methods section)

- Best-first search in batches of 256 boxes. Continuous coordinates are
  bisected; integer intervals split at integers.
- The natural enclosure is intersected with the Taylor bounds on boxes wider
  than 1/16 of the root in some coordinate.
- Two rounds of outward-rounded interval propagation run on the affine rows,
  including the objective cut $c_k+aL_k+\beta_k\cdot d\le\theta$. Integer
  bounds are rounded inward.
- An LP over the reduced box; when it is infeasible, a phase-1 LP followed by
  the Farkas test.
- Split coordinate: the largest estimated model loss
  $r_i\sum_j|H_{ij}|r_j+r_i\partial P/\partial r_i$. The weights are the LP
  multipliers (else the leading objective row), plus every side row not yet
  proved satisfied. Without the side-row weights the first version stalled.
- Parts:
  - eg_disc_s: 2 parts on i4 ([7,11], [12,15]);
  - eg_disc2_s: 8 parts on i7 ([20,23], [24,27], …, [44,47], [48,50]);
  - the parts share one incumbent, which is valid because it is feasible for
    the whole instance.
- Primal heuristic: SLSQP on the minimax problem with the integers fixed,
  followed by a push into the interior of nearly active side rows.

| run | instance | route | processed boxes | CPU s (shared machine) | certified value (binary64 repr) | closures (lp / farkas / fbbt / row) |
|---|---|---|---|---|---|---|
| C | eg_int_s | S-F | 56,189 | 274 | 6.4531031529331155 | 343 / 5 / 57 / 27,690 |
| H | eg_int_s | S-I | 56,189 (identical logged statistics) | 2,113 | same | same |
| E | eg_disc_s | S-F, 2 parts | 62,779 + 55,973 | 726 + 650 | min(5.7605396106949955, **5.760539610694994**) | 39/5/435/30,911; 216/1/289/27,481 |
| I | eg_disc_s | S-I, 2 parts | 62,779 + **55,971** | 2,660 + 2,373 | same | part 1: 215/1/289/27,481 |
| G | eg_disc2_s | S-F, 8 parts | 1,152,830 | 12,378 (parts 0, 2–7: 10,863) | 5.642100574331458 (every part) | part 1: 918/49/2,459/63,878 |
| G-p1 (review) | eg_disc2_s part 1 | S-I | 134,607 (identical statistics) | 5,755 | same | same |

| route R | leaves (closed + slabs) | pieces evaluated | failures | smallest LP margin over θ* | time (s) |
|---|---|---|---|---|---|
| eg_int_s | 33,385 (28,095 + 5,290) | 38,173 | 0 | 7.69e-11 | 218 |
| eg_disc_s part 0 / part 1 | 46,223 / 40,573 | 67,139 / 58,243 | 0 | 6.57e-5 / 2.04e-9 | 497 / 425 |
| eg_disc2_s, 8 parts | 1,114,361 | 1,769,947 | 0 | 1.011e-9 (part 1) | 41,162 (chunk wall time, summed; load ≈ 240) |

Logs: `open-instances-wave3/eg/retry/logs/{int9_final,int9_ni3,disc9_p0,disc9_p1,disc9_ni3_p0,disc9_ni3_p1,disc2_9_p0..7}.log`;
`reviews/eg-retry-review-checks/logs/{verify_*,disc2_9_ni_p1}.log`;
`publication/eg-recheck/logs/`. Certifier statistics are summed in
`r2/logs/margins2.log`.

**Ablation** on eg_int_s (tolerance 1e-6, 900 s limit; `retry/logs/abl_*.log`):

| variant | boxes | time | result |
|---|---|---|---|
| full | 55,903 | 591 s | closed |
| without domain reduction | 57,499 | 583 s | closed |
| second-order remainder only | 66,141 | 615 s | closed |
| without the LP | 125,375 | stopped at 900 s | 6.4526561, 30,720 boxes open |

**Enclosure tightness** against wave 3. The measure is the median gap between
the sampled box minimum and the lower bound, over 64 boxes × 24 rows; it is
evidence only (`retry/logs/cmp_bounds.log`). The ratio of the wave-3 gap to
the Taylor-model gap is 3.2, 19, 15, 7.1 and 2.9 at relative box widths 0.3,
0.1, 0.03, 0.01 and 0.003.

### 3.6 Lemma A1: rounding-error analysis of the independent certifier (written out)

Code: `reviews/eg-retry-review-checks/indep_cert.py`. Let $u=2^{-53}$ and
$\gamma_n=nu/(1-nu)$. I use four standard facts.

- (F1) A decimal datum read as a float has relative error $\le u$. The data
  are $s=0.1$ (relative error $0.5u$), $\mu$, $\gamma$, $a$, the linear
  coefficients, and $c$ (exact in the final tests).
- (F2) Each of $+,-,\times$ has relative error $\le u$ in the normal range,
  and absolute error $\le2^{-1074}$ on underflow, or $<2.3\cdot10^{-308}$
  under flush-to-zero. Every such case is absorbed by an absolute pad of
  $10^{-300}$.
- (F3) A float sum of $n$ terms, in any order and with or without FMA, has
  error at most $\gamma_{n-1}\sum|x_i|$.
- (F4) A float sum of $n$ products of $k$ factors has error at most
  $\gamma_{n+k-2}\sum|\text{products}|$. This covers `einsum` without
  optimisation and any BLAS order.

Let $\varepsilon$ be the relative error of `np.exp` on the arguments used
(A2: $\varepsilon\le10^{-14}$). Each line below lists the operations the code
performs, the worst-case error (the sum of contributions), and the code's
padding.

| quantity (code) | worst-case error | code padding | headroom |
|---|---|---|---|
| $t=\mu+sx$, ends and centre (`dt`) | $u\lvert\mu\rvert+2u\lvert sx\rvert+u\lvert t\rvert$ | $10^{-15}(\lvert\mu\rvert+\lvert sx\rvert+\lvert t\rvert)+10^{-300}$ | ≥ 4.5× |
| natural exponent ends $\sum\gamma\,t^2_{\max/\min}$ | squares (u) + γ data (u) + product (u) + 7-term sum ($6u$) ≈ $9u\sum\lvert\gamma\rvert t^2$ | $10^{-14}\sum\lvert\gamma\rvert t^2_{\max}+10^{-300}$ | 10× |
| exponent at centre $E_0$ (`dE`) | $\lvert\gamma\rvert(2\lvert\tilde t\rvert+dt)dt$ from $t$ + $9u\lvert\gamma\rvert\tilde t^2$ | $\sum\lvert\gamma\rvert[(2\lvert\tilde t\rvert+dt)dt+10^{-14}\tilde t^2]$; asserted $dE<10^{-6}$ | 10× on the rounding part |
| term $w=ae^{E_0}$ (`dw`) | $(e^{dE}-1)+\varepsilon+2u$ (data $a$, product) ≤ $1.0000005\,dE+\varepsilon+2u$ | $\lvert w\rvert(1.02\,dE+1.1\cdot10^{-14})$; plus $\lvert a\rvert10^{-300}$ for $E_0<-699$; $w:=0$ for $E_0<-700$ | covers $\varepsilon\le1.07\cdot10^{-14}$ per term |
| natural term ends $a\cdot e^{E}$ | $\varepsilon$ + exp-factor rounding + product + data ≈ $\varepsilon+4u$ | factor $(1\mp10^{-14})$ on exp, then $10^{-14}$ relative + $10^{-300}$ | covers $\varepsilon\le1.95\cdot10^{-14}$ per term |
| 97-term sums: natural and $S_0$ | $\gamma_{96}=1.066\cdot10^{-14}$ × Σ\|·\| | $10^{-13}$ Σ\|·\| | 9.4× |
| moment sums $S_1$, $S_2$, $T_{ijk}$ (`e1`–`e3`) | data: $dw\,\tau^k+k\lvert w\rvert\tau^{k-1}d\tau$ (exact algebra, with $\tau=\max_i(\lvert\tilde t_i\rvert+dt_i)$, $d\tau=\max_i dt_i$); rounding $\gamma_{97..99}\sum\lvert w\rvert\tau^k$ | the same data terms + $10^{-13}\sum\lvert w\rvert\tau^k$ | 9.1× |
| constants $2\gamma s$, $2\gamma s^2$ | ≤ 3u, ≤ 5u relative | $(1+10^{-14})$ on absolute values; $10^{-13}\lvert\cdot\rvert$ on products | ≥ 20× |
| gradient $\beta$ (`egrad`) | $\lvert k_1\rvert e_1$ + 3u\|k₁S₁\| + u\|lin\| + u\|β\| | $(1+10^{-14})\lvert k_1\rvert e_1+10^{-13}(\lvert k_1S_1\rvert+\lvert\mathrm{lin}\rvert+\lvert\beta\rvert)+10^{-300}$ | ≥ 30× |
| Hessian $H$, $\mathrm{fl}(H\pm eH)$ | $\lvert k_1\rvert^2e_2+8u\lvert H\rvert$; diagonal + $\lvert k_d\rvert e_0+5u\lvert k_dS_0\rvert$; the rounding of $H\pm eH$ (≤ u(\|H\|+eH)) | $+10^{-13}\lvert H\rvert$, $+10^{-13}\lvert k_dS_0\rvert$, then $\times(1+10^{-12})+10^{-300}$ | ≥ 10× |
| quadratic bounds $Q_L,Q_U$ | ≈ $(n+2)u$ relative | $\times(1+10^{-12})\mp10^{-300}$ | ≫ |
| radius $r$ | $\mathrm{fl}(h-c)\ge(h-c)(1-u)$ | $\times(1+10^{-15})$ | 4.5× |
| $\ell$, $q$ | ≤ 12u relative | $\times(1+10^{-13})$ | ≥ 75× |
| $e^{\ell}$ | $\varepsilon$ + 2 roundings | $\times(1+10^{-14})$, and $P\times(1+10^{-12})^2$ | covers $\varepsilon\lesssim10^{-12}$ |
| remainders $P_2$, $P_3$, $P_4$, cubic | ≈ 6u per term + $\gamma_{96}$ | $\times(1+10^{-12})$ (twice for $P_3$) | ≫ |
| final $aL$, $aU$ (6-term combination) | $\gamma_5\cdot\mathrm{tot}$ | $10^{-12}\cdot\mathrm{tot}+10^{-300}$ | ≫ |

With $AW=|w|+dw\ge|w_{\rm exact}|$, Lemmas 2–5 then hold for the exact data
with the computed $aL$, $aU$, $\beta$, $n^{\rm lo}$ and $n^{\rm hi}$. The final
tests convert these floats to Fractions exactly. I derived each line from the
code; the first review (§4–5) and review r1 (§1.7, spot check) did the same.
**No error found.** The paper can include this table with F1–F4 as an
appendix lemma; A1 then stops being an assumption.

**Proposition A2′ (A2 weakened by the padding slack; no computation).** All
enclosures above remain valid if $\varepsilon\le9.9\cdot10^{-14}$, which is at
least 446 ulp.

*Proof.*

- *Taylor path.* The per-term pad $1.1\cdot10^{-14}$ covers
  $\varepsilon\le1.1\cdot10^{-14}-3u$. A larger $\varepsilon$ leaves a
  per-term excess of at most $(\varepsilon-1.067\cdot10^{-14})|w|$. That
  excess enters $S_0$, $S_1$, $S_2$, $T$ and $e_0$–$e_3$ multiplied by
  $\tau^k$, and is absorbed by the unused part of the $10^{-13}\sum|w|\tau^k$
  pads, namely $10^{-13}-\gamma_{99}=8.90\cdot10^{-14}$. In $AW$ it is
  absorbed by the $(1+10^{-12})$ factors on $P$. Hence
  $\varepsilon\le1.067\cdot10^{-14}+8.90\cdot10^{-14}=9.97\cdot10^{-14}$
  suffices.
- *Natural path.* The term pads cover $1.95\cdot10^{-14}$, and the 97-sum
  pad adds $10^{-13}-1.07\cdot10^{-14}$, so about $1.087\cdot10^{-13}$
  suffices.
- *The $e^{\ell}$ path* tolerates about $9.9\cdot10^{-13}$.
- The minimum over the three paths exceeds $9.9\cdot10^{-14}$. ∎

### 3.7 Lemma S: error analysis of the fast search models (route S-F)

The analysis is stated in the `retry/egfast.py` docstring, items (1)–(4). The
first review re-derived it by hand (`reviews/eg-retry-review.md` §4); I
re-read the code against it. In brief:

- **`fexp`.**
  - Reduction $x=m\ln2/64+r$ with a 32-bit $L_1$. $mL_1$ is exact for
    $|m|<2^{20}$, and $x-mL_1$ is exact by Sterbenz's lemma (checked on
    152,472 arguments, `retry/logs/check_fexp_r.log`).
  - $|\tilde r-r|\le10^{-18}$; degree-6 Horner with error ≤
    $\gamma_{12}e^{0.0055}+u$ and truncation $<10^{-19}$.
  - Result $2^k\,\mathrm{fl}(T_j\tilde p)(1\pm4\cdot10^{-15})$, while the
    needed factor is $(1\pm u)(1\pm2\cdot10^{-15})$.
  - The table is the exactly checked one of Lemma 9.
  - Measured relative width: 9.0e-15 (`r2/logs/fexp_audit_cost.log`).
- **Term data.** Errors: $3.1u$ per element of $t$; $(d+5)u$ terms in
  $dE$; $dw=|a|\,de(1+4u)+(1.02dE+4u)|w|$.
- **Moment sums.** $(M+3)u$ or $(M+4)u$ times $\sum|\cdot|$, then a relative
  slack of $10^{-12}$ on every derived quantity. The slack also covers the
  few-ulp error of the midpoint constants $2\gamma s$ and $2\gamma s^2$.

**Empirical cross-check.** In runs H and I and in the review's part-1 replay,
the S-I models closed exactly the same boxes as the S-F models on more than
250,000 boxes (one box earlier in run I part 1). This shows the fast bounds
are not loose, but it is not a proof of Lemma S. **For the paper:** include
Lemma S as an appendix lemma if route S-F is to carry eg_disc2_s parts 0 and
2–7 without A2.

## 4. Exactly feasible primal points

- **Construction.**
  1. SLSQP on the minimax problem with the integers fixed, started from p1
     and from the best open boxes.
  2. A push into the interior of nearly active side rows, using the smallest
     margin in $10^{-13}\ldots10^{-10}$ that certifies.
  3. Certification on the interval path (`egbb.fpoint`). The point must lie
     in the inner-rounded box, have integral integer coordinates, and satisfy
     the side rows against inner-rounded bounds.
- **Stored points.** `open-instances-wave3/eg/retry/sol/*.retry.sol`.
  - Coordinates are written as shortest decimal representations of the
    binary64 search points.
  - objvar is the 60-digit maximum of the objective rows, rounded up at the
    20th digit.

| instance | integers | continuous part | objvar in sol file |
|---|---|---|---|
| eg_int_s | (i5,i6,i7) = (2,4,3) | x = (0.564219345763436, 0.6468471890552644, 1.0, 0.9390699678023392) | 6.4531031593842274088 |
| eg_disc_s | (i1..i4) = (3,10,8,12) | (x5,x6,x7) = (1.0800209145804143, 3.485358811359775, 2.2415838244871797) | 5.7605396164535106058 |
| eg_disc2_s | (i5,i6,i7) = (11,34,24) | x = (0.339986187975027, 1.0, 0.7526242429543005, 1.2370734367691458) | 5.6421005799711067563 |

**Feasibility proofs.** exp is transcendental, so the rows are enclosed with
interval arithmetic. There are four independent evaluations; two of them are
interval proofs.

1. **IEEE-only proof (search interval path, `egtm`, Lemma 9).** It works at
   the binary64 point and proves strict feasibility and
   $F\le U'$ = 6.4531031593862185, 5.760539616455533 and 5.642100579973559
   (the `UB` of the run logs).
2. **mpmath iv, 200 bits.**
   - It works at the decimal point of the sol file.
   - The literature track used the AMPL `.mod` rows; this dossier used the
     OSIL with a generic tree walker (`r2/osil_iv.py`).
   - All bounds and integrality hold exactly, and all 28 rows are proved.
   - The smallest proved slacks are 5.57e-20 (e12), 7.80e-20 (e12) and
     7.49e-20 (e10). They come from the rounding up of objvar.
   - Enclosures of $F(x^*)$:
     6.45310315938422740874425550708789…,
     5.76053961645351060572199741916493…,
     5.64210057997110675622508108759233…, each below the sol objvar.
3. **Retry, 50 digits.** `retry/verify_primal.py` with `ev.py`: zero
   violations. This is a high-precision evaluation, not an interval proof.
4. **Review, 60 digits.** An independent GAMS reader
   (`reviews/eg-retry-review-checks/logs/check_primal.log`): exact match to
   the printed digits. Also not an interval proof.

The decimal point of the sol file and the binary64 search point differ by
less than half an ulp per coordinate. Each is proved feasible by its own
evaluation; the paper should name the decimal point (item 2), since that is
what the sol file and the $U$ column refer to.

**Objective upper ends (safe 17-digit displays):** 6.4531031593842275,
5.7605396164535107 and 5.6421005799711068.

## 5. Numbers table

| | eg_int_s | eg_disc_s | eg_disc2_s |
|---|---|---|---|
| best listed dual | 6.32629896 (SCIP) | 3.36596129 (SCIP) | 0 (SHOT) |
| our dual, safe display | **6.4531031529331155** | **5.760539610694993** (summary: 5.760539610694994, valid by route R only) | **5.642100574331458** |
| binary64 value certified by the search | 6.4531031529331155383… (display − binary = −3.83e-17) | 5.7605396106949937618… (…994 − binary = +2.38e-16) | 5.6421005743314580627… (−6.27e-17) |
| primal, rounded up | 6.4531031593842275 | 5.7605396164535107 | 5.6421005799711068 |
| absolute gap (display dual vs primal display) | 6.4511120e-9 (≤ 6.46e-9) | 5.7585167e-9 (…994) / 5.7585177e-9 (…993) (≤ 5.76e-9) | 5.6396488e-9 (≤ 5.64e-9) |
| relative gap (÷ dual) | 9.9969e-10 | 9.9965e-10 | 9.9957e-10 |
| relative gap against IEEE-only $U'$ | 9.99999976e-10 | 9.9999989e-10 | **1.0000000754e-9** |
| improvement over listed dual | 0.12680 | 2.39458 | 5.64210 |
| 1-h campaign, best final dual (BARON 26.5.27, GUROBI 13.0.2, SCIP 10.0.3; none closes) | SCIP 5.43888535430 | SCIP 2.71549916578 | SCIP −2.83013002499 |

Sources:

- duals: `open-instances-summary.md` (authoritative) and the run logs of 3.5;
- exact binary64 values and all gaps: `r2/logs/displays.log` (Fractions);
- primal values: the sol files and Section 4;
- campaign: `publication/solver-runs/results_table.md` rows 57–65.

**Disagreements found.**

- The summary display 5.760539610694994 holds only through route R (see 3.2).
- `retry.md` §1 prints the primal values 6.4531031593842274 and
  5.7605396164535106. These truncate the sol objvars, which makes them 8.8e-18
  and 5.8e-18 *below* the proved objective values. As upper-bound displays
  they are unsafe; use the summary's values.
- "≤ 1e-9 relative" holds against the mpmath-enclosed (or 50/60-digit)
  objective. Against the IEEE-only value $U'$, eg_disc2_s's gap is
  1.0000000754e-9. This is by construction: the bound is
  $U'-10^{-9}U'_0$, computed in floating point.

## 6. Verification record

| review | date | independent of the author? | what it checked | verdict |
|---|---|---|---|---|
| `reviews/eg-retry-review.md` | 2026-10-01 | yes; own GAMS reader and certifier (route R) | exact decoding; primal points at 60 digits; the mathematics and `egfast` analysis by hand; tree replays (logs identical); exact coverage bookkeeping; every leaf of eg_int_s and eg_disc_s and of eg_disc2_s part 1 re-certified (route R), plus 110,676 sampled leaves of the other parts; negative/positive controls; S-I replay of eg_disc2_s part 1; literature | **verified**; 5 minor items, all applied (retry §10) |
| `reviews/eg-retry-confirm-r1.md` | 2026-10-01 | yes (fresh) | the corrections: exact `fexp` reduction check (TwoSum), ℓ ≤ 16.97, `dual_value` guard (never acted in 993,781 calls of the guarded reruns of A–E, G–I) | **verified**; 2 optional nits, applied and confirmed (`round4-nits-confirm.md`) |
| `publication/eg-recheck/report.md` | 2026-10-01/02 | a track reusing the review's certifier | replay of all 8 run-G trees (logs identical); **all 1,114,361 leaves** certified against θ* (0 failures); tree-free volume identity + 10⁶ random points per part; negative controls; `check_exp.py` (1,506,237 arguments, max 1.315e-16 = 1.18u, numpy 2.5.1, AVX512F/AVX512_SKX) | result under A1/A2 |
| `publication/reviews/eg-recheck-review-r1.md` | 2026-10-02 | yes | own bookkeeping; **exact tree-free guillotine coverage proof** (8 parts + domain); OSIL = certifier data; own outward-rounded interval certifier (no libm) on **10,404 leaves** of parts 0 and 2–7 (300 tightest + 1,000 random + 200 lowest-F per part; 117,214 pieces; 0 failures); float consistency check of every leaf; spot check of A1 | **verified, minor issues** (resolved 2026-10-03) |
| integration and minor-fixes reviews r1/r2 | 2026-10-03/04 | yes | displays, counts, the eg_disc_s display caveat, timing labels | issues resolved |
| this dossier (two passes) | 2026-10-04 | not a review | re-derivation; Lemma A1 and Proposition A2′; exp dispatch path; own OSIL parse and primal interval check; exact displays and gaps; exact interval-exp constants; margins; sensitivities; audit costs | no error that affects a result (Section 8) |

**Remaining assumptions and evidence gaps.**

- Route R needs A2, or A2′ with Proposition A2′. A1 is now a written lemma
  that still needs a referee's check.
- Route S-F needs Lemma S, a hand analysis reviewed once.
- All routes need (H0) and code correctness. Nothing is formally verified.
- Coverage of eg_int_s and eg_disc_s under route R rests on the logs of
  `verify_tree.py`; the recordings `rec_int.npz` and `rec_disc_p*.npz` were
  deleted after the review. Routes S do not need them (Lemma 8).
- Part 2 of the theorem at the displayed $U$ needs mpmath iv. With (H0) only,
  the bound is $U'$.

## 7. Relation to prior work

**On these instances** (literature small §9–11; summary table):

- **Göß, Burlacu, Martin, J. Glob. Optim. 94 (2026) 951–996**
  (`go2026-parabolic-approximation-relaxation-for-minlp`), Table 17, p. 988.
  SCIP 8.1 and Gurobi 11.0.1, 8 threads, 4 h.
  - eg_int_s, original model: SCIP solved it in 9,085.1 s (6.5/6.5). This is
    a floating-point solve, very likely to GAMS's default optCR = 1e-4
    (inferred from the repository; not stated in the paper).
  - eg_disc_s: 3.6/5.8, with an asterisk: the instance is excluded for
    "numerical and/or memory errors".
  - eg_disc2_s: −1.1/6.3.
  - The headers read "primal | dual", but only the reverse fits.
  - The publisher correction (doi:10.1007/s10898-026-01614-9; 47 pages) was
    **not read**.
- **CAMINO** (Ghezzi, Van Roy, Sager, Diehl, MPC 2026;
  `ghezzi2024-camino-a-mixed-integer-nonlinear`; public data
  `ghezzi2026-camino-benchmark-results-for-nonconvex`).
  - Gurobi 13.0.0 reported best bound = objective before its time limit:
    11.65415903480683, 6.191829847658548 and 5.88669499573929.
  - Our interval-proved feasible points (for the `.mod` rows) are lower by
    5.201056, 0.431290 and 0.244594. So these optimality claims are wrong.
  - The termination status is not recorded, and the cause is unknown. The
    argument assumes CAMINO's local `.mod` copies equal MINLPLib's.
- **Primal-only results:** Cristofari, Di Pillo, Liuzzi, Lucidi, JOTA 209
  (2026) 38 (`cristofari2026-an-augmented-lagrangian-based-method`); D'Ambrosio's
  habilitation thesis "Solving well-structured MINLP problems" (stored under
  the misleading slug `rovatti2014-optimistic-milp-modeling-of-non`; cite it
  by title), which reprints "A storm of feasibility pumps"; the 2008 COIN-OR
  GAMSlinks runs (BARON 8.1.5: primal 6.45310315899, bound −8.0807).
- **Novelty.** For eg_disc_s and eg_disc2_s, no valid prior closure was
  found. eg_int_s was already solved in floating point; ours is the first
  rigorous certificate found.

**On the mechanisms** (all classical; the contribution is the application and
the certificates):

- **Taylor models and centred forms.** Berz–Makino, "Rigorous global search
  using Taylor models" (`berz2009-rigorous-global-search-using-taylor`);
  Neumaier, "Taylor forms – use and limits" (`neumaier2003-taylor-formsuse-and-limits`).
  Neumaier's §12, "Cancellation effects", explains exactly why keeping the
  polynomial part signed beats interval evaluation on sums with cancellation.
  The paper must not present this as new.
- **Reliable affine relaxations + LP inside interval B&B.** Ninin, Messine,
  Hansen, "A reliable affine relaxation method for global optimization"
  (`ninin2015-a-reliable-affine-relaxation-method`). They build per-box
  affine relaxations (from affine arithmetic) as an LP with the problem's own
  dimensions, and derive safe bounds and infeasibility certificates. This is
  the closest methodological antecedent; our affine bounds come from a
  second-order Taylor model instead. On affine arithmetic, see also
  `stolfi2003-an-introduction-to-affine-arithmetic` and
  `messine2002-extensions-of-affine-arithmetic-application`.
- **Safe LP bounds from approximate multipliers.** Neumaier–Shcherbina
  (`neumaier2004-safe-bounds-in-linear-and`); Jansson 2004
  (`jansson2004-rigorous-lower-and-upper-bounds`, metadata only locally).
  On exact and verified MIP reasoning: Eifler–Gleixner (`eifler2024-safe-and-verified-gomory-mixed`).
- **Interval B&B, constraint propagation and FBBT.**
  `neumaier2004-complete-search-in-continuous-global`,
  `schichl2005-interval-analysis-on-directed-acyclic`,
  `vu2009-interval-propagation-and-search-on`,
  `belotti2012-on-feasibility-based-bounds-tightening`,
  `kearfott1996-rigorous-global-search-continuous-problems`,
  `hansen2004-global-optimization-using-interval-analysis`; Rump's survey
  `rump2010-verification-methods-rigorous-results-using`.
- **Rigorous or verified branching for nonlinear inequalities.**
  `smith2015-a-rigorous-generic-branch-and`,
  `narkawicz2014-a-formally-verified-generic-branching`,
  `solovyev2013-formal-verification-of-nonlinear-inequalities`.
- **Cluster problem.** `du1994-the-cluster-problem-in-multivariate`,
  `wechsung2014-the-cluster-problem-revisited`,
  `kannan2017-the-cluster-problem-in-constrained`. At the eg_int_s optimum, an
  objective row and a side row are active and $x_3$ is at a bound. The LP's
  first-order combination supplies the needed convergence order; the ablation
  agrees (without the LP, 30,720 boxes remain open). This is a reading of the
  evidence, not a test of the theory.
- **Gaussian-process / kernel models in deterministic global optimization.**
  Schweidtmann et al., "Deterministic global optimization with Gaussian
  processes embedded", MPC 2021, reprinted as chapter 3 of
  `schweidtmann2021-global-optimization-of-processes-through`. Their
  McCormick relaxations are propagated term by term and lose the
  cancellation of 1.3. That remark is an argument; it was not measured.
- **Accuracy of the library exp** (for A2): NumPy 2.5.1 source and tests
  (`umath-validation-set-exp.csv`: 238 float64 points within 1 ulp); Intel
  SVML HA documentation (vendor statement, not checked here); Tang 1989 on
  table-driven exp, cited in NumPy's source comment (not in the local KB).

## 8. Critical examination

### 8.1 Re-derivation

I re-derived the following and found no error:

- Lemmas 1–9, including both remainder families. The author sums the cubic
  with multiplicities 6/3/1 over $i\le j\le k$; the reviewer sums over
  ordered triples. Both are correct.
- The weak-duality and Farkas tests (also by reading `egbb._combine`,
  `dual_value` and `farkas`, and `indep_cert._combine`, `_dual_value` and
  `_farkas`). Side bounds are rounded outward in S and exact in R;
  $c_k^{\rm lo}$ is used in S, and $c_k$ exact in R.
- Domain reduction (`egbb.fbbt`): with
  `rest = tot − tmin_i` ≤ $\sum_{j\ne i}$ lower bounds, the bounds `qp`/`qn`
  are rounded outward.
- The invariant of Lemma 8, including incumbent updates inside an iteration
  and the pre-closure `bkey ≥ θ`.
- The coverage bookkeeping of `verify_tree.py`: the slab decomposition
  (integer slabs start at the next integer), recomputed children, and
  multiset equality.
- The parts: eg_disc_s i4 ∈ [7,11] ∪ [12,15]; eg_disc2_s i7 ∈ [20,23] ∪ … ∪
  [48,50], checked exactly against the OSIL bounds (eg-recheck
  `summarize.py`, r1 `own_cover.py`).
- Lemma A1 line by line from `indep_cert.Model.natural` and `.taylor`, and
  Proposition A2′.

Points that need care in the paper:

- **Strict versus weak inequalities.** Route R proves "no feasible point with
  $F<\theta^*$"; routes S prove it for $F\le\theta$. Both give
  $F\ge\theta$.
- **The decimal θ\* in route R** is passed as a string and parsed as an exact
  `Fraction` (`verify_tree.py` → `Certifier(name, theta)`), so route R
  certifies the printed decimal itself.
- **Integer relaxation inside leaves** is sound (Lemma 7).
- **Failure modes are loud.**
  - A NaN reaching the exact tests raises in `Fraction`.
  - Non-finite `aL`/`aU` become $\mp\infty$, which gives no certificate.
  - A point box that cannot be certified recurses to depth 24 and is
    reported as a failure.
  - `iexp_pt_fast` asserts $|x|\le700$; runs H and I completed, so the
    assertion never fired.
- **Route S does not need the recorded trees.** Route R does not need the
  trees to be the search trees; it needs only exact coverage.

### 8.2 Cheap checks run for this dossier (all on /tmp copies)

| check | what | result (log in `r2/logs/` unless noted) |
|---|---|---|
| `osil_iv.py` (own code) | generic OSIL parse, linear block decompressed; structure; primal points in mpmath iv | 24 objvar coefficients only; 97 terms/row; same 97 centres in all rows; γ common per row; e27 ≡ e28; linear terms only in e25/e26; all three points feasible (slacks 5.57e-20, 7.80e-20, 7.49e-20); $F(x^*)$ enclosures as in Section 4 |
| `struct2.py` | γ ranges, $c_k$ range, side-row slacks | as in 1.2–1.3; eg_int_s e26 slack 1.492e-11 |
| `displays.py` | exact binary64 values, display safety, all gaps | Section 5 table; IEEE-only relative gaps 0.99999998e-9, 0.99999989e-9, 1.00000008e-9 |
| `table_exact.py` | Lemma 9 constants without mpmath | 64/64 table entries enclose $2^{j/64}$ (max relative width 6.6e-16); ln 2 bracket proved; LN2/64 exact; remainder 1.28e-26 ≤ 1e-25; 1/j! intervals correct |
| `exp_path.py` + source + `objdump` | which exp numpy runs | numpy 2.5.1 float64 exp loop dispatch `X86_V4`; v2.5.1 `loops_exponent_log.dispatch.c.src` (lines 666–691, 1316–1337) sends `DOUBLE_exp` to `simd_exp_f64` → `__svml_exp8_ha` when `NPY_HAVE_AVX512_SKX && NPY_CAN_LINK_SVML`, else glibc; the installed `DOUBLE_exp_X86_V4` calls `__svml_exp8_ha@plt` (6 call sites); contiguous, strided and scalar `np.exp` are bit-identical and differ from glibc 2.39 `math.exp` on 4.6% of 10⁶ arguments by exactly 1 ulp |
| `margins2.py` | recorded route-R margins of every eg_disc2_s leaf | 98,234 leaves +∞ (85,685 side, 373 Farkas, the rest split); 15 leaves < 1e-8, 58 < 1e-6, 432 < 1e-3, 2,733 < 1e-2; below 1e-6 only part 1 plus one part-5 leaf (1.40e-7); row min 4.35e-9, LP min 1.011e-9; 1,769,947 pieces (1,556,596 in parts 0, 2–7) |
| `sens.py`, `sens_int.py`, `pad_int.py` (first pass, rerun) | multipliers, sensitivity $S=\sum_ky_k\sum_m\lvert w_{km}\rvert/\sum y$, padding | tightest eg_disc2_s leaves: e8/e10/e12 (0.333/0.143/0.525), $S\approx76.5$, margin/S ≈ 1.3e-11; eg_int_s near the optimum: e12 + 22.27·e26, $S\approx1808$; padding there ≈ 2.5e-10, against the smallest eg_int_s LP margin 7.69e-11 |
| `timing.py` | certifier cost and exp load | 512 random part-1 leaves: 806 pieces in 4.3 s (5.3 ms/piece at load ≈ 10/36); **10,864 `np.exp` arguments per piece**; np.exp 1.5 ns/argument; `kan_iv.iexp_pt_fast` 600 ns/argument with relative width up to **3.45e-13** |
| `fexp_audit_cost.py` | a tight enclosure as an auditor | `fexp` 178 ns/argument, relative width 9.0e-15; np.exp passes the ε = 1e-14 audit on 4·10⁶ arguments |

### 8.3 Can A1 and A2 be removed or reduced without a full rerun?

**A1.** Yes, by writing it out (3.6). The tightness numbers show why it must
be exactly right, not roughly right. On eg_int_s, the combined padding near
the optimum (≈ 2.5e-10) exceeds the smallest leaf margin (7.69e-11). A padding
constant that was too small by a factor of about 1.3 at the critical rows
could therefore flip that leaf. The margin covers the realistic rounding error
($\gamma_{99}S\approx2\cdot10^{-11}$) only about four times over. The
lemma's headroom (≥ 4.5× per line) is what makes the leaf sound. Cost: paper
text plus a referee's check; no computation. Machine checking (for example in
Gappa or Coq) would take days and is not needed.

**A2: facts.**

- The exp used is Intel SVML `__svml_exp8_ha` (AVX-512), reached through
  NumPy 2.5.1's `DOUBLE_exp_X86_V4` for every loadable stride; otherwise
  glibc would be used (8.2).
- The arguments are $E_0,E^{\rm lo},E^{\rm hi}\in[-700,\approx0]$ (smaller
  arguments are handled by absolute pads) and $\ell\in[0,16.97]$.
- Evidence of accuracy, none of which is a proof:
  - sampled maximum 1.315e-16 relative (1.18u) over 1,531,237 arguments;
  - NumPy's own test: 238 float64 points within 1 ulp;
  - Intel's vendor statement.
- Environment of the original runs: the review's `check_libm_exp.log`
  (2026-10-01) prints numpy 2.5.1, and the recheck's `check_exp.log` (same
  first pass as the all-leaf certification) prints numpy 2.5.1 with
  AVX512F/AVX512_SKX. Per-run dispatch was not recorded (READINESS).

**A2: options.**

| option | what it achieves | cost (measured inputs in 8.2) | recommendation |
|---|---|---|---|
| (a) Proposition A2′ | A2 weakened to ε ≤ 9.9e-14 (≥ 446 ulp), about 750× the observed error | none (proved in 3.6) | state in the paper |
| (b) Re-frame the claim on routes S | A2 leaves the claim for eg_int_s, eg_disc_s and eg_disc2_s part 1 (S-I) and for parts 0 and 2–7 (S-F with Lemma S); route R becomes independent re-verification under A2′ | none computationally; write Lemma S (≈ half a day) and have it checked | **recommended** |
| (c) Prove an error bound for `__svml_exp8_ha` | removes A2 for exactly this routine | reverse-engineer vendored AVX-512 assembly; certify the table and polynomial exactly (minutes) plus a rounding analysis (expert days); version- and dispatch-specific | not recommended |
| (d) Margin argument | quantifies robustness only: tolerated *extra* exp error ≈ margin/S, e.g. 1.3e-11 at the tightest eg_disc2_s leaves and 4.3e-14 beyond A2′ at the tightest eg_int_s leaf; no tolerance is recorded for side/Farkas leaves | per-leaf $S$ needs the Taylor data of every piece (≈ 0.5–1 CPU-h for unsplit leaves; split leaves need reruns) | not recommended: it cannot remove A2, because an implementation fault has no a-priori size |
| (e) Outward-rounded recheck of small-margin leaves | done by r1 for parts 0 and 2–7 (10,404 leaves, including all with recorded margin ≤ 4.7e-3 … 7.2e-2 per part) | done | cite as robustness evidence; the other 968,640 leaves of route R still need A2′ |
| (f) **Exp-audited rerun of route R** | Wrap `np.exp` in a copy of the certifier. Keep its value, but assert $\lvert\hat e-e^x\rvert\le\varepsilon e^x$ against a tight rigorous enclosure. Decisions are unchanged, so `res/` is reproduced bit for bit. If no assertion fires, route R needs only (H0) and Lemma A1 (plus the auditor's lemma). The auditor must have relative width < 2ε: `fexp` (9.0e-15; rests on its short, already-checked lemma), or an outward-rounded interval version of the same Cody–Waite scheme (IEEE only; est. ≈ 600 ns/argument). **`kan_iv.iexp_pt_fast` is too wide** (3.45e-13; its `NI(m)·LN2_64` product is widened by an ulp of a number near 700). | Pieces: 1,556,596 (eg_disc2_s parts 0 and 2–7); 1,933,502 in all. Per piece: certification 5.3–9.2 ms (this pass at load ≈ 10; the review at load 25–45) plus audit 1.9 ms (`fexp`) or ≈ 6.5 ms (interval). **Parts 0, 2–7 with `fexp`: 11,200–17,300 s = 3.1–4.8 CPU-h (1.6–2.4 h wall on 2 cores).** All leaves: 13,900–21,500 s, plus ≈ 1,650 s to regenerate the eg_int_s/eg_disc_s recordings = 4.3–6.4 CPU-h (2.2–3.2 h wall). Interval auditor: about 6.3–8.4 CPU-h for all leaves. Under the load seen in the recheck, about 2.5× these figures. Development and testing: about 1–2 h. | **recommended** if the paper wants an A2-free *independent* certificate |
| (g) S-I replay of eg_disc2_s parts 0 and 2–7 (`EGMODEL=ni`) | an A2-free and Lemma-S-free certificate of every part, by the authors' code | 10,863 s × 3.7–7.7 (3.8 measured on part 1) = 40,000–84,000 s = 11–23 CPU-h; 6–12 h wall on 2 cores | optional; (b) + (f) are cheaper |

A variant of (f) would audit unsplit leaves by recomputing only the Taylor and
natural arguments, and rerun only the 327,384 split leaves of eg_disc2_s. It
saves perhaps 30%, but the arguments must be reproduced bit for bit; the
plain rerun is simpler.

**Conclusion.** A1 is removed by the written lemma. A2 is reduced for free to
A2′, and with re-framing (b) it is not needed for the theorem at all. Only the
*independent* route R depends on it, and that can be removed with about 3–5
CPU-h of audited rerun. No margin argument removes A2, because the leaf
margins bound what a small exp error could do, not what a faulty
implementation could do.

### 8.4 Issues found (none invalidating)

1. **The trust framing is inconsistent across documents.** The summary and
   READINESS give "A1/A2" for all three duals (route R). The closing results
   (lines 377–381) say the bounds "rest on a hand-derived floating-point
   error analysis, reproduced box for box by an interval model" (routes S).
   Neither mentions that the two kinds of route are alternative certificates.
   *Resolution:* present all three routes with their trust bases (3.4) and
   the per-part hypotheses (3.2).
2. **A2 is an unproved assumption of route R.** *Resolution:* (a) and (b)
   now; (f) if wanted (≈ 3–5 CPU-h).
3. **A1 is labelled "hand-checked".** *Resolution:* Lemma A1 (3.6), supplied
   here, for a referee's check.
4. **Lemma S is not written in paper form.** It is needed if route S-F
   carries eg_disc2_s parts 0 and 2–7 without A2. *Resolution:* turn the
   `egfast.py` docstring into an appendix lemma; no computation.
5. **eg_disc_s display.** 5.760539610694994 holds only through route R.
   *Resolution:* print 5.760539610694993 (the gap changes by 1e-15).
6. **The relative gap sits at 1e-9 by construction.** *Resolution:* write
   "relative gap below 1.0e-9 (at most 9.997e-10), with the objective of the
   feasible point enclosed in mpmath interval arithmetic". Against the
   IEEE-only enclosure, eg_disc2_s's gap is 1.00000008e-9.
7. **Evidence retention.** The recorded trees of eg_int_s and eg_disc_s were
   deleted. *Resolution:* regenerate them with `record_run.py`
   (deterministic, ≈ 1,650 s), then run `verify_tree.py` in coverage-only
   mode and r1's guillotine `own_cover.py` (minutes). This fits into (f).
8. **Stale wording in R/ documents** (for the owners; not edited here):
   - `SYNTHESIS.md` line 42 ("eg_disc2_s partly by sampling") and lines
     478–479;
   - `closing-research-results.md` lines 377–381 ("box for box"; "sample of
     leaves (110,676 of 979,044)");
   - the literature small report §9 header ("Verified: all leaves were
     re-certified independently" without A1/A2) and §10 ("Verified");
   - `retry.md` §1 primal displays (Section 5).
9. **"Same tree" and "box for box" are slightly overstated.** Run I part 1
   closed one box earlier (55,971 vs 55,973 boxes). *Resolution:* write
   "followed the same search (identical logged statistics, except one box in
   run I part 1)".
10. **A robustness remark does not generalise.** The eg-recheck report says
    the margins lie "several orders of magnitude above" the float error
    scale. That holds for eg_disc2_s (1.0e-9 against ≈ 2e-11), not for
    eg_int_s (8.3). *Resolution:* restrict the remark to eg_disc2_s.
11. **Primal-point semantics.** The IEEE-only proof is for the binary64
    point; the mpmath proof is for the decimal point of the sol file. Both
    are feasible. *Resolution:* name the decimal point and its mpmath
    enclosure in the paper; mention $U'$ as the (H0)-only bound.
12. **Literature.** The Table 17 headers are inverted; the publisher
    correction is unread; the local fulltext lacks the SCIP rows.
    *Resolution:* read the correction before citing (cost: access only).
13. **Model semantics are undocumented.** *Resolution:* describe the
    structure (common centres, common per-row length scales) as an
    observation, not as provenance.

### 8.5 Corrections to the first draft of this dossier (same file, earlier on 2026-10-04)

- The audit overhead is not "a few %". A certified piece makes 10,864 exp
  calls, so a rigorous auditor costs +1.9 ms (`fexp`) or about +6.5 ms
  (interval) per piece, against 5.3–9.2 ms per piece. The cost estimates in
  8.3 are revised accordingly.
- `kan_iv.iexp_pt_fast` cannot serve as the auditor: its relative width
  reaches 3.45e-13, which exceeds both 2·10⁻¹⁴ and 2·9.9e-14.
- The IEEE-only relative gaps are 0.99999998e-9, 0.99999989e-9 and
  1.00000008e-9, not "1.0000000010e-9" for all three.
- Neumaier's "Taylor forms – use and limits" and Schweidtmann et al.'s GP
  paper *are* in the local KB (slugs above). Ninin–Messine–Hansen 2015 is
  added as the closest methodological antecedent.
- The A2 analysis now also uses route S-F (Lemma S), so A2 can be dropped
  from the theorem without any computation.

### 8.6 Does anything invalidate a claimed result?

**No.** Every dual bound has at least two certificates from different
enclosure code (Section 3.4), and eg_int_s, eg_disc_s and eg_disc2_s part 1
have one in outward-rounded interval arithmetic without libm. Every primal
point is proved feasible by two interval evaluations. The only display that
needs care is eg_disc_s's (issue 5).

## 9. What the paper may claim and must not claim

**May claim (suggested wording).**

- "For the MINLPLib models eg_int_s, eg_disc_s and eg_disc2_s, we prove,
  with computer assistance, that every feasible point has objective value at
  least 6.4531031529331155, 5.760539610694993 and 5.642100574331458. We
  exhibit feasible points with objective values at most 6.4531031593842275,
  5.7605396164535107 and 5.6421005799711068 (relative gaps below 1.0·10⁻⁹;
  objective values enclosed in interval arithmetic)."
- Rigor sentence, recommended version (re-framing (b), no new computation):
  "The bounds are certified by a branch and bound in outward-rounded interval
  arithmetic (eg_int_s, eg_disc_s, and the part of eg_disc2_s that contains
  the optimum). For the remaining parts of eg_disc2_s, they are certified by
  the same search with explicit floating-point error bounds and a library-free
  exponential (Appendix X). An independent program re-certified every leaf of
  all three search trees, with exact rational final tests and an exact
  coverage check. Its enclosures rely on a rounding-error lemma
  (Appendix Y) and on the assumption that the vectorised library exponential
  it calls (Intel SVML, via NumPy 2.5.1) has relative error at most
  9.9·10⁻¹⁴; the observed maximum is 1.2·2⁻⁵³."
- After option (f), replace the last clause with "…and every exponential
  value it used was verified against a rigorous enclosure."
- "To the best of our knowledge, these are the first rigorous dual
  certificates for all three instances and the first global closures of
  eg_disc_s and eg_disc2_s. eg_int_s had been reported solved in floating
  point by SCIP 8.1 [Göß, Burlacu, Martin 2026], very likely to a relative
  gap of 10⁻⁴." Qualify: this rests on a literature search, not on proof of
  novelty.
- "The best dual bounds listed on MINLPLib (6.32629896, 3.36596129 and 0)
  are improved by 0.127, 2.395 and 5.642. In our one-hour single-thread runs,
  BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3 closed none of the three."
- "Optimality claims of Gurobi 13.0.0 recorded in the CAMINO benchmark data
  (11.654, 6.1918, 5.8867) are contradicted by feasible points whose
  objectives are lower by 5.20, 0.431 and 0.245." Add: the termination
  status is not recorded, and the cause is unknown.
- On the method: "a Taylor-model / LP-relaxation / FBBT branch and bound in
  the tradition of [Berz–Makino; Neumaier 2003; Ninin–Messine–Hansen 2015]".
  What made it work here is keeping the signed cancellation among the 97
  kernel terms (evidence: the tightness ratios and the failure of wave 3) and
  the per-box LP over the 24 minimax rows (evidence: the ablation).

**Must not claim.**

- That eg_int_s was solved for the first time.
- An exact optimal value. Only the enclosure $[L,U]$ is known.
- "Assumption-free" or "verified in interval arithmetic on every leaf" for
  eg_disc2_s parts 0 and 2–7, unless option (f) or (g) is run. Without them
  the A2-free certificate there rests on Lemma S.
- The display 5.760539610694994 without the route-R qualification.
- "Box-for-box identical" interval replays.
- A diagnosis of Gurobi's error, or that its run "terminated optimally".
- Novelty of Taylor models, safe LP bounds, FBBT or affine relaxations.
- A physical or GP-training provenance of the models.
- Feasibility of the listed p1 points of eg_int_s and eg_disc_s; they are
  feasible only to tolerance.
- Any value below $L$ as a solution value (old GAMS World 6.4531031527;
  CAMINO S-B-MIQP 5.642100351878204).
- That leaf margins are far above floating-point error for all three
  instances (issue 10).
- "Relative gap ≤ 10⁻⁹" without saying that the objective is enclosed with
  mpmath intervals.

## 10. Candidate figures and tables

1. **Table: instances and results.** Structure (1.2 table), listed dual and
   primal, our $L$ and $U$, absolute and relative gaps, improvement (merges
   Sections 2 and 5).
2. **Table: certificate routes and trust bases** (3.4), with a per-part
   coverage matrix: rows are eg_int_s, eg_disc_s p0/p1 and eg_disc2_s p0–p7;
   columns are S-I, S-F, R and the r1 interval sample.
3. **Table: run statistics** (3.5): processed boxes, leaves, pieces,
   certificate types, CPU time, and the CPU-time ratios of the interval mode.
4. **Figure: enclosure tightness against box size.** Log-log median gap for
   wave 3, natural and Taylor-model enclosures, ρ = 0.3 … 0.003 (data:
   `retry/logs/cmp_bounds.log`).
5. **Figure: cancellation.** For e12 and e26 at the eg_int_s optimum, bars of
   $\sum|w|$ against $|G|$ (61.4 vs 7.115; 78.4 vs 0.083). Optionally add the
   natural-enclosure width against the Taylor-model width on one small box.
6. **Figure: ablation convergence** on eg_int_s. Lower bound against
   processed boxes, with and without the LP (`retry/logs/abl_full.log`,
   `abl_nolp.log`).
7. **Figure: histogram of route-R leaf margins** for eg_disc2_s, log scale, by
   certificate type. Mark the +∞ leaves and r1's interval sample (data:
   `publication/eg-recheck/res/`, `r2/margins2.py`).
8. **Appendix lemma tables:** Lemma A1 (3.6), Lemma S (3.7) and the A2
   options with costs (8.3), the latter for the reproducibility appendix.

---

### Commands run for this pass

All ran in `/tmp/egd2` copies, single-threaded (`OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`), one process at a time, under `timeout`. No
project-wide checks, no CI, nothing under R/ or literature/ modified, no
commit.

- `cp` of the OSIL files, sol files, `publication/eg-recheck/res/*.npz`,
  `reviews/eg-retry-review-checks/{indep_cert.py,gms_model.py,data/*.gms}`,
  and `kan/kan_iv.py` and `small/ia.py` into `/tmp/egd2`.
- `python3 osil_iv.py eg_int_s eg_disc_s eg_disc2_s`, `struct2.py`,
  `displays.py`, `exp_path.py`, `margins2.py`; `(kiv) table_exact.py`,
  `fexp_audit_cost.py`; `(ic) timing.py`, and the first-pass `sens.py`,
  `sens_int.py` and `pad_int.py`. Scripts and logs are copied to
  `paper-open-minlplib/development/dossiers/checks/eg/r2/`.
- `curl` of NumPy v2.5.1 `numpy/_core/src/umath/loops_exponent_log.dispatch.c.src`,
  `numpy/_core/tests/test_umath_accuracy.py` and
  `numpy/_core/tests/data/umath-validation-set-exp.csv` from
  raw.githubusercontent.com.
- `nm` and `objdump -d` of the installed `_multiarray_umath` (symbols
  `DOUBLE_exp_X86_V4`, `__svml_exp8_ha`); `numpy.lib.introspect.opt_func_info`.
- Read-only inspection (`sed`, `grep`) of the reports, logs and code cited
  above.
