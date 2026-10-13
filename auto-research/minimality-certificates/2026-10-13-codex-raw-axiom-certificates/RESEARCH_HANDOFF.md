# Research handoff

## Result

One independently checkable contribution: raw-axiom certificates for the lower-bound direction of the accepted least-profile theorem. The saved example proves `P(7,11) >= 193648/6561` with 96 rationally weighted rows. A separate checker expands boundary, concavity and shifted-tripling axioms without evaluating an admissible profile. The README derives the recipe for all positive integer targets; executable coverage is finite and explicitly recorded in RESULT.json.

Dependency accounting: every generated certificate uses only the boundary equality `P(1,1)=1`. Thus the all-integer recipe also shows that the full boundary family is unnecessary for the lower-bound implication. It does not remove the boundary conditions from the separate admissibility claim.

Base commit: `0b09d3616da31d8750366747d7821d70ae6d1b90`. Branch: `research/seed75-minimality-certificates`. Assignment seed 75. No research-track folder, review ledger or negative-result registry existed at this base. No open or pinned coordination issue was available, so CLAIM.md records the scope locally. Open PR #3 is separate leg-resolved work and is not used as an assumption.

## Commands and evidence

- `python3 -B run_checks.py`: baseline 14 tests passed on system Python 3.9.6 / SymPy 1.14.0. This first check was supplemental because the repository requests 3.11 or 3.12.
- `.venv/bin/python -B run_checks.py`: all 14 baseline tests passed on the supported Python 3.12 environment with SymPy 1.14.0 and mpmath 1.3.0.
- `.venv/bin/python -B auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/verify.py`: PASS, 149 certificates, maximum 975 rows, 8 negative controls, saved certificate 96 rows.
- `.venv/bin/python -O -B auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/verify.py`: PASS with identical counts; the same controls remain enabled under optimization. Unlike the repository runner, the new checker uses explicit exceptions rather than assertions.
- `.venv/bin/python -B auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/check.py auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/certificate.json`: PASS, independently checked the saved exact bound.
- Additional exact witness evaluation found all 96 saved raw rows attain equality on `P_min`. Runtime used for final checks: Python 3.12.14. `git diff --check` passed.

## Failures and lessons

- No proposed stronger bound was searched for. There is no failed-search or impossibility claim.
- The false unshifted-tripling assertion fails concretely: `P_min(2,6)=26/3 < 10`. Expected behavior: retain the additive `a-1` in every raw tripling row; never infer an unshifted inequality.
- Without the boundary normalization the zero profile satisfies the remaining axioms. Expected behavior: a positive lower-bound certificate must account for a normalization equality, not silently assume positivity.
- Malformed certificates must fail on residual coefficients, invalid domains or negative inequality multipliers. A numerical replay on a single model is not sufficient evidence of the raw-axiom implication. This expectation motivated the independent coefficient checker and its adversarial controls.
- Fetching in the supplied checkout failed because its `.git/FETCH_HEAD` is read-only under the sandbox. The authorized independent clone in `Runtime/tmp/sector-seed75` succeeded; the supplied checkout and its work were preserved.
- Python 3.12 initially lacked SymPy. A workspace-local virtual environment and workspace-local pip cache resolved this; no global dependency installation was used.
- The first pinned-issue GraphQL query used the wrong schema shape and failed; the corrected `nodes { issue { ... } }` query returned no pinned issues. An error was not interpreted as an empty successful result.

## Review scope and next steps

Review the three displayed coefficient identities and the checker's raw axiom definitions. Finite certificates are exact implications under the declared axioms; they are not formal verification of the full tensor theorem. Remaining external obligations are human review and maintainer acceptance. The upstream manuscript hash is inherited from the source manifest, not independently fetched in this run. There is no new omega bound and no realizability claim.

Stop after packaging this one contribution. Further experiments are unnecessary to meet the current request; smaller certificates or axiom necessity are separate possible follow-ups. No delegated agents, paid services, intensive search or global artifact regeneration were used.
