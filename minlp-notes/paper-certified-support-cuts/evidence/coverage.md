# Claim map

Each result of the manuscript, where it is proved, how it was checked, and
its status relative to prior work (from `literature-L1.md` ... `L5.md` and the
first review round). Numbering is that of the current `main.pdf`.

## Theory

| Result | Proof | Checks (`verification/`) | Prior work and status |
|---|---|---|---|
| Prop. 2.1 support description | Sec. 2 | standard | classical (Ballerstein 2013; Tawarmalani 2010; Liers et al. 2021) |
| Prop. 3.1 path gap 1/128, cut (path-cut) | Sec. 3.1 | `M4_example.py` | explicit degree-two witness not found in prior work; mechanism known (Tawarmalani 2010 Ex. 3.8; sparse moment literature) |
| Thm. 3.2 interleaving | Sec. 3.2, App. A.1 | `M4_family.py` (4,000 instances) | not found in prior work |
| Thm. 3.3 alternation | Sec. 3.3, App. A.2 | `M4_alternation.py` (8,002 cases), `R3-lit_radon_check.py` | reading of Radon partitions on the moment curve (Breen 1973) and Chebyshev sign changes (Karlin-Studden); its use for gluing interfaces not found |
| kappa = 3 example after Thm. 3.3 | Sec. 3.3 | `M6_revision_checks.py` item 3 | new example |
| Prop. 3.4 full gap for every kappa | Sec. 3.3 | `M6_revision_checks.py` item 4 | new |
| identity (sdp-identity), App. A.3 | Sec. 3.4, App. A.3 | `M4_family.py`, `R2-math_identity.py` | special case of Burer-Natarajan-Willemsen 2025 Thm 1 (stated in the text) |
| Prop. 3.5 gain from merging, (ii) re-splitting; examples App. A.4 | Sec. 3.5 | `M4_star_oracle.py`, `M6_revision_checks.py` items 1, 2, 6 | Lagrangian decomposition (Geoffrion 1974; Guignard-Kim 1987); interface polynomials (Grimm-Netzer-Schweighofer 2007); credited in the text |
| four-variable path and full-gap instances: dense first-level relaxation not exact | Sec. 3.4 | `M7_dense_fullgap.py` (exact rational feasible points), `R9_math_bnw_path4.py` | four-variable path from Burer-Natarajan-Willemsen 2025 Ex. 4 / Sec. 6.4; the full-gap observation is ours |
| Thm. 4.1 polytope support, Cor. 4.2 | Sec. 4.1, App. B | `M2_polytope_checks.py` (964 checks), `M2_crosscheck_impl.py` | total enumeration of faces (Murty 1997); degeneracy-complete statement and encoding bounds given |
| Prop. 4.3 hardness, coNP | App. B | `M2_polytope_checks.py` | folklore (Burer-Letchford 2009; Karp; Garey-Johnson-Stockmeyer) |
| Thm. 4.4 constrained stars | Sec. 4.2, App. C | `M3_star_sweep.py` (400 cases), `M3_bounds_and_examples.py`, `experiments/v4/star_bench.py` | box case in Del Pia-Khajavirad 2026; center-leaf rows: no earlier exact algorithm found |
| lower bound for Thm. 4.4 | App. C |
| two-leaf rows strongly NP-hard (stable set) | Sec. 4.2 | `R9_math_twoleaf.py` | Nemhauser-Trotter half-integrality applied | `M3_bounds_and_examples.py` | Ben-Or 1983 applied |
| Rem. 4.5 depth two | App. C | `M3_irrational_breakpoint.py` | example new; consistent with Del Pia-Khajavirad |
| Prop. 5.1 aggregated cut | Sec. 5.1 | `M1_examples.py` | weak Lagrangian duality; Lagrangian cuts (Nowak 2005) |
| Thm. 5.2 closure, Cor. 5.3 | Sec. 5.2 | `M1_closure_random.py` | Lagrangian dual = convexification (Falk; Geoffrion; Lemarechal-Renaud); argument as in Chen-Luedtke 2022 Thm 3 |
| Ex. 5.4; Prop. D.1, Ex. D.2, hierarchy and D=[0,2] example | Sec. 5.2-5.3, App. D | `M1_examples.py`, `M6_revision_checks.py` item 5 | elementary; stated for this interface |
| (C1)-(C4), Prop. 6.1 safe export | Sec. 6.1 | `M1_rounding.py`, replay, Part U export census | established (Neumaier-Shcherbina; Cook et al.; Eifler-Gleixner); applied to joint support cuts |
| Lemma E.1, Prop. E.2, Lemma E.3 | App. E | `M5_bernstein.py`, `M5_chord.py` | classical |
| Lemma F.1, Thm. F.2, Lemma F.3 | App. F | `M5_separation.py`, `M5_domain_net.py` | assembled from classical tools (GLS; Gilbert; local cuts; Kelley) |

## Implementation and computations

| Claim | Where | Evidence |
|---|---|---|
| Implementation facts (Sec. 6.3, 7) | Sec. 6.3, 7 | `implementation-facts.md` |
| Campaigns 1 and 2 | App. G | `experiment-audit.md`, `E1_audit_experiments.py` (418 checks) |
| Campaign 3, Parts A-C, diagnostic | Sec. 8.3-8.5 | `experiments/v3/`, `experiments/v3d/`, `funnel-and-time.md`, `experiments/v4/results-c3/` |
| Campaign 4, Parts C2, C3, B2, D | Sec. 8.2-8.5 | `campaign4-digest.md`, `campaign4-replay.md`; independent checks `campaign4-verify-{path,minlplib,funnel-time}.md` (`R8_path.py`, `R8_minlplib.py`, `R8_funnel_time.py`) |
| Campaign 4, Part C4 | Sec. 8.5 | `campaign4-c4-digest.md`; independent check `campaign4-verify-c4.md` (`R8_c4.py`) |
| Part U ablation | Sec. 8.2 | `ablation-uncertified.{md,json}`, `ablation-final-summary.md`, `ablation-slsqp-check.json`; independent check `ablation-verify.md` (`R8_ablation.py`) |
| Part S star benchmark | Sec. 8.6 | `experiments/v4/star-bench.{md,json}` |
| Campaign 5, Parts 5S, 5C-a, 5C-b | Sec. 8.5-8.6 | `experiments/v5/results-s5/`, `results-c5a/`, `results-c5b/`; replays `experiments/v5/runs/replay-part*.log` |
| Part 5U (numerical global solve) | Sec. 8.2 | `ablation-global-solve.md`, spot check `ablation-global-solve-spotcheck.json` |
| Replay of every recorded cut (campaigns 3-5) | Sec. 8.2 | `experiments/v3/runs/*/replay.json`, `experiments/v3d/runs/*/replay.json`, `experiments/v4/runs/*/replay.json`, `experiments/v5/runs/*/replay.json` (Parts 5S, 5C-a, 5C-b and the informational 5S rerun) |
