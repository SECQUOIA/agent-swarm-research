"""Independent review regressions for replay data and producer boundaries."""
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from certify import recheck
from certify.summarize import summarize


def replay_inputs(tmp_path):
    instances = tmp_path / "instances"
    instances.mkdir()
    (instances / "tiny.py").write_text("model source\n")
    outroot = tmp_path / "artifacts"
    certdir = outroot / "tiny"
    certdir.mkdir(parents=True)
    for name in ("lemma.json", "master.lp", "master_complete.vipr"):
        (certdir / name).write_text("original\n")
    return SimpleNamespace(instances=instances, outroot=outroot, viprchk=None, timeout=0.5)


def test_replay_refuses_artifact_changed_during_check(tmp_path, monkeypatch):
    args = replay_inputs(tmp_path)

    def fake_worker(command, **kwargs):
        report = Path(command[command.index("--report") + 1])
        report.write_text(json.dumps({"ok": True, "sense": 1,
                                      "certified_bound_original_sense": "1"}))
        (args.outroot / "tiny" / "lemma.json").write_text("changed\n")
        return SimpleNamespace(pid=99999999, wait=lambda **kw: 0)

    monkeypatch.setattr(recheck.subprocess, "Popen", fake_worker)
    monkeypatch.setattr(recheck.os, "killpg", lambda *args: None)
    result = recheck.replay(0, {"instance": "tiny"}, args, None)
    assert result["status"] == "artifacts_changed"
    assert result["artifacts"] != result["artifacts_after"]
    assert result["certified_bound_original_sense"] is None
    assert result["bound_comparison"] == "unavailable"


def test_timeout_stops_checker_descendant(tmp_path, monkeypatch):
    args = replay_inputs(tmp_path)
    pidfile = tmp_path / "descendant.pid"
    actual_popen = subprocess.Popen
    program = (
        "import pathlib,subprocess,sys,time; "
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
        "pathlib.Path(sys.argv[1]).write_text(str(child.pid)); time.sleep(30)"
    )

    def hanging_worker(command, **kwargs):
        return actual_popen([sys.executable, "-c", program, str(pidfile)], **kwargs)

    monkeypatch.setattr(recheck.subprocess, "Popen", hanging_worker)
    result = recheck.replay(0, {"instance": "tiny"}, args, None)
    assert result["status"] == "timeout"
    assert result["certified_bound_original_sense"] is None
    assert pidfile.exists(), "the descendant must start before testing its termination"
    stat = Path("/proc") / pidfile.read_text() / "stat"
    # A dead orphan may remain a zombie until this container's init reaps it.
    assert not stat.exists() or stat.read_text().split()[2] == "Z"


def test_summary_completion_requires_every_unique_historical_index():
    record = {"schema": 1, "record_index": 0, "instance": "tiny", "status": "rejected",
              "historical_checker": "OK", "historical_viprchk": "OK"}
    partial = summarize([record], {}, {}, expected_records=2)
    assert partial["replay_complete"] is False
    assert partial["historical_accepted_unrevalidated"] == 1
    assert summarize([record, record], {}, {}, expected_records=2)["replay_complete"] is False
    second = dict(record, record_index=1, instance="second")
    assert summarize([record, second], {}, {}, expected_records=2)["replay_complete"] is True
    assert summarize([record], {}, {})["replay_complete"] is not True


@pytest.mark.parametrize("safe_accepts", [True, False])
def test_producer_retries_internal_rejection_and_reports_final_verdict(tmp_path, monkeypatch, safe_accepts):
    from certify import driver, run_all

    outroot = tmp_path / "new-artifacts"
    verdicts = iter([False, safe_accepts])
    calls = []

    def build(instance, outdir, **kwargs):
        Path(outdir).mkdir(parents=True)
        return {"status": "master_written", "convexity": {"certified": True}}

    def tool(command, cwd, **kwargs):
        name = Path(command[0]).name
        if name == "scip":
            (Path(cwd) / "master.vipr").write_text("raw proof\n")
            return SimpleNamespace(returncode=0, stdout="SCIP Status : solved\nExact Dual Bound : 1\n")
        if name == "viprcomp":
            (Path(cwd) / "master_complete.vipr").write_text("RTP range 1 2\n")
            return SimpleNamespace(returncode=0, stdout="")
        assert name == "viprchk"
        return SimpleNamespace(returncode=0, stdout="Successfully verified optimal value range [1, 2]\n")

    def check(instance, certdir, **kwargs):
        calls.append(kwargs)
        accepted = next(verdicts)
        return {"ok": accepted, "sense": -1, "checks": [],
                "certified_bound_original_sense": "-1" if accepted else None}

    monkeypatch.setattr(driver, "build_certificate", build)
    monkeypatch.setattr(driver, "check_certificate", check)
    monkeypatch.setattr(run_all.subprocess, "run", tool)
    result = run_all.run_instance("tiny", str(outroot), 1, 1, 1)
    assert len(calls) == 2
    assert all(call["require_vipr"] for call in calls)
    assert [attempt["label"] for attempt in result["scip_attempts"]] == ["default", "safe"]
    assert result["scip_attempts"][0]["checker"] == "FAIL"
    assert result["status"] == ("verified" if safe_accepts else "rejected")
    assert result["checker"] == ("OK" if safe_accepts else "FAIL")
    assert result["certified_bound_original_sense"] == ("-1" if safe_accepts else None)
    if safe_accepts:
        assert result["scip_mode"] == "safe"
        assert result["certified_lb"] == 1


def test_producer_refuses_existing_output_instead_of_mixing_campaigns(tmp_path, monkeypatch, capsys):
    from certify import run_all

    names = tmp_path / "names.txt"
    names.write_text("tiny\n")
    output = tmp_path / "prior.jsonl"
    original = '{"instance":"old"}\n{"interrupted'
    output.write_text(original)
    monkeypatch.setattr(sys, "argv", ["run_all", "--names", str(names), "--out", str(output)])
    monkeypatch.setattr(run_all.shutil, "which", lambda name: name)
    with pytest.raises(SystemExit) as error:
        run_all.main()
    assert error.value.code == 2
    assert "producer output must be new" in capsys.readouterr().err
    assert output.read_text() == original
