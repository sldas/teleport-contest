#!/usr/bin/env python3
"""Compare JS dice values, log events and subsequent state with actual patched C.
Run through ops/with-toolchain.sh after building the recorder. C function text
is copied unchanged into a test-only harness; no gameplay JS is generated.
"""
from pathlib import Path
import hashlib,json,subprocess,tempfile
root=Path(__file__).resolve().parent.parent
rec=root/'nethack-c/recorder'
rnd=(rec/'src/rnd.c').read_text()
start=rnd.index('\nint\nd(int n, int x)')+1
end=rnd.index('\n/* 1 <= rne',start)
dice=rnd[start:end]
prelude=r'''#include "config.h"
#include "isaac64.h"
#include <stdio.h>
#include <stdlib.h>
static isaac64_ctx state;
static FILE *rng_logfile;
static int RND(int x) { return (int)(isaac64_next_uint64(&state) % x); }
static void rng_log_write(const char *fn,const char *args,int result) {
 printf("%s(%s)=%d\n",fn,args,result);
}
'''
main=r'''
int main(int argc, char **argv) {
 unsigned long long seed=strtoull(argv[1],NULL,10);
 unsigned char bytes[8];
 for(int i=0;i<8;i++) { bytes[i]=(unsigned char)(seed & 255); seed >>= 8; }
 isaac64_init(&state,bytes,8); rng_logfile=stdout;
 int n,x;
 while(scanf("%d %d",&n,&x)==2) {
   printf("value=%d\n",d(n,x));
   printf("next=%d\n",RND(1000003));
 }
 return 0;
}
'''
js=r'''
import { readFileSync } from 'node:fs';
const {initRng, enableRngLog, getRngLog, d, rn2}=await import(process.argv[2]);
initRng(BigInt(process.argv[3]));enableRngLog();
for(const line of readFileSync(0,'utf8').trim().split('\n')) {
 const [n,x]=line.split(' ').map(Number);const before=getRngLog().length;
 const value=d(n,x);
 for(const item of getRngLog().slice(before)) console.log(item);
 console.log(`value=${value}`);console.log(`next=${rn2(1000003)}`);
}
'''
seeds=[0,1,2,7,42,102,8000,65535,2**31-1,2**32,2**53-1,2**63,2**64-1]
cases=[(0,0)]+[(n,x) for n in [0,1,2,3,5,16] for x in [1,2,6,20,1000]]
inputs=''.join(f'{n} {x}\n' for n,x in cases)
with tempfile.TemporaryDirectory(prefix='dice-oracle-') as tmp:
 p=Path(tmp);(p/'oracle.c').write_text(prelude+dice+main);(p/'probe.mjs').write_text(js)
 subprocess.run(['clang','-I'+str(rec/'include'),str(p/'oracle.c'),str(rec/'src/isaac64.c'),'-o',str(p/'oracle')],check=True,capture_output=True,text=True)
 for seed in seeds:
  c=subprocess.run([str(p/'oracle'),str(seed)],input=inputs,check=True,capture_output=True,text=True).stdout
  j=subprocess.run(['node',str(p/'probe.mjs'),(root/'js/rng.js').as_uri(),str(seed)],input=inputs,check=True,capture_output=True,text=True).stdout
  if c!=j:
   cl=c.splitlines();jl=j.splitlines();idx=next((i for i,(a,b) in enumerate(zip(cl,jl)) if a!=b),min(len(cl),len(jl)))
   print(json.dumps({'passed':False,'seed':str(seed),'line':idx,'expected':cl[idx:idx+3],'actual':jl[idx:idx+3]}));raise SystemExit(1)
print(json.dumps({'passed':True,'seeds':len(seeds),'cases_per_seed':len(cases),'total_sequences':len(seeds)*len(cases),'checks':['dice value','aggregate log','next raw RNG result'],'source_function_sha256':hashlib.sha256(dice.encode()).hexdigest()}))
