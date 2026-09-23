"""Replay audit contracts and exact reference-comparison regressions."""
import json
import subprocess
import sys

import pytest

from certify.recheck import exact_comparison, read_results
from certify.run_all import canonicalize_fractions
from certify.summarize import reference_comparison, summarize


def test_exact_comparisons_do_not_round_or_count_negative_gaps_as_closed():
    assert exact_comparison("1000000000000000001", "1000000000000000000") == "changed"
    assert exact_comparison("2/6", "1/3") == "equal"
    result = reference_comparison("1000000000000000001", "1000000000000000000", 1)
    assert result["reference_beyond_bound"]
    assert not result["near_reference_1e4"]
    assert reference_comparison("3", "4", -1)["reference_beyond_bound"]
    assert reference_comparison("4", "3", -1)["signed_difference"] == "1"
    assert reference_comparison("0", "0", 1)["near_reference_1e4"]
    assert reference_comparison("0", "inf", 1) is None


def test_historical_acceptance_is_not_a_replay_verdict():
    old = {"instance": "old", "status": "done", "checker": "OK", "viprchk": "OK"}
    result = summarize([old], {}, {})
    assert result["historical_accepted_unrevalidated"] == 1
    assert result["verified"] == 0


def test_canonicalization_preserves_solution_and_inference_sections(tmp_path):
    proof = tmp_path / "proof.vipr"
    proof.write_text("RTP range -2/4 4/6\nSOL 1\ns 1 0 2/4\nDER 1\nd G 2/4 1 0 1 { sol } -1\n")
    canonicalize_fractions(proof)
    assert proof.read_text() == "RTP range -1/2 2/3\nSOL 1\ns 1 0 1/2\nDER 1\nd G 1/2 1 0 1 { sol } -1\n"
    proof.write_text("SOL 1\ns 1 0 2/0\n")
    with pytest.raises(ZeroDivisionError):
        canonicalize_fractions(proof)
    assert proof.read_text() == "SOL 1\ns 1 0 2/0\n"


def test_resume_recovers_only_unfinished_final_line(tmp_path):
    output = tmp_path / "out.jsonl"
    output.write_text('{"record_index": 0}\n{"record_')
    with output.open("r+") as stream:
        assert read_results(stream) == {0: {"record_index": 0}}
    assert output.read_text() == '{"record_index": 0}\n'
    output.write_text('{bad}\n{"record_index": 1}\n')
    with output.open("r+") as stream, pytest.raises(ValueError):
        read_results(stream)


def test_replay_is_separate_resumable_and_pins_inputs(tmp_path):
    history = tmp_path / "history.jsonl"
    history.write_text(json.dumps({"instance": "already_ok", "status": "done", "checker": "OK", "viprchk": "OK"}) + "\n")
    original = history.read_bytes()
    output = tmp_path / "replay.jsonl"
    cmd = [sys.executable, "-m", "certify.recheck", "--records", str(history),
           "--out", str(output), "--outroot", str(tmp_path / "artifacts"),
           "--instances", str(tmp_path / "instances")]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    first = output.read_bytes()
    record = json.loads(first)
    assert record["status"] == "missing_artifacts"
    assert record["historical_checker"] == "OK"
    assert record["certified_bound_original_sense"] is None
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert output.read_bytes() == first
    assert history.read_bytes() == original
    history.write_text(history.read_text() + json.dumps({"instance": "new"}) + "\n")
    rejected = subprocess.run(cmd, capture_output=True, text=True)
    assert rejected.returncode != 0
    assert "changed; use a new output" in rejected.stderr
    assert output.read_bytes() == first
    same_file = subprocess.run(cmd[:cmd.index("--out")] + ["--out", str(history)], capture_output=True, text=True)
    assert same_file.returncode != 0
    assert "output must differ" in same_file.stderr
