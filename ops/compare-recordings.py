#!/usr/bin/env python3
"""Strict reference calibration: compare segment inputs and all step fields.
Recording metadata is intentionally excluded. No normalization is performed.
Exit 0 means exact compared-field parity, 2 means divergence/empty output.
"""
import argparse, json, pathlib, sys
p=argparse.ArgumentParser();p.add_argument('reference');p.add_argument('actual');a=p.parse_args()
x=json.loads(pathlib.Path(a.reference).read_text());y=json.loads(pathlib.Path(a.actual).read_text())
xs=x.get('segments',[]);ys=y.get('segments',[]);issues=[];counts={};lengths=[]
def issue(kind,**details):
 counts[kind]=counts.get(kind,0)+1
 if len(issues)<10:issues.append({'kind':kind,**details})
if not xs or not ys:issue('empty_segments')
if len(xs)!=len(ys):issue('segment_count',expected=len(xs),actual=len(ys))
for si,(s,t) in enumerate(zip(xs,ys)):
 for k in ['seed','datetime','nethackrc','moves']:
  if s.get(k)!=t.get(k):issue('input_'+k,segment=si)
 ss=s.get('steps',[]);ts=t.get('steps',[]);lengths.append({'reference':len(ss),'actual':len(ts)})
 if not ss or not ts:issue('empty_steps',segment=si)
 if len(ss)!=len(ts):issue('step_count',segment=si,expected=len(ss),actual=len(ts))
 for i,(u,v) in enumerate(zip(ss,ts)):
  for k in sorted(set(u)|set(v)):
   if (k in u)!=(k in v) or u.get(k)!=v.get(k):issue('step_'+k,segment=si,step=i)
r={'exact_compared_fields_match':not counts,'normalization':False,'segment_lengths':lengths,'mismatch_counts':counts,'first_differences':issues}
print(json.dumps(r,indent=2));sys.exit(0 if not counts else 2)
