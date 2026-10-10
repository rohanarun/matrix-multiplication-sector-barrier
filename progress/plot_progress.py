"""Draw progress/omega_progress.png from progress/omega_history.json.

Left: the record of upper bounds on the matrix multiplication exponent,
with OpenAI's 9/4 preprint claim highlighted and this repository's
barrier line. Right: the bracket on the least admissible diagonal
constant, which this repository closed. Requires matplotlib.
"""
from datetime import date, datetime
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SURFACE, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'


def parse(d):
    return date.fromisoformat(d)


def main():
    data = json.loads((HERE / 'omega_history.json').read_text())
    recs = data['records']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                         'xtick.color': INK2, 'ytick.color': INK2,
                         'text.color': INK})
    fig = plt.figure(figsize=(16, 6.2), facecolor=SURFACE)
    gs = fig.add_gridspec(1, 3, width_ratios=[2.4, 1, 1], wspace=0.3,
                          left=0.05, right=0.985, top=0.80, bottom=0.15)
    ax = fig.add_subplot(gs[0])
    bx = fig.add_subplot(gs[1])
    cx = fig.add_subplot(gs[2])
    for a in (ax, bx, cx):
        a.set_facecolor(SURFACE)
        a.grid(True, color=GRID, linewidth=0.8)
        a.set_axisbelow(True)
        for side in ('top', 'right'):
            a.spines[side].set_visible(False)

    xs = [parse(r['date']) for r in recs]
    ys = [r['omega'] for r in recs]
    ax.step(xs, ys, where='post', color=BLUE, linewidth=2, zorder=3)
    ax.plot(xs, ys, linestyle='none', marker='o', markersize=5,
            color=BLUE, zorder=4)
    b = data['barrier']
    ax.axhline(b['omega'], color=ORANGE, linewidth=2, linestyle=(0, (5, 3)),
               zorder=2)
    ax.text(parse('1969-06-01'), b['omega'] - 0.012, b['label'],
            color=INK2, fontsize=9, va='top')
    for r in recs:
        if 'label' not in r:
            continue
        x, y = parse(r['date']), r['omega']
        if r.get('highlight'):
            ax.plot([x], [y], marker='o', markersize=11, markerfacecolor=BLUE,
                    markeredgecolor=SURFACE, markeredgewidth=2, zorder=5)
            ax.annotate(r['label'] + '\n' + 'ω ≤ 2.25, Oct 2 2026',
                        (x, y), xytext=(-128, 150), textcoords='offset points',
                        fontsize=10, color=INK, fontweight='bold',
                        arrowprops=dict(arrowstyle='-', color=INK2, lw=0.8))
        else:
            dx, dy = (6, 10) if r['omega'] > 2.4 else (6, 14)
            if r['label'].startswith('AlphaEvolve'):
                dx, dy = (-104, -20)
            ax.annotate(r['label'], (x, y), xytext=(dx, dy),
                        textcoords='offset points', fontsize=9, color=INK2)
    ax.set_ylim(2.2, 2.86)
    ax.set_xlim(parse('1967-01-01'), parse('2029-06-01'))
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylabel('best proven upper bound on ω')
    ax.set_title('Matrix multiplication exponent: record upper bounds',
                 loc='left', fontsize=12, color=INK, pad=22)
    ax.text(0, 1.02, 'Each point is a new record. Lower is faster. '
            'Naive multiplication is ω = 3; the trivial floor is 2.',
            transform=ax.transAxes, fontsize=9, color=INK2)

    pts = data['least_constant_bracket']['points']
    px = [parse(p['date']) for p in pts]
    lo = [p['lower'] for p in pts]
    up = [p['upper'] for p in pts]
    bx.plot(px, lo, color=BLUE, linewidth=2, marker='o', markersize=6,
            label='lower bound (OpenAI growth lemma)', zorder=4)
    ux = [x for x, u in zip(px, up) if u is not None]
    uy = [u for u in up if u is not None]
    bx.plot(ux, uy, color=ORANGE, linewidth=2, marker='o', markersize=6,
            label='upper bound (explicit profile)', zorder=4)
    bx.fill_between(ux, [l for l, u in zip(lo, up) if u is not None], uy,
                    color=ORANGE, alpha=0.12, linewidth=0, zorder=1)
    bx.annotate('P* : 1.7171', (ux[0], uy[0]), xytext=(-62, 6),
                textcoords='offset points', fontsize=9, color=INK2)
    bx.annotate('exact: 3/(2Γ(4/3))\n= 1.67977', (px[-1], lo[-1]),
                xytext=(-96, -36), textcoords='offset points', fontsize=9,
                color=INK2)
    bx.set_ylim(1.66, 1.74)
    bx.set_xlim(parse('2026-10-01'), parse('2026-10-12'))
    bx.set_xticks([parse('2026-10-02'), parse('2026-10-09'), parse('2026-10-10')])
    bx.set_xticklabels(['Oct 2', 'Oct 9', '\nOct 10'])
    bx.set_title('Least diagonal constant', loc='left', fontsize=12,
                 color=INK, pad=22)
    bx.text(0, 1.02, 'min P(a,a)/a^(4/3); bracket closed by PR #2',
            transform=bx.transAxes, fontsize=9, color=INK2)
    bx.legend(loc='upper right', frameon=False, fontsize=8.5)

    sc = data['barrier_scope']['points']
    sx = [datetime.fromisoformat(q['when']) for q in sc]
    sy = [q['count'] for q in sc]
    cx.step(sx, sy, where='post', color=BLUE, linewidth=2, zorder=3)
    cx.plot(sx, sy, linestyle='none', marker='o', markersize=6, color=BLUE,
            zorder=4)
    for q, x, y in zip(sc, sx, sy):
        if y == 0:
            continue
        dy = {2: -36, 3: 0, 4: 8}[y]
        cx.annotate(q['label'], (x, y), xytext=(-10, dy),
                    textcoords='offset points', fontsize=8.5, color=INK2,
                    ha='right')
    cx.set_ylim(-0.3, 5)
    cx.set_yticks([0, 1, 2, 3, 4])
    cx.set_xlim(datetime(2026, 10, 1, 12), datetime(2026, 10, 11, 12))
    cx.set_xticks([datetime(2026, 10, 2), datetime(2026, 10, 9),
                   datetime(2026, 10, 10)])
    cx.set_xticklabels(['Oct 2', 'Oct 9', '\nOct 10'])
    cx.set_title('Barrier scope', loc='left', fontsize=12, color=INK, pad=22)
    cx.text(0, 1.02, 'rule classes of the 9/4 proof shown barriered',
            transform=cx.transAxes, fontsize=9, color=INK2)

    fig.suptitle('Progress on the matrix multiplication exponent and on the '
                 '9/4 barrier of the symmetrized sector method',
                 x=0.05, ha='left', fontsize=14, color=INK, y=0.955)
    fig.text(0.05, 0.025,
             'Sources: published records (Strassen 1969 … Alman et al. 2025, '
             'Dupont et al. 2026); OpenAI, "An Upper Bound of 9/4 for the '
             'Matrix Multiplication Exponent", preprint Oct 2 2026 (claim, '
             'not peer reviewed).\nBarrier and bracket: '
             'github.com/rohanarun/matrix-multiplication-sector-barrier '
             '(the barrier is a limit of one proof method, not a bound on ω).',
             fontsize=8, color=INK2, linespacing=1.5)
    out = HERE / 'omega_progress.png'
    fig.savefig(out, dpi=160, facecolor=SURFACE)
    print('wrote', out)


if __name__ == '__main__':
    main()
