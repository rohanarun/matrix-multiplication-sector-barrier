# Matrix multiplication: a barrier for symmetrized sector inequalities

An independent, AI-generated research draft prepared with Codex. We construct an explicit abstract profile satisfying the retained scalar constraints from OpenAI's matrix-multiplication manuscript, then show that it also survives arbitrary numbers of standard matched sectors with unequal lengths.

**This is a limitation of a specified proof method, not a new matrix-multiplication algorithm, a lower bound on the actual exponent, or a proof that 9/4 is optimal.** The profile is not claimed to be realizable by a tensor character. Mathematical priority, independent review, and formal verification are not claimed.

## Explicit profile

For $a,b\ge1$, put $u=\min(a,b)$ and $v=\max(a,b)$. Define

$$P_*(a,b)=\left(\frac{3u-1}{2}\right)^{1/3}\left(v+\frac{u-1}{2}\right).$$

The proof shows positivity, symmetry, monotonicity, separate concavity, the boundary value $P_*(1,b)=b$, shifted tripling, and the rank envelope at $t=3/4$:

$$P_*(a,3h+a-1)\ge3P_*(a,h),\qquad P_*(a,b)\le(a+b-1)^{4/3}.$$

Yet its diagonal grows only as

$$P_*(a,a)=\left(\frac{3a-1}{2}\right)^{4/3}=\Theta(a^{4/3}).$$

Thus those abstract constraints alone cannot exclude $t=3/4$ or force a larger diagonal power.

## Why unequal and additional standard sectors do not remove this obstruction

Suppose $C(a,B)$ degenerates to $s$ standard polynomial-multiplication blocks $C(a,h_i)$ sharing the first leg, with independent second and third legs. Allow an exchange of those two legs in each block, but no auxiliary output factors. Counting the two spaces forces

$$B\ge\sum_i h_i+\lfloor s/2\rfloor(a-1).$$

Using a common probability vector across the six permuted characters, the source's entropy inequality yields the symmetrized consequence

$$P(a,B)\ge\sum_iP(a,h_i).$$

The profile above satisfies every such consequence. Indeed, writing $d=(a-1)/2$ and $L=((3a-1)/2)^{1/3}$ gives $P_*(a,h)\le L(h+d)$, with equality for $h\ge a$. The needed dominance reduces, after cubing positive quantities, to

$$A(A+2H)^3-H(2A+H)^3=(A-H)^3(A+H)\ge0\qquad(A\ge H).$$

The dimension bound then implies the desired sum inequality. See [proof.tex](proof.tex) for both complete analytic arguments.

The obstruction leaves open new block types, auxiliary factors, stronger tensor identities, and information retained before symmetrization. It does not rule out improving the actual matrix-multiplication exponent.

## Reproduce

Use Python 3.11 or 3.12:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -B run_checks.py
```

GitHub Actions runs the same command on pushes and pull requests. Do not enable Python optimization (`-O` or `PYTHONOPTIMIZE`); certificate assertions must remain active. The runner rejects optimized execution.

The full argument is in [proof.tex](proof.tex), which has been compiled successfully with the Codex document editor. No compiled PDF is bundled. The tests supplement the mathematical argument; they are not a formal proof of the original papers or an independent review.

## What the tests establish

Five tests check the symbolic derivatives and their matching at the diagonal, 10,000 exact rational cube comparisons for tripling and the rank envelope, the dominance identity, finite sector-dimension cases and unequal-length tuples, and a counterexample to incorrectly omitting the additive shift in tripling.

No floating-point cube roots are used. Finite tests supplement the all-parameter analytic proofs; they are not an asymptotic extrapolation or a test of tensor realizability.

## Original source

OpenAI, [*An Upper Bound of 9/4 for the Matrix Multiplication Exponent*](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026), October 2, 2026, at commit [`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). Credit for the tensor constructions, character framework, entropy inequality, and original exponent claim belongs to OpenAI.

[source-manifest.json](source-manifest.json) records the inspected manuscript's hash. Optionally retrieve it with `python -B fetch_sources.py --output upstream`; the tests themselves do not need a network connection once dependencies are installed. This is not an official OpenAI publication.
