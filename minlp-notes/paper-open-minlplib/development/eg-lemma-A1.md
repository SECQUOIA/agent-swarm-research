# Lemma A1: rounding-error analysis of the independent eg certifier, with audited exp and powers

Date: 2026-10-04. Scope: route R of the eg dossier (`development/dossiers/eg.md` §3.4), the
independent re-certification of every leaf of the search trees of eg_int_s, eg_disc_s and
eg_disc2_s. This note replaces the dossier's §3.6 table and Proposition A2′. It applies the
critique's corrections C1 (integer powers), C9 (no flush-to-zero claim) and C10 (roundings of
the padding operations themselves).

Code (all under `development/eg-audit/`):

- `cert/indep_cert_audit.py`: the review's certifier `reviews/eg-retry-review-checks/indep_cert.py`
  with every `np.exp` and every `**` result passed to the auditor. `tests/check_copies.py`
  undoes the wrappers mechanically and recovers the original file line for line. So the audited
  run computes exactly the values the original computes.
- `cert/auditor.py`: the auditor (Lemma E below). It is new code. It shares nothing with the
  author's `fexp`, `kan_iv` or `ia`, or with review r1's `own_ia.py`.

Line references below are to `indep_cert_audit.py`. The original line numbers are 12 to 15
lower in `natural` and `taylor`.

## 1. The statement

**Data and exact row functions.** The certifier reads the GAMS files with exact rationals:
weights $a^*_{km}$, centres $\mu^*_{kmi}$, length scales $\gamma^*_{ki}<0$ (common to the 97
terms of a row), scalings $s^*_i\in\{1,\tfrac1{10}\}$, linear coefficients $\lambda^*_{ki}$, and
the right-hand sides. For row $k$ and $x\in\mathbb R^7$,

$$g^*_k(x)=\sum_{m=1}^{97}a^*_{km}\exp\Big(\sum_{i=1}^7\gamma^*_{ki}\big(\mu^*_{kmi}+s^*_ix_i\big)^2\Big)+\sum_i\lambda^*_{ki}x_i .$$

Row $k\le24$ reads $\text{objvar}\ge c_k+g^*_k(x)$; rows 25–28 bound $g^*_k$ from above or below.
The float data are $A=\mathrm{fl}(a^*)$, $MU=\mathrm{fl}(\mu^*)$, $GA=\mathrm{fl}(\gamma^*)$,
$S=\mathrm{fl}(s^*)$ and $LIN=\mathrm{fl}(\lambda^*)$.

**Hypotheses.**

- **(H0) Arithmetic.** numpy float64 arithmetic is IEEE-754 binary64 with round-to-nearest-even
  and gradual underflow (numpy's default). Python `int` and `Fraction` arithmetic is exact, and
  `float(Fraction)` is correctly rounded. Comparisons, `abs`, `max`, `min`, `where`, `clip` and
  `floor` are exact, and so are `rint` and int64 operations (used by the auditor). Sums and dot
  products may be evaluated in any order, with or without FMA.
- **(E) Exponentials.** Let $\varepsilon=10^{-14}$. For every call `np.exp(x)` that `natural` or
  `taylor` makes for a box, with result $y$: if $x\ge-708$ then $|y-e^x|\le\varepsilon e^x$; if
  $x<-708$ then $0\le y\le2^{-1020}$.
- **(P) Powers.** For every evaluation `x ** k` there ($k\in\{2,3,4\}$; arguments $\tau$, $p$
  and $S$): $x\ge0$ and $|y-x^k|\le\varepsilon x^k$.

(E) and (P) are checked, call by call, by the audit (Section 4). They are hypotheses of
Lemma A1 and conclusions of the audit.

**Lemma A1.** Assume (H0), and assume (E) and (P) for the calls made for a box
$X=[lo,hi]$ (floats, $lo\le hi$; integer coordinates relaxed to intervals). Let `natural`
return $n^{lo}_k,n^{hi}_k$ and `taylor` return the centre $c$, the gradient $\beta_k$ and the
constants $aL_k,aU_k$. Then for every row $k$ and every $x\in X$:

1. $n^{lo}_k\le g^*_k(x)\le n^{hi}_k$;
2. $aL_k+\beta_k\cdot(x-c)\le g^*_k(x)\le aU_k+\beta_k\cdot(x-c)$.

Infinite values satisfy these trivially; the certifier ignores them. A NaN would make the
exact tests raise an error.

**Consequence (route R).** `Certifier._one` evaluates the tests of Lemma 6 of the dossier (row
bound, side-row infeasibility, LP weak duality and Farkas). It does so in exact `Fraction`
arithmetic, on these floats and on the exact box $[lo-c,\ hi-c]$ of $d=x-c$. With Lemma A1 every
passed test is a proof for the exact model. With the coverage lemma (Lemma 7 of the dossier)
this gives:

**Theorem R.** Assume (H0). Assume that the programs do what is described here; they were
reviewed, not formally verified. Assume that, for every instance $I$:

- (i) the leaves cover the domain (exact bookkeeping, and a tree-free guillotine proof);
- (ii) every leaf passes a test at $\theta^*_I$, possibly after splitting;
- (iii) the audit reports no violation of (E) or (P) for any piece of any leaf.

Then every feasible point of $I$ has objective at least $\theta^*_I$, where
$\theta^*_I$ is 6.4531031529331155 (eg_int_s), 5.760539610694994 (eg_disc_s) and
5.642100574331458 (eg_disc2_s). Route R parses these decimals exactly. For eg_disc_s, routes S
certify only the binary64 number 2.38e-16 below this decimal (dossier §3.2).

Theorem R removes assumptions A1 (now this lemma), A2 (now (E)) and the pow hypothesis of
critique C1 (now (P)). (E) and (P) are established by computation, together with the
auditor's lemma (Lemma E), whose constants are checked in exact rational arithmetic.
Remaining trust base: (H0) and the correctness of the code. The certifier was reviewed; the
auditor, the audit wrappers and the drivers are new and still need an independent review. mpmath
is used only on the primal side (unchanged).

## 2. Rounding facts and notation

Let $u=2^{-53}$, $\gamma_n=nu/(1-nu)$ and $\eta_0=2^{-1075}$. A hat or "fl" denotes a computed
value. "Exact value of a code expression" means its value with every operation done in real
arithmetic on the same floats and float constants.

- **(F0) One operation.** If $z$ is the exact result of $+,-,\times,\div$ on floats and $\hat z$
  the rounded one:
  - $|\hat z-z|\le u|\hat z|$, and $|\hat z-z|\le u|z|$;
  - plus $\eta_0$ for $\times$ and $\div$ when the result is subnormal;
  - a sum or difference that is subnormal is exact;
  - rounding is monotone: $z_1\le z_2$ implies $\hat z_1\le\hat z_2$.
- **(F1) Data.** `float` of a rational has relative error at most $u$. $S=1$ is exact.
  $S=\mathrm{fl}(0.1)$ exceeds $0.1$ by a relative $0.5u$, so $S\ge s^*$ and $S^2\ge s^{*2}$.
- **(F2) Sums.** A float sum of $n$ terms, in any order, has error at most
  $\gamma_{n-1}\sum|x_i|$.
- **(F3) Sums of products.** A float sum of $n$ products of $k$ factors (`einsum`, any order,
  with or without FMA) has error at most $\gamma_{n+k-2}\sum|\text{products}|$.
- **(F4) Computed pads.** A nonnegative expression with nonnegative float operands, evaluated
  with $j$ operations $+,\times$, is computed with a value of at least $(1-u)^j$ times its exact
  value, apart from underflow terms (see the next paragraph).
- **(F5) Directed steps.** Let $v,e\ge0$ be floats.
  - $\mathrm{fl}(v-e)\le(v-e)+u\,|\mathrm{fl}(v-e)|$.
  - $\mathrm{fl}(v\cdot(1+\delta))$ with the float $1+\delta$ lies within a relative $u$ of
    $v(1+\delta)$.
  - So a pad applied by a float operation must exceed the error it covers by $u$ times the
    padded value. This is the critique's C10, included in every line below.

The float constants of the code are (exact binary64 values; computed with `Fraction`):

| constant in code | binary64 value |
|---|---|
| `1e-15`, `1e-14`, `1e-13`, `1e-12`, `1.1e-14`, `1.02` | within a relative $8\cdot10^{-17}$ of the decimal |
| `1 - 1e-14`, `1 + 1e-14` | $1\mp9.992007\cdot10^{-15}$ |
| `1 + 1e-15` | $1+1.110223\cdot10^{-15}$ |
| `1 + 1e-13` | $1+9.992007\cdot10^{-14}$ |
| `1 + 1e-12` | $1+1.000089\cdot10^{-12}$ |

Values used: $u=1.110\cdot10^{-16}$; $\varepsilon=10^{-14}=90.07u$;
$\gamma_6=6.66\cdot10^{-16}$; $\gamma_{96}=1.066\cdot10^{-14}$; $\gamma_{97}=1.077\cdot10^{-14}$;
$\gamma_{98}=1.088\cdot10^{-14}$; $\gamma_{99}=1.099\cdot10^{-14}$; $\gamma_{343}=3.81\cdot10^{-14}$.

**Underflow.** Each final output carries an absolute pad of $10^{-300}$ as its last
operation: `glo`/`ghi` (lines 134–135) and `aL`/`aU` (lines 229–230).

- Every other underflow error is an absolute $\eta_0\approx2.5\cdot10^{-324}$ from one product.
  It reaches an output multiplied by later factors.
- Box half-widths $r_i$ are $0$ or at least $2^{-55}$, because all box ends are floats of at least
  $0.25$.
  Every $\tau$ is at least $3\cdot10^{-17}$, and the data satisfy $|a|\le1712$,
  $|\gamma|\le46.4$ and $|K_1|\le93$.
- So these later factors are below $10^{8}$: products of at most three of $|K_1|$, $r$, $\tau$,
  $|a|$, and $e^{\ell}$. The factor $e^{\ell}$ multiplies only powers of $p\ge\ell$: if such a
  power underflows, then $\ell<10^{-100}$ and $e^\ell<1.01$.
- Fewer than $10^6$ operations feed one output.
- So all underflow errors of one output total less than $10^{14}\eta_0<10^{-309}$. The final
  pad absorbs them, with room to spare. The tables below therefore treat only relative errors.
- The explicit underflow cases of the exp calls ($E<-700$ and $E<-708$) are treated in place.

## 3. The proof, line by line

For each computed quantity the tables give:

- the property it must have;
- the worst-case error that has to be covered, including the rounding of the padding
  operations (F5);
- the code's pad;
- the headroom (the pad's exact value divided by the error to be covered), or the largest
  $\varepsilon$ tolerated.

Every pad is evaluated in floats. By (F4) its computed value is at least $(1-ju)$ times its exact
value, with $j\le10$ for the per-element pads and $j\le100$ for the 97-term pads. A headroom of 2
or more absorbs this. Where the headroom is below 2 (the term-weight pad `dw` and the natural
term ends), these roundings are included in the stated tolerance.

### 3.1 Natural enclosure (`Model.natural`, lines 107–137)

Goal: $n^{lo}\le g^*(x)\le n^{hi}$ on $X$. For $x_i\in[lo_i,hi_i]$,
$t^*_{mi}=\mu^*_{mi}+s^*_ix_i$ is increasing in $x_i$.

| quantity (code) | required property | error to cover | code pad | headroom / tolerance |
|---|---|---|---|---|
| `tl`, `th` (110–114) | $tl\le t^*(lo)$, $th\ge t^*(hi)$ | $u\lvert MU\rvert$ (data) + $2.01u\,\lvert S x\rvert$ ($S$ vs $s^*$; product) + $u\lvert t\rvert$ (sum) + $u\lvert t'\rvert$ (pad step, F5) | $10^{-15}(\lvert MU\rvert+\lvert Sx\rvert_{\max}+\max(\lvert tl\rvert,\lvert th\rvert))+10^{-300}$ | ≥ 4.4× per term |
| `sqmin`, `sqmax` (115–116) | $sqmin\le\min t^{*2}$, $sqmax\ge\max t^{*2}$ over $[tl,th]$ | $u$ relative (one product) | none; carried into the next line | — |
| `Elo`, `Ehi` (117–120) | $Elo\le E^*(x)\le Ehi$ on $X$, with $E^*=\sum_i\gamma^*_it^{*2}_i$ | data $u$ + square $u$ + product $u$ + 7-sum $\gamma_6$ + pad step $u$: $\le10u\sum\lvert GA\rvert sqmax$ (uses $sqmin\le sqmax$) | $10^{-14}\sum\lvert GA\rvert\,sqmax+10^{-300}$ | 9.0× |
| `elo` (122) | $elo\le e^{Elo}$ when $Elo\ge-700$; else $elo=0$ | (E): $(1+\varepsilon)$; factor `1-1e-14`; product $u$ | see the next row (chained) | — |
| `ehi` (123) | $ehi\ge e^{Ehi}$ | (E): $(1-\varepsilon)$ if $Ehi\ge-708$. If $Ehi<-708$, $e^{Ehi}<10^{-300}\le ehi$ because $y\ge0$. The cap at 700 never binds ($Ehi\le10^{-8}$) | `1+1e-14`, $+10^{-300}$ | (chained) |
| term ends `tlo`, `thi` (124–128) | $tlo\le a^*e^{E^*}\le thi$ on $X$ | chain for $a>0$, lower end: $(1+\varepsilon)(1-9.992\cdot10^{-15})(1+u)^4(1-10^{-14}(1-u))\le1$; for $a<0$ through `ehi`: $(1-\varepsilon)(1+9.992\cdot10^{-15})(1-u)^4(1+10^{-14}(1-u))\ge1$ | $\mp10^{-14}\lvert\cdot\rvert\mp10^{-300}$ | both hold for $\varepsilon\le1.9548\cdot10^{-14}$ (1.95× the audited ε) |
| 97-term sums (129–130) | $glo\le\sum_m tlo_m$, $ghi\ge\sum_m thi_m$ | $\gamma_{96}\sum\lvert\cdot\rvert$ + two pad steps $2u\sum\lvert\cdot\rvert$ | $10^{-13}\sum\lvert\cdot\rvert+10^{-300}$ | 9.1× |
| linear part (131–135) | adds $\min/\max$ of $\sum_i\lambda^*_ix_i$ | data $u$ + product $u$ + 7-sum $\gamma_6$ + sum with $glo$ ($u$) + pad steps ($2u$) | $10^{-13}(\sum\lvert llo\rvert+\lvert glo\rvert)+10^{-300}$ | > 10× |

Item 1 of Lemma A1 follows: $\exp$ is increasing, and each term lies between its two ends.

### 3.2 Taylor model (`Model.taylor`, lines 140–232)

Notation as in Lemma 2 of the dossier. Centre $c$, $d=x-c$, $t^*_{mi}=\mu^*_{mi}+s^*_ic_i$,
$w^*_m=a^*_m e^{E^*_{0m}}$ with $E^*_{0m}=\sum_i\gamma^*_it^{*2}_{mi}$, $K_1^*=2\gamma^*s^*$,
$K_D^*=2\gamma^*s^{*2}$, $S_0^*=\sum_mw^*_m$, $S_{1,i}^*=\sum_mw^*_mt^*_{mi}$,
$S^*_{2,ij}=\sum_mw^*_mt^*_{mi}t^*_{mj}$, $T^*_{ijk}=\sum_mw^*_mt^*_{mi}t^*_{mj}t^*_{mk}$. Then
$G^*=g^*(c)=S_0^*+\sum_i\lambda^*_ic_i$, $\nabla^*_i=K^*_{1i}S^*_{1i}+\lambda^*_i$ and
$H^*_{ij}=K^*_{1i}K^*_{1j}S^*_{2ij}+\delta_{ij}K^*_{Di}S^*_0$. Lemmas 2 and 3 (form R) give, for
$|d_i|\le r_i$,

$$\big|g^*(c+d)-G^*-\nabla^*\!\cdot d-\tfrac12d^\top H^*d\big|\le\min(P_2^*,P_3^*),$$

with $P_2^*=\sum_m|w^*_m|R_2(\ell^*_m,q^*)$,
$P_3^*=\tfrac16\sum_{abc}|K^*_{1a}K^*_{1b}K^*_{1c}||T^*_{abc}|r_ar_br_c+\big(\sum_i|K^*_{1i}||S^*_{1i}|r_i\big)q^*+\sum_m|w^*_m|R_4(\ell^*_m,q^*)$,
$\ell^*_m=\sum_i|K^*_{1i}||t^*_{mi}|r_i$ and $q^*=\sum_i|\gamma^*_i|s^{*2}_ir_i^2$. $R_2$ and
$R_4$ are increasing in $\ell$ and $q$.

| quantity (code) | required property | error to cover | code pad | headroom / tolerance |
|---|---|---|---|---|
| `c`, `r` (144–145) | $c\in X$; $r_i\ge\max(hi_i-c_i,c_i-lo_i)$ | $\mathrm{fl}(hi-c)\ge(hi-c)(1-u)$ (a subnormal difference is exact); product $u$ | factor `1+1e-15` $=1+1.11\cdot10^{-15}$ | 5× ($2u$ needed) |
| `t`, `dt` (148–149) | $\lvert t-t^*\rvert\le dt$ | $u\lvert MU\rvert+2.01u\lvert Sc\rvert+u\lvert t\rvert+2\eta_0$ | $10^{-15}(\lvert MU\rvert+\lvert Sc\rvert+\lvert t\rvert)+10^{-300}$ | ≥ 4.48× per term |
| `E0`, `dE` (150–152) | $\lvert E_0-E^*_0\rvert\le dE$; asserted $dE<10^{-6}$ | from $t$: $\lvert GA\rvert(1+u)(2\lvert t\rvert+e_t)e_t$ with $e_t\le dt/4.48$; rounding: data $u$, two products $2u$, 7-sum $\gamma_6$ ($\le9u\sum\lvert GA\rvert t^2$) | $\sum\lvert GA\rvert[(2\lvert t\rvert+dt)dt+10^{-14}t^2]+10^{-300}$ | 4.48× (data part); 10× (rounding part) |
| `ex`, `w`, `dw` (154–156) | $\lvert w-w^*\rvert\le dw$ | $E_0\ge-700$: $\lvert w\rvert\,\lvert1-e^{-\theta}/((1+\delta_a)(1+\delta_e)(1+\delta_\times))\rvert$ with $\lvert\theta\rvert\le dE$, $\lvert\delta_a\rvert,\lvert\delta_\times\rvert\le u$, $\lvert\delta_e\rvert\le\varepsilon$ (E): at most $\lvert w\rvert(1.000001\,dE+\varepsilon+2u)$. $E_0<-700$: $w=0$ and $\lvert w^*\rvert\le\lvert A\rvert(1+u)e^{-700+dE}<1.0\cdot10^{-304}\lvert A\rvert$ | $\lvert w\rvert(1.02\,dE+1.1\cdot10^{-14})$; $+\lvert A\rvert10^{-300}$ if $E_0<-699$; $+10^{-300}$ | 1.02 vs 1.000001 on $dE$; tolerates $\varepsilon\le1.0778\cdot10^{-14}$ (at ε = 1e-14 the computed pad exceeds the error by at least 2%: 2% on the $dE$ part, 7.6% on the rest); ≥ $10^4$ for $E_0<-700$ |
| `AW` (158) | $AW\ge\lvert w^*\rvert(1-u)$ | $\lvert w^*\rvert\le aw+dw$ (exact); one rounding | none; the deficit $u$ is absorbed by the `(1+1e-12)` factors on $P$ | — |
| `S0`, `e0`, `G`, `eG` (159–163) | $\lvert S_0-S^*_0\rvert\le e_0$; $\lvert G-G^*\rvert\le eG$ | $\sum dw$ + $\gamma_{96}\sum aw$; the linear part at $c$: data, product, 7-sum, final sum ($\le4u$) | $e_0=\sum dw+10^{-13}\sum aw$; $eG=e_0+10^{-13}(\lvert S_0\rvert+\sum\lvert LIN\,c\rvert)+10^{-300}$ | 9.1×; the deficit $\gamma_{96}\sum dw$ of the computed $\sum dw$ is at most $1.1\cdot10^{-20}\sum aw$ (plus absolute terms below $10^{-311}$) |
| `tau`, `dtau` (170–171) | $\tau_m\ge\lvert t_{mi}\rvert,\lvert t^*_{mi}\rvert$ and $d\tau_m\ge\lvert t_{mi}-t^*_{mi}\rvert$ for $i\in$ dims | $\lvert t^*\rvert\le\lvert t\rvert+dt/4.48\le(\lvert t\rvert+dt)(1-u)$, because $dt\ge9u\lvert t\rvert$ | (none needed) | — |
| `ak1`, `kd` (172–173, 186–187) | $ak1\ge\lvert K_1^*\rvert$; $\lvert kd\rvert(1+10^{-14})\ge\lvert K_D^*\rvert$ | `K1` = fl(2·GA·S): $\le3u$; `KD` = fl(2·GA·fl(S·S)): $\le5u$; product $u$ | factor `1+1e-14` | 22× ($K_1$); 18× ($K_D$) |
| `S1`, `e1` (174–175) | $\lvert S_{1i}-S^*_{1i}\rvert\le e_1$ | $wt-w^*t^*=(w-w^*)t^*+w(t-t^*)$: $\sum(dw\,\tau+aw\,d\tau)$; einsum $\gamma_{97}\sum aw\,\tau$ (F3) | $\sum(dw\,\tau+aw\,d\tau+10^{-13}aw\,\tau)$ | 9.1× (rounding); the data part is covered with the slack of $dw$ (≥ 1.02) and $d\tau$ (≥ 4.48), which absorb the $\gamma_{96}$ deficit of the computed sum |
| `S2`, `e2` (176–177) | $\lvert S_{2ij}-S^*_{2ij}\rvert\le e_2$ | $\lvert t_it_j-t^*_it^*_j\rvert\le2\tau\,d\tau$: $\sum(dw\,\tau^2+2aw\,\tau\,d\tau)$ + $\gamma_{98}\sum aw\,\tau^2$; `tau ** 2` by (P): factor $1-\varepsilon$ | $\sum(dw\,\tau^2+2aw\,\tau\,d\tau+10^{-13}aw\,\tau^2)$ | 9.1×; the (P) deficit $\varepsilon$ is absorbed by the slack of $dw$ (≥ 2%) and of the $10^{-13}$ term |
| `e3` (178), `cub` (213–221) | $s_3=\lvert\hat T_{abc}\rvert+e_3\ge\lvert T^*_{abc}\rvert$ | $\lvert t_at_bt_c-t^*_at^*_bt^*_c\rvert\le3\tau^2d\tau$: $\sum(dw\,\tau^3+3aw\,\tau^2d\tau)$ + four-factor products $\gamma_{99}\sum aw\,\tau^3$; `tau ** 3`, `tau ** 2` by (P) | $\sum(dw\,\tau^3+3aw\,\tau^2d\tau+10^{-13}aw\,\tau^3)$ | 9.1×; tolerates a power error of at least $5\cdot10^{-8}$ |
| gradient `beta`, `egrad` (179–182) | $\lvert\beta_i-\nabla^*_i\rvert\le egrad_i$ | $\lvert K^*_1\rvert e_1$ + $(3u+u)\lvert K_1S_1\rvert$ + $u\lvert LIN\rvert$ + $u\lvert\beta\rvert$ | $ak1\,e_1+10^{-13}(\lvert k_1S_1\rvert+\lvert LIN\rvert+\lvert\beta\rvert)+10^{-300}$ | 180×. For $i\notin$ dims, $r_i=d_i=0$ |
| Hessian `H`, `eH` (183–188) | $H-eH\le H^*\le H+eH$ elementwise | off-diagonal: $ak1_iak1_je_2+8u\lvert H\rvert$; diagonal also $\lvert kd\rvert(1+5u)e_0+6u\lvert kd\,S_0\rvert$ and the sum $u\lvert H_{\rm new}\rvert$ | $+10^{-13}\lvert H\rvert$, $+10^{-13}\lvert kd\,S_0\rvert$, then $\times(1+10^{-12})+10^{-300}$ | 112× on the rounding parts |
| `Hl`, `Hh`, `QL`, `QU` (191–200) | $QL\le\tfrac12d^\top H^*d\le QU$ for $\lvert d\rvert\le r$ | the pad steps fl($H\mp eH$): $u(\lvert H\rvert+eH)$, covered by the unused $10^{-13}\lvert H\rvert$ ($\ge9.9\cdot10^{-14}\lvert H\rvert$); the quadratic form: squares, products, sums ($\le30u$ relative) | $\times(1+10^{-12})\mp10^{-300}$ | ≥ 300× |
| `ell`, `q` (202–204) | $ell\ge\ell^*_m$; $q\ge q^*$ | $\ell$: $ak1(\lvert t\rvert+dt)\ge\lvert K_1^*\rvert\lvert t^*\rvert$, then ≤ 10 roundings; $q$: data $u$, $S^2\ge s^{*2}$, `S ** 2` by (P) ($\varepsilon$), ≤ 12 roundings | $\times(1+10^{-13})$ | 75× ($\ell$); 8.8× ($q$, with ε) |
| `p` (205) | $p\ge\ell^*+2q^*$ | one sum: $u$ | (slack of `ell`) | — |
| `el` (207) | $el\ge e^{\ell^*}(1-3u)$ | (E): $(1-\varepsilon)$; factor $1+9.992\cdot10^{-15}$; product $u$ | `1+1e-14` | deficit $\le u$, absorbed by $P$'s factors; tolerates $\varepsilon\le10^{-12}$ |
| `R2`, `R4`, `P2`, `P4` (208–211) | $P_2\ge P_2^*$, $P_4\ge\sum_m\lvert w^*_m\rvert R_4(\ell^*_m,q^*)$ | `p**3`, `p**4`, `p**2` by (P): $\varepsilon$; ≤ 10 roundings; $AW$: $u$; 97-sum: $\gamma_{96}$ | $\times(1+10^{-12})$ | 45× ($\varepsilon+\gamma_{96}+12u=2.2\cdot10^{-14}$) |
| `U1`, `U2`, `P3`, `P` (222–225) | $P\ge\min(P_2^*,P_3^*)$ | `cub`: $\gamma_{343}$ (accumulation) + 6 roundings; $U_1\ge\sum\lvert K^*_1\rvert\lvert S^*_1\rvert r$; $U_2\ge q^*(1-1.4\cdot10^{-15})$ (factor `1+1e-14` against $\varepsilon+12u$) | $P_3\times(1+10^{-12})$, then $P=\min(P_2,P_3)\times(1+10^{-12})+10^{-300}$; $P=\infty$ if some $\ell>600$ | ≥ 25× |
| `LE` (226) | $LE\ge\sum_i egrad_i\,r_i$ | 7 products and the sum: $\le8u$ | $\times(1+10^{-12})$ | ≫ |
| `aL`, `aU` (227–232) | $aL\le G-eG-P+QL-LE$ and $aU\ge G+eG+P+QU+LE$ | the five-term chain $\gamma_5\,\mathrm{tot}$ and the pad steps $2u\,\mathrm{tot}$ | $10^{-12}\,\mathrm{tot}+10^{-300}$ (`SLK`) | 750× |

Item 2 of Lemma A1 follows. For $x=c+d\in X$:

$$\begin{aligned}
g^*(x)&\ge G^*+\nabla^*\cdot d+\tfrac12d^\top H^*d-\min(P_2^*,P_3^*)\\
&\ge(G-eG)+\beta\cdot d-LE+QL-P\ \ge\ aL+\beta\cdot d,
\end{aligned}$$

because $|(\nabla^*-\beta)\cdot d|\le\sum_i egrad_i\,r_i\le LE$. The upper bound is
symmetric. ∎

### 3.3 Margins in ε (why the audit uses $\varepsilon=10^{-14}$)

Tolerance of each path that uses exp or a power, at the code's pads:

| path | largest relative error tolerated |
|---|---|
| term weight $w$ (`dw`) | $1.0778\cdot10^{-14}$ |
| natural term ends | $1.9548\cdot10^{-14}$ |
| $e^{\ell}$ in the remainders | about $10^{-12}$ |
| `tau ** 2`, `tau ** 3` in `e2`, `e3` | at least $5\cdot10^{-8}$ |
| `p ** k` in `R2`, `R4` | about $10^{-12}$ |
| `S ** 2` in `q` | about $10^{-13}$ |
| `S ** 2` in `U2` | about $10^{-12}$ (through $P$) |

The smallest is $1.0778\cdot10^{-14}$, at the per-term pad. The audit therefore checks every
result against $\varepsilon=10^{-14}$, which is covered line by line. The dossier's
Proposition A2′ (tolerance $9.97\cdot10^{-14}$ by moving slack between lines) is not needed.
The observed errors are about $1.1u=1.3\cdot10^{-16}$, about 80 times below ε.

## 4. Lemma E: what the audit proves

`cert/auditor.py` (docstring; constants derived and every inequality asserted in exact rational
arithmetic at import, `self_test`).

**Lemma E (exp).** Under (H0), for floats $x\in[-708,709]$ the auditor computes floats
$lo\le e^x\le hi$, or reports that it cannot (then the call counts as a violation).

*Proof.*

1. **Reduction.** Let $L=\ln2/64$. The bracket $\ln2\in[s_{400},s_{400}+1/(400\cdot2^{400})]$
   with $s_n=\sum_{k\le n}1/(k2^k)$ gives $L$ to within $10^{-120}$.
2. **Constants.**
   - $L_1$ is $L$ truncated to 36 significant bits.
   - $L_2=\mathrm{fl}(L-L_1)$, and $|L-L_1-L_2|\le DL=1.6\cdot10^{-30}$, an exact bound.
3. **Steps.** $m=\mathrm{rint}(\mathrm{fl}(x\cdot\mathrm{INV\_L}))$; any integer works.
   - The program checks $|m|<2^{17}$, so $p_1=mL_1$ is exact.
   - $s=\mathrm{fl}(x-p_1)$, $p_2=\mathrm{fl}(mL_2)$, $r=\mathrm{fl}(s-p_2)$.
   - The program checks $|r|\le0.0055$.
4. **Error of $r$.** By (F0), $r_{\rm true}=x-mL$ satisfies
   $|r_{\rm true}-r|\le u(|r|+|s|+|p_2|)+|m|DL+3\eta_0\le DR=1.3\cdot10^{-18}$.
5. **Polynomial.** $H$ is the Horner value of the degree-7 Taylor polynomial at $r$, with
   float coefficients $c_i\approx1/i!$. Higham's bound $\gamma_{14}\sum|c_i||r|^i$ for Horner's rule
   (*Accuracy and Stability of Numerical Algorithms*, 2nd ed., §5.1), the exact coefficient errors,
   the Lagrange remainder $|r|^8e^{|r|}/8!$ and an underflow term give
   $|e^r-H|\le\rho_H H$ with $\rho_H=1.572\cdot10^{-15}$.
6. **Table.** With $m=64k+j$, $0\le j<64$: $e^x=2^k\,2^{j/64}e^{r_{\rm true}}$. The floats
   $TLO_j\le2^{j/64}\le THI_j$ are proved by $TLO_j^{64}\le2^j\le THI_j^{64}$ in integers.
7. **Result.** $lo=\mathrm{fl}(\mathrm{fl}(TLO_jH)\,C_{lo})\cdot2^k$ and
   $hi=\mathrm{fl}(\mathrm{fl}(THI_jH)\,C_{hi})\cdot2^k$.
   - The constants satisfy $C_{lo}(1+u)^2\le(1-\rho_H)(1-DR)$ and
     $C_{hi}(1-u)^2\ge(1+\rho_H)(1+2DR)$.
   - $2^k$ is built from its bit pattern, so no `ldexp` is used.
   - For $x\ge-708$ every result is normal, because $e^{-708}(1-10^{-14})>2^{-1022}$ is checked
     exactly. So the scalings are exact.
8. **Width.** The relative width of $[lo,hi]$ is at most $4.4\cdot10^{-15}$ (measured against
   mpmath at 300 bits on 32,010 arguments; 9,000 of them are reduction half-points
   $(m+\tfrac12)L$ and their float neighbours; no enclosure failure).

**The check.** For $x\ge-708$ the call passes iff $y\le\mathrm{fl}(lo\cdot F_{up})$ and
$y\ge\mathrm{fl}(hi\cdot F_{dn})$, with floats $F_{up}(1+u)\le1+\varepsilon$ and
$F_{dn}(1-u)\ge1-\varepsilon$ (checked exactly). Then $(1-\varepsilon)e^x\le y\le(1+\varepsilon)e^x$.
For $x<-708$ it passes iff $0\le y\le2^{-1020}$. Anything else fails, including NaN, $x>709$ and
a failed reduction check. So **a passed call proves (E) for that call.** Conversely, every
$y$ with $|y-e^x|\le5\cdot10^{-15}e^x$ passes, wherever $e^x$ lies in $[lo,hi]$. np.exp's
errors (at most 1.13u observed) pass with a wide margin.

**Lemma P (powers).** For $x\in[2^{-250},2^{250}]$ let $z=\mathrm{fl}(x\cdot x)$ ($k=2$),
$\mathrm{fl}(\mathrm{fl}(x\cdot x)\cdot x)$ ($k=3$) or $\mathrm{fl}(\mathrm{fl}(x\cdot x)^2)$
($k=4$). Then $|z-x^k|\le G_z x^k$ with $G_z=(1+u)^3-1$ (no underflow or overflow).

- The call passes iff $|\mathrm{fl}(y-z)|\le\mathrm{fl}(C_p z)$, with
  $C_p(1+G_z)(1+u)+G_z\le\varepsilon$ checked exactly.
- A pass forces $z/2\le y\le2z$. So $y-z$ is exact (Sterbenz), and
  $|y-x^k|\le C_p z(1+u)+G_zx^k\le\varepsilon x^k$.
- $x=0$ passes only with $y=0$. $0<x<2^{-250}$ is checked in exact rational arithmetic.
- Negative or NaN $x$, and $x>2^{250}$, fail.
- **A passed call proves (P).** In the certifier, $\tau\ge3\cdot10^{-17}$ (because
  $dt\ge10^{-15}|Sc|$ and $|Sc|\ge0.3$), and
  $p$ is $0$ or above $10^{-35}$ (because $p\ge ak1_i\,dt\,r_i$ with $r_i=0$ or $r_i\ge2^{-55}$).
  So neither the exact path nor an underflow occurs in practice. An underflowed
  power would be flagged, which is conservative.

**Per-leaf bookkeeping.** Each call's check is reduced to one flag per box (axis 0 of the arrays).
The audited `_batch` propagates the flags through the splitting recursion. A leaf is reported
"audit-clean" only if no call made for it or for any of its pieces failed. A call that fails for
a piece that was later split also flags the leaf. This is conservative, because such a piece's
values do not enter any certificate. The certification decisions themselves are unchanged
(Section 5).

## 5. How the audited run relates to the saved results

- `indep_cert_audit.py` computes the same floats as the original in the same order. The audit
  only reads them. `tests/check_copies.py` proves this textually: undoing the wrappers gives the
  original file.
- The rerun uses the same recorded trees and the same chunking (eg_disc2_s: 38 chunks; eg_int_s
  and eg_disc_s: one chunk per part, as the review's `verify_tree.py` runs). So every 64-box
  Taylor batch, every LP and every exact test is the same as in the saved runs.
- `compare_audit.py` checks this byte for byte against `publication/eg-recheck/res/` for
  eg_disc2_s. For eg_int_s and eg_disc_s it checks against the review's logs: every progress
  line, the full statistics and the smallest LP margin.
- `compare_audit.py` also checks hypotheses (i)–(iii) of Theorem R on the audited outputs
  themselves, for all three instances: every leaf of every part was certified in this run (the
  chunks' leaf indices are exactly $0,\dots,n-1$); the bookkeeping flags; r1's exact tree-free
  guillotine coverage proof; the domain check against the GAMS bounds; no flagged leaf and no
  violation; and, per output file, that every call site was exercised and that the number of
  audited exp results at `tay_E0`, `nat_Elo` and `nat_Ehi` equals pieces × 28 rows × 97 terms.
- If the comparison and the audit both pass, the saved certificate is the audited certificate,
  and Theorem R holds for the saved run.

## 6. Status (2026-10-04)

- Built and tested; see the eg-audit report. The full run has not been launched yet.
- Command (runs a /tmp copy; the research tree is only read):

  `rm -rf /tmp/eg-audit-run && cp -a paper-open-minlplib/development/eg-audit /tmp/eg-audit-run && cd /tmp/eg-audit-run && EG_AUDIT_R=/workspace/minlp-notes/research-20260929 python3 run_audit.py --workers 2`

  (from the repository root; about 1.5 h wall with 2 workers, about 25–30 min with 8). To restart
  after an interruption, rerun only the last part (`cd /tmp/eg-audit-run && EG_AUDIT_R=… python3
  run_audit.py --workers 2`); finished jobs are skipped. Afterwards copy `/tmp/eg-audit-run/out`
  to `eg-audit/out`.
- After the full run, `out/compare.log` must end with
  `RESULT: PASS (complete run; …, 0 violations)` for Theorem R to apply as stated.
