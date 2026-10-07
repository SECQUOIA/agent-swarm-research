"""SIGINT test: like smoke/manual/sigtest.py, but after N s send SIGINT only to the
process of the run's group with the most CPU time (the solver), or to the group."""
import os, signal, subprocess, sys, time
G, gms, solver, d, n, mode = sys.argv[1:7]
os.makedirs(d, exist_ok=True)
p = subprocess.Popen([G, gms, f'NLP={solver}', 'reslim=120', 'threads=1', 'optcr=1e-9', 'optca=1e-9', 'lo=2',
                      'logfile=gams.log', 'o=x.lst', 'savepoint=1', 'trace=trace.trc', 'traceopt=3'],
                     cwd=d, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, start_new_session=True)
time.sleep(float(n))
best = None
for q in os.listdir('/proc'):
    if not q.isdigit():
        continue
    try:
        st = open(f'/proc/{q}/stat').read()
    except OSError:
        continue
    comm = st[st.find('(') + 1:st.rfind(')')]
    f = st[st.rfind(')') + 2:].split()
    if int(f[2]) == p.pid:
        cpu = int(f[11]) + int(f[12])
        print('  group member', q, comm, 'cpu ticks', cpu)
        if best is None or cpu > best[1]:
            best = (int(q), cpu, comm)
if mode == 'solver':
    os.kill(best[0], signal.SIGINT)
    print('  SIGINT to', best)
else:
    os.killpg(p.pid, signal.SIGINT)
t = time.time()
rc = p.wait()
tr = open(os.path.join(d, 'trace.trc')).read().strip().splitlines()[-1].split(',')
print(solver, n, mode, 'rc', rc, 'exit after SIGINT', round(time.time() - t, 2), 's', 'ms/ss', tr[13], tr[14],
      'obj', tr[15], 'gdx', os.path.exists(os.path.join(d, 'm_p.gdx')))
