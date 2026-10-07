Checks run by the independent critic of ann-kan.md (2026-10-04), in a disposable copy
(/tmp/annkan_critic) with copies of osilx.py (reviews/open-instances-verification), rosil.py and
rint.py (publication/reviews/primal-water-ann-kan-r1), kan_iv.py (path insertion removed) and ia.py.
- cmp_readers.py: exact comparison of the shared reader osilx with the independent reader rosil
  for ann_cumene_tanh, ann_cumene_exp and the six KAN OSIL files (all variables, bounds, types,
  objective, row bounds and constants, linear, quadratic and nonlinear terms). Log: cmp_readers.log.
- silu_exact.py: rational check that kan_iv.SILU_MIN_LO itself (not a nearby constant) is a lower
  bound of min silu. Log: silu_exact.log.
Also rerun (logs not kept): ann-kan-checks/kan_infeas_edge_class.py for kan_r5_h1_n3/x776,
kan_r5_h1_n5/x1292 and kan_r5_h1_n8/x2066 (6 of 6 pieces certified each).
