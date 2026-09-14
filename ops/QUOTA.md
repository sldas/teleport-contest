# Quota lookup and enforcement investigation

Status: real lookup route identified and tested; hosted authentication blocks
live numbers. Strict20% project enforcement is not established.

## Observed in this runtime

- Codex CLI exists at /opt/codex/bin/codex (0.154.0-alpha.3), although not on PATH.
  Earlier PATH-only checks missed it.
- Local daemon proxy was unavailable. A fresh stdio app-server initialized
  successfully without starting a model turn.
- account/read returned ChatGPT authentication with an unknown plan type.
- account/rateLimits/read reached the service but returned401: current managed
  authentication was rejected. No credential files were read or copied; no
  login/logout, token refresh, reset credit, or paid API action was performed.
- The cloud browser was logged out. Browser sign-in is a separate supported
  way to inspect the usage dashboard; it does not authenticate a child CLI.
- The installed protocol exposes thread/goal/set tokenBudget. Its schema
  confirms a token budget field, not a project percentage ceiling.

Run `python3 ops/quota_probe.py` in an authenticated hosted environment. The
probe uses only initialization and the documented quota read. It suppresses
identity/credential details, emits all returned primary/secondary buckets,
rejects missing/expired data, and exits2 when unavailable. This is a read-only
probe, not a deployed scheduler or account-wide enforcement mechanism. All
outputs explicitly keep recurring_dispatch_allowed=false.

Eight synthetic parser tests pass. A real probe returned authentication_rejected.
Do not publish live personal quota snapshots to this public repository.

## What each control actually gives us

| Control | Gives us | Does not establish |
|---|---|---|
| account/rateLimits/read | Account usage percentages and reset windows | Which project spent the allowance |
| account/usage/read | Token activity summaries | Subscription allowance billing conversion |
| thread goal tokenBudget | Native goal token budgeting | Hard20% account/project ceiling or bounded overshoot |
| Budget controller | Admission decisions and stop requests | Refund of already consumed tokens or instant cancellation |
| Prompt instruction | Agent guidance | Enforceable billing limit |

Official sources:
- https://learn.chatgpt.com/docs/app-server
- https://learn.chatgpt.com/docs/pricing

The pricing documentation says an active turn may continue after the account
reaches its usage limit. Even the account's own exhaustion boundary is therefore
not proof that our20% allocation can be enforced with zero overshoot.

## Proposed conservative controller, once authenticated

1. Keep a private ledger for each metered bucket/window: baseline, last sample,
   project upper-bound usage, in-flight reservations and sample freshness.
   Persist it outside the public gameplay repository.
2. Serialize model work initially. Charge all positive account usage during a
   project batch to this project if attribution is unavailable. This can overcount
   unrelated usage; it must not be described as accurate attribution. Measurement
   lag/precision must be bounded before this is a proven upper bound.
3. A changed reset timestamp, stale sample, missing bucket or auth failure closes
   admission. Reconcile the prior window before starting a new one. Never interpret
   a reset as negative spending or silently discard an unfinished reservation.
4. Target16% as an early stop; reserve4 percentage points inside the20% ceiling.
   Native goal token budgets can limit runaway continuation. Updating an existing
   goal must preserve its usage history; changing its objective resets accounting.
5. Poll with ordinary code, not repeated model wake-ups, and request interruption
   when the early-stop threshold is reached. No purchases, automatic credit resets,
   parallel batches or unmetered retries.
6. Claim a hard guarantee only if a supported provider/controller gives a verified
   bound for next-run consumption, measurement lag and cancellation overshoot, or
   provides a native project spending cap. The current surfaces do not establish
   those bounds. An empirical safety margin is useful but is not a proof.

## Immediate continuation

Use secure browser sign-in to obtain a first visible account usage snapshot.
Then test the same read-only CLI probe in the actual connected repository cloud
environment using its supported authentication. Do not export browser cookies or
ChatGPT tokens into the container. If that environment exposes only task-scoped
credentials, a supported host-side quota capability is required.

Earlier project usage is unmeasured. A new baseline cannot retroactively certify
that earlier work stayed within20%. Start auditable accounting at a known window
boundary; keep historical consumption explicitly unknown.

Until both lookup and enforceable admission are established, recurrence stays
disabled. No amount of prompt wording turns this investigated limitation into a
working hard cap. Do not ask for credentials in chat.
