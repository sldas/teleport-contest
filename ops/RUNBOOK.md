# Operating runbook

## Admission and quota

The project's allowance ceiling is 20% of the user's total applicable subscription allowance, not 20% of whatever balance happens to remain. Account for every project director, implementation, review and reporting invocation across the relevant short and weekly windows. Prefer a 16% working allocation with 4 percentage points reserved for uncertainty and finishing work, all inside the 20% ceiling.

Before adding a model task, a supported adapter must return fresh project-attributable usage, the applicable limits/reset times, all in-flight work reservations and an enforceable upper bound on the next run. Admission requires `(project_used + inflight_reserved + next_run_bound) / allowance <= 0.20` in every applicable window. Stop issuing tasks when any input is unavailable. The 16% target is an additional conservative operational stop, not proof of a 20% guarantee. Ordinary shell tests do not themselves invoke another model, but their results can consume tokens when processed by an agent.

The kit has NO adapter or platform spending cap configured. A subscription usage dashboard alone may not provide attribution or a run upper bound. Do not scrape authentication tokens or silently switch to metered API usage. If supported hard enforcement cannot be established, report that strict unattended operation under the ceiling is unavailable. This is a capability gate, not a request to relax the ceiling.

## Hosted persistence and dispatch

Use Git commits, native cloud task artifacts and separately persisted run evidence as durable state. A checkout, cache or sleeping process is not durable scheduling infrastructure. Start every run from a recorded commit and end at a checkpoint. Recovery must work in a fresh hosted checkout.

Initially run one writer. This removes the need for cross-host locks. Do not create a permanent manager agent. The director is a bounded task activated at a checkpoint, plateau, dependency change, scheduled review or new contest target. Scripts collect evidence before it runs. Authorized parallel work is added only after two isolated branches demonstrate clean integration and better accepted throughput per allowance. A local SQLite file must not be used as a distributed lock.

Test native scheduled tasks separately from native cloud coding tasks. A timer firing does not establish that it can launch the selected environment/model, publish a code checkpoint, or enforce quota. No production recurrence until one real scheduled edit/test/checkpoint/resume cycle and a budget-stop simulation pass. Preferred infrastructure: Codex native scheduling plus Codex cloud execution and GitHub durable repository. If the dispatch capability is missing, mark it blocked; a GitHub Actions timer alone does not supply a supported subscription-authenticated Codex runner.

## Per-task loop

1. Script prepares a compact evidence packet: SHA, source contracts, relevant failure, score delta, admission result and unresolved assumptions.
2. Director selects the highest-value dependency-unblocking task. It sets scope, acceptance, falsifier, allowed files, cost bound and stopping condition.
3. Worker reads the actual source and authors the implementation directly. Keep changes reviewable; split oversized work at real behavioral boundaries.
4. Evaluate independently with clean canonical fixtures. Run focused checks first, then the regression gate warranted by the change. Preserve traces for the first divergence, not all raw logs in model context.
5. Integrator accepts or rejects on evidence. Commit code, provenance and checkpoint together when possible. Publish only a reviewed candidate through the authorized repository workflow.

A task report records: task_id, base/result SHA, model and reasoning setting actually used, start/end, relevant source paths/functions, hypothesis, files changed, tests/results, public and private-validation deltas, failure class, usage evidence, risks and next action. Missing usage must stay missing; do not populate estimated values as actual billing.

## Provenance

One JSON object per actual contribution in provenance.jsonl, with keys: task_id, commit, target_paths, source_paths, source_functions, origin, model, tests and notes. Useful origin values: llm_authored_gameplay, generated_data, llm_authored_tooling, human_edit, upstream_frozen. Do not put fictitious examples in the ledger. Compute origin summaries separately for gameplay, tables/assets, infrastructure and frozen code. There is no verified official counting formula; never pad lines to obtain a category ratio.

## Correctness and promotion

Maintain three independent views: scored output, PRNG/effect trace, and internal state invariants. Matching RNG does not prove correct hidden state; matching a screen does not prove future behavior. Check numeric semantics, object identity/aliasing, inventory chains, input ordering and persistence. Keep official scoring exact.

Use a development corpus, a disjoint validation corpus and a sealed audit corpus generated with the calibrated C oracle. A held-out case used for debugging becomes development data; replace the audit coverage. Variation should exercise roles, alignments, names, time, options, commands, rare objects, deeper levels and multi-segment storage. Record reproducible seeds. Never deliver reference recordings or seed-specific answer logic in the gameplay engine.

Every accepted batch: inspect the focused checks and regression summary. Full public scoring is required before judged-branch promotion. Architectural candidates may temporarily regress on isolated branches when they have a bounded recovery target and a concrete acceptance gate. Do not require every intermediate commit to maximize score.

## Strategic review without tunnel vision

Review after five accepted batches, two failed hypotheses on one failure, a public-score plateau, a worse generalization gap, growing review/context cost, an upstream rule change or a new phase target. Ask: Which assumption may be false? Is the oracle calibrated? Is this the earliest cause or only a downstream symptom? Which unimplemented subsystem limits unseen sessions? Is the architecture becoming expensive to change? Should this branch be abandoned?

Rank the next tasks by expected generalization gain, dependency unlock, risk reduction and Phase 2 change locality, divided by expected quota and wall time. Preserve some admitted work for broader coverage and architecture checks even when public-score patches look easier. The director updates the charter only when evidence changes strategy and records why.

## Observability and intervention

Start with a generated STATUS.md and compact JSON run summaries; no dashboard service is needed. Show best verified public points/session passes, validation results, latest official hidden score with timestamp, first-divergence clusters, unimplemented reachable functions, regression count, phase-change diff size, budget state, environment readiness, active task and blocked work. Store full traces as bounded artifacts with links and retention, not in prompts or the source tree.

Send no person-directed notifications without explicit authorization. Native task results can provide routine updates. Human intervention is needed for unavailable account connection/control, an irreducible organizer-rule ambiguity, or a requested scope/budget change. Technical failures should first produce bounded retries and a durable blocker report.

## Source and size discipline

Mirror source modules and function names where useful, but use explicit state ownership and a single suspension convention. No arbitrary repository LOC ceiling: this is a large port. Bound task context, change review size, trace retention and public interfaces instead. Lazy-load evidence. Exclude generated logs and recordings from gameplay. Keep Lua-derived level logic source-linked. Avoid broad renames and format churn before the Phase 1 freeze.
