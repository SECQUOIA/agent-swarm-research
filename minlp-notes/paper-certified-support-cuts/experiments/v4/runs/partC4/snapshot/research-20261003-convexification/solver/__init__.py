"""Native-preserving integration with explicitly reused frozen support kernels."""
from pathlib import Path

# Reuse reviewed v1 primitives without copying or changing frozen sources.
__path__.append(str(Path(__file__).resolve().parents[2] /
                    "research-20261002-convexification" / "solver"))
