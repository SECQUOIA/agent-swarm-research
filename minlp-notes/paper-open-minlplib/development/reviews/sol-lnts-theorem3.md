# Independent review of lnts Theorem 3

Reviewer: sol review sub-agent. Date: 2026-10-04.

**Verdict: verified.** Theorem 3 gives the exact, attained global optimum of
each cached OSIL model for N = 50, 100, 200, 400. I found no blocker or major
issue. The zero-gap result is justified by the theorem's newly defined
linear-tangent point. It does not make the previously stored primal points
optimal; those points are strictly suboptimal, although their objective
enclosures overlap the optimum. Three minor reporting issues are listed below.

I independently parsed all four OSIL files and wrote a new checker using only
the Python standard library. Its proof arithmetic uses integers, `Fraction`,
and `isqrt`; it does not use floating point, mpmath, Newton iteration, or any
repository module. The code, exact rational certificates, and output are in
[/tmp/sol-lnts-review/verify.py](/tmp/sol-lnts-review/verify.py),
[certificate.json](/tmp/sol-lnts-review/certificate.json), and
[run.log](/tmp/sol-lnts-review/run.log). These scratch artifacts must be retained
elsewhere if the paper needs a permanent reproduction package.

## 1. Reconstruction from the OSIL files

I read `~/.cache/minlplib/minlplib/osil/lnts{50,100,200,400}.osil` directly with
`xml.etree.ElementTree`. Every finite decimal is converted directly from its
string to an exact rational. The parser expands the compressed linear arrays,
including `mult` and `incr`, and checks every variable, objective coefficient,
linear row, quadratic term, and nonlinear expression tree. It rejects
unexpected instance-data sections and unexpected attributes in the checked
sections. No repository reader is used.

The variable order is θ, px, py, vx, vy, each with N+1 entries, followed by h at
zero-based index 5N+5. All variables have default type C. The objective is
minimize N h, with default constant 0 and weight 1. There are exactly 4N
equality rows, each with both bounds 0 and default row constant 0. In their
OSIL order they are, for i = 0,...,N−1:

\[
\begin{aligned}
px_{i+1}-px_i-\tfrac12 h(vx_i+vx_{i+1})&=0,\\
py_{i+1}-py_i-\tfrac12 h(vy_i+vy_{i+1})&=0,\\
vx_{i+1}-vx_i-50h(\cos\theta_i+\cos\theta_{i+1})&=0,\\
vy_{i+1}-vy_i-50h(\sin\theta_i+\sin\theta_{i+1})&=0.
\end{aligned}
\]

The position rows contain two quadratic coefficients −.5; the velocity rows
contain the exact product of a sum of two trigonometric terms, each with
coefficient 100, the number −.5, and h. There are no other objective or row
terms. Bounds are exactly:

- −B ≤ θ_j ≤ B, where B = 1.5707963267949 = 15707963267949/10^13;
- h ≥ 0, with no upper bound;
- px_0 = py_0 = vx_0 = vy_0 = vy_N = 0, py_N = 5, vx_N = 45;
- every other state variable is free, including px_N.

Several initial-state bounds and vy_N use `ub="0"` with the default variable
lower bound 0. Treating their missing lower bounds as −∞ would change the
model. My reader applies the defaults explicitly. The OSIL variable names
skip the eliminated objective variable: h is named x257, x507, x1007, and
x2007, respectively. The index formula in the dossier is correct.

| Instance | Variables | Equality rows | Result |
|---|---:|---:|---|
| lnts50 | 256 | 200 | Every row, bound, and objective term matches |
| lnts100 | 506 | 400 | Every row, bound, and objective term matches |
| lnts200 | 1006 | 800 | Every row, bound, and objective term matches |
| lnts400 | 2006 | 1600 | Every row, bound, and objective term matches |

The SHA-256 of each OSIL file matches the corresponding stored primal point's
`osil_sha256`. All four full hashes are recorded in `certificate.json`.
The model statement in dossier §1.1 matches these files exactly.

## 2. Proof audit

**Elimination and weights.** Starting from the fixed zero initial states,
each recursion determines the next state with coefficient 1. For arbitrary
controls and h, summing the velocity equations gives

\[
vx_N=100h\sum_jw_j\cos\theta_j,\qquad
vy_N=100h\sum_jw_j\sin\theta_j,
\]

where w_0 = w_N = 1/2 and every interior w_j = 1. Substituting the vertical
velocity recursion into the position recursion gives

\[
py_N=100h^2\sum_jc_j\sin\theta_j,
\quad c_0=(2N-1)/4,\quad c_j=N-j\ (1\le j<N),\quad c_N=1/4.
\]

My code derives the entire coefficient vectors by symbolic forward recursion
on integer arrays, rather than using the dossier's double-sum definition or
random stand-ins. The derived vectors match these formulas and satisfy
c_{N−j} = Nw_j − c_j exactly. The horizontal position equations add no terminal
restriction because px_N is free. There are no omitted state bounds.

An exactly feasible point cannot have h = 0: its horizontal terminal velocity
would be zero. Thus every exactly feasible point has h > 0 and satisfies
E1–E3 with A(h) = 9/(20h), B(h) = 1/(20h²). Conversely, those three equations,
the control bounds, and h > 0 make the recursion point exactly feasible.
Lemma 1 is therefore an equivalence for this OSIL model.

**Proposition 2 and the split.** For any real μ and ν ≥ 0, E1–E3 imply

\[
A(h)+\nu B(h)=\sum_j
\{w_j\cos\theta_j+(\mu w_j+\nu c_j)\sin\theta_j\}
\le\sum_j\sqrt{w_j^2+(\mu w_j+\nu c_j)^2}=S(\mu,\nu).
\]

Each inequality is Cauchy–Schwarz against the unit vector
(cos θ_j, sin θ_j). It holds for every real angle. In particular, the tiny
part of the OSIL interval beyond ±π/2 causes no failure. No positivity of
cos θ at arbitrary feasible points is assumed. μ is unrestricted: the
optimal μ is negative, which is allowed. The older `lnts_bound.py` docstring's
phrase “mu, nu >= 0” is not a condition in the reviewed proposition and must
not be imported into it.

The function being compared is strictly decreasing on h > 0:

\[
\frac{d}{dh}(A(h)+\nu B(h))
=-\frac9{20h^2}-\frac\nu{10h^3}<0.
\]

The nonnegative sign condition on ν is sufficient and is satisfied by the
certified root. No convexity of the original feasible set, convex relaxation
exactness theorem, or general strong-duality assertion is needed.

**Theorem 3, step 1: feasibility.** Reflection gives r_{N−j} = −r_j, where
r_j = c_j/w_j − N/2. At θ_j* = arctan(ν*r_j), the cosine is positive and equals
(1+ν*²r_j²)^(−1/2); the sine is ν*r_j times that value. Reflected sine terms
cancel in E2, including the zero middle control. E1 follows from
h* = 9/(20C(ν*)). The root equation yields
D(ν*) = (20/81) C(ν*)² = 1/(20h*²), exactly the constant required in E3.
The recursion then meets every row and terminal bound. C is positive and
finite, so h* > 0.

The angle-bound step is also valid for the exact decimal B. My rational
alternating-series check, using Machin's identity
π/2 = 8 arctan(1/5) − 2 arctan(1/239), proves
3×10^−15 < B−π/2 < 4×10^−15. Thus |arctan t| < π/2 < B for every finite t.
Independently, the certified brackets give max |ν*r_j| < 3/2, and
arctan(3/2) = π/4 + arctan(1/5) < 1 < B. Attainment is well inside the bounds;
it does not depend on replacing B by π/2.

**Theorem 3, step 2: global optimality.** With μ* = −ν*N/2,
μ*w_j + ν*c_j = w_j ν*r_j. Since w_j > 0, each support inequality is attained
by θ_j*. Consequently S(μ*,ν*) = A(h*)+ν*B(h*). For any exactly feasible
point, Proposition 2 gives A(h)+ν*B(h) ≤ A(h*)+ν*B(h*). Strict decrease implies
h ≥ h*. The attaining point has objective N h*, proving both the lower bound
and attainment. This argument covers every exactly feasible point, including
points outside the symmetry ansatz.

**Theorem 3, step 3: existence and enclosure.** C and D are continuous. A
strict sign change at positive rational endpoints proves a positive root by
the intermediate value theorem. Each term of C is nonincreasing on ν ≥ 0,
so C(b) ≤ C(ν*) ≤ C(a) for a ≤ ν* ≤ b. Inverting positive outward bounds for
C gives the correct objective enclosure, with the lower objective end using
the upper bound for C(a) and the upper objective end using the lower bound for
C(b). The dossier's signs and inversion directions are correct.

Uniqueness is unnecessary, as stated. It can also be proved directly. Reflection
rewrites D(ν) as ν Σ_j w_j r_j²/(1+ν²r_j²)^(1/2), so
D'(ν) = Σ_j w_j r_j²/(1+ν²r_j²)^(3/2) > 0. Since C > 0 and C' ≤ 0,
g' = D' − (40/81)CC' > 0 on ν ≥ 0. Thus each certified bracket contains the
unique positive root.

## 3. Independent exact-arithmetic computation

For rational t, put q = 1+t² = p/d and M = 10^120. My checker computes
k = isqrt(floor(d M²/p)), then verifies the integer inequalities

\[
k^2p\le dM^2<(k+1)^2p.
\]

They prove k/M ≤ 1/√q < (k+1)/M. This directly encloses the reciprocal square
root, unlike the dossier's square-root enclosure followed by inversion.
Positive weighted sums give bounds for C and, using the reflection identity,
for D = ν Σ w_j r_j²/√(1+ν²r_j²). There is no cancellation in my D evaluation.
If [C_L,C_U] and [D_L,D_U] are those bounds, g is enclosed by
[D_L−(20/81)C_U², D_U−(20/81)C_L²].

Starting independently at [0,4/N], the checker verifies opposing signs and
performs 300 rational bisections. It accepts a side only after its entire
g enclosure has a strict sign, and fails if precision cannot decide a sign.
The final endpoints a,b are positive, have b−a < 10^−90, and satisfy
g(a) < 0 < g(b). Their exact fractions and C/g enclosures are saved in
`certificate.json`. The following compact sign displays are outward bounds;
the units in both sign columns are 10^−93.

| N | Enclosure of g(a), ×10^−93 | Enclosure of g(b), ×10^−93 |
|---|---|---|
| 50 | [−233669, −233668] | [72259, 72260] |
| 100 | [−993424, −993423] | [231184, 231185] |
| 200 | [−4104248, −4104247] | [795068, 795069] |
| 400 | [−17463433, −17463432] | [2134718, 2134719] |

Each resulting rational optimum enclosure is narrower than 1.11×10^−91.
Outward rounding to 40 decimal places reproduces the dossier's four displayed
intervals exactly:

| N | Lower end | Upper end |
|---|---|---|
| 50 | 0.5546687649386788986220922339726517468015 | 0.5546687649386788986220922339726517468016 |
| 100 | 0.5545954011669111610017828739043968162226 | 0.5545954011669111610017828739043968162227 |
| 200 | 0.5545770161030836720556252926039795506005 | 0.5545770161030836720556252926039795506006 |
| 400 | 0.5545724137006871088173911331507631508456 | 0.5545724137006871088173911331507631508457 |

Negative checks pass for all four N: changing one OSIL acceleration constant
by 10^−40 is rejected, and shifting the final bracket by either +10^−55 or
−10^−55 is rejected by the strict sign test. These checks use altered data in
memory; the source files are untouched.

## 4. Comparison with the exactly feasible stored points

I compared with `research-20260929/publication/primal/lnts/points/lnts<N>_point.json`
using both the displayed 25-digit objective intervals and the stored 60-digit
enclosure of h multiplied exactly by N. Every one contains my entire optimum
enclosure. The comparisons use exact rational endpoints, not the log JSON's
floating-point width fields. I did not rerun the Krawczyk existence proof; its
independent primal reviews remain the evidence that these stored points exist.
Theorem 3 independently proves existence of its own attaining points.

Here P is the stored point's objective. The following bounds for P−opt are
outward-rounded interval subtractions, in units of 10^−59. The last column also
uses the analytical nonnegativity proved above.

| N | Stored objective interval minus my optimum interval, ×10^−59 | Safe upper bound on the stored point's gap |
|---|---|---|
| 50 | [−1.156894, 3.843107] | 3.843107×10^−59 |
| 100 | [−8.848572, 1.151429] | 1.151429×10^−59 |
| 200 | [−2.881321, 17.118680] | 1.7118680×10^−58 |
| 400 | [−35.030304, 4.969697] | 4.969697×10^−59 |

These interval overlaps are consistency checks, not equality proofs. In fact,
each stored middle fixed control is a nonzero rational with magnitude below
10^−110, confirmed directly from the point files. For the theorem's multipliers,
the middle support term has r_{N/2}=0, w_{N/2}=1, and its deficit is
1−cos θ_{N/2}. Equality at h=h* requires that deficit to be zero, as all support
deficits are nonnegative. Within the OSIL angle bounds this requires
θ_{N/2}=0. Every stored point therefore has P > opt. The available 60-digit
enclosures do not resolve its positive gap.

## 5. Numbered issues and safe paper displays

1. **Minor — distinguish the attaining point from the stored primal points.**
   The dossier's proposed strengthening is correct, but adopting it must also
   adopt the exact control θ_j* = arctan(ν*r_j) as the attaining point. Do not
   infer that the previously stored points are optimal from overlapping
   objective enclosures. The critic's §Verdict says “agree ... to at most
   3.5e-58”; that is an approximate description of enclosure agreement, not
   proof of equality. The exact interval comparisons above clarify this.
   A literal zero gap to those stored points would be false. Zero primal-dual
   gap at the theorem's point is proved.
2. **Minor — distinguish rational certificate width from displayed width.**
   The dossier's sub-10^−60 width claim refers to its underlying rational
   enclosures; its 40-place table has width 10^−40. Both are valid, but the paper
   should identify which interval its width describes. My underlying rational
   intervals have width below 1.11×10^−91; the table above still has width
   10^−40. The `lnts_exact_opt.json` width fields are approximate floating-point
   reports, not exact certificate endpoints. My JSON saves both exact ends.
3. **Minor — separate the old primal's rounding effects from enclosure width.**
   Dossier §8.1 L2's “at most 7e-26 above” comparison is valid as a coarse bound,
   but the 25-digit display width does not measure the loss from rounded
   controls. Its `point_obj_ge_opt_lower` flag tests the point enclosure's
   upper end against the optimum's lower bound, not that the entire point
   enclosure lies above it. Use the 60-digit comparisons above and state that
   the stored point's small positive gap is unresolved by those enclosures.

There are **no blocker or major issues** with the model match, Proposition 2,
Theorem 3, or adoption of the exact-optimum result.

For a concise paper table, I recommend these endpoints, with 16 decimal places:

| Instance | Certified lower, rounded down | Certified upper, rounded up |
|---|---|---|
| lnts50 | 0.5546687649386788 | 0.5546687649386789 |
| lnts100 | 0.5545954011669111 | 0.5545954011669112 |
| lnts200 | 0.5545770161030836 | 0.5545770161030837 |
| lnts400 | 0.5545724137006871 | 0.5545724137006872 |

Recommended accompanying claim: “For each lntsN, N ∈ {50,100,200,400}, the
optimal value is exactly 9N/(20C(ν*)), where ν* is the positive root of
D(ν)−(20/81)C(ν)²=0. It is attained by θ_j*=arctan(ν*r_j) and the model's
forward recursion. Hence the mathematical primal-dual gap is zero.” The
finite decimal table gives enclosures, whose upper-minus-lower difference is
10^−16; its endpoints are not themselves equal to the optimum.

## 6. Commands and verification limits

The targeted computation was run from the repository working directory as:

```bash
taskset -c "$(python3 -c 'import os; print(min(os.sched_getaffinity(0)))')" \
  env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 /tmp/sol-lnts-review/verify.py > /tmp/sol-lnts-review/run.log
```

Result: exit 0; all four model checks, root signs, optimum enclosures,
primal/dossier comparisons, angle-bound checks, and negative checks pass.
I ran this command twice, with the second run adding the explicit assertion
that every stored middle control is nonzero. The final log and certificate
are from the second run. A separate read-only `python3` inspection of the
certificate confirmed the compact sign intervals and the 3×10^−15 to
4×10^−15 bound on B−π/2 printed in this review. Other commands were source
reads and XML/JSON inspections.

The computation was pinned to one available CPU core. No repository script
was imported or executed, in place or otherwise. No project-wide verification,
CI status inspection, solver run, network lookup, or commit was performed.
All writes were confined to `/tmp/sol-lnts-review/` and this review file.
The arithmetic trust base is Python exact integer/Fraction arithmetic,
integer square root, and the checked XML reconstruction; the analytic proof
uses Cauchy–Schwarz, elementary trigonometric identities, monotonicity,
the alternating-series remainder bound, and the intermediate value theorem.
