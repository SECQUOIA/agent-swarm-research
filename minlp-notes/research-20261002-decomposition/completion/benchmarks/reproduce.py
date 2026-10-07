"""Re-run one archived lane in a new directory, without changing old evidence.

Example: python3 reproduce.py completed_exact /tmp/minlp-exact-reproduction
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lane',choices=('baseline','completed_grid','completed_exact',
                                       'completed_recourse','completed_constraints','completed_sets'))
    parser.add_argument('destination',type=Path)
    args=parser.parse_args()
    frozen=HERE/'frozen'/args.lane
    if not frozen.is_dir():parser.error('This lane has not been frozen yet')
    if args.destination.exists():parser.error('Destination must not already exist')
    args.destination.mkdir(parents=True)
    runner=frozen/('run_benchmarks_snapshot.py' if args.lane=='baseline' else 'runner_snapshot.py')
    copies={runner:'run_benchmarks.py',frozen/'corpus_snapshot.py':'corpus.py',
            frozen/'constrained_cases_snapshot.py':'constrained_cases.py',
            frozen/'cases_snapshot.json':'cases.json',
            frozen/'constrained_references_snapshot.json':'constrained_references.json'}
    for source,name in copies.items():shutil.copy2(source,args.destination/name)
    shutil.copytree(HERE/'frozen'/'baseline',args.destination/'frozen'/'baseline')
    if args.lane!='baseline':shutil.copytree(frozen,args.destination/'frozen'/args.lane)
    result=subprocess.run([sys.executable,str(args.destination/'run_benchmarks.py'),'--run',args.lane])
    raise SystemExit(result.returncode)
if __name__=='__main__':main()
