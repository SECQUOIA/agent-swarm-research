#!/usr/bin/env python3
"""Run existing research checks and preserve their exact provenance and output.

These finite checks supplement the manuscript's proofs; they do not certify them.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STAGE1 = [
    'code/mip_relaxation_binaries/check_bounds.py',
    'code/mip_relaxation_binaries/check_graph_precision.py',
    'code/quadratic_rank/check_simplex.py',
    'code/quadratic_rank/check_shrunk.py',
    'code/quadratic_rank/check_vector.py',
    'code/quadratic_rank/check_smooth_polynomial.py',
    'code/quadratic_rank/check_one_sided.py',
]
STAGE2 = [
    'code/quadratic_rank/' + name + '.py' for name in [
        'check_weighted_covariance', 'check_covariance_algorithm',
        'check_block_logdet_repair', 'check_block_psd_precision',
        'check_nonlinear_input_rank', 'check_l1_errors',
        'check_ellipsoidal_errors', 'check_effective_output_image',
        'check_precision_hardness', 'check_forest_laplacian_precision',
        'check_integer_feature_precision',
        'check_unconditional_allocation_repair',
    ]
] + ['paper-integer-dimension/verification/check_covariance_certificate.py']

STAGE3 = [
    'code/quadratic_rank/' + name + '.py' for name in [
        'check_accuracy_dependent_curvature', 'check_compiled_curvature_mass_knots',
        'check_curvature_integral_quadrature', 'check_signed_curvature_panels',
        'check_convex_polynomial_hybrid', 'check_positive_polynomial_shape_geometry_review',
        'check_positive_polynomial_degree_gap', 'check_positive_polynomial_loglog',
        'check_positive_separable_polynomials', 'check_positive_rational_stieltjes',
        'check_pure_power_reciprocal_interpolation', 'check_sparse_positive_polynomial_circuits',
        'check_compiled_power_knots', 'check_compiled_knots_second',
        'check_unconditional_allocation_repair',
    ]
] + ['code/small_exponent_soc/check_first_review.py',
     'paper-integer-dimension/verification/check_general_rational_interpolation.py']

STAGE4 = [
    'code/quadratic_rank/' + name + '.py' for name in [
        'check_implicit_knot_overlay', 'check_coupled_separable_rank_review',
        'check_oracle_curvature_rank_bands', 'check_oracle_curvature_rank_mixed_coordinates',
        'check_polynomial_binary_integer_gap', 'check_rational_polar_spanner_second',
        'check_separable_oracle_rank_precision',
    ]
] + ['code/positive_vector_obstruction/check_first_review.py',
     'code/positive_vector_obstruction/check_box_gap_root.py']

def run_one(path, interpreter, timeout, destination):
    started = time.monotonic()
    source = ROOT / path
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    try:
        result = subprocess.run([interpreter, str(source)], cwd=ROOT,
                                capture_output=True, text=True, timeout=timeout, env=env)
        output = result.stdout + result.stderr
        status = 'passed' if result.returncode == 0 else 'failed'
        code = result.returncode
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b'') + (exc.stderr or b'')
        if isinstance(output, bytes):
            output = output.decode(errors='replace')
        status, code = 'timeout', None
    log = destination / (source.parent.name + '__' + source.stem + '.txt')
    log.write_text(output)
    return dict(script=path, sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                status=status, returncode=code, seconds=round(time.monotonic()-started, 3),
                output=str(log.relative_to(ROOT)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument('--stage', choices=['stage1', 'stage2', 'stage3', 'stage4', 'all'], default='stage1')
    parser.add_argument('--timeout', type=int, default=300)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    paths = {'stage1': STAGE1, 'stage2': STAGE2, 'stage3': STAGE3,
             'stage4': STAGE4}.get(args.stage) or sorted(set(STAGE1 + STAGE2 + STAGE3 + STAGE4))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    destination = OUT / (args.stage + '-' + stamp)
    destination.mkdir()
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(run_one, p, args.python, args.timeout, destination) for p in paths]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(result['status'], result['script'], result['seconds'], flush=True)
    report = dict(time_utc=stamp, interpreter=args.python,
                  interpreter_version=subprocess.check_output([args.python, '--version'], text=True).strip(),
                  checks=sorted(results, key=lambda r:r['script']),
                  limitation='Finite exact and numerical checks supplement, and do not establish, universal mathematical claims.')
    (destination/'manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print('Manifest:', destination/'manifest.json', flush=True)
    return int(any(r['status'] != 'passed' for r in results))

if __name__ == '__main__':
    raise SystemExit(main())
