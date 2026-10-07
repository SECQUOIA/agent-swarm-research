"""Same instance as scip_stats_probe.py with SCIP's progress display on."""
import instances as I
m, x, t, c = I.build_scip(12, 0, amp=0.3)
m.hideOutput(False)
m.setParam("display/freq", 5000); m.setParam("display/verblevel", 4)
m.setParam("timing/clocktype", 1); m.setParam("limits/time", 200)
m.setParam("limits/absgap", 1e-4); m.setParam("limits/gap", 0.0)
m.optimize()
