#!/usr/bin/env python3
"""Verify compressed evidence by streaming every member, without extraction."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import time


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('archive',type=Path)
    ap.add_argument('manifest',type=Path)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    entries=json.loads(args.manifest.read_text())['files']
    expected={r['path']:r for r in entries}
    assert len(expected)==len(entries),'duplicate manifest paths'
    seen=set();total=0;started=time.monotonic()
    with tarfile.open(args.archive,'r|gz')as tar:
        for member in tar:
            prefix='minlp-certified-evidence/'
            assert member.name.startswith(prefix),member.name
            name=member.name[len(prefix):]
            assert name not in seen and name in expected,name
            seen.add(name);record=expected[name]
            if 'symlink'in record:
                assert member.issym()and member.linkname==record['symlink'],name
            else:
                assert member.isfile()and member.size==record['bytes'],name
                stream=tar.extractfile(member);h=hashlib.sha256()
                for data in iter(lambda:stream.read(1048576),b''):h.update(data)
                assert h.hexdigest()==record['sha256'],name
                total+=member.size
            if len(seen)%500==0:print('Verified members:',len(seen),flush=True)
    assert seen==set(expected),'missing archive members'
    result={'archive':str(args.archive),'manifest':str(args.manifest),'verified_members':len(seen),'uncompressed_file_bytes':total,'wall_seconds':time.monotonic()-started,'all_member_hashes_match':True}
    if args.out:args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
