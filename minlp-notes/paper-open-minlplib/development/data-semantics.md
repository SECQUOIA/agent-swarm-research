# Data semantics of all certificates (code reading)

Task: data-semantics audit for the paper. Date: 2026-10-04.
Paths: `R/` = `research-20260929/`, `D/` = `paper-open-minlplib/development/`.
My scripts and logs are in `D/data-semantics-checks/` (README there). Every run used copies under
`/tmp`; nothing in `R/` or `literature/` was changed.

## 0. Main points

- **The exact-rational convention holds for every certificate.** I read the dual codes (author and
  independent verifier) and the primal-point proofs of all families in scope, plus the audit's
  class (i) certificates. Each code reads the OSIL decimals in one of four ways (Section 1):
  - **E**: exact rationals;
  - **O**: an outward enclosure of the exact decimal;
  - **M**: the correctly rounded double, with the rounding error covered by an explicit margin;
  - **B̂**: a binary64 parse whose used data are binary64-exact or are re-entered exactly.

  No code uses unenclosed binary64 data in a way that affects a stated bound or gap. **No stated gap
  or bound fails to bound the optimum of the exact-rational model.**
- **This closes PP-1 and critique C2.** C2 listed the dual codes of powerflow, camshape, catmix,
  waterno2, ANN, KAN, eg and pindyck as unchecked. All are now confirmed (Section 2).
  - Three code paths are of type M: eg route S-F (`egfast.py`, Lemma S), eg route R (Lemma A1,
    item F1) and the second ANN code `annx.py` (slack TAU).
  - The first-wave author scripts are of type B̂. The displayed values for those families come from
    verifier codes of type E or O.
- **The draft model definition has one wording defect (new; no number changes).** The draft in
  primal-points §1.1 defines `power(a, b)` only for a > 0, as exp(b ln a). Our exactly feasible
  points contain zero bases in x³ terms:
  - pricing050: 5;
  - waterno2_06, 09, 12, 18, 24: 44, 56, 69, 97 and 125.

  Every code evaluates a constant integer exponent by repeated multiplication, so the computed
  values are correct. The definition must still say so, and it needs a domain rule (Section 5).
- **Cheap checks run now** (Section 3):
  - All 164,791 distinct numeric strings of the 46 OSIL files involved are enclosed by every
    conversion the codes use, with 0 failures. The conversions are `iv.mpf(s)` at 53 or 64 bits and
    at 30–60 digits, the two doubles around fl(s), and `iv.mpf(repr(float(s)))`.
  - The pricing050 verifier rerun reproduced its stored log exactly. Its exactly feasible point is
    now saved, which resolves the replay part of PP-3.
  - **All 19 class (i) refutations and the 3 rocket refutations also hold with the data rounded to
    binary64.** The margins agree to at least 4 significant digits, and the smallest is still 1.116
    display units.

## 1. Readings and what "consistent" means

The paper's model is the OSIL file, with every decimal string read as the rational it denotes and
OSiL defaults otherwise (reading (b) in primal-points §1.1). A certificate is consistent with this
model if it proves its statement for those rationals. For each code I recorded how a datum `s`
enters:

| code | meaning | valid for reading (b)? |
|---|---|---|
| E | `Fraction(s)`, sympy `Rational(s)`; or a hard-coded exact rational after an exact string match against the file | yes |
| O | `iv.mpf(s)`; `iv.mpf(p)/q` of `Fraction(s)`; [prev double, next double] around fl(s) (`ivnp.const`, `ivx.const`, `ia.NI.const`, `rbb.dec_iv`); `kan_iv.frac_iv`, `fdn`/`fup`; dyadic floor/ceil | yes, if the enclosure is outward (checked for all strings, Section 3) |
| M | fl(s) used as data; an error analysis in the code covers relative error ≤ u, u = 2⁻⁵³ | yes, if the analysis covers the datum (checked by reading) |
| B̂ | `float(s)` from the first-wave reader `research-20260922/scouting/minlplib-open-data/osil.py` | yes only for the data that are binary64-exact or re-entered exactly (checked case by case) |

## 2. Family table

Notes: "dual A" is the author code, and "dual V" is the independent verifier (and later dossier
codes). The last column answers the question: does a stated gap or bound fail for the
exact-rational model? Details and file paths follow the table.

| family | dual A | dual V | primal proof | consistent with (b) | stated gap or bound at risk |
|---|---|---|---|---|---|
| lnts50–400 | B̂ (data used are exact; angle bound unused) | E/O | E/O | yes | no |
| lukvle10 | B̂ (integer data) | E/O | E/O | yes (all readings agree) | no |
| dtoc5 | O (h = 1/50000 exactly) | O; dossier exact certificate E (via .gms) | E | yes | no |
| optcdeg2 | O | E | E | yes | no |
| camshape100–800 | O (repr round trip exact) | E | E | yes | no |
| chain50–400 | O | O | E | yes | no |
| catmix100–800 | O | E → O | E | yes | no |
| hvycrash | E/O | E/O | O | yes | no |
| ex6_2_5, ex6_2_7 | O | E → O | E | yes | no |
| etamac | E/O | E/O | O | yes | no |
| pricing050 | O (objective numerators only; all integer) | O | E/O | yes | no |
| pindyck | E/O | E/O | O | yes | no |
| eg_int_s, eg_disc_s, eg_disc2_s | O (S-I) / M (S-F) | M (route R); O (r1 sample) | E/O | yes; S-F and R by margin (Lemma S; Lemma A1 F1) | no |
| powerflow0030p/0039p/0039r | E | E | E/O | yes | no |
| waterno2_06–24 | O | E | E | yes | no |
| ann_cumene_tanh | O | M (TAU) | E | yes; second code by margin | no |
| KAN R (6 models) | O | O; infeasibility E | E | yes | no |
| audit class (i), 19 pairs / 15 instances; rocket ×3 | primal only | primal only | E/O | yes; also holds for binary64 data | no |

### 2.1 Details per family

**lnts50–400.**
- *Dual A*: `R/open-instances/lnts_bound.py`, B̂.
  - It uses the first-wave float reader, which also ignores `constant` attributes. No lnts file has
    one.
  - The certificate uses a = 100, the coefficient −0.5 (h/2), 45, 5 and 0, all binary64-exact. The
    trapezoid weights are Fractions.
  - The only inexact datum is the angle bound ±1.5707963267949. The certificate does not use it,
    because S(μ, ν) = Σ_j √(w_j² + (μw_j + νc_j)²) maximizes over unconstrained θ.
- *Dual V*: `R/reviews/open-instances-verification/v_lnts.py`, E/O.
  - It reads the file with the string-preserving reader `osilx.py` and checks the structure by
    string equality.
  - The certificate uses `iv.mpf(100)`, 45 and 5.
  - The adopted exact-optimum theorem uses the same data. Its attaining controls have
    |θ_j| ≤ 0.9523. The bound exceeds π/2 by 3.38e-15 (decimal) and 3.49e-15 (its double), so
    attainment holds under both readings (`misc_checks.log`).
- *Primal*: `R/publication/primal/lnts/lnts_primal.py` with `osil_iv.py`, E/O. It uses
  `Fraction(s)` and the outward `ivnum`, and it checks the angle bounds against both the decimal and
  its double.

**lukvle10.**
- The file has no non-integer and no binary64-inexact string, so every reading gives the same model.
- *Dual A*: `R/open-instances/lukvle10_bound.py`. *Dual V*: `v_lukvle10_prep.py`, which
  string-matches the `power` trees, and `v_lukvle10_bnb.py`, which uses mpmath iv.
- *Primal*: `R/publication/primal/dtoc5-lukvle10/osil_exact.py` and `lukvle10_enclose.py`
  (Fraction).
- *Operator note*: the verifier's `pow_range` sets the value to 0 at base 0. The primal point has
  all bases x_k² ≥ 0.0676. The dual is valid under the rule of Section 5.

**dtoc5.**
- *Dual A*: `R/open-instances/dtoc5_bound.py`, O.
  - Its pattern check compares parsed doubles with 2e-5 and 8e-5. That check alone would not
    separate two decimals that round to the same double.
  - The certificate uses h = `iv.mpf(1)/50000` and 4h.
- *Dual V*: `R/reviews/open-instances-verification/v_dtoc5.py`, O. It checks the strings `'2e-5'`,
  `'-2e-5'` and `'8e-5'` by string equality, which also closes the gap in the author's float-level
  pattern check. It then uses h = `iv.mpf(1)/50000`.
- *Dossier exact certificate (gap 7.2e-43)*: `D/dossiers/checks/dtoc5-optcdeg2/dtoc5_checks.py`, E.
  - It reads the Fractions 1/50000 and 4/50000 from `dtoc5.gms`, not from the OSIL.
  - The OSIL strings are exactly 2e-5, −2e-5 and 8e-5, by the verifier's string check. They are also
    the file's only binary64-inexact strings (`data_survey.log`). So the rationals agree.
- *Primal*: `R/publication/primal/dtoc5-lukvle10/dtoc5_construct.py` asserts the OSIL Fractions
  1/50000 and 1/12500; `check_exact_point.py` completes the check. E.

**optcdeg2.**
- *Dual A*: `R/theory-bangbang/optcdeg2_qcal_certify.py`, O.
  - The GAMS-form constants "0.0004", "0.02" and "0.2" are enclosed by `ivnp.const`.
  - The products 0.02h = 8e-6 and 0.2h = 8e-5 are enclosed as interval products.
  - The control box [−0.2, 0.2] is enclosed outward.
  - The older `R/open-instances/optcdeg2_bound.py` uses `iv.mpf("0.0004")` and similar calls.
- *Dual V*: `R/reviews/bangbang-verification/v_model.py`, E. It reads the OSIL with `Fr(s)` and
  asserts the coefficients 4/10⁴, 8/10⁶, 8/10⁵ and 2/10⁴. `v_qcal_exact.py` and `v_states.py` use
  these Fractions.
- *Primal*: `v_primal.py` (Fractions, enclosed as `M.mpf(p)/q`) and the dossier's
  `optcdeg2_primal_int.py` (asserts `H == Fr("4e-4")` and similar). E.

**camshape100–800.**
- *Dual A*: `R/open-instances/camshape_bound.py`, O.
  - It uses the float reader and then `dec(x) = iv.mpf(repr(float(x)))`.
  - Every string of the four files has at most 15 significant digits, so `repr` returns the same
    decimal value: 0 round-trip failures (`data_survey.log`) and 0 enclosure failures
    (`enclosure_check.log`).
- *Dual V*: `R/reviews/open-instances-verification/v_camshape.py`, E. It reads `Fraction(s)` after a
  string-level structure check and computes the bound −c₀·ΣE exactly.
- *Primal*: the verifier's exact rational envelope, and the dossier's
  `D/dossiers/checks/camshape/check_exact.py`. E.
- The zero gap is a statement about reading (b) (critique C3).

**chain50–400.**
- *Dual A*: `R/open-instances-wave2/cops/chain_bound.py`, O. It takes η = `iv.mpf(η string)` and
  asserts `Fraction(η) = 1/(2N)`.
- *Dual V*: `R/reviews/cops-verification/v_chain_bnb.py`, O. It uses η = `iv.mpf(1)/(2N)` after
  `v_chain_checks.py` asserts `Fr(η) = 1/(2N)`.
- *Primal*: `R/publication/primal/chain/verify_points.py`, E. It uses its own reader with
  `Fraction`, η = `Fraction(1, 2N)`, and arithmetic in Q(√R).

**catmix100–800.**
- *Dual A*: `R/open-instances-wave2/cops/catmix_bound.py` with `catmix_model.py`, O.
  - The model keeps the strings.
  - `ivx.const(s)` gives the two doubles around fl(s), which enclose every decimal, including
    4.5000000000000005e-2.
- *Dual V*: `R/reviews/cops-verification/v_catmix_model.py`, E → O.
  - It reads `Fr(s)` and derives exact polynomial coefficients with sympy.
  - `v_catmix_dp.py` encloses these coefficients with `fr_iv`.
  - `R/reviews/catmix-recheck-checks/recheck_dp.py` (catmix400/800) reuses these maps.
- *Primal*: E. It uses an exact rational simulation (`simulate_exact` with Fraction data, and
  `policy_exact.py`). The 60-digit `simulate_iv` uses `iv.mpf(strings)`.
- The OSIL decimals differ from the .gms intent (c − 9a ≤ 5e-18). The claims are for the OSIL
  (chain-catmix CC-1; Proposition M8 transports the duals).

**hvycrash.**
- *Dual A* (`R/open-instances-wave2/small/hvycrash.py`) and *dual V*
  (`R/reviews/wave2-small-verification/v_hvycrash.py`): E/O.
  - Both use `osilx` strings and match the expression templates exactly.
  - The identity −50·(4.37e-3) = −0.2185 is checked in Fraction.
  - The point is evaluated with `iv.mpf(s)`.
- The identity holds only for the decimals: 50·fl(4.37e-3) − 0.2185 = −1.24e-17 (critique C3).

**ex6_2_5, ex6_2_7.**
- *Dual A*: `gibbs.py` and `gibbs_model.py`, O. Fraction constants are enclosed by `ia.NI.const`.
  The lower bound y ≥ 1e-7/t_max is computed as a double nudged one ulp down; I checked that it lies
  below the exact value.
- *Dual V*: `gibbs_sym.py` (sympy `Rational(s)`), `ivgen.py` (`iv.mpf(p)/iv.mpf(q)`), `gibbs_bb.py`
  and `gibbs_bound.py`, E → O.
  - b enters as `iv.mpf(s)`.
  - The ideal-phase constant ".156969560191053" is checked symbolically against the OSIL.
- *Primal*: the own point in `gibbs_bound.py` (Fraction) and the dossier's `ex62_check.py`. E.

**etamac.**
- *Dual A* (`etamac.py`) and *dual V* (`v_etamac.py`): E/O. They match templates on the strings,
  enter data as `iv.mpf(s)` and use exponents as Fractions.
- *Primal*: the verifier's recursion, O.
- The certificate needs s > 1 and p₁q < 1. Here s − 1 = 4.14e-16 (decimal) and 3.71e-16 (binary64),
  and p₁q = 0.28, so neither step depends on the reading.

**pricing050 (max).**
- *Dual A*: `pricing050.py` with `pricing050_model.py`, O.
  - a, g and r enter as `iv.mpf(s)`.
  - The objective uses `iv.mpf(cF[j].numerator)`. This is correct only because all 46 objective
    coefficients are integers (`misc_checks.log`).
- *Dual V*: `v_pricing050.py`, O. It uses `iv.mpf(s)` for a, g and r, and c as `Fraction` enclosed
  as `iv.mpf(p)/q`.
- *Primal*: the verifier's own point, E/O. It is in Fractions, and its rows are enclosed with
  `iv.mpf(s)`. Five coordinates are 0 inside x³ terms (DS-1).

**pindyck.**
- *Dual A*: `pindyck_global.py`, E/O. It uses Fractions of the strings ".87", ".13" and so on, plus
  `iv.mpf(KAP)` and `iv.mpf("1.02")`.
- *Dual V*: `R/reviews/pindyck-review-checks/own_osil.py`, `own_model.py`, `own_ranges.py`,
  `own_psi.py` and `final_bound.py`, E/O.
- *Primal*: `primal_check.py`, O. It asserts that `iv.mpf(s)` encloses `Fraction(s)`.

**eg_int_s, eg_disc_s, eg_disc2_s.**
- *Routes S-I/S-F (author)*: O/M.
  - `R/open-instances-wave3/eg/eg_model.py` reads Fractions of the OSIL strings.
  - `retry/egtm.py` encloses each datum by `kan_iv.frac_iv` (the two doubles around it).
  - `retry/egfast.py` uses the midpoints and accounts for their error (≤ 2u) in Lemma S.
- *Route R (the independent certifier; also the planned all-leaf rerun)*: M.
  - `R/reviews/eg-retry-review-checks/gms_model.py` reads the .gms decimals as Fractions.
  - `indep_cert.py` rounds a, μ, γ, s and the linear coefficients to doubles. The padding covers this
    rounding (Lemma A1, item F1, eg dossier §3.6).
  - The objective constants c_k, the side-row bounds, the variable bounds and θ* enter the final
    Fraction tests exactly (`indep_cert._one`, `_combine`). `R/publication/eg-recheck/margin_cert.py`
    keeps these tests.
  - `recheck_leaves.py` asserts that the root box contains the exact box.
  - The .gms and the OSIL are identical as rationals for all three instances (`check_decode.log`: 0
    exact mismatches). The r1 check `cmp_model.py` compares the term data only as doubles and the
    constants exactly.
- *r1 interval sample*: `R/publication/reviews/eg-recheck-r1/own_ia.py` and `own_model.py` enclose the
  OSIL Fractions by two doubles. O.
- *Primal*: E/O. The dossier's `eg_dyadic_check.py` encloses each Fraction by floor/ceil at 2⁻²⁵⁶;
  the corrected `eg_iv_check.py` is a second proof. `verify_primal.py` is a 50-digit point
  evaluation, not a proof.

**powerflow0030p, 0039p, 0039r.**
- *Dual A*: `R/open-instances-wave3/powerflow/pf_model.py` (Fractions of the OSIL decimals; rational
  outward tan bounds), `pf_cert.py`, `ext/pf_bb3.py` and `ext/verify_exact.py` (exact rational
  bound, exact LDLᵀ). E.
- *Dual V*: `R/reviews/wave3-verification/powerflow/pfv.py`, `run_root.py` and `sdp_node.py`. It
  uses Fractions; floats only propose multipliers. E.
- *Primal*: `R/publication/primal/powerflow/pfmodel.py` and `certify.py` (Fraction; iv). E/O.
- All readers apply the objective constant 2 of 0039p and 0039r.

**waterno2_06–24.**
- *Dual A*: O.
  - `R/open-instances-wave2/waterno2/wmodel.py` reads through `osilx`.
  - `rbb.py` uses `dec_iv`: the nearest double, widened by one ulp unless it is exact.
  - The implied bounds are stored as outward floats.
  - `certify.py` sums in Fraction.
- *Dual V*: E. `R/reviews/waterno2-verification/vmodel.py` and `vbb.py` use Fractions and treat
  integer powers as monomials. `R/reviews/waterno2-recheck/vbb2.py` uses exact rational constants.
- *Primal*: `R/publication/primal/water-ann-kan/code/osil.py`, `water_exact.py` and
  `check_water_point.py`, E. They use Fractions and quadratic fields, and evaluate integer powers by
  repeated multiplication.
- The GAMS and OSIL forms are exactly identical (waterno2 dossier W8).

**ann_cumene_tanh.**
- *Dual A*: `R/open-instances-wave3/ann/ann_model.py` (Fraction), `ann_tm.py`, `ann_bb.py` and
  `ann_fast.py` (`frac_iv`, `NIq`). O.
- *Second code*: `R/reviews/ann-extension-review-checks/annx.py`, M.
  - The model comes from `R/reviews/wave3-verification/ann/annv.py` as Fractions.
  - W, b, the objective coefficients and the objective constant are rounded to doubles.
  - The slack TAU = 1e-12 per step is applied to |W|, |b|, |a| and |const| (lines 258, 300 and
    310–311). It far exceeds the representation error, which is at most u/2.
  - The bound sides are enclosed exactly (`fiv`).
- *Primal*: `nn_exact.py` (Fraction). E.
- The dual claim needs either code, and the author's code has no data hypothesis.

**KAN R (six models).**
- *Dual A*: `R/open-instances-wave3/kan/kan_model.py` (Fraction) and `kan_bb.py` (`frac_iv`, `NIq`).
  O.
- *Dual V*: `R/reviews/wave3-verification/kan_decode.py` (Fraction) with `kan_bnb.py`. The dossier's
  rigorous-exp rerun `D/dossiers/ann-kan-checks/kan_bnb_rigexp.py` encloses the Fractions with
  `fdn`/`fup`. O.
- *Infeasibility of the full models*: `R/reviews/wave3-verification/kan_infeas_cert.py` (kan_decode,
  sympy). E.
- *Points of R*: `nn_exact.py`. E.

**Audit class (i) and rocket.**
- The certificates are primal only.
  - Audit: `R/bound-audit/verify.py`, `verify_one.py`, `cert_linear.py`, `cert_ndnetgen.py` and
    `cert_topopt.py` (`osilx` strings → Fraction or `iv.mpf(s)`).
  - First verifier: `R/reviews/bound-audit-verification/osil.py` (Fraction), `kraw.py` and
    `topopt_exact.py`.
  - Second rocket proof: `D/dossiers/checks/audit-r2/rocket_kraw.py`.
  - All are E/O.
- The emfl dual certificates (`cert_socp.py`) are exact as well.

## 3. Cheap re-evaluations run for this audit

All commands are in `D/data-semantics-checks/README.txt`. They ran on `/tmp` copies with one core.

| check | result |
|---|---|
| `data_survey.py` (46 files) | Non-binary64-exact distinct strings: lukvle10 0; lnts 2 (±1.5707963267949); chain 2; dtoc5 3; optcdeg2 6; catmix 6, including one 16–17-digit binary64 print; camshape 7; rocket 1 (0.6); the other families 10–3332. ANN has 2234 strings with 16–17 digits, KAN 977–2412 and powerflow0039r 24 (binary64 prints). `repr` round trip: 0 failures. |
| `enclosure_check.py` (164,791 strings) | `iv.mpf(s)` at prec 53 and 64 and at dps 30, 40, 50 and 60, the two doubles around fl(s), and `iv.mpf(repr(float(s)))`: **0 failures**. This covers every O-type conversion and is the data part of the mpmath-iv trust base. |
| `power_survey.py` | `power` nodes occur in pricing050 (x³, 77 nodes), waterno2 (x³, 78–312 nodes), etamac (fractional exponents, positive bases), lukvle10 (variable exponent, base x²) and pindyck (constant base 1.02). Objective constants: catmix −1, powerflow0039p/r 2. No row constants. |
| `pricing050_rerun.sh` (20 s) | The `/tmp` rerun of `v_pricing050.py` reproduced the stored `logs/pricing050.json` exactly. Its point was saved (`logs/pricing050_own_point.txt`). It has 7 zero coordinates, 5 of them inside x³ terms. |
| `zero_bases.py` | Zero bases of x³ at the exact points: waterno2_06/09/12/18/24 have 44/56/69/97/125; pricing050 has 5. |
| `misc_checks.py` | All pricing050 objective coefficients are integers. etamac: s − 1 = 4.14e-16 (b) and 3.71e-16 (c). lnts: bound − π/2 = 3.38e-15 (b) and 3.49e-15 (c). |
| `run_audit_b64.sh` + `summarize_b64.py` (4.3 min) | The audit's point certificates were rerun with every binary64-inexact datum replaced by its binary64 value (reading (c)). Results below. |

**Class (i) and rocket under binary64 data.** Every certificate succeeds again, and the objective
upper ends are nearly unchanged:
- smallinvDAX ×4, ghg_3veh, glider100, methanol50, nuclear14 and sssd ×4: identical to 12 or more
  digits;
- watercontamination0303: +1.0e-12;
- nd_netgen: +2.1e-10;
- topopt p5: +2.8e-11.

| instance (solver) | d − f_hi under (c) | display units |
|---|---|---|
| smallinvDAXr1/r2b200-220 (LINDO) | 1.1158e-6 | 1.116 |
| smallinvDAXr1/r2b150-165 (LINDO) | 7.40e-7 | 7.40 |
| watercontamination0303 (BONMIN; LINDO) | 3.976e-7; 4.976e-7 | 3.98; 4.98 |
| nd_netgen (CPLEX; GUROBI) | 1.445; 3.565 | 144; 356 |
| gross pairs (glider100, topopt, methanol50, sssd ×4, ghg_3veh, nuclear14) | unchanged | ≥ 2800 |
| rocket100/200/400 (LINDO) | 1.069e-7; 4.707e-8; 1.895e-7 | 1.07; 4.71; 18.9 |

## 4. Findings, consequences and fixes

**DS-1 (minor, wording; new). The draft model definition does not cover `power` with an integer
exponent and a zero base, and it has no domain rule.**
- *Evidence.* The draft reads `power(a, b)` with a > 0 as exp(b ln a). The exactly feasible points
  contain power(0, 3): 5 times in pricing050 and 44–125 times in each waterno2 point.
- *How the codes treat these cases.*
  - pricing050 `xp`, the waterno2 `vmodel.poly` monomials, water `osil.py` and rbb's cubes all
    multiply.
  - lukvle10's verifier sets base^e = 0 at base 0.
  - hvycrash's identity divides by r, so it needs r ≠ 0.
- *Consequence.* No number changes. Read literally, the draft leaves these points undefined, so the
  claim "exactly feasible" would not formally apply to pricing050 and waterno2.
- *Fix.* Use the wording of Section 5. No computation is needed.

**DS-2 (resolves PP-1 and C2). The convention is confirmed for every dual code.**
- *Consequence.* None. The draft sentence "Every primal and dual proof reads each decimal string … as
  the exact rational" is true in substance but imprecise.
- *Fix.* Replace it with:

  > Every certificate proves its statement for the decimals read as exact rationals. Most codes use
  > the rationals exactly or enclose them outward. The float routes of the eg certifiers (S-F and
  > the independent route R) and the second ANN bounding code use the correctly rounded doubles, and
  > their error analyses (Lemma S, Lemma A1, the slack TAU) cover the rounding.

**DS-3 (minor). The first-wave author scripts parse the data to binary64** (lnts, dtoc5, lukvle10,
camshape and the older optcdeg2 scripts).
- *Why it is harmless.*
  - lnts uses only binary64-exact data, and its angle bound is unused.
  - lukvle10 has only integer data.
  - dtoc5 re-enters h = 1/50000 exactly.
  - camshape's `repr` round trip returns the exact decimals.
  - The older optcdeg2 script uses string literals.
  - None of these files has a `constant` attribute, which this reader would ignore.
- *Consequence.* None. The displayed values come from E/O verifier codes.
- *Fix.* One sentence in the reproduction appendix. No rerun.

**DS-4 (minor; eg route R and its rerun). Route R reads the data from the .gms and rounds the term
data to doubles.**
- *Consequence.* None. Lemma A1 item F1 covers the rounding, and the final tests use exact c_k, side
  bounds, variable bounds and θ*.
- *Fix for the planned all-leaf rerun.*
  1. State F1 as "every datum used as a double lies within relative distance u of the exact
     decimal". This holds for the .gms and the OSIL decimals alike, so the double-level identity of
     `cmp_model.py` would also suffice.
  2. Add a start-up assertion that the `GmsModel` Fractions equal the `eg_model.decode` Fractions of
     the OSIL. The test exists in `check_decode.py` and takes seconds.
  3. Keep the exact Fraction tests unchanged.

**DS-5 (minor; ANN). The second code `annx.py` uses rounded doubles, with TAU covering the rounding.**
The coverage is documented in code comments, not in a written lemma.
- *Consequence.* None. The claim needs either code, and the author's code is outward.
- *Fix.* One sentence in the trust-base table. Optionally, write a short TAU lemma (1–2 h of reading).

**DS-6 (minor; dtoc5). The dossier's exact dual certificate reads `dtoc5.gms`, not the OSIL.**
- *Consequence.* None. The OSIL strings are exactly 2e-5, −2e-5 and 8e-5 (verifier's string check).
- *Fix.* Cite that check. Alternatively, let `dtoc5_checks.py` parse the OSIL (minutes to write; it
  runs in 3 s).

**DS-7 (cosmetic). The author's pricing050 code uses only the numerators of the objective
coefficients.**
- *Consequence.* None, because all 46 coefficients are integers.
- *Fix.* None. The summary uses the verifier.

**DS-8 (wording; audit). The refutations are proved for reading (b), while the solvers read binary64
data.**
- *Consequence.* None. The rerun shows that all 19 class (i) pairs and the 3 rocket refutations hold
  with the same margins under reading (c).
- *Fix.* The paper may say: "the refuted bounds are invalid for the model as defined; the
  refutations are unchanged if all data are rounded to binary64
  (`D/data-semantics-checks/logs/summarize_b64.log`)". This also answers the objection that a
  solver's bound might be valid for its binary64 model.

**DS-9 (PP-3, replay part). The pricing050 verifier point was not saved.**
- *Status.* Regenerated in `/tmp`. The output was identical, and the point is saved in
  `D/data-semantics-checks/logs/pricing050_own_point.txt`.
- *Fix.* Add the point to the reproduction package.

Known reading-(b)-specific statements are unchanged by this audit: the hvycrash identity, the camshape
zero gaps, the 1e-16-level gaps, KAN infeasibility, and the catmix OSIL ≠ .gms difference. Word them
as critique C3 proposes.

## 5. Proposed text for the model definition

> **Model.** An instance is the OSiL file distributed by MINLPLib (SHA-256 recorded in the
> supplement). Every numeric string — variable and row bounds, linear and quadratic coefficients,
> `coef` attributes, `number` values, and objective and row `constant` attributes — denotes the
> rational number written in decimal. Omitted values take the OSiL defaults: variable bounds
> [0, +∞) ([0, 1] for binaries), type continuous, row bounds (−∞, +∞), `coef` 1, `constant` 0.
> Operators have their real meaning. `sqrt` is the nonnegative root and `ln` the natural logarithm.
> `power(a, k)` with a constant nonnegative integer exponent k is the polynomial a^k. Any other
> `power(a, b)` is exp(b ln a) for a > 0, and 0 for a = 0 < b. A point lies in the model only where
> every expression is defined: no division by zero, no logarithm of a nonpositive number, no square
> root of a negative number. A point is exactly feasible if it satisfies every bound, row and
> integrality requirement with no tolerance. A number L is a valid dual bound if L ≤ f(x) for every
> exactly feasible x. The OSiL schema types these values as xs:double, and solvers read binary64
> data. Our results concern the decimal reading. Where we compare with solver output, we say whether
> a statement also holds for binary64 data.

Check against the codes:
- pricing050 and waterno2 are covered by the integer-exponent rule.
- lukvle10's dual covers base 0, and its primal has positive bases.
- etamac and pindyck have positive bases.
- hvycrash, ex6_2_5 and KAN divide only by nonzero denominators at their points, and hvycrash's
  identity uses this.
- The chain and ex6_2 `sqrt` and `ln` arguments are positive.

## 6. Files

- Report: `paper-open-minlplib/development/data-semantics.md` (this file).
- Scripts, README and logs: `paper-open-minlplib/development/data-semantics-checks/`.
  - `data_survey.py`, `enclosure_check.py`, `power_survey.py`, `zero_bases.py`, `misc_checks.py`.
  - `pricing050_rerun.sh`, `run_audit_b64.sh`, `summarize_b64.py`.
  - The reader copies and patches `osilx_ro.py`, `osilx_b64_wrapper.py` and `rocket_b64.patch.py`.
  - `logs/`.

Checks run: only the targeted commands above. No project-wide verification was run.
