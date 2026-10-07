Critic checks for the powerflow dossier (powerflow.md), 2026-10-04.
Independent critic of the dossier; not the dossier author. Nothing under research-20260929/ or
literature/ was imported, executed or edited. Every script ran from a scratch copy in /tmp/pfcrit,
one thread (OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1).

Inputs copied to /tmp/pfcrit (sha256 checked against the dossier):
  OSIL: powerflow0030p 5c4b386b..., powerflow0039p 0a27073f..., powerflow0039r d8ba3132...
  GAMS: publication/literature/network/sources/minlplib_powerflow*.gms (f17e87ee..., af99868d..., 4053321f...)
  certificates: open-instances-wave3/logs/powerflow0030p.sdpcert.json (63cf1e21...),
                open-instances-wave3/powerflow/ext/logs/powerflow0039{p,r}.bb3t.json (8af24081..., 09e1a62a...)
  code copies in /tmp/pfcrit/rev: the 0039 reviewer's verify_leaves.py, own_relax.py, own_osil.py
  (reviews/powerflow0039-review-checks/), plus pf_model.py, leafcut.py and osilx.py (4bcdc1d8...)
  because verify_leaves.py takes row ORDER from pf_model and compares its own plane list with leafcut.

Patches (only paths, plus one option):
  pf_model.py, own_relax.py, verify_leaves.py: OSIL/log paths -> /tmp/pfcrit/rev/...
  verify_leaves.py: optional third argument "noangle" sets every angle-row multiplier of each
  leaf to zero before the Lagrangian is formed (saved here as verify_leaves_patched.py).

Scripts and results:
  verify_leaves_patched.py powerflow0039p bb3t noangle -> logs/noangle_0039p.log (9 s)
      Independent replay of the dossier's angle-free 0039p variant with the reviewer's code
      (own OSIL reader and rows; 50-digit eigenvalue, 60-digit Cholesky, exact residual, Gershgorin).
      All 6 leaves: lam_min(A) > 0 (4.29e-9 .. 5.80e-8; decisive leaf 4.60e-8); minimum
      41869.05148528834, floor*1e12 = 41869051485288344. Matches the dossier exactly.
  verify_leaves_patched.py powerflow0039p bb3t -> logs/control_0039p.log
      Control: reproduces the 0039 review's numbers (41869.051485240394; decisive lam_min -1.094e-9).
  root0030p_ownrows.py -> logs/root0030p_ownrows.log
      Stored 0030p multipliers on the reviewer's own rows: const+inner == stored bound_exact
      exactly; A positive definite (own natural-order exact LDL^T: 60 positive pivots, min 1.12e-7;
      Gershgorin route: shift -1e-30). lam_min(A) = 4.001115e-9.
  eigpair.py -> logs/eigpair.log
      50-digit smallest eigenvalues come in exactly equal pairs: 0030p root 4.00111498512691e-9 (x2);
      0039p decisive leaf -1.09429999213631e-9 (x2), angle-free +4.60033383239604e-8 (x2);
      next pair 0.7654. (Shows the "split into a pair" wording in dossier section 3.6 is wrong.)
  anglemult.py -> logs/anglemult.log: largest stored angle multiplier per 0039p leaf (max 2.256e-7).
  jcheck.py -> logs/jcheck.log
      Own ElementTree read of powerflow0039r.osil: all 262 quadratic rows in (e,f) (184 flow,
      78 voltage) commute exactly with J (every 2x2 block has the form [[a,-c],[c,a]]).
  planes.py -> logs/planes.log
      Own exact enumeration of vertex planes for all 15 tight leaves: 4 planes per leaf, H >= F at all
      8 vertices; on every leaf two planes touch exactly 4 vertices and two touch 5 (a whole W_LL face
      plus one vertex), because on each face W_LL = const, F is a separable quadratic in (Pg,Qg)
      (no Pg*Qg term), so its 4 vertex values on that face are coplanar.
  misc_exact.py -> logs/misc_exact.log
      Exact containment of the exact points in the decisive leaves; exact W_NN(x*) = F; root
      envelope error 7.216e-3; gaps, displays, improvements; 0039r display ...244 vs the rational.
