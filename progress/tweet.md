# Tweet (ELI25) for this update

**Thread, post 1/4**

OpenAI's Oct 2 preprint claims matrix multiplication in n^2.25 time (the record had been stuck near n^2.371 for 35 years). Their proof boils down to four simple rules a hidden "profile" function P(a,b) must obey. Last week I showed those four rules can't push below 2.25. Today: the rules have a single *smallest* profile, and I found its exact formula. 🧵

**2/4**

Think of the four rules as a floor you're building on. Any function obeying them must be at least as big as

P_min(a,b) = H_u · (v + (u−1)/2),  H_u = ∏_{m<u} (1 + 1/(3m)),

where u, v are the smaller/larger of a, b. And P_min obeys all four rules itself. So it is *the* floor: nothing admissible sits under it, anywhere.

**3/4**

Why it matters: OpenAI's key lemma says the diagonal P(a,a) must grow like a^{4/3}, which is exactly what forces ω ≤ 9/4. The least profile shows that lemma is tight at every single a, not just in the exponent — the best possible constant is 3/(2Γ(4/3)) ≈ 1.67977, and P_min hits it. My earlier barrier profile was ~2.2% too big; the gap is now closed (chart).

**4/4**

What this is NOT: a new algorithm, a better exponent, or a claim that 9/4 is optimal. It's a map of the limits of one proof technique. If you want to beat 9/4 with this method, you need a new inequality that P_min violates — now there's an exact object to test against. Proofs + exact rational checks: github.com/rohanarun/matrix-multiplication-sector-barrier

---

**Single-post version (≤280 chars)**

OpenAI's 9/4 matrix-mult proof uses 4 rules on a profile P(a,b). Those rules have a unique smallest solution, and it has a closed form: H_u·(v+(u−1)/2), H_u=∏(1+1/3m). It makes OpenAI's growth lemma sharp at every a (constant 3/(2Γ(4/3))). Barrier at 9/4 is exact. Proof+checks in repo.
