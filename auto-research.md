Contribute one useful, independently reviewable result to:
https://github.com/rohanarun/matrix-multiplication-sector-barrier

This is a coordinated research sprint with many agents working concurrently.
Work autonomously within the available time, reserving the final 25% for
verification and a clear handoff. Prefer one completed contribution over
several unfinished investigations. Do not assume that a stronger bound exists.

1. ESTABLISH THE CURRENT STATE

Clone or fetch the repository and record your exact base commit.

Read:
- README.md
- proof.tex
- source-manifest.json
- progress/omega_history.json
- tests/

Follow the current main result to its actual construction and checks.
Some older documentation names historical results. Do not treat those
numbers, or claims in open PR titles, as the current accepted result.

The project concerns obstructions to symmetrized sector inequalities from
OpenAI's matrix-multiplication manuscript: explicit abstract profiles that
satisfy the retained constraints yet grow only like a^(4/3) on the diagonal.
Stronger barriers (covering more sector types or proof methods), or a precise
account of where a barrier fails, are better. Rigorous audits, useful tools and
scoped negative results are valuable contributions.

2. ASSIGN YOURSELF A TRACK — DO NOT AUTOMATICALLY PICK THE NEWEST RECORD

Generate a fresh random integer from 0 through 99 using the operating
system's randomness, and record it as your assignment seed:

00–19: Main result: improve one specific step, parameter, constant, or
       certificate of the current refinement.

20–39: Alternative construction: test one different mechanism, template, or
       parameter region for the same target.

40–49: Structural research: investigate one mechanism that changes the
       underlying geometry, counting, or construction template.

50–59: Source interfaces: make one dependency on the upstream manuscript
       explicit, or remove it, with complete accounting.

60–74: Adversarial mathematical audit: examine one specific lemma,
       interface assumption, accounting step, or proposed construction.

75–84: Independent verification or formalization: check one precise
       identity or obligation using a genuinely independent implementation
       or a clearly scoped formal proof.

85–94: Verification engineering: make one costly check faster or more
       reproducible without weakening its mathematical coverage.

95–99: Research consolidation: resolve one concrete discrepancy in claims,
       provenance, dependencies, or previously recorded negative results.
       Avoid cosmetic rewrites.

Within your track, identify three narrow candidate tasks. Inspect relevant
open PRs, the review ledger, prior negative results, and sprint claims.
Choose an underexplored task rather than duplicating the most obvious one.

Use your random seed to diversify the choice of object, parameter region,
method, or proof obligation. A different seed alone does not make a
duplicate experiment useful.

3. CLAIM A NARROW SCOPE

If a pinned sprint coordination issue exists, post one short claim there:

- Track and seed
- Base commit
- Exact object or claim being investigated
- Proposed method or parameter range
- Expected deliverable
- Expected finish time

Check recent claims immediately before posting. If your task is already
claimed, choose another. A second independent audit is welcome when it
uses a meaningfully different method; say so explicitly.

Do not open a separate issue merely to reserve work. If no coordination
issue exists or you lack posting access, record your claim locally and
continue, checking PRs for overlap.

Keep delegated workers within your claimed scope. Do not launch a swarm
that repeats the repository-wide investigation.

4. RUN A BOUNDED EXPERIMENT

Spend at most the first 20% of your time orienting and selecting the task.
Then test a specific hypothesis.

For a proposed mathematical improvement:
- Identify the restriction or expense your mechanism changes.
- Price its optimistic complete cost before a large implementation.
- Include every required helper, source-access operation, frame change,
  copy, restoration, and recursive child.
- Check whether another supplier or assembly constraint becomes binding.
- Stop or revise the idea if even its favorable budget cannot help.

Do not reopen a previously closed search merely with more computation.
Explain what new assumption, mechanism, or search class makes it different.

For an audit:
- Name the precise statement and its dependencies.
- Distinguish a concrete counterexample, missing proof, failed test,
  and failed search. They are different findings.
- Never describe a finite replay as a formal proof of the full theorem.

For performance work:
- Benchmark before and after on the same input.
- Preserve exactness, failure detection and proof-relevant coverage.

One evidence-driven pivot is reasonable. Do not spend the entire session
moving between speculative ideas.

5. VERIFY AND PACKAGE THE RESULT

Use a branch or isolated worktree. Keep upstream/ unchanged.
Avoid unrelated refactors and global regeneration of unrelated artifacts.

Provide:
- A concise statement of what changed or was learned.
- Exact base commit and dependency/source pins.
- One reproducible command and its expected result.
- Exact certificates where appropriate, plus meaningful negative controls.
- Clear scope, inherited assumptions and unresolved obligations.
- Contributor attribution and disclosure of substantial AI assistance.

For a search, record the domain, seed, stopping rule and completed coverage.
"No candidate found" is not an impossibility theorem.

Credit predecessor work, including concurrent contributions that your
result depends on or independently corroborates. Follow repository licenses.

Run the relevant required checks. Avoid repeatedly launching expensive
repository-wide suites or CI for unfinished intermediate commits.

6. HAND OFF ONE REVIEWABLE CONTRIBUTION

Before submitting, refresh PR metadata and check for overlapping work.
If someone got there first, explain what independent evidence, additional
coverage, or distinct improvement your work adds.

If GitHub access is available, submit at most one focused PR. Label its
status accurately: construction, conditional bound, research note,
independent verification, negative result, or tooling improvement.

Research notes are welcome when they contain concrete new evidence.
Do not submit an unsupported speculative essay or claim a new kappa from
an unimplemented cost model.

If you cannot submit, leave a clean patch and a short handoff.
Update your sprint claim once with the result and link.

Do not merge, close others' PRs, or edit the current main result on your own.

Success means useful evidence that another person can check—not necessarily
a bigger headline number.

SUBMITTING RESEARCH TO /auto-research

Put all research in the auto-research/ folder. That covers constructions,
improved bounds, negative and no-gain results, audits, verifications and
tooling. Do not edit or move existing top-level files and folders; scripts and
manifests may pin their paths.

Each top-level folder in auto-research/ is a research track. Before you start,
list the tracks and read their README.md files.

- If your work continues, replays or audits an existing track, add your
  contribution to that track as a new folder:
    auto-research/<track>/<YYYY-MM-DD>-<handle>-<short-slug>/
  Then append one line to the track's README.md index: date, handle, result,
  status and PR number. Do not edit files other contributors committed.

- If no existing track fits, create a new one:
    auto-research/<new-track>/README.md   (goal, open questions, index)
    auto-research/<new-track>/<YYYY-MM-DD>-<handle>-<short-slug>/
  Use a short lowercase slug that names the idea, and link related tracks.

Each contribution folder contains README.md (what was tried, the result, the
exact reproduce command and its scope), RESULT.json, a verify.py or verify.sh
command, MANIFEST.json (sha256 of every file) and NOTICE.md (pinned sources,
credits and AI-assistance disclosure).
