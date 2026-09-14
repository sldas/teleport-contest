# Status — hosted bootstrap checkpoint

Kickoff authorized. Bootstrap merged to main via PR1. Current work: dice RNG semantics. Canonical base:
364e9d6708aa9b6b369d5683ceec2df73ae93d37. GitHub identity: sldas.
User confirmed sldas/teleport-contest is connected. GitHub publication verified:
PR1 merged at c48fdd3d7415ccf47b973471afd9fe5422c63b41.
Recurring model work remains disabled.

## Completed
- Agentic category metadata and operating kit committed locally.
- Canonical JS baseline rerun: 0/44 sessions, 0/11405 screen points.
- Frozen evaluator, patches and official recordings retain canonical hashes.
- Pinned NetHack source fetched: 16ff59115315917b93185d026aeefea06db9b0f4.
- Portable toolchain installed in a local prefix: micromamba2.9.0,
  Clang18.1.8, Bison, Flex, ncurses; explicit package lock recorded.
- Official patched C recorder built and installed on this hosted Ubuntu24.04
  runtime. No MacBook/VPS or weakened sandbox controls required.
- Linux sysconf installation gap fixed by installing upstream sample config;
  optional unavailable GDB crash-debugging setting omitted in installed copy.
- Tourist(23 steps) and Ranger(25 steps) rerecorded: all screens, cursors,
  keys, RNG and animation fields agree. Both omit one canonical depth
  annotation. Strict whole-step comparison correctly reports failure.
- Empty recording rejected by our comparison gate despite canonical recorder
  helper returning exit0. Environment startup errors are not parity evidence.
- Fresh independent checkout recovered first bootstrap commit from Git bundle;
  canonical fixture integrity passed. Final bundle is refreshed at delivery.
- Ordinary startup Lua dependency verified in actual source.

## Remaining gates
1. Fork exists and is readable through the connected GitHub account. Native
   environment connection is user-confirmed; no environment management or
   cloud-task launch control is exposed in this session.
2. No live project quota adapter or enforceable per-run budget demonstrated.
   Recurring inference stays disabled under the strict20% ceiling.
3. No scheduled cloud coding round trip demonstrated. Current hosted execution
   is verified; that does not establish a persistent unattended dispatcher.
4. Extend oracle calibration to environment-sensitive and multi-segment cases;
   resolve missing metadata separately. Two sessions do not certify all behavior.

First implementation correction: js/rng.js d(n,x) now uses raw core draws and
emits one aggregate d event, matching the patched C function. Test-only C
oracle uses the unchanged source function and actual ISAAC64 implementation:
403 sequences pass for values, log events and next RNG state. All44 public
session metrics are unchanged; score remains0/11405. This helper is not yet
used by the starter's real gameplay path, so no score gain is claimed.
Next engineering work: complete RNG contexts/luck wrappers and input contracts,
then replace the initialization fastforward dependencies with real source logic.
Tests: run through ops/with-toolchain.sh python3 tests/rng-dice-oracle.py.
No agent remains running after a checkpoint unless explicitly recorded.
Model setting Astra High was user-reported; runtime billing/routing unmeasured.
No child-agent or paid API work was launched.
