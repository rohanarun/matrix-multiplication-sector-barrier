# Independent raw-axiom certificates for minimality

The lower-bound half of the accepted least-profile theorem can be certified by a **finite nonnegative rational combination of raw axioms for every positive integer target**. This contribution gives the certificate recipe and a separate coefficient checker, plus a saved certificate proving

\[
P(7,11)\ge\frac{193648}{6561}.
\]

The existing test `test_minimality_chain_on_star_profile` evaluates a candidate profile and its recursion. Here the checker instead treats every profile value as a free formal variable and verifies that raw axiom rows cancel to the claimed bound. It never imports the repository's profile functions or the generator. This independently checks the algebraic implication, rather than testing another numerical instance of an admissible profile.

Base: `0b09d3616da31d8750366747d7821d70ae6d1b90`. Track assignment: OS randomness seed **75**, independent verification. This is a verification contribution, not a stronger bound or a new construction. No result from open PR #3 is assumed.

## Reproduce

From the repository root, with Python 3.11 or 3.12 (the contribution itself needs only the standard library):

```sh
python3 -B auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/verify.py
```

Expected final line:

```text
PASS {"certificates_checked": 149, "max_rows": 975, "negative_controls": 8, "saved_certificate_rows": 96}
```

The frozen domain is every ordered pair in `[1,12]^2`, plus `(2,75)`, `(75,2)`, `(25,25)`, `(7,31)`, `(31,7)`. Symmetry means transposed targets deliberately share a certificate. Seed 75 shuffles verification order; all cases are completed, and the stopping rule is exhaustion of this declared domain. The asymmetric pair involving 75 uses the assignment seed to select a longer propagation case. This is a finite verification domain, not a search for an improved bound.

To check only the saved proof object, independently of the generator, run:

```sh
python3 -B auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/check.py auto-research/minimality-certificates/2026-10-13-codex-raw-axiom-certificates/certificate.json
```

Expected: `PASS {"a": 7, "b": 11, "lower": "193648/6561", "rows": 96}`. `build.py a b` prints a certificate for any requested positive integers; generating very large targets is not part of this bounded run.

## Axioms and the certificate recipe

Work over real-valued functions on positive integer pairs. Symmetry is implemented by identifying `P(x,y)` and `P(y,x)`. The only allowed raw rows are

\[
E_n=P(1,n)-n=0,\qquad
C_{a,k}=2P(a,k)-P(a,k-1)-P(a,k+1)\ge0\quad(k\ge2),
\]
\[
T_{a,h}=P(a,3h+a-1)-3P(a,h)\ge0.
\]

Boundary equalities may have arbitrary rational multipliers; all inequality multipliers must be nonnegative. The generated certificates use **only `E_1`**, so the lower-bound implication already follows from the single normalization `P(1,1)=1`, symmetry, concavity and shifted tripling. The rest of the boundary family is unnecessary for this direction. This does not assert that those weaker assumptions force boundary equality or establish admissibility. No positivity, monotonicity, rank envelope, Gamma function, sector inequality, tensor operation or limiting argument is used.

Write `D_a=P(a,a)` and `Delta_h=P(a,h+1)-P(a,h)` with the first argument fixed at `a`. For `h>=a` put `K=3h+a-1`. Telescoping the second differences gives the raw identity

\[
S_{a,h}:=T_{a,h}
 +\sum_{k=h+1}^{K-1}(K-k)C_{a,k}
 +2\sum_{k=a+1}^{h}(k-a)C_{a,k}
 =(3a-1)\Delta_h-2D_a.
\]

Indeed, the first sum is `(K-h) Delta_h - (P(a,K)-P(a,h))`, and the second sum before its factor 2 is `P(a,h)-D_a-(h-a) Delta_h`. Adding `T` leaves the displayed right side. Empty sums vanish. All coefficients in both sums are nonnegative, so `S>=0` follows for every integer `h>=a` without importing the slope lemma as an axiom.

For `a>=2`, symmetry gives the next exact identity:

\[
R_a:=\frac{S_{a-1,a-1}}{3a-4}+C_{a,a}
        +\frac{S_{a,a}}{3a-1}
 =\alpha_aD_a-\beta_aD_{a-1},
\quad
\alpha_a=\frac{3a-3}{3a-1},\quad
\beta_a=\frac{3a-2}{3a-4}.
\]

Both coefficients are positive. Starting from the equality certificate `D_1-1=E_1`, recursively form

\[
D_a-d_a=\frac{R_a}{\alpha_a}
       +\frac{\beta_a}{\alpha_a}(D_{a-1}-d_{a-1}),
\qquad d_1=1,\qquad d_a=\frac{\beta_a}{\alpha_a}d_{a-1}.
\]

Multiplication of this recursion yields

\[
d_a=\frac{3a-1}{2}\prod_{m=1}^{a-1}\frac{3m+1}{3m}.
\]

Finally, for `b>=a`, set `F=1+2(b-a)/(3a-1)>0`. Then

\[
P(a,b)-F d_a
 =\sum_{h=a}^{b-1}\frac{S_{a,h}}{3a-1}+F(D_a-d_a).
\]

Here `F d_a` is exactly the accepted `P_min(a,b)`. Symmetry covers `b<a`. These formulas constitute an ordinary all-integer analytic proof of the certificate recipe. Every target uses finitely many raw rows; no coordinate exceeds `max(4a-1,3b+a-4)` after ordering `a<=b`. The code is an exact finite implementation and checker, **not a proof-assistant formalization** of that all-integer argument.

## Verification and failure detection

`build.py` works only with axiom weights and the diagonal lower-bound recursion. `check.py` independently expands raw axioms into sparse coefficient vectors over `Fraction`, checks nonnegative inequality weights and valid positive-integer domains, and requires exact cancellation to `P(a,b)-lower`. It deliberately accepts any correctly certified lower bound; `verify.py` separately checks equality with the claimed least-profile value using the direct product formula.

Eight controls reject an inflated target, a negative tripling multiplier, an omitted concavity row, an altered boundary index, an altered tripling index, an out-of-domain concavity row, the false unshifted-tripling assertion, and omission of boundary normalization. The unshifted assertion has the exact counterexample `P_min(2,6)=26/3 < 3 P_min(2,2)=10`. This is a concrete failure, not merely an unsuccessful search. Removing boundary normalization also admits the zero profile, which cannot imply any positive target bound. All checker requirements use explicit exceptions and remain active under Python optimization.

`MANIFEST.json` hashes every other contribution file. It excludes itself to avoid a self-referential digest; the Git commit pins the manifest. It excludes ephemeral `__pycache__` directories, and reproduction uses `-B`.

## Scope and remaining obligations

These certificates corroborate the lower-bound implication in merged PR #2. They do not independently establish admissibility of `P_min`, the analytic asymptotic constant, any upstream tensor/entropy statement, a stronger exponent barrier, or realizability by tensor characters. Admissibility remains supplied by the accepted analytic proof and existing tests. Human review and maintainer acceptance remain separate from a local or CI pass.
