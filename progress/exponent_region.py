"""Map the exponent triples (p_X, p_Y, p_Z) with p_X+p_Y+p_Z = 9/4 that survive
the leg-resolved necessary conditions of proof.tex Section 5 (tripling at
every (a, h) with the monotone lower bounds, before symmetrization).

Writes progress/exponent_region.png. Requires numpy and matplotlib.
"""
from itertools import permutations
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SURFACE, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
BLUE, ORANGE = '#2a78d6', '#eb6834'
S = 9 / 4


def phi(p, vals):
    if p == 0:
        return max(vals)
    return sum(v ** (1 / p) for v in vals) ** p


def survives(p, amax=40, hmax=12):
    """Necessary condition: for every placement (shared leg s, second-input
    leg r, third leg u), every a, h: the rank bound on C(a,3h+a-1) must
    dominate the Hoelder form of tripling with the monotone lower bounds
    ell(a,h) >= max(a^{p_r}, h^{p_s}) and ell'(a,h) >= max(a^{p_u}, h^{p_s})."""
    for s, r, u in permutations(range(3)):
        ps, pr, pu = p[s], p[r], p[u]
        for a in range(1, amax + 1):
            for h in range(1, hmax + 1):
                m1 = max(a ** pr, h ** ps)
                m2 = max(a ** pu, h ** ps)
                if 3 * h + 2 * a - 2 < phi(ps, [m1, m1, m2]) - 1e-12:
                    return False
    return True


def main():
    n = 161
    xs = np.linspace(0, 1, n)
    grid = np.full((n, n), np.nan)
    for i, px in enumerate(xs):
        for j, py in enumerate(xs):
            pz = S - px - py
            if pz < -1e-12 or pz > 1 + 1e-12:
                continue
            grid[j, i] = 1.0 if survives((px, py, max(0.0, min(1.0, pz)))) else 0.0
    surv = np.count_nonzero(grid == 1.0)
    tot = np.count_nonzero(~np.isnan(grid))
    print(f'{surv}/{tot} grid points on the 9/4 slice survive ({100*surv/tot:.1f}%)')

    fig, ax = plt.subplots(figsize=(6.4, 6.0), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    cmap = matplotlib.colors.ListedColormap(['#f6d9cc', '#cfe0f6'])
    ax.imshow(grid, origin='lower', extent=(0, 1, 0, 1), cmap=cmap, vmin=0,
              vmax=1, interpolation='nearest')
    ax.plot([0.25, 1], [1, 0.25], color=INK2, lw=0.8)
    ax.plot([0.25, 1], [1, 1], color=INK2, lw=0.8)
    ax.plot([1, 1], [0.25, 1], color=INK2, lw=0.8)
    ax.plot([0.75], [0.75], marker='o', markersize=9, color=BLUE,
            markeredgecolor=SURFACE, markeredgewidth=2, zorder=5)
    ax.annotate('symmetric (3/4, 3/4, 3/4):\nthe P_min solution', (0.75, 0.75),
                xytext=(-150, -52), textcoords='offset points', fontsize=9,
                color=INK, arrowprops=dict(arrowstyle='-', color=INK2, lw=0.8))
    ax.plot([1], [1], marker='x', markersize=8, color=ORANGE, mew=2, zorder=5)
    ax.annotate('(1, 1, 1/4): excluded\n(two exponents 1 force the third to 0)',
                (1, 1), xytext=(-205, -34), textcoords='offset points',
                fontsize=9, color=INK,
                arrowprops=dict(arrowstyle='-', color=INK2, lw=0.8))
    ax.text(0.27, 0.27, 'blue: survives the leg-resolved\nnecessary conditions\n'
            'peach: excluded before symmetrization', fontsize=9, color=INK2)
    ax.set_xlim(0.2, 1.03)
    ax.set_ylim(0.2, 1.03)
    ax.set_xlabel('p_X')
    ax.set_ylabel('p_Y')
    ax.set_title('Exponent triples on the slice p_X + p_Y + p_Z = 9/4',
                 loc='left', fontsize=11, color=INK, pad=12)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    fig.text(0.02, 0.015, 'Necessary conditions only: tripling at all (a,h) ≤ (40,12) with '
             'monotone lower bounds, six placements (proof.tex, Section 5).',
             fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out = HERE / 'exponent_region.png'
    fig.savefig(out, dpi=160, facecolor=SURFACE)
    print('wrote', out)


if __name__ == '__main__':
    main()
