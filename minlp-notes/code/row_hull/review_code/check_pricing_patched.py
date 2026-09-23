"""check_pricing.py with the corrected _compress (also with forced interval merging)."""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from patched_pricing import install
install()
import check_pricing as c
for d, k in ((2, 4000), (1, 4000), (1, 30), (2, 30), (None, 30)):
    c.main(d, 300, 10, k)
