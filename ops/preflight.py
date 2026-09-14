#!/usr/bin/env python3
"""Read-only prerequisites/integrity probe. This does not enforce quota."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('repo',type=pathlib.Path)
a=p.parse_args(); root=a.repo.resolve()
manifest=json.loads((pathlib.Path(__file__).parent/'fixture-manifest.json').read_text())
def command(args):
    try:
        r=subprocess.run(args,cwd=root,capture_output=True,text=True,timeout=15)
        return {'rc':r.returncode,'output':r.stdout.strip()[:300]}
    except (OSError,subprocess.TimeoutExpired) as e:return {'error':type(e).__name__}
changes=[]
for rel,digest in manifest['sha256'].items():
    f=root/rel
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:changes.append(rel)
category=None
try:category=json.loads((root/'.teleport/repo-metadata.json').read_text()).get('category')
except (OSError,ValueError):pass
tools={n:shutil.which(n) for n in ['node','python3','git','clang','make','bison','flex','rsync']}
report={'read_only':True,'source_pin':manifest['upstream_template_commit'],
        'head':command(['git','rev-parse','HEAD']), 'fixture_mismatches':changes,
        'category':category,'tools':tools,'node':command(['node','--version']),
        'live_quota_adapter':'not_configured','unattended_dispatch_ready':False}
print(json.dumps(report,indent=2))
sys.exit(0 if not changes and all(tools.values()) and category=='agentic' else 2)
