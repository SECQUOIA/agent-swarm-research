"""Compare values printed in Mittelmann's cnconv logs (2026 versions, stored in
sources/mittelmann_cnconv/logs/) with our certified MINLPLib optima
(open-instances-summary.md). Decimal arithmetic on the printed digits only.
camshape: the QPLIB copies differ from MINLPLib by ~1e-10 relative rounding
(see qplib_camshape_compare.log), so those comparisons are evidence only.
dtoc5/optcdeg2: QPLIB_8585/8803 are textually identical to MINLPLib
(qplib_dtoc5_optcdeg2_identity.log)."""
from fractions import Fraction as F

opt = {  # certified optimum (exact optimum rounded down, or certificate value)
    "camshape100": F("-4.28414712174675"), "camshape200": F("-4.27850023299273"),
    "camshape400": F("-4.27568847892555"), "camshape800": F("-4.27427414195420"),
    "dtoc5": F("5.38967211918114"), "optcdeg2": F("293.87607509587509"),
}
# (instance, solver/log, kind, printed value)
rows = [
    ("camshape100", "ANTIGONE 2738.ant", "best feasible at 'Global minimum'", "-4.284302"),
    ("camshape100", "ANTIGONE 2738.ant", "best possible", "-4.284302"),
    ("camshape100", "ANTIGONE 2738.ant", "after CONOPT polish", "-4.28414626579"),
    ("camshape100", "BARON 2738.bar", "solution", "-4.28414710266608"),
    ("camshape100", "COPT 2738.cop", "best solution", "-4.284189915"),
    ("camshape100", "SCIP 9.2.1 2738.sci", "primal", "-4.28414626680553"),
    ("camshape200", "ANTIGONE 2480.ant", "best feasible", "-4.278491"),
    ("camshape200", "ANTIGONE 2480.ant", "best possible", "-4.601964"),
    ("camshape200", "BARON 2480.bar", "solution", "-4.27849246237069"),
    ("camshape200", "COPT 2480.cop", "best solution", "-4.278677725"),
    ("camshape400", "ANTIGONE 2703.ant", "best possible", "-4.969835"),
    ("camshape400", "BARON 2703.bar", "solution", "-4.27565886682199"),
    ("camshape400", "COPT 2703.cop", "best solution", "-4.276430314"),
    ("camshape400", "SCIP 9.2.1 2703.sci", "primal", "-4.33023953971002"),
    ("camshape800", "MINOTAUR 3177.mnt", "'Optimal solution found' value", "-4.2774"),
    ("camshape800", "BARON 3177.bar", "solution", "-4.51546318707998"),
    ("camshape800", "COPT 3177.cop", "best solution", "-4.277371318"),
    ("camshape800", "SCIP 9.2.1 3177.sci", "primal", "-4.27418677010926"),
    ("dtoc5", "MINOTAUR 8585.mnt", "'Optimal solution found' value", "5.3897"),
    ("dtoc5", "BARON 8585.bar", "solution", "5.38966688447816"),
    ("dtoc5", "COPT 8585.cop", "best solution", "5.389829024"),
    ("dtoc5", "COPT 8585.cop", "best bound", "0.761858180"),
    ("optcdeg2", "BARON 8803.bar", "solution", "293.876075074557"),
    ("optcdeg2", "COPT 8803.cop", "best solution", "293.880662592"),
    ("optcdeg2", "COPT 8803.cop", "best bound", "283.407898545"),
]
print(f"{'instance':12s} {'log':22s} {'kind':34s} {'value':>18s} {'value - optimum':>16s}")
for inst, log, kind, v in rows:
    d = F(v) - opt[inst]
    print(f"{inst:12s} {log:22s} {kind:34s} {v:>18s} {float(d):>16.3e}")
