"""Explicitly prepare the pinned kinetics table for local numerical replay.

The scientific checks never fetch inputs. This separate preparation command
verifies the immutable SHA-256 before writing its locally obtained input.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

SOURCE_COMMIT = "430090e610446aab88328ce495ffb15b684c56c4"
SOURCE_URL = (
    "https://raw.githubusercontent.com/dowlinglab/measurement-opt/"
    + SOURCE_COMMIT + "/kinetics_source_data/Q_drop0.csv"
)
SOURCE_SHA256 = "54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca"
DEFAULT_OUTPUT = Path(__file__).with_name("kinetics_Q_drop0.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-file", type=Path, help="verify a separately obtained copy instead of downloading")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.from_file:
        raw = args.from_file.read_bytes()
    else:
        with urlopen(SOURCE_URL, timeout=30) as response:
            raw = response.read()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("Input SHA-256 differs from the pinned source; no output written.")
    if args.output.exists() and args.output.read_bytes() != raw:
        raise SystemExit("Output already contains different bytes; choose another --output.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print("Prepared pinned kinetics input; SHA-256 " + SOURCE_SHA256)


if __name__ == "__main__":
    main()
