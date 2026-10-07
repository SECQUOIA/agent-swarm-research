import subprocess, os, signal, sys, time
G, gms, solver, d = sys.argv[1:5]
os.makedirs(d, exist_ok=True)
p = subprocess.Popen([G, gms, f'NLP={solver}', 'reslim=60', 'threads=1', 'optcr=1e-9', 'optca=1e-9', 'lo=2', 'logfile=gams.log', 'o=x.lst', 'savepoint=1', 'trace=trace.trc', 'traceopt=3'], cwd=d, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, start_new_session=True)
time.sleep(25)
os.killpg(p.pid, signal.SIGINT)
t = time.time()
rc = p.wait()
print(solver, 'rc', rc, 'exit after SIGINT', round(time.time() - t, 2), 's')
