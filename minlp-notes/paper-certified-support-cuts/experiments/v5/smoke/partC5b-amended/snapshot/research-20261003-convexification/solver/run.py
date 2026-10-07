"""Run native SCIP with optional certified original-row aggregation cuts."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.integration import run_instance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('mode', choices=('baseline','all','auto'))
    parser.add_argument('--time-limit', type=float, default=30.)
    parser.add_argument('--node-limit', type=int)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    result = run_instance(args.path,args.mode,args.time_limit,args.seed,args.node_limit,quiet=not args.verbose)
    text = json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
