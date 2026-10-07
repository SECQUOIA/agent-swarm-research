"""Write SCIP statistics for one n = 12 probe3 instance whose node rate collapsed
after about 300 CPU s (amp 0.3, seed 0), to see where the time goes."""
import sys, time
import instances as I
tl = float(sys.argv[1])
m, x, t, c = I.build_scip(12, 0, amp=0.3)
m.setParam("timing/clocktype", 1); m.setParam("limits/time", tl)
m.setParam("limits/absgap", 1e-4); m.setParam("limits/gap", 0.0)
t0 = time.time(); m.optimize()
m.writeStatistics(f"logs/scip_stats_n12_amp0.3_seed0_tl{int(tl)}.txt")
print(m.getStatus(), m.getNNodes(), m.getSolvingTime(), time.time() - t0, m.getPrimalbound() - m.getDualbound())
