# Audit of the two historical solver discrepancies

The saved outputs contain two independently demonstrable primal feasibility
failures. Neither conclusion needs the historical nonlinear certificate. The
SBB run returned a point violating two linear rows of `clay0204m`; the SHOT run
returned `b4 = b5 = 1` in `risk2bpb`, although both variables were fixed to zero.
These are findings about the saved GAMS/solver runs. The evidence does not
identify which component of either solver integration caused the failure.

This audit was performed on 2026-09-13. It supersedes descriptions of these cases
as disagreements established solely by consensus or historical certificate
acceptance. Hardened complete replay of the saved `clay0204m` certificate now passes.
Together with the independent exact feasible witness below, it establishes
that this model has exact optimum **6545**. This conclusion is specific to
`clay0204m`; it does not certify the other historically near-matching primal
values.

## Reproduction and evidence

From `code/minlp_solver_lab`, run:

```sh
.venv/bin/python -m certify.audit_solver_discrepancies
```

The script uses exact rational arithmetic to evaluate polynomial constraints and
bounds, compares the two GAMS/Pyomo source formulations symbolically, and writes:

- `results/solver_discrepancy_audit/audit.json`: source hashes, status records,
  all residuals of the printed vectors, and model comparison results.
- `results/solver_discrepancy_audit/clay0204m_primal_witness.json`: an exact
  feasible point with objective `6545`.

To also reproduce the joined optimality result, run:

```sh
.venv/bin/python -m certify.audit_solver_discrepancies --verify-certificate \
  --viprchk /home/sgusev/.local/opt/scip-exact/bin/viprchk
```

This writes `results/solver_discrepancy_audit/clay0204m_optimality.json`, which
contains the complete lower-bound check, the independently rechecked feasible
witness objective, and SHA256 hashes of the source model, witness, certificate
artifacts, and checker source files. The command confirms those inputs and
checker files did not change during its execution. Both the internal exact
proof replay and the external checker passed. The external checker is optional;
the internal exact proof replay is always required for the joined result.

Without `--verify-certificate`, the script does not invoke a solver, a certificate
checker, or the production nonlinear cut code. It uses Pyomo to load expressions and SymPy to compare source
formulas. Its exact primal evaluator permits only rational operations and
integer powers. It does not evaluate the fractional-power risk objective as an
exact rational or certify a risk upper bound.

The original evidence is in `code/minlp_solver_lab/baseline/lst/`, in the
`clay0204m.sbb.{log,lst}` and `risk2bpb.shot.{log,lst}` files. The compact records
are in `baseline/out/`. Their columns are `modelstat, solvestat, objval, objest,
resusd, nodusd`, as written by `baseline/run_one.sh`. The wrapper used a
60-second limit, `optcr=1e-4`, `optca=1e-6`, and four threads.

## `clay0204m`: SBB

The historical compact record is:

```text
8,1,5075.0000000000,5075.0000000000,1.799,655
```

The listing explicitly identifies model status 8 as **Integer Solution** and
solver status 1 as **Normal Completion**. It does not identify model status 1
(Optimal). The SBB log reports a zero gap and best possible value `5075`, but
also warns `Non convex model!`, with numerical jumps in objectives and bounds.
The old benchmark summarizer counted status 8 as solved when its reported gap
closed. Accordingly, describing this as an unqualified SBB “optimal” status
loses a material distinction.

More decisively, the saved listing itself contains these row levels:

| GAMS row | Pyomo row | Expression | Level | Upper bound | Violation |
|---|---|---|---:|---:|---:|
| `e30` | `e29` | `x2 - x4 + 51*b13` | 51 | 46.5 | 4.5 |
| `e41` | `e40` | `x6 - x7 + 86*b24` | 85 | 82 | 3 |

The corresponding variable levels are `x2 = x4 = 50.4233`, `b13 = 1`,
`x6 = 75.6615`, `x7 = 76.6615`, and `b24 = 1`. Exact evaluation of these printed
numbers gives the same violations. They cannot be explained by four-decimal
printing. Even assigning every displayed variable an error of `0.00005` changes
the respective expressions by at most `0.00265` and `0.0044`.

The listing's report summary nevertheless says zero infeasible rows. This is
an inconsistency in the saved returned solution/report, not evidence that the
listed point is feasible. A small printed noninteger value of `b34` is separately
reported by the audit and is not used to establish the failure.

### Exact feasible point at 6545

Starting from the BARON listing, interpret the displayed values as rationals
and replace the tiny positive values of `x41`, `x48`, `x49`, and `x52` by zero.
The resulting point passes all 90 constraints, all 52 variable bounds, and all
32 binary requirements exactly. Its objective is exactly `6545`.

The eight layout coordinates are:

```text
x1..x8 = (47.8184, 47.8184, 43.8184, 51.3184,
          79.9456, 74.4456, 79.9456, 79.9456)
```

The distance variables are:

```text
x41..x52 = (0, 4, 3.5, 4, 3.5, 7.5, 5.5, 0, 0, 5.5, 5.5, 0)
```

The binary variables equal to one are `b11`, `b14`, `b16`, `b24`, `b27`, `b37`,
`b38`, `b39`, and `b40`; all other binary variables are zero. The artifact stores
all coordinates as rational strings. This establishes an exact upper bound of
`6545`. Complete replay of the saved certificate with the hardened checker establishes
a matching lower bound of exactly `6545` for the same hashed model. The joined
report therefore establishes an exact optimum of `6545`. All model coefficients in this case are
integers or dyadic fractions, so decimal and exact binary64 coefficient
interpretations coincide.

## `risk2bpb`: SHOT

The historical compact record is:

```text
1,1,-56.8208726095,-56.8208726095,0.046,0
```

The log identifies SHOT version `1.1`, Git hash `a81275b4`, using CPLEX 22.1
for its dual problem. It classifies the model as convex and reports a globally
optimal primal solution with an absolute gap about `4.74e-11`.

However, the listing contains:

| Variable | Lower | Level | Upper |
|---|---:|---:|---:|
| `b4` | 0 | 1 | 0 |
| `b5` | 0 | 1 | 0 |

GAMS uses `.` for zero in this listing. The source explicitly sets `b4.fx = 0`
and `b5.fx = 0`; the Pyomo source gives both binary variables bounds `(0,0)`.
Thus the returned point violates each fixed upper bound by one. No certificate,
objective comparison, fractional-power evaluation, or numerical tolerance
argument is needed to identify this failure.

After applying the necessary variable renaming, the row residuals of the
printed vector are small (largest about `4.8e-5`), consistent with display
rounding. Checking only rows would miss the error. Checking all variable bounds
is essential here. A floating evaluation of the correctly mapped objective is
about `-56.82087261065`, consistent with the saved objective; this numerical
agreement does not repair the infeasible binary values.

The listing again reports zero infeasibilities. The cause could lie in the
solver, model import, bound handling, solution export, or the GAMS interface;
these saved files do not distinguish those possibilities. No fresh execution or
upstream root-cause diagnosis is claimed.

## Model equivalence and limits of the conclusions

For both cases, symbolic comparison passes for every constraint and the
objective after eliminating GAMS's free objective variable and its defining
row. Every variable domain and bound also matches. Specifically:

- `clay0204m`: GAMS has 53 variables and 91 equations; Pyomo has 52 variables
  and 90 constraints. GAMS `e(k+1)` corresponds to Pyomo `e(k)`; remaining
  variable names are unchanged.
- `risk2bpb`: GAMS has 464 variables and 581 equations; Pyomo has 463 variables
  and 580 constraints. Rows have the same shift. GAMS `x462`, `x463`, `x464`
  correspond to Pyomo `x461`, `x462`, `x463`. Other variables retain their names.

The automated source comparison interprets each floating literal as its exact
binary64 value before symbolic arithmetic. It establishes equivalence of the
supplied source formulas under that common interpretation. It does not verify
the GAMS compiler, reconstruct the precise historical in-memory model, or prove
that a rational-decimal model equals its binary64 counterpart. Initial levels
are not part of the feasible-set comparison. The baseline commands show no
`u1` model override.

These interpretation limits do not weaken the two specific infeasibility
findings: the violated row coefficients and bounds are exactly representable
integers or halves, and the source and listing agree on them. The appropriate
claim is that the saved GAMS/SBB and GAMS/SHOT runs returned infeasible points
with apparently successful completion/status reporting. An attribution to a
particular upstream software defect requires further reproduction and diagnosis.
The exact `clay0204m` feasible witness and matching complete certificate replay
establish exact optimality for this instance. General
claims that all historical near-matching primal values are certified upper
bounds remain unsupported.
