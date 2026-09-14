# Dice wrapper correction

Hypothesis: summing rnd(x) produces the correct numeric distribution but emits
per-die log events that differ from patched C d(n,x). The native source uses
RND(x) directly, adds n, and logs one aggregate event, including d(0,0).
Falsifier: compare values, complete helper logs, and subsequent raw RNG values
against unchanged C d() compiled with actual source ISAAC64.

Before change: native test failed at seed0 because d(0,0)=0 was missing.
After change:403 sequences pass (13 seeds ×31 argument cases), including
zero dice, one-sided dice, multiple dice and64-bit seed boundaries. Every
public session's score/RNG/cursor/error metrics remain identical to baseline.

Scope: valid C calls with nonnegative n, positive sides unless n=0, and no C
signed-int result overflow. Invalid/overflowing calls are not certified.
Display RNG, luck wrappers and Lua-specific dice semantics remain separate
work; existing aliases are retained, not independently certified by this test.
The test copies source C into a temporary native harness, never generates
executable gameplay JavaScript, and leaves canonical fixtures untouched.
