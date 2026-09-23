"""Yee-Grossmann (1990) SYNHEAT stage-wise superstructure MINLP (isothermal mixing, Chen LMTD)
with an optional 'lifted' area formulation v1 = A*dt1, v2 = A*dt2.

Data sources (all three examples are Tables 5-7 of Mistry & Misener 2016, "Optimising heat
exchanger network synthesis using convexity properties of the logarithmic mean temperature
difference", Comput. Chem. Eng. 94:1-17; open-access PDF:
https://spiral.imperial.ac.uk/bitstreams/73f1f43f-70a2-4142-84c7-54b3798583b5/download
The tables attribute the data to Escobar & Grossmann 2010; Table 5 is Yee & Grossmann 1990
Example 1; Table 7 is the classical 10SP1 problem (Pho & Lapidus 1973 / Cerda et al. 1983)
in SI units. The same data underlie MINLPLib heatexch_gen1/2/3
(https://www.minlplib.org/heatexch_gen1.html etc.), which we used to cross-check U, costs
and EMAT (dt lower bound 10 in all three).
U_ij = 1/(1/h_i + 1/h_j) from the film coefficients h.

Original formulation (per exchanger):  q <= U * A * (dt1*dt2*(dt1+dt2)/2)^(1/3)
Lifted formulation:                    v1 = A*dt1, v2 = A*dt2,
                                       q <= U * (v1*v2*(v1+v2)/2)^(1/3)   [concave RHS]
                                   or  q^3 <= U^3 * v1*v2*(v1+v2)/2       [lift_form='cubic']
Both use identical bounds on A, dt (A in [0, A_max], A_max = Qmax/(U*LMTD_min)) so that the
projection of the lifted feasible set onto the original variables equals the original feasible set.
"""
import pyomo.environ as pe

EXAMPLES = {
    # name: dict(hot={name: (Tin, Tout, F, h)}, cold=..., cu=(Tin,Tout,h), hu=(Tin,Tout,h),
    #            cf, c, beta, ccu, chu, emat)
    "ex1_yg1990_2h2c": dict(  # Mistry-Misener Table 5 = Yee-Grossmann 1990 Example 1 = heatexch_gen1 data
        hot={"H1": (650, 370, 10, 1), "H2": (590, 370, 20, 1)},
        cold={"C1": (410, 650, 15, 1), "C2": (350, 500, 13, 1)},
        cu=(300, 320, 1), hu=(680, 680, 5),
        cf=5500, c=150, beta=1.0, ccu=15, chu=80, emat=10),
    "ex2_5h1c": dict(  # Mistry-Misener Table 6 = heatexch_gen2 data
        hot={"H1": (500, 320, 6, 2), "H2": (480, 380, 4, 2), "H3": (460, 360, 6, 2),
             "H4": (380, 360, 20, 2), "H5": (380, 320, 12, 2)},
        cold={"C1": (290, 660, 18, 2)},
        cu=(300, 320, 1), hu=(700, 700, 2),
        cf=5500, c=1200, beta=0.6, ccu=10, chu=140, emat=10),
    "ex3_10sp1_5h5c": dict(  # Mistry-Misener Table 7 = 10SP1 (SI) = heatexch_gen3 data
        hot={"H1": (160, 93.3, 8.8, 1.7), "H2": (248.9, 137.8, 10.6, 1.7), "H3": (226.7, 65.6, 14.8, 1.7),
             "H4": (271.1, 148.9, 12.6, 1.7), "H5": (198.9, 65.6, 17.7, 1.7)},
        cold={"C1": (60, 160, 7.6, 1.7), "C2": (115.6, 221.7, 6.1, 1.7), "C3": (37.8, 211.1, 8.4, 1.7),
              "C4": (82.2, 176.7, 17.3, 1.7), "C5": (93.3, 204.4, 13.9, 1.7)},
        cu=(25, 40, 1.7), hu=(240, 240, 3.4),
        cf=4000, c=146, beta=0.6, ccu=10, chu=200, emat=10),
}


def chen(a, b):
    return (a * b * (a + b) / 2) ** (1 / 3)


def build(data, stages=2, lifted=False, lift_form="pow"):
    d = data
    m = pe.ConcreteModel()
    H, C = list(d["hot"]), list(d["cold"])
    K = list(range(1, stages + 1))
    K1 = list(range(1, stages + 2))
    TinH = {i: d["hot"][i][0] for i in H}; ToutH = {i: d["hot"][i][1] for i in H}
    FH = {i: d["hot"][i][2] for i in H}; hH = {i: d["hot"][i][3] for i in H}
    TinC = {j: d["cold"][j][0] for j in C}; ToutC = {j: d["cold"][j][1] for j in C}
    FC = {j: d["cold"][j][2] for j in C}; hC = {j: d["cold"][j][3] for j in C}
    TcuIn, TcuOut, hcu = d["cu"]; ThuIn, ThuOut, hhu = d["hu"]
    emat, beta, c, cf = d["emat"], d["beta"], d["c"], d["cf"]
    QH = {i: FH[i] * (TinH[i] - ToutH[i]) for i in H}
    QC = {j: FC[j] * (ToutC[j] - TinC[j]) for j in C}
    U = {(i, j): 1 / (1 / hH[i] + 1 / hC[j]) for i in H for j in C}
    Ucu = {i: 1 / (1 / hH[i] + 1 / hcu) for i in H}
    Uhu = {j: 1 / (1 / hC[j] + 1 / hhu) for j in C}
    Qmax = {(i, j): min(QH[i], QC[j]) for i in H for j in C}
    # bounds --------------------------------------------------------------------------
    dtUB = {(i, j): max(emat, TinH[i] - TinC[j]) for i in H for j in C}
    dtcuUB = {i: max(emat, TinH[i] - TcuOut) for i in H}
    dthuUB = {j: max(emat, ThuOut - TinC[j]) for j in C}
    dtcuFix = {i: ToutH[i] - TcuIn for i in H}       # fixed end of cooler
    dthuFix = {j: ThuIn - ToutC[j] for j in C}       # fixed end of heater
    # LMTD_min from EMAT (Chen LMTD is nondecreasing in each argument) -> A_max = Qmax/(U*LMTD_min)
    Amax = {(i, j): Qmax[i, j] / (U[i, j] * chen(emat, emat)) for i in H for j in C}
    AcuMax = {i: QH[i] / (Ucu[i] * chen(emat, dtcuFix[i])) for i in H}
    AhuMax = {j: QC[j] / (Uhu[j] * chen(emat, dthuFix[j])) for j in C}
    Gam = {(i, j): dtUB[i, j] - min(0, ToutH[i] - ToutC[j]) for i in H for j in C}
    Gcu = {i: dtcuUB[i] - (ToutH[i] - TcuOut) if ToutH[i] - TcuOut < dtcuUB[i] else 0 for i in H}
    Ghu = {j: dthuUB[j] - (ThuOut - ToutC[j]) if ThuOut - ToutC[j] < dthuUB[j] else 0 for j in C}
    m.meta = dict(H=H, C=C, K=K, U=U, Ucu=Ucu, Uhu=Uhu, Amax=Amax, AcuMax=AcuMax, AhuMax=AhuMax,
                  dtUB=dtUB, dtcuFix=dtcuFix, dthuFix=dthuFix, QH=QH, QC=QC)
    # variables -----------------------------------------------------------------------
    m.th = pe.Var(H, K1, bounds=lambda m, i, k: (ToutH[i], TinH[i]))
    m.tc = pe.Var(C, K1, bounds=lambda m, j, k: (TinC[j], ToutC[j]))
    m.q = pe.Var(H, C, K, bounds=lambda m, i, j, k: (0, Qmax[i, j]))
    m.qcu = pe.Var(H, bounds=lambda m, i: (0, QH[i]))
    m.qhu = pe.Var(C, bounds=lambda m, j: (0, QC[j]))
    m.z = pe.Var(H, C, K, within=pe.Binary)
    m.zcu = pe.Var(H, within=pe.Binary)
    m.zhu = pe.Var(C, within=pe.Binary)
    m.dt = pe.Var(H, C, K1, bounds=lambda m, i, j, k: (emat, dtUB[i, j]))
    m.dtcu = pe.Var(H, bounds=lambda m, i: (emat, dtcuUB[i]))
    m.dthu = pe.Var(C, bounds=lambda m, j: (emat, dthuUB[j]))
    m.A = pe.Var(H, C, K, bounds=lambda m, i, j, k: (0, Amax[i, j]))
    m.Acu = pe.Var(H, bounds=lambda m, i: (0, AcuMax[i]))
    m.Ahu = pe.Var(C, bounds=lambda m, j: (0, AhuMax[j]))
    # heat balances --------------------------------------------------------------------
    m.hb_h = pe.Constraint(H, rule=lambda m, i: QH[i] == sum(m.q[i, j, k] for j in C for k in K) + m.qcu[i])
    m.hb_c = pe.Constraint(C, rule=lambda m, j: QC[j] == sum(m.q[i, j, k] for i in H for k in K) + m.qhu[j])
    m.st_h = pe.Constraint(H, K, rule=lambda m, i, k: FH[i] * (m.th[i, k] - m.th[i, k + 1]) == sum(m.q[i, j, k] for j in C))
    m.st_c = pe.Constraint(C, K, rule=lambda m, j, k: FC[j] * (m.tc[j, k] - m.tc[j, k + 1]) == sum(m.q[i, j, k] for i in H))
    m.tin_h = pe.Constraint(H, rule=lambda m, i: m.th[i, 1] == TinH[i])
    m.tin_c = pe.Constraint(C, rule=lambda m, j: m.tc[j, stages + 1] == TinC[j])
    m.mono_h = pe.Constraint(H, K, rule=lambda m, i, k: m.th[i, k] >= m.th[i, k + 1])
    m.mono_c = pe.Constraint(C, K, rule=lambda m, j, k: m.tc[j, k] >= m.tc[j, k + 1])
    m.cu_bal = pe.Constraint(H, rule=lambda m, i: m.qcu[i] == FH[i] * (m.th[i, stages + 1] - ToutH[i]))
    m.hu_bal = pe.Constraint(C, rule=lambda m, j: m.qhu[j] == FC[j] * (ToutC[j] - m.tc[j, 1]))
    # logical ----------------------------------------------------------------------------
    m.log_q = pe.Constraint(H, C, K, rule=lambda m, i, j, k: m.q[i, j, k] <= Qmax[i, j] * m.z[i, j, k])
    m.log_cu = pe.Constraint(H, rule=lambda m, i: m.qcu[i] <= QH[i] * m.zcu[i])
    m.log_hu = pe.Constraint(C, rule=lambda m, j: m.qhu[j] <= QC[j] * m.zhu[j])
    # approach temperatures --------------------------------------------------------------
    m.dt_hot = pe.Constraint(H, C, K, rule=lambda m, i, j, k:
                             m.dt[i, j, k] <= m.th[i, k] - m.tc[j, k] + Gam[i, j] * (1 - m.z[i, j, k]))
    m.dt_cold = pe.Constraint(H, C, K, rule=lambda m, i, j, k:
                              m.dt[i, j, k + 1] <= m.th[i, k + 1] - m.tc[j, k + 1] + Gam[i, j] * (1 - m.z[i, j, k]))
    m.dt_cu = pe.Constraint(H, rule=lambda m, i: m.dtcu[i] <= m.th[i, stages + 1] - TcuOut + Gcu[i] * (1 - m.zcu[i]))
    m.dt_hu = pe.Constraint(C, rule=lambda m, j: m.dthu[j] <= ThuOut - m.tc[j, 1] + Ghu[j] * (1 - m.zhu[j]))
    # area constraints -------------------------------------------------------------------
    if not lifted:
        m.area = pe.Constraint(H, C, K, rule=lambda m, i, j, k:
                               m.q[i, j, k] <= U[i, j] * m.A[i, j, k] * chen(m.dt[i, j, k], m.dt[i, j, k + 1]))
        m.area_cu = pe.Constraint(H, rule=lambda m, i: m.qcu[i] <= Ucu[i] * m.Acu[i] * chen(m.dtcu[i], dtcuFix[i]))
        m.area_hu = pe.Constraint(C, rule=lambda m, j: m.qhu[j] <= Uhu[j] * m.Ahu[j] * chen(dthuFix[j], m.dthu[j]))
    else:
        m.v1 = pe.Var(H, C, K, bounds=lambda m, i, j, k: (0, Amax[i, j] * dtUB[i, j]))
        m.v2 = pe.Var(H, C, K, bounds=lambda m, i, j, k: (0, Amax[i, j] * dtUB[i, j]))
        m.vcu = pe.Var(H, bounds=lambda m, i: (0, AcuMax[i] * dtcuUB[i]))
        m.vhu = pe.Var(C, bounds=lambda m, j: (0, AhuMax[j] * dthuUB[j]))
        m.lift1 = pe.Constraint(H, C, K, rule=lambda m, i, j, k: m.v1[i, j, k] == m.A[i, j, k] * m.dt[i, j, k])
        m.lift2 = pe.Constraint(H, C, K, rule=lambda m, i, j, k: m.v2[i, j, k] == m.A[i, j, k] * m.dt[i, j, k + 1])
        m.liftcu = pe.Constraint(H, rule=lambda m, i: m.vcu[i] == m.Acu[i] * m.dtcu[i])
        m.lifthu = pe.Constraint(C, rule=lambda m, j: m.vhu[j] == m.Ahu[j] * m.dthu[j])

        def gm(q, u, a, b):
            # q <= u * (a*b*(a+b)/2)^(1/3)   (a, b linear in v -> concave RHS)
            if lift_form == "pow":
                return q <= u * (a * b * (a + b) / 2) ** (1 / 3)
            return q ** 3 <= u ** 3 * a * b * (a + b) / 2
        m.area = pe.Constraint(H, C, K, rule=lambda m, i, j, k: gm(m.q[i, j, k], U[i, j], m.v1[i, j, k], m.v2[i, j, k]))
        m.area_cu = pe.Constraint(H, rule=lambda m, i: gm(m.qcu[i], Ucu[i], m.vcu[i], m.Acu[i] * dtcuFix[i]))
        m.area_hu = pe.Constraint(C, rule=lambda m, j: gm(m.qhu[j], Uhu[j], m.Ahu[j] * dthuFix[j], m.vhu[j]))
    # objective ----------------------------------------------------------------------------
    def apow(a):
        return a if beta == 1 else a ** beta
    m.obj = pe.Objective(sense=pe.minimize, expr=
        cf * (sum(m.z[i, j, k] for i in H for j in C for k in K) + sum(m.zcu[i] for i in H) + sum(m.zhu[j] for j in C))
        + c * (sum(apow(m.A[i, j, k]) for i in H for j in C for k in K) + sum(apow(m.Acu[i]) for i in H) + sum(apow(m.Ahu[j]) for j in C))
        + d["ccu"] * sum(m.qcu[i] for i in H) + d["chu"] * sum(m.qhu[j] for j in C))
    return m


def point(m):
    return {v.name: pe.value(v) for v in m.component_data_objects(pe.Var)}


def max_violation(m, vals, tol_binary=1e-6):
    """Load vals (by name; missing lifted vars are computed from A*dt) and return max constraint/bound violation."""
    for v in m.component_data_objects(pe.Var):
        if v.name in vals:
            v.set_value(vals[v.name], skip_validation=True)
    for comp, a, d1, d2 in (("v1", "A", "dt", 0), ("v2", "A", "dt", 1)):
        if hasattr(m, comp):
            for idx in getattr(m, comp):
                i, j, k = idx
                getattr(m, comp)[idx].set_value(pe.value(m.A[i, j, k]) * pe.value(m.dt[i, j, k + d2]), skip_validation=True)
    if hasattr(m, "vcu"):
        for i in m.vcu:
            m.vcu[i].set_value(pe.value(m.Acu[i]) * pe.value(m.dtcu[i]), skip_validation=True)
        for j in m.vhu:
            m.vhu[j].set_value(pe.value(m.Ahu[j]) * pe.value(m.dthu[j]), skip_validation=True)
    viol = 0.0
    for con in m.component_data_objects(pe.Constraint, active=True):
        b = pe.value(con.body)
        if con.has_lb():
            viol = max(viol, con.lower() - b)
        if con.has_ub():
            viol = max(viol, b - con.upper())
    for v in m.component_data_objects(pe.Var):
        x = pe.value(v)
        if v.lb is not None:
            viol = max(viol, v.lb - x)
        if v.ub is not None:
            viol = max(viol, x - v.ub)
    return viol, pe.value(m.obj)


if __name__ == "__main__":
    for name, data in EXAMPLES.items():
        m = build(data)
        ml = build(data, lifted=True)
        nb = sum(1 for v in m.component_data_objects(pe.Var) if v.is_binary())
        nc = sum(1 for _ in m.component_data_objects(pe.Constraint))
        ncl = sum(1 for _ in ml.component_data_objects(pe.Constraint))
        print(name, "binaries", nb, "constraints orig/lifted", nc, ncl,
              "Amax (process)", {k: round(v, 1) for k, v in list(m.meta["Amax"].items())[:4]})
