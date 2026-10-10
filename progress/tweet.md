# Tweets (ELI25)

## PR #3 — the barrier survives before symmetrization (Oct 10 2026)

**1/4** OpenAI's 9/4 matrix-multiplication proof actually has *six* copies of every inequality — one per way of labelling a tensor's three legs — and then averages them into one "profile". Averaging loses information. Natural question: could the un-averaged, leg-by-leg version push the exponent below 9/4? 🧵

**2/4** Answer: no. Once you optimize the paper's entropy inequality over its free probability vector, each leg-by-leg rule becomes a clean Hölder-type inequality, and the whole system turns out to be *convex* in log-coordinates. Two explicit solutions — the three classic "flattening" characters (3t = 2) and the symmetric P_min assignment (3t = 9/4) — then give solutions at every 3t in between.

**3/4** The fun part: the leg-by-leg system isn't empty talk. It proves a small structural fact about *every* tensor character: if two of its three dot-product exponents are 1, the third must be 0. So on the 9/4 slice, exponent shapes like (1, 1, 1/4) are impossible — only the corners of the triangle get cut off (map in the repo). It constrains the shape of the exponent, never its sum.

**4/4** Scoreboard for the barrier: scalar rules ✔ arbitrary matched sectors ✔ least profile / sharp growth lemma ✔ leg-resolved (pre-symmetrization) ✔. Beating 9/4 with this method now needs a genuinely new tensor inequality. Proofs + exact checks (19 tests): github.com/rohanarun/matrix-multiplication-sector-barrier

**Single post:** OpenAI's 9/4 proof averages 6 leg-labelled inequalities into one profile. The un-averaged system is convex in log-coords, and explicit solutions (flattenings at 3t=2, P_min at 3t=9/4) show it can't beat 9/4 either. Bonus: any character with two exponents =1 has the third =0.

## PR #2 — the least admissible profile (Oct 10 2026)

**1/4** OpenAI's Oct 2 preprint claims matrix multiplication in n^2.25 time (the record had been stuck near n^2.371 for 35 years). Their proof boils down to four simple rules a hidden "profile" function P(a,b) must obey. Last week I showed those four rules can't push below 2.25. Today: the rules have a single *smallest* profile, and I found its exact formula. 🧵

**2/4** Think of the four rules as a floor you're building on. Any function obeying them must be at least as big as P_min(a,b) = H_u · (v + (u−1)/2), H_u = ∏_{m<u} (1 + 1/(3m)), where u, v are the smaller/larger of a, b. And P_min obeys all four rules itself. So it is *the* floor: nothing admissible sits under it, anywhere.

**3/4** Why it matters: OpenAI's key lemma says the diagonal P(a,a) must grow like a^{4/3}, which is exactly what forces ω ≤ 9/4. The least profile shows that lemma is tight at every single a, not just in the exponent — the best possible constant is 3/(2Γ(4/3)) ≈ 1.67977, and P_min hits it. My earlier barrier profile was ~2.2% too big; the gap is now closed (chart).

**4/4** What this is NOT: a new algorithm, a better exponent, or a claim that 9/4 is optimal. It's a map of the limits of one proof technique. If you want to beat 9/4 with this method, you need a new inequality that P_min violates — now there's an exact object to test against. Proofs + exact rational checks: github.com/rohanarun/matrix-multiplication-sector-barrier

**Single post:** OpenAI's 9/4 matrix-mult proof uses 4 rules on a profile P(a,b). Those rules have a unique smallest solution, and it has a closed form: H_u·(v+(u−1)/2), H_u=∏(1+1/3m). It makes OpenAI's growth lemma sharp at every a (constant 3/(2Γ(4/3))). Barrier at 9/4 is exact. Proof+checks in repo.
