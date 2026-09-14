# Execution charter — revision 2

Goal: top agentic-category performance through faithful directly LLM-authored
JavaScript, robust hidden-case generalization, and localized Phase 2 adaptation.
Contest-first: build no general agent platform unless an immediate task needs it.
Constraints: hosted execution, no Mac/VPS dependency, <=20% project quota, no paid
fallback. Target 16% to reserve uncertainty inside the ceiling.

Architecture: hosted director chooses outcomes; deterministic scripts prepare
source packets, tests and evidence; workers author bounded changes; independent
evaluation precedes a single integration lane. Strategy review at milestone,
plateau, generalization regression, fixture change, or a material resource change.
Use compact durable Git state; traces are separate durable artifacts. A local
SQLite DB is a per-batch convenience, not cross-host locking.

The old transpiler and VM proposals are superseded. The intended production
method is direct LLM authorship of substantially all nontrivial gameplay. The
contest's published majority threshold is not a detailed counting formula.
Provenance is evidence of the method, not an invented official certification.

Internal deadline: November 26, 2026 before Phase 1's November 28, 4 PM Pacific
cutoff. Phase 2 target: November 30; internal final freeze December 28 before the
December 30, 4 PM Pacific cutoff. Exact phase-2 penalty remains unpublished.

Default worker: Sol, standard speed; narrow extraction/utilities may use Luna;
Astra handles expensive ambiguity when expected retry savings justify it.
Resolve actual model availability in the hosted runtime, log what really ran,
and do not silently upgrade or expand inference when a selected model fails.
