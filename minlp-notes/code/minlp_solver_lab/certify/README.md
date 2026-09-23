# Checkable bounds for convex MINLP

The checker reconstructs exact expressions from a loaded Pyomo model, checks rigorous rational cuts, and independently replays a complete rational MILP proof. A numerical solver is needed to generate benchmark certificates, but not to replay the bundled example.

Start with [the self-contained quadratic example](examples/quadratic/README.md). Its source, rational master, nonlinear lemmas, and complete proof are included. It establishes the exact optimum `1/4` using a checked lower bound and an explicit feasible point. The example's pinned requirements contain only Pyomo, NumPy, SymPy, mpmath, and python-flint.

The [repair and replay record](../../../notes/certified-minlp-repair-and-replay.md) gives the current results, independent reviews, and remaining restrictions. The [soundness note](../../../notes/certified-minlp-soundness.md) states the mathematical hypotheses. This is an ordinary software checker with an explicit trusted base, not an end-to-end Lean proof.

**Checking an existing certificate.** From `code/minlp_solver_lab` in an environment containing the example's dependencies:

```python
from certify.driver import check_certificate

result = check_certificate(
    "certify/examples/quadratic/instance.py",
    "certify/examples/quadratic",
    verbose=False,
)
assert result["ok"]
assert result["certified_bound_original_sense"] == "1/4"
```

`ok=True` means the nonlinear checks, master identity, and exact discrete proof all passed. For maximization, `certified_bound_original_sense` is an upper bound; `sense` is `-1`. An optional `viprchk="/path/to/viprchk"` requires external corroboration in addition to internal replay. The checker never relies on that external binary alone.

`require_vipr=False` deliberately performs only nonlinear-lemma and regenerated-master checks. It returns `status="partial"` and `partial_ok=True` when those checks pass, but `ok=False` and no certified bound. Rejection can mean unsupported evidence, insufficient enclosures, malformed input, or a failed mathematical check; it is not generally proof that the proposed bound is false. The checker reads saved certificate directories without modifying them.

The loaded Python model is trusted input construction and is executed by the loader. Numeric leaves denote their exact stored values. Arithmetic and model rewrites that occurred before the tree was loaded cannot be recovered. In particular, this convention does not silently convert binary floating values back into source decimal rationals.

**Replaying a campaign.** The full benchmark collection and large proof artifacts are local data excluded from version control. The final replay records include their hashes. To reproduce, obtain those exact artifacts or regenerate a separate campaign; absent artifacts are reported explicitly.

Run from `code/minlp_solver_lab`, choosing a new output name:

```sh
.venv/bin/python -m certify.recheck \
  --records results/cert_all.jsonl \
  --outroot results/cert \
  --out results/my_replay.jsonl \
  --jobs 6 --timeout 1200 \
  --viprchk /path/to/viprchk

.venv/bin/python -m certify.summarize results/my_replay.jsonl \
  --out results/my_replay_summary.json
```

The replay reads every historical record, including previously accepted records. It pins code, environment, input records, and the optional external checker, hashes artifacts before and after checking, and records explicit missing/rejected/verified/error/timeout outcomes. Reusing the same command resumes only when those inputs still match. The summary checks that every expected record index is present before declaring completion. Replaying different code or artifacts requires a new output. Large proofs can need substantial time and memory; each worker timeout includes its child checker processes.

Reference primal values and solver objectives are unverified comparison data. Their distances from checked bounds do not certify nonlinear feasibility or optimality. The summary uses exact rational comparisons and original objective sense; small negative differences can reflect rounding of the reference value. See [the two audited solver cases](../../../notes/certified-minlp-solver-discrepancies.md) for stronger, case-specific evidence.

**Generating new certificates.** The numerical producer additionally needs the solver-lab environment, licensed Gurobi for the current OA implementation, an IPOPT executable on `PATH`, and exact SCIP plus `viprcomp`/`viprchk`. Their search is untrusted: only complete replay confers a certified result. Use fresh output and artifact paths so historical evidence is preserved.

```sh
.venv/bin/python -m certify.run_all \
  --names results/cert_regenerated_20260913_names.txt \
  --out results/my_generated.jsonl --outroot results/my_generated \
  --oa-time 60 --scip-time 90 --threads 1 --par 3 \
  --scip-bin /path/to/scip-exact/bin
```

The producer tries default exact SCIP settings and, after failed complete verification, a conservative fallback with selected features disabled. Each attempt has its own budget; proof completion and verification add time. Therefore these are not total per-instance wall-clock limits. Independently replay a generated campaign with `recheck --records results/my_generated.jsonl --outroot results/my_generated --out results/my_generated_replay.jsonl`.

**Validation and scope.** Run the complete focused regression suite from the solver-lab directory:

```sh
uv run --with pytest python -m pytest -q certify/tests -p no:cacheprovider
.venv/bin/python -m certify.audit_solver_discrepancies --verify-certificate
```

The second command needs the local source models, saved solver listings, and `clay0204m` certificate. It checks all model rows and variable bounds, source-model equivalence, a rational feasible witness, and a matching lower-bound certificate.

The curvature rules are sufficient and incomplete. Original domains must be justified over the declared box; nonlinear equalities, general two-sided nonlinear rows, unsupported expressions and symbolic derivatives, active GDP/SOS/logical constraints, and variable or row names outside the supported LP identifier syntax are rejected. The former perspective shortcut is disabled pending a proof on the actual ratio domain. No finite termination, polynomial certificate-size, universal convexity recognition, or general nonconvex support is claimed.

The discrete proof grammar accepts a scoped complete VIPR 1.0/1.1 subset, including SCIP's optional `global` annotation only after independently establishing no remaining assumptions. It rejects unsupported syntax, unsafe integer-cutoff extensions, invalid references, and unproved final bounds. The exact rules and trusted arithmetic are documented in [the VIPR replay note](../../../notes/certified-minlp-vipr-replay.md).
