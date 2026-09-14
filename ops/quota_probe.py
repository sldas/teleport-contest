#!/usr/bin/env python3
"""Read-only Codex quota probe. Never logs in, refreshes auth, or starts inference.
Only allowlisted quota fields are emitted. Exit2 means unavailable, not zero use.
Successful lookup does not establish project attribution or hard enforcement.
"""
import argparse,asyncio,json,math,shutil,time
from pathlib import Path

def normalize(response):
    if 'error' in response:
        message=str(response['error'].get('message',''))
        return {'lookup_ok':False,'reason':'authentication_rejected' if '401' in message or 'Unauthorized' in message else 'quota_endpoint_error'}
    result=response.get('result') or {}
    buckets=result.get('rateLimitsByLimitId')
    if not isinstance(buckets,dict) or not buckets:
        single=result.get('rateLimits')
        buckets={single.get('limitId') or 'default':single} if isinstance(single,dict) else {}
    windows=[]
    for bucket_id,bucket in buckets.items():
        if not isinstance(bucket,dict):continue
        for slot in ['primary','secondary']:
            w=bucket.get(slot)
            if w is None:continue
            if not isinstance(w,dict):return {'lookup_ok':False,'reason':'invalid_window'}
            used=w.get('usedPercent');reset=w.get('resetsAt');duration=w.get('windowDurationMins')
            if type(used) not in (int,float) or not math.isfinite(used) or used<0:
                return {'lookup_ok':False,'reason':'invalid_usage'}
            if type(reset) not in (int,float) or not math.isfinite(reset) or reset<=time.time():
                return {'lookup_ok':False,'reason':'missing_or_expired_reset'}
            if type(duration) not in (int,float) or not math.isfinite(duration) or duration<=0:
                return {'lookup_ok':False,'reason':'invalid_window_duration'}
            windows.append({'bucket':str(bucket_id),'window':slot,'used_percent':used,'remaining_percent':max(0,100-used),'duration_minutes':duration,'resets_at':reset})
    if not windows:return {'lookup_ok':False,'reason':'no_metered_windows'}
    return {'lookup_ok':True,'observed_at':time.time(),'scope':'account_not_project','windows':windows}

async def lookup(binary,timeout):
    process=await asyncio.create_subprocess_exec(binary,'app-server','--stdio',stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.DEVNULL)
    async def send(value):
        process.stdin.write((json.dumps(value)+'\n').encode());await process.stdin.drain()
    async def exchange():
        await send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'mazes_quota_probe','version':'1.0'},'capabilities':{'experimentalApi':True}}})
        while True:
            line=await process.stdout.readline()
            if not line:return {'lookup_ok':False,'reason':'transport_closed'}
            try:r=json.loads(line)
            except ValueError:continue
            if r.get('id')==1:
                if 'error' in r:return {'lookup_ok':False,'reason':'initialization_failed'}
                await send({'method':'initialized'});await send({'id':2,'method':'account/rateLimits/read'})
            elif r.get('id')==2:return normalize(r)
    try:return await asyncio.wait_for(exchange(),timeout)
    except asyncio.TimeoutError:return {'lookup_ok':False,'reason':'timeout'}
    finally:
        if process.returncode is None:
            process.terminate()
            try:await asyncio.wait_for(process.wait(),3)
            except asyncio.TimeoutError:process.kill();await process.wait()

async def main():
    p=argparse.ArgumentParser();p.add_argument('--codex');p.add_argument('--timeout',type=float,default=20);a=p.parse_args()
    binary=a.codex or shutil.which('codex') or ('/opt/codex/bin/codex' if Path('/opt/codex/bin/codex').is_file() else None)
    if not binary:r={'lookup_ok':False,'reason':'codex_not_found'}
    else:
        try:r=await lookup(binary,a.timeout)
        except (OSError,BrokenPipeError,ConnectionError):r={'lookup_ok':False,'reason':'transport_error'}
    r.update({'inference_started':False,'project_attribution_verified':False,'hard_cap_verified':False,'recurring_dispatch_allowed':False})
    print(json.dumps(r,indent=2));return 0 if r['lookup_ok'] else 2
if __name__=='__main__':raise SystemExit(asyncio.run(main()))
