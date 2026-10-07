"""Clean-checkout guard for the reproduction runs (loaded through PYTHONPATH as usercustomize).

Installs a Python audit hook that watches file and directory accesses. Any access to a path
inside the main working tree /workspace/minlp-notes/ (the clean worktree is
/workspace/minlp-notes-clean/, a different prefix) is appended to the file named by
REPRO_GUARD_LOG. With REPRO_GUARD_MODE=strict (the default) the access is also refused with
PermissionError, which simulates a machine on which only the clean checkout exists.
The run scripts copy this file to a directory outside the main tree and put that directory on
PYTHONPATH; the guard log also lies outside the main tree.
Limitation: only accesses made through Python's audited calls are seen (open, os.listdir,
os.scandir, ...); C extensions that open files themselves are not watched.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import os
import sys

_MAIN = (_PUBLIC_REPO + '/')
_LOG = os.environ.get("REPRO_GUARD_LOG")
_STRICT = os.environ.get("REPRO_GUARD_MODE", "strict") == "strict"
_EVENTS = {"open", "os.listdir", "os.scandir", "os.chdir", "os.remove", "os.rename",
           "os.mkdir", "os.rmdir", "shutil.copyfile", "shutil.rmtree", "glob.glob"}
_busy = [False]


def _hook(event, args):
    if _busy[0] or event not in _EVENTS or not args:
        return
    p = args[0]
    if isinstance(p, bytes):
        p = p.decode(errors="replace")
    if not isinstance(p, str):
        return
    _busy[0] = True
    try:
        full = os.path.realpath(p)
        hit = full.startswith(_MAIN) or full + "/" == _MAIN
        if hit and _LOG:
            try:
                with open(_LOG, "a") as f:
                    f.write(f"{os.getpid()}\t{event}\t{full}\t{' '.join(sys.argv)[:200]}\n")
            except Exception:
                pass
    finally:
        _busy[0] = False
    if hit and _STRICT:
        raise PermissionError(f"repro guard: access to the main tree refused: {full}")


sys.addaudithook(_hook)
