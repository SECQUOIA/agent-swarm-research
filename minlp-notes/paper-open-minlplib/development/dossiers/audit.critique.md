# Critique of the audit dossier (family `audit`, second pass)

Reviewer: independent critic, 2026-10-04. `R/` means `research-20260929/`.
I edited nothing under `R/` or `literature/` and committed nothing. Every check
ran on copies in `/tmp/audcrit` (copies of `R/bound-audit/{pages.json,
results.json, screen.json, summary.json}` and `pages/minlplib.solu`). I also
parsed some OSIL files read-only with my own short scripts. I imported or
executed no script from `R/`.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.** All 19 class (i)
refutations, the 3 rocket refutations, the 12 (i-r) re-proofs, the emfl
enclosures and the spring optimum hold. I checked the data, the margins, the
proofs and the new checks of this pass. The problems are these:

1. A headline claim about MINLPLib's aggregate dual is false as stated for
   two family instances.
2. The data-based aggregation rule is explained wrongly. It holds in 589 of
   589 cases, not 585.
3. Lemma 1(b) is false as stated, although none of the 22 refuted bounds is
   affected.
4. The novelty section misses prior reports of wrong dual bounds that are in
   the knowledge base.
5. There are several small number and wording slips.

## What I recomputed (cheap, exact or high precision)

| check | result |
|---|---|
| exact screen from `pages.json` (own code) | 1633 pages, 2816 points, 11086 bounds (11031 finite), 19 labels; senses 1366/264/3; 158 pairs, 46 instances, 56 points, 131 (instance, solver) pairs, 110 from "other" points; 3851 ties on 1133 instances; no beyond-dual point has infeas > 1e-5. All as stated |
| class counts from `results.json` | 19 (i) on 15 instances (11 gross on 9, 8 tolerance-scale on 6); 12 (i-r) on 4; 12 (ii)-proven on 4; 63 (ii)-repair on 11; 25 (iii) on 12. Instance lists as in Section 5.5 |
| margins of all (i)/(i-r) pairs from `obj_hi` | Every Section 5.1 "≥" value is a correct round-down. Smallest (i) ratio: 1.11584 units (smallinvDAX*200-220). With objvar := xᵀQx it is exactly 279/250000000, i.e. 1.116 units. Largest (i-r) ratio: 0.435 units |
| histogram and per-solver split | as stated |
| spring, all 1100 assignments at 60 digits | 210 feasible. f* = 0.8462456656431542812516646350371412952753…; runner-up 0.859275535297028… at (5, 0.307); third 0.891317680305808… at (10, 0.283); d − f* = 4.356845719e-9 (0.871 of 5e-9) |
| smallinvDAX r1 vs r2 (OSIL, exact) | Variables, bounds, row sides, Q and objective are identical. Only e2 differs, with every coefficient exactly 1e-3 lower in r2 |
| operators (OSIL census) | Class (i) and rocket files use only sum, product, negate, divide, square, integer power (2 and 3, ghg_3veh), exp and sqrt. No abs, min, max or trig. oil has log10, ln and power 0.8981 |
| rocket second proof (`rocket_kraw.py`, read) | Sound. It reads the OSIL file through the verifier's parser and asserts the layout and the mass-row structure. The mass rows, g_0 = 1 and D_0 = 0 are checked exactly by `kraw.box_check`. All variable bounds, including T and m, are checked exactly. Krawczyk uses 4N unknowns. The enclosures match the logs and the dossier |
| verify.py and kraw.py Krawczyk terms | The γ_n terms, the factors (1+1e-6)² and (1+4U)·(1+1e-12), the inner/outer radii and the box check are as described. The proof of Proposition 2 is correct (weighted max-norm bound on the spectral radius; uniqueness by the mean value theorem) |
| `gms_osil_drive*.py` (read) | Mistakes in the bound and declaration regexes would show up as mismatches, not as false identities. The comparison iterates over .gms rows only, but row counts match in every log. Note: the smallinvDAX logs print `rows_gms 3` because the epigraph patch leaves no objective row to subtract. All 4 rows were compared |
| `.solu` aggregation rule (own code) | See C1: 589/589 when per-solver `inf` entries are counted |
| emfl050_3_3 p2 as evaluated (`obj_eval` in results.json) | 10.401737934668741. The audit's L minus this value is 1.41970e-5 < 1.42e-5 (confirms AUD-11 on the actual point) |

## Corrections

**C1 (Section 2 "How MINLPLib aggregates"; Section 0; AUD-13). The rule is
explained wrongly.** The four "exceptions" (ball_mk4_15, chp_shorttermplan2c,
nuclear10a, powerflow0057r) are not explained by having no listed point. Each
has one per-solver entry `inf` (an infeasibility claim: CPLEX, GUROBI, SCIP,
SCIP). `solu.py` drops these entries. If they count as bounds, the third-best
entry equals `=bestdual=` in all four cases. For example, ball_mk4_15 has inf,
226 and 58.828859, and `.solu` lists 58.8288590000. Then
`min(third-best incl. inf, lowest listed point)` reproduces **589 of 589**
`=bestdual=` values: 422 exactly, the rest within 6e-9 relative. *Fix:* report
589/589 and state the counting of infinite entries.

**C2 (Section 0 "never invalidated beyond display rounding in this family";
Section 2 "Consequence"; AUD-13). The claim is false as stated for eniplac and
stockcycle.**
- Their third-best per-solver bounds are −132117. and 119949. These are also
  the dual column of `instances.html` (`listing_dual`).
- They exceed the proven exactly feasible objectives by 0.083 and 0.31. The
  dossier's own table shows this ("+0.083 (slack 0.5)", "+0.31 (slack 0.5)").
- The audit-ir review showed that the page displays at 10 significant digits.
  A stored value at or below the proven objective would be shown as
  −132117.083 or 119948.6883, so the page's display rounding allows only 5e-5.
- These two aggregates are therefore "invalid as displayed" in exactly the
  (i-r) sense. They are explained only by the unproven six-digit pre-storage
  rounding.

The claim holds for the 15 class (i) instances, rocket, emfl, spring (8-decimal
page rounding, proved) and lop97icx (+4.0e-7 < 5e-7). It also holds for the
`.solu` values of eniplac and stockcycle (`=opt=`). Section 9, item 6 ("these
instances") is correct if it means the 15 class (i) instances; say so
explicitly. *Fix:* restrict the statement as above. Add: "for eniplac and
stockcycle the third-best per-solver bound, which MINLPLib displays as the
instance dual bound, has the same (i-r) status as the entries it is built
from." The first pass's own `checks/audit/third.log` flags both instances
("third invalid? True").

**C3 (Section 3.2, Lemma 1(b)). Lemma 1(b) is false as stated.** The page rule
that the dossier cites can display binary artefacts. The audit-ir review notes
that the rule reproduces fac1's 160912612.40000001. Example: a stored
b = 160912612.43 is rounded to 10 significant digits, giving 160912612.4. That
decimal is stored as a binary64 value slightly above it, and printing with 8
decimals gives "160912612.40000001". So u(s) = 1e-8, but |b − d(s)| ≈ 0.03,
and H fails. The proof's step "u(s) ≥ v′ as in (a)" needs d(s) to be a
multiple of v′, which fails here. In general, artefacts can occur once
|d| ≥ 2^26 ≈ 6.7e7. Below that, the half-ulp is under 5e-9 and printing
recovers the decimal exactly.

All 22 refuted bounds have |d| ≤ 1.08e7 and at most 10 significant digits, so
no conclusion changes. *Fix:* add the hypothesis "d(s) has at most 10
significant digits (true whenever |d| < 2^26)". Also note that for |b| < 10 the
page rule is two roundings (10 significant digits, then 8 decimals). This case
is covered by (c) with a final rounding to nearest, not by one rounding at v′.

**C4 (Section 2 table, last column). Two values are inconsistent.**
- smallinvDAX*150-165 shows "−1e-11; −1e-11". This is an artefact: `agg.py`
  used the outward display end 88.10493476001. The exact values are −6e-15
  with the listed point (88.104934760000006) and 0 with the xᵀQx point.
- eniplac ".solu − f = +1.4e-5" uses the audit enclosure end. The caption says
  f is the Section 5 value, and Section 5.2 gives −132117.08301998871…, which
  yields +2.0e-5.
- For "not beaten" statements the conservative end is the *lower* end of the
  enclosure, not the upper one used in `agg.py`. No conclusion changes.

*Fix:* use one f per instance and the exact values.

**C5 (Section 1.1, "Models"). The OSIL file check is overstated.** The dossier
says the 1632 OSIL files are "byte-identical to the live files (checked by
both verifiers and the status track)". The status track checked 69 files
(sha256). The verifiers checked only the files they re-fetched. *Fix:* state
this scope.

**C6 (Section 2 and Section 7, Vigerske quote).** The slide reads "Only trust
a solvers dual bound claim if it has been verified by at least 2 other
solvers." *Fix:* quote it verbatim or use [sic].

**C7 (Section 9, item 4). The wording is ambiguous and incomplete.** "The other
eight" follows the four >1% pairs, so it reads as "the other 15". The seven
gross pairs at 1.2e-5–7.3e-5 of |d| are not mentioned. These are below common
1e-4 relative gap tolerances, a caveat the audit report stresses. *Fix:* "Of
the other 15, seven lie between 1.2e-5 and 7.3e-5 of |d|, below common 10⁻⁴
gap tolerances. The eight tolerance-scale margins lie between …"

**C8 (AUD-5 resolution). The topopt points are not three independent
points.**
- The committed point (10.3354743278…) and the one-thread regenerated point
  (10.3354743278317…) both come from `cert_topopt.py`. Only the verifier's
  `topopt_exact.py` is independent, so there are two independent
  implementations.
- The verifier's "≤ 10.335474275747004" is `float()` of an exact rational
  (rounded to nearest), so it can sit up to about 1e-15 below the exact upper
  bound.

*Fix:* write "two independent implementations, all proven points ≤ 10.33548".
If the verifier's value is quoted as a bound, use "≤ 10.33547427574701".

**C9 (AUD-8, oil). The numbers and the proposed method need refinement.**
- "1408 rows of rank 1391" is the first attempt. The route C reduced system
  has 1141 rows of rank 1131, which matches the audit report's "10 dependent
  equality rows after all reductions" (`logs/verify/oil.p2.json`).
- The oil rows contain log10, ln and power 0.8981. Dropped rows can be
  "verified identically" only by symbolic identity after merging the variables
  that are equal. Exact evaluation of these rows is not possible.
- "Would add two class (i) pairs" should read "could add".
- The violation 7.1e-11 is the audit's measurement; MINLPLib lists 4e-12.

*Fix:* update the text, and treat the cost estimate as uncertain.

**C10 (Section 1.5, negative controls).** The spring change
x3.up 0.02 → 0.0200000000001 is 1e-13 absolute but 5e-12 relative, not
"about 1e-13 relative".

**C11 (Section 1.3, sssd).** The objective coefficient of q is
113818.899052505, not 113818.9. Give the exact value or mark the display as
rounded.

**C12 (Section 0, emfl bullet).** "The listed primal values lie below the
exact optimum" should be "the best listed primal values". emfl050_3_3 p3 lies
at least 4.913e-5 above the proven upper bound.

**C13 (AUD-1, rocket margin).** Under the audit's display convention, margins
are sizes rounded to nearest, so the summary's "1.1e-7" is not an error. If
the paper uses "at least", the summary's rocket400 "1.9e-7" (true value
1.895e-7) needs the same change as rocket100: use 1.89e-7. The dossier's own
Section 9, item 10 already does this.

## Additional issues

**A1 (minor; strengthens AUD-2). The knowledge base contains prior reports of
wrong solver dual bounds that Section 7 does not cite.**
- Nowak and Vigerske 2008 (`nowak2008-lago-a-heuristic-branch-and`): "For the
  QQP bayes2_10 LaGO found a better point because BARON computed a wrong lower
  bound in the root node."
- Vigerske and Gleixner 2017 (`vigerske2017-scip-global-optimization-of-mixed`):
  "SCIP fails on a few instances, e.g., by computing a wrong dual bound."
- The stored `instances.html` lists removed instances with notes such as
  "bearing: Difficult numerical behavior. Optimal value changes by > 2% when
  increasing feasibility tolerance" (also minlphix).

These are anecdotal and tolerance-based, not rigorous. Still, any priority
claim must be about the systematic screen of listed data with exact-feasibility
proofs, not about finding wrong bounds. *Resolution:* cite these in Section 7
and fold them into the AUD-2 search.

**A2 (minor; scope of the corollaries). The refutations are proofs for the
decimal (exact rational) reading of the model files.** GAMS and the solvers
parse decimals into binary64, so they see a slightly perturbed model. The
"tolerance independence" corollary covers feasibility tolerances, not this
data rounding. The GAMS-form corollary inherits the exact reading. Each of the
two status-track documents notes this ("exact under the stated reading"). The
effect is negligible next to the margins: relative coefficient changes of
about 1e-16, against margins of at least 1.9e-9 relative. It is not proved,
though. *Resolution:* one sentence in Section 3.2 and in claim 3.

**A3 (minor; coverage of the form check). stockcycle has no exact .gms/OSIL
comparison.** The (i-r) statements are also model statements, and stockcycle
rests only on GAMS conversion plus sample-point evaluation. The parser rejects
its objective only because the defining row is a rational function.
*Resolution:* extend `gms_objective` to rational defining rows (a few lines;
seconds to run), or state the limit.

**A4 (minor; AUD-11 evidence).** The point p2 itself, not only a widened
display, contradicts the audit's "at least 1.42e-5". The listed
`emfl050_3_3.p2.sol` evaluates to 10.401737934668741 (`results.json`
`obj_eval`). The audit's exact L minus this value is 1.41970e-5. Use "at least
1.41e-5" in the paper.

**A5 (note on cost estimates).** The other estimates (AUD-3 under a minute,
AUD-4 seconds, AUD-5 about 165 s for topopt) match the logs and the
reproduction guide. The optional AUD-6 all-rational nuclear14 test is a dense
434×434 product in `Fraction`s, about 8e7 rational operations. Expect tens of
minutes rather than "minutes"; it is still cheap.

## Points that survive scrutiny (no change needed)

- Proposition 1 and Lemma 1(a) and (c) are correct.
- All 22 refutations exceed one display unit (minimum 1.069, rocket100). All
  19 class (i) refutations exceed 10/9 units (minimum 1.1158).
- Proposition 2 and its corollary are correct. Only rows that vanish
  identically or have point enclosures can pass as equalities, so no equality
  passes by accident.
- Proposition 3 (weak duality) is correct for the asserted structure.
- Proposition 4 (spring): the reduction, h(x) = (x−1) + 7/4 + 3/(4(x−1)), the
  convexity, the evaluation at (9, 0.283) and the enumeration counts are
  reproduced.
- All Section 5 numbers I checked agree: the margins and their round-downs,
  the relative margins, units, distribution and per-solver counts, the emfl
  shortfalls, 3.4e-11 (the recheck's widest enclosure, emfl050_5_5,
  3.33e-11), and the rocket margins.
- The dossier's own critical items AUD-1 to AUD-15 are sound apart from the
  refinements above (C8, C9, C13, A1, A4).

## Commands run (targeted; not project-wide verification, not CI)

All in `/tmp/audcrit` on copies, one process, inline `python3` snippets:
exact screen and recount from `pages.json`; class recount and margins from
`results.json`; `.solu` aggregation test with `inf` entries counted; spring
1100-assignment scan at 60 digits (mpmath); smallinvDAX r1/r2 OSIL comparison;
operator census of 19 OSIL files (read-only XML parse of `~/.cache` files);
binary64 display-artefact demonstration for Lemma 1(b); emfl p2 shortfall from
`obj_eval`. I read without running: `rocket_kraw.py`, `gms_osil_drive*.py`,
`agg.py`, `solu.py`, `recount.py`, `R/bound-audit/verify.py` (krawczyk,
check_on_box, polish_and_verify), the verifier's `kraw.py` and `ivl.py`,
`R/publication/minlplib-status/exact_forms.py`, and the logs and reports cited
above.
