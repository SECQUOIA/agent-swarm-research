"""run_one.py with the corrected pricing._compress installed (same arguments as run_one.py)."""
import runpy, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from patched_pricing import install
install()
runpy.run_path(str(HERE.parent / "run_one.py"), run_name="__main__")
