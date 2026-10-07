Critic's checks for the camshape dossier (2026-10-04). Written from scratch by the critic; nothing imported from
the dossier's checks/camshape/ scripts, the verifier's code or the authors' code. Run on copies in /tmp/camcrit
(OSIL from ~/.cache/minlplib/minlplib/osil/, .gms/.sol copies from R/publication/literature/control/sources/qplib/
camshape_copies/, MINLPLib .sol from R/open-instances/minlplib_sol/); input sha256 prefixes in input_sha256.txt are
identical to the dossier's checks/camshape/input_sha256.txt. One core, each script under 2 s.

mine.py          regex OSIL parser + full template match; exact rational S; R, B, envelope in fixed point with
                 directed rounding (scale 1e-120) -> rigorous enclosure of v_n (width ~3e-120). Log mine.log.
exactfeas.py     exact Fraction envelope and generic exact evaluation of every OSIL row/bound, n = 100, 200.
minlp_gms.py     own tokenizer for the MINLPLib .gms files; every row and bound equals the OSIL template.
qplib.py         own tokenizer for the QPLIB copies; template match; copy optimum via Theorem 1 + Lemma 3
                 hypotheses C1-C5 (not row evaluation) and the directed-rounding enclosure; exact evaluation of
                 QPLIB reference points.
robust_mine.py   eta = 1e-14 corner enclosures (dossier I-6) recomputed with the enclosure code.
evalpts.py       exact evaluation of MINLPLib p1/p2 points; counts rows violated by > 1e-12.
tol_attain.py    explicit eps-feasible points (G_j = eps chain, cap 2+eps, slope alpha+2eps), mpmath 80 digits:
                 numerical lower estimates of the worst-case deficit, compared with the dossier's D_n(eps).
minotaur_eps.py, antigone_eps.py  same construction on QPLIB_3177 / QPLIB_2738: smallest eps whose explicit
                 eps-feasible point reaches MINOTAUR's / ANTIGONE's printed value (numerical evidence).
