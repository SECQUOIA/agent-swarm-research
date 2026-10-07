"""Print the diff between the reviewer's Certifier methods and the MarginCertifier copies.
Every changed or added line must end with '# MARGIN'; the script asserts this."""
import difflib
import inspect

from margin_cert import MarginCertifier, Certifier

bad = 0
for name in ("certify_batch", "_batch", "_one"):
    a = inspect.getsource(getattr(Certifier, name)).splitlines()
    b = inspect.getsource(getattr(MarginCertifier, name)).splitlines()
    d = list(difflib.unified_diff(a, b, f"indep_cert.Certifier.{name}", f"margin_cert.MarginCertifier.{name}", lineterm="", n=0))
    print("\n".join(d))
    for line in d:
        if line.startswith("+") and not line.startswith("+++"):
            bad += not line.rstrip().endswith("# MARGIN")
    removed = [line for line in d if line.startswith("-") and not line.startswith("---")]
    print(f"== {name}: {len(removed)} original lines replaced")
print(f"added/changed lines without the '# MARGIN' marker: {bad}")
assert bad == 0
