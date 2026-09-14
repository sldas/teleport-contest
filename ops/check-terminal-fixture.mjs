// Diagnostic only. No fixture edits, no changes to acceptance criteria.
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const root=path.resolve(process.argv[2]||'.');
const {Terminal}=await import(pathToFileURL(path.join(root,'frozen/terminal.js')));
const {decodeScreen}=await import(pathToFileURL(path.join(root,'frozen/screen-decode.mjs')));
const t=new Terminal(null,{rows:24,cols:80});
for(let c=20;c<24;c++)t.setCell(c,0,' ',8,1);
for(let i=0;i<4;i++)t.setCell(24+i,0,'Name'[i],8,1);
const got=decodeScreen(t.serialize());
const expected=decodeScreen('\x1b[20C\x1b[7m    Name\x1b[0m');
const lost=[];
for(let c=20;c<24;c++)if(got[0][c].attr!==expected[0][c].attr)lost.push(c);
console.log(JSON.stringify({issue:'https://github.com/davidbau/teleport-contest/issues/18',reproduced:lost.length>0,lost_inverse_columns:lost}));
