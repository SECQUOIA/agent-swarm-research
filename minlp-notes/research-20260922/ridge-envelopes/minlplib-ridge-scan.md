# How often ridge subexpressions occur in MINLPLib

Date: 2026-09-22. Scanned all 1632 OSiL files in `~/.cache/minlplib/minlplib/osil`; none failed to parse.
An instance counts as open if it is listed in
`scouting/minlplib-open-data/open.csv` (537 of the scanned instances; the other 1095 count as solved).

Files:

- `code/scan_ridges.py` is the scanner. It uses `scouting/minlplib-open-data/osil.py` for parsing.
- `minlplib-ridge-counts.csv` has one row per instance.
- `code/minlplib-ridge-agg.json` holds per-instance occurrence counters. The tables below are built from it.

A **ridge** is a subexpression g(a^T x + b) where g is univariate and a has at least 2 nonzero entries.
An occurrence is **relevant** if it needs an envelope side on which g is not convex (or not concave) over the
interval of a^T x + b. Only for these occurrences can a box-aware envelope differ from the envelope computed on the interval.

## Main numbers

The headline subset is "direct+quad+defined". It leaves out the over-counting `defined-loose` rule
(see "Detection rules").

| subset | instances with >=1 | open among them | occurrences |
|---|---:|---:|---:|
| any ridge, direct+quad | 197 | 99 | 284,233 |
| any ridge, direct+quad+defined | 333 | 165 | 379,621 |
| relevant, direct+quad | 149 | 78 | 280,538 |
| **relevant, direct+quad+defined** | **245** | **128** | **292,804** |
| relevant and bounded (all argument variables have finite bounds) | 158 | 68 | 87,078 |
| relevant, top-level only (not nested inside another operator) | 154 | 63 | 75,330 |
| relevant, `defined-loose` only (reported separately; over-counts) | 153 | 68 | 122,273 |

The headline subset has 144,457 distinct relevant ridge arguments. Many occurrences reuse the same a^T x. For
example, sin and cos of the same angle difference both count, and the same pair difference can appear in several rows.

**Open vs solved.** Some relevant ridge occurs in 128/537 = 24% of open instances and in 117/1095 = 11% of solved
instances. With finite bounds required, the counts are 68 open (13%) and 90 solved (8%). Counting top-level
occurrences only gives 63 open (12%) and 91 solved (8%).

**Main findings**

1. Five model families supply almost all occurrences: circle, ring, and sphere packing (expanded (x_i - x_j)^2);
   electron problems (`elec*`, squared differences inside 1/sqrt); polar AC power flow (`powerflow*`,
   `transswitch*`, `deb*`, `var_con*`, sin/cos(theta_i - theta_j)); `polygon*`; and kissing-number models (`knp*`).
   All 40 instances with the most relevant occurrences are open.
2. 97% of relevant occurrences have an argument with 2 variables. Arguments with 3 or more variables occur in 83
   instances (43 of them open; 9,662 occurrences). Most of them come from defined variables or from logs and exps of short sums.
3. Missing bounds are the main obstacle. Most sin/cos occurrences (only 248 of the 56,779 sin occurrences are
   bounded) and all `elec` squares have unbounded variables in the file. Of the 87,078 relevant bounded occurrences,
   71,411 are rank-1 quadratic squares from packing and kissing-number models.
4. Excluding squares, 82 instances (30 open) have a relevant, bounded ridge. Families: `polygon*` (cos/sin of bounded
   angle differences); `gastrans582_*`; `waternd_*` (power 2.435 or 1.852 of a defined flow); `ann_cumene_*` and
   `arki0002`/`arki0015` (sigmoid or tanh of a defined pre-activation); `pooling_epa*` (exp of 3-10-variable sums);
   `ex14_2_*`, `ex6_2_*`, and `ex6_1_*` (ln of sums in Gibbs-energy and phase-equilibrium models); `supplychainp1_*`
   (sqrt of a defined 6-100-variable sum in a minimized objective); `multiplants_*`; `cvxnonsep_pcon*`; and `t1000`.
   Some of these are false positives from the nested rule; see "Known false positives and gaps".

## Detection rules and approximations

All detection is syntactic, on the OSiL expression trees. It does not check whether one expression equals another in value.

- **direct**: the scanner looks for a maximal nonlinear subtree T whose affine sub-subtrees that contain variables all
  have the same direction a (up to scaling), with |supp(a)| >= 2. Then T = g(a^T x + b).
  - If T is op(affine), the sigma label is the operator: `exp`, `ln`, `log10`, `sqrt`, `square`, `power` (constant
    exponent), `kpow` (k^t), `signpower`, `abs`, `sin`, `cos`, `tan`, `tanh`, `erf`, `gammaFn`, or `inv` (c/t).
  - Otherwise the label is `comp[ops]`, listing the nonlinear operators inside T. Examples: `comp[div,exp]` for a
    sigmoid 1/(1+exp(-t)); `comp[cos,sin]` for a cos(t) + b sin(t) with a shared t.
  - Constant multipliers and constant offsets are absorbed. exp(x)*exp(y) and other products of separate factors
    are *not* recombined into exp(x+y).
- **quad**: the scanner collects a row's quadratic terms: the OSiL `qTerm`s plus top-level quadratic monomials in
  the nonlinear tree. It splits them into connected components of the bilinear graph. A component with >= 2
  variables is counted if its coefficient matrix has rank 1, meaning it is c (v^T x)^2, an expanded (a^T x + b)^2.
  - A component is not decomposed further. If several squares share variables in one row, as in
    sum_j (x_i - x_j)^2, the component has rank > 1 and is missed. Differences of squares are also not ridges
    under this rule.
- **defined**: w is a variable that appears inside a maximal univariate nonlinear subtree g(w), or in a lone
  quadratic term c w^2. It is counted if it appears in a linear equality with >= 3 variables and in no other purely
  linear row. Then g(w) = g(a^T x + b) with |supp(a)| >= 2. This rule is a proxy for an auxiliary variable.
  - The interval of w is its own bounds intersected with the interval of the defining expression.
- **defined-loose**: same as defined, but w also appears in other linear rows. The shortest linear equality is used
  as the definition. This fires on flow balances and similar rows that are not definitions, so it is reported only separately.
- **Envelope side needed** (the task's simple rule):
  - The row needs an underestimator if ub < inf or it is a minimized objective. It needs an overestimator if
    lb > -inf or it is a maximized objective. An equality needs both.
  - For a top-level term c*g, an underestimator needs conv(g) when c > 0 and conc(g) when c < 0. An overestimator
    is the reverse.
  - A **nested** occurrence (inside another nonlinear operator, e.g. v_i v_j cos(theta_i - theta_j) or
    1/sqrt(sum of squares)) is assumed to need both sides, as for an auxiliary variable in a factorable relaxation.
    This is conservative: it ignores monotone or convex outer operators.
- **Convexity on the interval**: the interval of a^T x + b comes from the variable bounds and is clipped to sigma's
  domain (t > 0 for ln, log10, and gamma; t >= 0 for sqrt and non-integer powers).
  - Standard operators are tested analytically. For sin, cos, and tan, the test checks whether an inflection point
    lies inside the interval. An unbounded interval counts as neither convex nor concave.
  - Composites are tested numerically: second differences on a 401-point grid, with infinite ends clipped to a
    width of 200.
  - An occurrence is relevant if it needs conv(g) and g is not convex there, or needs conc(g) and g is not concave there.
  - Because square is convex, squares are relevant only when the concave side is needed: equalities,
    (a^T x)^2 >= r, nested occurrences, and so on.
- **bounded**: every variable in a^T x has finite lower and upper bounds in the file. For defined variables, this means
  the variables on the right-hand side, not w. Implied bounds, for example from a sphere constraint, are not derived.

Known false positives and gaps:

- Nested occurrences inside convex, monotone expressions are counted as relevant. Example: `cvxnonsep_pcon*`,
  which is convex, is flagged for k^(x+y) inside another operator.
- The 1-variable affine case (a x + b)^p is not a ridge under |supp(a)| >= 2, so it is not counted.
- Products of separate ridges are not recombined.
- For each instance, "top-level only" gives a stricter count than "relevant". It drops the nested rule.

## Relevant occurrences by kind

| kind | occurrences | of which bounded | instances | open instances |
|---|---:|---:|---:|---:|
| direct | 209,048 | 12,366 | 96 | 57 |
| quad (expanded rank-1 square) | 71,490 | 71,411 | 54 | 22 |
| defined | 12,266 | 3,301 | 103 | 55 |
| defined-loose (not in headline) | 122,273 | 20,632 | 153 | 68 |

## Relevant occurrences by sigma type (direct+quad+defined)

| sigma | occurrences | of which bounded | instances | open instances |
|---|---:|---:|---:|---:|
| square (direct 81,943; quad 71,490; defined 7,875) | 161,308 | 74,440 | 121 | 56 |
| cos | 65,780 | 9,250 | 30 | 29 |
| sin | 56,779 | 248 | 33 | 29 |
| comp[cos,sin] (a cos t + b sin t) | 3,576 | 0 | 7 | 7 |
| power (constant exponent; mostly defined) | 2,129 | 711 | 35 | 21 |
| comp[div,exp] (sigmoid-like) | 1,567 | 1,478 | 6 | 2 |
| exp | 568 | 266 | 9 | 6 |
| tanh (defined) | 339 | 250 | 4 | 4 |
| ln | 237 | 156 | 19 | 11 |
| comp[square] | 177 | 41 | 28 | 2 |
| sqrt | 116 | 58 | 8 | 2 |
| kpow (k^t) | 88 | 87 | 4 | 1 |
| comp[abs] | 26 | 26 | 1 | 1 |
| inv (c/t) | 25 | 25 | 1 | 0 |
| comp[ln,prod] (t ln t etc.) | 24 | 24 | 5 | 4 |
| signpower (defined) | 11 | 0 | 7 | 7 |
| other composites (prod, log10, erf, sin*square, power, div, ln) | 54 | 18 | 12 | 4 |

For comparison, here are the occurrences that are not relevant (convex side only). Across all ridge occurrences,
square has 242,003, ln 1,803, comp[ln,prod] 4,226, and exp 686. The difference from the relevant counts consists of
convex uses such as (a^T x)^2 <= r, -ln(sum) <= ..., and sum x ln(x/sum) in minimized objectives.

## Relevant occurrences by argument size |supp(a)| (direct+quad+defined)

| variables in a^T x | occurrences | of which bounded | instances | open instances |
|---|---:|---:|---:|---:|
| 2 | 283,142 | 84,414 | 183 | 102 |
| 3-5 | 7,856 | 1,219 | 58 | 34 |
| 6-10 | 1,004 | 785 | 29 | 14 |
| 11-100 | 776 | 634 | 16 | 9 |
| >100 | 26 | 26 | 1 | 1 |

Relevant, bounded occurrences with a non-square sigma and >= 3 variables fall into these groups:

- `waternd_*`: power of a defined flow sum with 6-60 variables.
- `ann_cumene_*` and `arki0015`: sigmoid or tanh with 3-5 variables.
- `pooling_epa*`: exp with 3-10 variables.
- `supplychainp1_*`: sqrt with 6-100 variables in the objective.
- `ex14_2_*` and `ex6_2_*`: ln with 3-5 variables.
- `cesam2cent`: ln with 3-10 variables.
- `densitymod`: abs of a 100+ variable defined sum in the objective.
- `lip`, `primary`, and `st_e32`: 11-100 variables.

## Relevant occurrences by context (direct+quad+defined)

| context | occurrences | of which bounded | instances | open instances |
|---|---:|---:|---:|---:|
| equality, nested | 125,778 | 850 | 76 | 61 |
| objective, nested | 81,693 | 1,956 | 24 | 19 |
| inequality, top-level | 71,354 | 71,354 | 58 | 22 |
| inequality, nested | 10,003 | 9,691 | 39 | 8 |
| equality, top-level | 3,760 | 3,074 | 78 | 34 |
| objective, top-level | 216 | 153 | 22 | 8 |

## Top 40 instances by relevant occurrences (direct+quad+defined)

All 40 are open. "distinct" counts distinct relevant ridge arguments. "bounded" counts relevant occurrences whose
argument variables all have finite bounds.

| # | instance | gap | relevant | distinct | bounded | sigma | args | context | structure note |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | elec200 | 2.21 | 59,700 | 59,700 | 0 | square | 2 | obj-nested | electron problem: sum 1/sqrt(sum_d (x_id - x_jd)^2); coordinates unbounded in file |
| 2 | powerflow2736spp | 0.392 | 27,800 | 3,494 | 0 | cos, sin | 2 | eq-nested | polar AC power flow: v_i v_j (G cos + B sin)(theta_i - theta_j); angles free |
| 3 | transswitch2736spp | 0.392 | 27,800 | 3,494 | 0 | cos, sin | 2 | eq-nested | as powerflow, with switching binaries |
| 4 | powerflow2383wpp | inf | 22,308 | 2,886 | 0 | cos, sin | 2 | eq-nested | polar AC power flow |
| 5 | transswitch2383wpp | inf | 22,308 | 2,886 | 0 | cos, sin | 2 | eq-nested | polar AC power flow + switching |
| 6 | ringpack_30_2 | 0.0533 | 15,920 | 870 | 15,920 | square (quad) | 2 | ineq | ring packing, expanded (x_i - x_j)^2 + (y_i - y_j)^2 >= ..., the same differences reused across many rows |
| 7 | elec100 | 2.11 | 14,850 | 14,850 | 0 | square | 2 | obj-nested | electron problem |
| 8 | ringpack_30_1 | 0.109 | 14,180 | 870 | 14,180 | square (quad) | 2 | ineq | ring packing |
| 9 | ringpack_20_3 | 0.0395 | 5,804 | 380 | 5,804 | square (quad) | 2 | ineq | ring packing |
| 10 | ringpack_20_2 | 0.0604 | 5,124 | 380 | 5,124 | square (quad) | 2 | ineq | ring packing |
| 11 | polygon100 | 42.3 | 5,049 | 4,950 | 5,049 | cos 4,950, sin 99 | 2 | ineq/obj-nested | max-area polygon: r_i r_j cos(theta_i - theta_j) in distance rows, r_i r_j sin(.) in objective; angles bounded |
| 12 | knp5-44 | 3.23 | 4,730 | 4,730 | 4,730 | square (quad) | 2 | ineq | kissing number / point packing, pairwise (x_i - x_j)^2 terms expanded |
| 13 | knp5-43 | 3.22 | 4,515 | 4,515 | 4,515 | square (quad) | 2 | ineq | as above |
| 14 | ringpack_20_1 | 0.0604 | 4,364 | 380 | 4,364 | square (quad) | 2 | ineq | ring packing |
| 15 | knp5-42 | 3.17 | 4,305 | 4,305 | 4,305 | square (quad) | 2 | ineq | as knp5-44 |
| 16 | knp5-41 | 3.13 | 4,100 | 4,100 | 4,100 | square (quad) | 2 | ineq | as knp5-44 |
| 17 | knp5-40 | 3.06 | 3,900 | 3,900 | 3,900 | square (quad) | 2 | ineq | as knp5-44 |
| 18 | elec50 | 1.94 | 3,675 | 3,675 | 0 | square | 2 | obj-nested | electron problem |
| 19 | gasoil400 | 8.15e5 | 3,200 | 1,600 | 0 | square (defined) | 3-5 | eq-nested | collocation: w^2 * (y + z), w defined by a collocation equality |
| 20 | powerflow0300p | inf | 3,012 | 408 | 0 | cos, sin | 2 | eq-nested | polar AC power flow |
| 21 | transswitch0300p | inf | 3,012 | 408 | 0 | cos, sin | 2 | eq-nested | polar AC power flow + switching |
| 22 | polygon75 | 30.7 | 2,849 | 2,775 | 2,849 | cos, sin | 2 | ineq/obj-nested | max-area polygon |
| 23 | gasoil200 | 8.15e5 | 1,600 | 800 | 0 | square (defined) | 3-5 | eq-nested | collocation |
| 24 | powerflow0118p | inf | 1,396 | 179 | 0 | cos, sin | 2 | eq-nested | polar AC power flow |
| 25 | transswitch0118p | inf | 1,396 | 179 | 0 | cos, sin | 2 | eq-nested | polar AC power flow + switching |
| 26 | polygon50 | 18.5 | 1,274 | 1,225 | 1,274 | cos, sin | 2 | ineq/obj-nested | max-area polygon |
| 27 | knp4-24 | 2.68 | 1,104 | 1,104 | 1,104 | square (quad) | 2 | ineq | as knp5-44 |
| 28 | truck | 1.26 | 998 | 998 | 998 | square | 2 | obj-nested | objective built from squared differences of consecutive variables divided by a time variable |
| 29 | deb7 | inf | 928 | 232 | 0 | comp[cos,sin], sin, cos | 2 | eq-nested | power-flow-type network, a cos + b sin of one angle difference |
| 30 | deb8 | inf | 928 | 232 | 0 | comp[cos,sin], sin, cos | 2 | eq-nested | as deb7 |
| 31 | deb9 | inf | 928 | 232 | 0 | comp[cos,sin], sin, cos | 2 | eq-nested | as deb7 |
| 32 | arki0002 | inf | 912 | 912 | 912 | comp[div,exp] (defined) | 2 | eq | y = -1 + 2/(1+exp(-w)) (tanh-like activation), w defined by a linear equality |
| 33 | elec25 | 1.70 | 900 | 900 | 0 | square | 2 | obj-nested | electron problem |
| 34 | gasoil100 | 8.15e5 | 800 | 400 | 0 | square (defined) | 3-5 | eq-nested | collocation |
| 35 | ringpack_10_2 | 0.0395 | 760 | 90 | 760 | square (quad) | 2 | ineq | ring packing |
| 36 | var_con10 | inf | 688 | 172 | 0 | comp[cos,sin], sin, cos | 2 | eq-nested | power-flow-type network |
| 37 | var_con5 | inf | 688 | 172 | 0 | comp[cos,sin], sin, cos | 2 | eq-nested | power-flow-type network |
| 38 | case_1scv2 | 7.74 | 600 | 600 | 0 | square | 2 | obj-nested | objective: weighted squared distances ((x - x_j)^2 + (y - y_j)^2) * allocation variable |
| 39 | ringpack_10_1 | 0.0395 | 580 | 90 | 580 | square (quad) | 2 | ineq | ring packing |
| 40 | powerflow0057p | inf | 560 | 78 | 0 | cos, sin | 2 | eq-nested | polar AC power flow |

Gap values come from `open.csv`. `inf` means no finite gap is recorded there.

## Reproduction and checks run

```
PY=~/miniconda3/envs/exact-quadratic-hull/bin/python
cd research-20260922/ridge-envelopes/code
$PY scan_ridges.py --jobs 8        # ~40 s; writes ../minlplib-ridge-counts.csv and ./minlplib-ridge-agg.json
$PY scan_ridges.py --report        # prints the tables above
```

Targeted checks run locally (no CI involvement):

- Spot runs on `ann_compressor_tanh`, `kall_circles_c6a`, `eniplac`, `fac1`, `gasnet`, `4stufen`, and `ex1223`.
- The analytic curvature rules for sin, cos, tan, odd, negative, and fractional powers, c/t, tanh, and abs were
  checked on hand-picked intervals. The numeric composite test was checked on a sigmoid over [-5,5], [0,5], and [-5,0].
- Example rows from `powerflow0057p`, `arki0002`, `deb7`, `truck`, `case_1scv2`, and `gasoil100` were inspected by hand
  to confirm the detected structure.
- None of this checks recall. Ridges that are hidden by expansion (other than the rank-1 quadratic case) or spread
  across auxiliary variables in other ways are not counted.
