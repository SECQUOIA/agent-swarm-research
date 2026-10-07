"""Collect current metadata and recorded timings; never run scientific scripts."""
import contextlib
import hashlib
import io
import json
import os
import platform
from decimal import Decimal
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
cpu = Path('/proc/cpuinfo').read_text()
blocks = [dict(line.split(':', 1) for line in b.splitlines() if ':' in line)
          for b in cpu.split('\n\n') if b.strip()]
blocks = [{k.strip(): v.strip() for k, v in b.items()} for b in blocks]
cores = {(b['physical id'], b['core id']) for b in blocks}
mem_kib = int(Path('/proc/meminfo').read_text().splitlines()[0].split()[1])
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    np.show_config()
    np.show_runtime()
env = {
    'capture_date': '2026-10-04',
    'scope': 'Current host and reproduction environment, not a recovered original-run environment',
    'cpu_model': blocks[0]['model name'], 'physical_cores': len(cores),
    'logical_cpus': len(blocks), 'flags': blocks[0]['flags'].split(),
    'mem_total_kib': mem_kib, 'mem_total_gib_exact': str(Decimal(mem_kib) / 1048576),
    'uname': list(platform.uname()), 'os_release': platform.freedesktop_os_release(),
    'libc': platform.libc_ver(), 'python': platform.python_version(),
    'numpy_config_and_runtime': buf.getvalue(),
    'check_thread_limits': {k: os.environ.get(k) for k in
                            ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS')},
    'pinned_reproduction': json.loads((BASE/'publication/reproduction/environment.json').read_text()),
}
(OUT/'environment-r1.json').write_text(json.dumps(env, indent=2)+'\n')
index_path = BASE/'publication/reproduction/commands.json'
index = json.loads(index_path.read_text(), parse_float=Decimal)
assert len(index) == 443
by_id = {x['id']: x for x in index}
assert len(by_id) == len(index)
groups = [
    ('lnts50/100/200/400', ['control/lnts_bound']),
    ('dtoc5', ['control/dtoc5_bound']),
    ('camshape100/200/400/800', ['control/camshape_bound']),
    ('lukvle10', ['control/lukvle10_bound']),
    ('optcdeg2 quadratic calibration', ['control/bb_qcal_certify']),
    ('hvycrash', ['small/A02_hvycrash_cert']),
    ('ex6_2_7 / ex6_2_5', ['small/A04_ex6_2_7_cert', 'small/A05_ex6_2_5_cert']),
    ('etamac / pricing050 / pindyck', ['small/A06_etamac_cert', 'small/A08_pricing050_cert', 'small/A10_pindyck_cert']),
    ('chain50/100/200/400', [f'cops/a_chain_bound_{n}' for n in (50,100,200,400)]),
    ('catmix100/200/400/800', [f'cops/a_catmix_bound_{n}' for n in (100,200,400,800)]),
    ('powerflow0030p/0039p/0039r', ['network/pf.pf_cert.powerflow0030p', 'network/pf.bb3.powerflow0039p', 'network/pf.bb3.powerflow0039r']),
    ('waterno2_06/09/12/18/24 period certificates', [f'water-audit/w{n}_certify' for n in ('06','09','12','18','24')]),
    ('waterno2_06 cell-slope certificate replay', ['water-audit/w06_ind_verify_certB']),
    ('ann_cumene_tanh extension replay and region verification', ['network/ann.replay_run1', 'network/ann.replay_run2', 'network/ann.verify_regions_run1.p2', 'network/ann.verify_regions_run2.p2', 'network/ann.verify_open_run2.p2']),
    ('KAN R, r3 n4/n5/n9; r5 n3/n5/n8', [f'network/kan.run_kan.kan_r{r}_h1_n{n}' for r,n in ((3,4),(3,5),(3,9),(5,3),(5,5),(5,8))]),
    ('eg_int_s / eg_disc_s parts 0/1; eg_disc2_s part 1 only', ['small/A31_eg_int_cert', 'small/A32_eg_disc_cert_p0', 'small/A33_eg_disc_cert_p1', 'small/A34_eg_disc2_cert_p1']),
    ('listed-bound audit: linear / nd_netgen / four emfl / topopt p4/p5 regeneration', ['water-audit/audit_cert_linear', 'water-audit/audit_cert_ndnetgen'] + [f'water-audit/audit_cert_socp_emfl{n}' for n in ('050_3_3','050_5_5','100_3_3','100_5_5')] + ['water-audit/audit_cert_topopt_p4', 'water-audit/audit_cert_topopt_p5']),
]
records = []
lines = ['| family and operation | recorded wall seconds, in listed order | command-index IDs |', '|---|---|---|']
for family, ids in groups:
    entries = [by_id[k] for k in ids]
    assert all(x['exit'] == 0 for x in entries)
    for x in entries:
        p = BASE/'publication/reproduction'/x['output']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == x['sha256'], x['id']
    records.extend(entries)
    lines.append('| '+family+' | '+' / '.join(str(x['wall_s']) for x in entries)+' | '+', '.join('`'+k+'`' for k in ids)+' |')
(OUT/'runtime-table-r1.md').write_text('\n'.join(lines)+'\n')
(OUT/'runtime-evidence-r1.json').write_text(json.dumps({
    'index_count': len(index), 'index_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest(),
    'selection_scope': 'Selected successful recorded reproduction commands; not complete original-run costs',
    'entries': records,
}, indent=2, default=str)+'\n')
print('PASS /proc hardware, uname, OS, current BLAS/SIMD/libc captured')
print('PASS 443 indexed commands; selected runtime sources and output hashes verified')
print(buf.getvalue())
