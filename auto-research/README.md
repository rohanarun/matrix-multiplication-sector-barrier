# auto-research/

Put all research for this repository here. Agent instructions are in [../auto-research.md](../auto-research.md).

## Layout: tracks and contributions

Each top-level folder is a **research track**, meaning one line of work. Each contribution is a dated subfolder inside a track:

```
auto-research/<track>/                                  README.md: goal, open questions, contribution index
auto-research/<track>/<YYYY-MM-DD>-<handle>-<short-slug>/
```

- **Existing track:** if your work extends, replays or audits a track, add a dated subfolder there and append a line to the track's README index. Do not edit other contributors' files.
- **New track:** create one only if nothing fits. Use a short lowercase slug that names the idea, write its README, and link related tracks.

Required files in each contribution folder: `README.md` (what was tried, the result, the exact reproduce command and its scope), `RESULT.json`, `verify.py` or `verify.sh`, `MANIFEST.json` (sha256 of every file) and `NOTICE.md` (pinned sources, credits and AI-assistance disclosure).
