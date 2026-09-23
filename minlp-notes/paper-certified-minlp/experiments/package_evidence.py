#!/usr/bin/env python3
"""Build core and streaming bulk evidence without duplicating full proof trees.

Run only after generation and timed independent replay have finished.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import tarfile


def records(p):return [json.loads(s)for s in p.read_text().splitlines()if s.strip()]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb')as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')


def redact(p):
    text=p.read_text(errors='strict');original=text
    # Remove only positively identified solver-license banners; preserve every
    # status, model statement, objective, and returned numerical value.
    text=re.sub(r'(?m)^Licensee:[^\n]*\n(?:[ \t]+[^\n]*\n)*','[License-identifying banner omitted.]\n',text)
    text=re.sub(r'(?m)^USER:[^\n]*\n[^\n]*\n[^\n]*\n','[License-identifying banner omitted.]\n',text)
    text=re.sub(r'(?m)^.*(?:Set parameter LicenseID|Academic license.*registered to)[^\n]*\n','[License-identifying banner omitted.]\n',text)
    if text!=original:
        before=hashlib.sha256(original.encode()).hexdigest();p.write_text(text)
        return {'original_sha256':before,'distributed_sha256':sha(p),'transformation':'Remove license-identifying banner lines only; no numerical output, status, model, or proof edits.'}


class HashReader:
    def __init__(self,f):self.f=f;self.h=hashlib.sha256()
    def read(self,n=-1):
        b=self.f.read(n);self.h.update(b);return b


def archive(path,items,expected=None):
    manifest=[];expected=expected or{}
    with tarfile.open(path,'w:gz',compresslevel=1)as tar:
        for index,(source,relative)in enumerate(items):
            info=tar.gettarinfo(str(source),'minlp-certified-evidence/'+relative)
            info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
            if info.isfile():
                with source.open('rb')as stream:
                    reader=HashReader(stream);tar.addfile(info,reader);digest=reader.h.hexdigest()
                if relative in expected:assert digest==expected[relative],relative
                manifest.append({'path':relative,'bytes':info.size,'sha256':digest})
            elif info.issym():tar.addfile(info);manifest.append({'path':relative,'symlink':info.linkname})
            else:raise ValueError(source)
            if index%100==0:print(path.name,index+1,'/',len(items),flush=True)
    return manifest


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lab',type=Path,required=True);ap.add_argument('--paper',type=Path,required=True);ap.add_argument('--phase',choices=['all','bulk','core'],default='all');a=ap.parse_args()
    lab=a.lab.resolve();paper=a.paper.resolve();core=paper/'supplement/core';campaign=paper/'experiments/uniform-20260913';dest=paper/'supplement'
    # Core-only rebuilds retain the already fully verified bulk archive and
    # digest. The size check below is not a new integrity verification.
    previous_bulk = None
    if a.phase == 'core' and (dest/'archives.json').is_file():
        previous = json.loads((dest/'archives.json').read_text())
        previous_bulk = next((x for x in previous['archives']
                              if x['file'] == 'certified-minlp-certificates.tar.gz'), None)
        if previous_bulk is not None and (dest/previous_bulk['file']).stat().st_size != previous_bulk['bytes']:
            previous_bulk = None
    assert(campaign/'replay-timing.json').exists()and len(records(campaign/'replay.jsonl'))==289
    assert json.loads((campaign/'postgeneration-integrity.json').read_text())['all_frozen_bytes_unchanged']
    campaigns=[campaign]+sorted(p for p in(paper/'experiments').glob('producer-repair-*')if p.is_dir())
    for run in campaigns:
        assert(run/'replay-timing.json').exists()
        assert len(records(run/'replay.jsonl'))==len((run/'names.txt').read_text().split())
    # Compact records and logs live in the core. Large proof and master files
    # enter the bulk archive directly from their original locations.
    for source in(paper/'experiments').glob('*'):
        if source.is_file():target=core/'experiments'/source.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    for run in campaigns:
        for source in run.rglob('*'):
            if not source.is_file()or source.is_symlink():continue
            rel=source.relative_to(run)
            if rel.parts[0]=='artifacts' and source.suffix!='.json':continue
            if rel.parts[0]=='artifacts' and source.name=='lemma.json':continue
            if rel.parts[0]=='replay-artifacts':continue
            target=core/'experiments'/run.name/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    reporting=paper/'experiments/reporting-repair-20260914'
    assert(reporting/'replay-timing.json').exists()
    for source in reporting.rglob('*'):
        if source.is_file()and not source.is_symlink():
            target=core/'experiments/reporting-repair-20260914'/source.relative_to(reporting)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    for name in('source-snapshots','proof-steps','new-proof-step-extracts'):
        shutil.copytree(paper/'evidence'/name,core/'evidence'/name,dirs_exist_ok=True)
    for name in('proof-step-checks.json','new-proof-step-summary.json'):
        shutil.copy2(paper/'evidence'/name,core/'evidence'/name)
    shutil.copytree(paper/'tables',core/'tables',dirs_exist_ok=True)
    previous=core/'redactions.json'
    redactions={r['path']:r for r in json.loads(previous.read_text())}if previous.exists()else{}
    for source in sorted(core.rglob('*')):
        if source.is_file()and(source.suffix in('.log','.lst','.stdout','.stderr')):
            r=redact(source)
            if r:redactions[str(source.relative_to(core))]={'path':str(source.relative_to(core)),**r}
    dump(core/'redactions.json',list(redactions.values()))
    bulk={};expected={}
    for recordfile in ('cert_replay_20260913_complete.jsonl','cert_regenerated_20260913_complete.jsonl'):
        for r in records(lab/'results'/recordfile):
            for key in('lemma','master','proof'):
                item=r['artifacts'][key]
                if item.get('missing'):continue
                source=Path(item['path']);relative='lab/'+str(source.relative_to(lab))
                bulk[relative]=source;expected[relative]=item['sha256']
    inventory=[]
    for run in campaigns:
        prefix='experiments/'+run.name+'/'
        for name in(run/'names.txt').read_text().split():
            folder=run/'artifacts'/name
            complete=sorted(folder.glob('master_complete*.vipr'))
            # Keep raw proof only when no completed proof exists.
            raw=sorted(p for p in folder.glob('*.vipr*')if p.is_file())
            keep=complete or raw
            for source in keep+[folder/n for n in('lemma.json','master.lp')if(folder/n).is_file()]:
                relative=prefix+str(source.relative_to(run));bulk[relative]=source
            inventory.append({'campaign':run.name,'instance':name,'completed_proofs':[p.name for p in complete],
                              'retained_proofs':[p.name for p in keep],
                              'omitted_redundant_raw_proofs':[p.name for p in raw if p not in keep]})
            for source in sorted(folder.iterdir())if folder.is_dir()else[]:
                if source.is_file()and source.suffix in('.log','.stdout','.stderr'):
                    relative=prefix+str(source.relative_to(run));copy=dest/'bulk-log-copies'/relative
                    copy.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,copy)
                    r=redact(copy)
                    if r:redactions[relative]={'path':relative,**r}
                    bulk[relative]=copy
        for r in records(run/'replay.jsonl'):
            for key in('lemma','master','proof'):
                item=r.get('artifacts',{}).get(key,{})
                if item.get('sha256'):
                    source=Path(item['path']).resolve();relative=prefix+str(source.relative_to(run))
                    expected[relative]=item['sha256']
        for source in(run/'replay-artifacts').rglob('*'):
            if source.is_symlink():bulk[prefix+str(source.relative_to(run))]=source
    for record in records(reporting/'replay.jsonl'):
        for key in('lemma','master','proof'):
            item=record['artifacts'][key];relative=str(Path(item['path']).resolve().relative_to(paper))
            assert relative in bulk
            expected[relative]=item['sha256']
    dump(core/'fresh-artifact-inventory.json',inventory)
    dump(core/'redactions.json',list(redactions.values()))
    bulkfile=dest/'certified-minlp-certificates.tar.gz'
    if a.phase!='core':
        manifest=archive(bulkfile,[(source,relative)for relative,source in sorted(bulk.items())],expected)
        dump(core/'bulk-manifest.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'files':manifest,
             'proof_files_preserved_byte_for_byte':True,'historical_and_selected_fresh_hashes_match_replay':True})
        if a.phase=='bulk':
            print('Bulk archive complete; core packaging remains.',flush=True);return
    else:assert bulkfile.is_file()and(core/'bulk-manifest.json').is_file()
    items=[(p,str(p.relative_to(core)))for p in sorted(core.rglob('*'))if p.is_file()and '__pycache__'not in p.parts]
    # A manifest cannot contain its own digest. The archive SHA below covers it.
    manifest=[{'path':rel,'bytes':p.stat().st_size,'sha256':sha(p)}for p,rel in items if rel!='core-manifest.json']
    dump(core/'core-manifest.json',{'files':manifest})
    corefile=dest/'certified-minlp-core.tar.gz'
    items=[(p,str(p.relative_to(core)))for p in sorted(core.rglob('*'))if p.is_file()and '__pycache__'not in p.parts]
    archive(corefile,items)
    core_record={'file':corefile.name,'bytes':corefile.stat().st_size,'sha256':sha(corefile)}
    bulk_record=(previous_bulk if previous_bulk is not None else
                 {'file':bulkfile.name,'bytes':bulkfile.stat().st_size,'sha256':sha(bulkfile)})
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'archives':[core_record,bulk_record],
            'bulk_uncompressed_regular_bytes':sum(x.get('bytes',0)for x in json.loads((core/'bulk-manifest.json').read_text())['files']),
            'core_uncompressed_bytes':sum(p.stat().st_size for p,_ in items),'redacted_log_copies':len(redactions)}
    if previous_bulk is not None:
        report['bulk_digest_provenance']='Retained from the previously verified archive index; this core-only rebuild checked bulk size but did not reread or rehash its contents.'
    dump(dest/'archives.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
