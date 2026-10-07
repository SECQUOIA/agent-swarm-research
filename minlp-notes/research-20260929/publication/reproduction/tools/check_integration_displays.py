"""Use exact saved rational values to check the displays corrected for integration r1."""
from fractions import Fraction as Q
import json
import re

from finish_paths import RESEARCH, OUT


def main():
    checks = []

    def check(name, source, exact, display, direction):
        shown = Q(display)
        passed = shown >= exact if direction == "up" else shown <= exact
        checks.append(dict(name=name, source=source, exact=str(exact), display=display,
                           direction=direction, passed=passed))
        assert passed, name

    readme = (OUT / "README.md").read_text()
    for name, shown in [("eg_int_s", "6.4531031593842275"),
                        ("eg_disc_s", "5.7605396164535107"),
                        ("eg_disc2_s", "5.6421005799711068")]:
        source = f"open-instances-wave3/eg/retry/sol/{name}.retry.sol"
        text = (RESEARCH / source).read_text()
        exact = Q(re.search(r"objvar\s+(\S+)", text)[1])
        assert shown in readme
        check(name + " primal", source, exact, shown, "up")
    source = "publication/primal/water-ann-kan/points/waterno2_06.exact.json"
    primal = Q(json.loads((RESEARCH / source).read_text())["objective"])
    cert_source = "open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"
    lower = Q(json.loads((RESEARCH / cert_source).read_text())["bound_exact"])
    report = (RESEARCH / "publication/literature/network/report.md").read_text()
    assert "282.888038, listed (≤ 1.68%)" in report
    check("waterno2_06 primal", source, primal, "282.888038", "up")
    check("waterno2_06 lower", cert_source, lower, "278.230573", "down")
    check("waterno2_06 gap percent vs exact lower", source + "; " + cert_source,
          (primal - lower) / lower * 100, "1.68", "up")
    check("waterno2_06 gap percent vs displayed lower", source,
          (primal - Q("278.230573")) / Q("278.230573") * 100, "1.68", "up")
    check("waterno2_06 gap percent vs both displays", source + "; " + cert_source,
          (Q("282.888038") - Q("278.230573")) / Q("278.230573") * 100, "1.68", "up")
    # The all-leaf target is an exact decimal, not the author's float representation.
    source = "publication/eg-recheck/logs/cert_p7_c0.log"
    text = (RESEARCH / source).read_text()
    target = re.search(r"theta\* = (\S+): certified", text)[1]
    check("eg_disc2_s lower", source, Q(target), "5.642100574331458", "down")
    (OUT / "logs/integration-r1-displays.json").write_text(json.dumps(checks, indent=2) + "\n")
    print(f"PASS: {len(checks)} exact rational display checks")


if __name__ == "__main__":
    main()
