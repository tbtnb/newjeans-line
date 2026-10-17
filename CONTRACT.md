# Development contract

The current design and implementation contracts are [design/ART_DIRECTION.md](design/ART_DIRECTION.md) and [design/IMPLEMENTATION.md](design/IMPLEMENTATION.md). The final renderer uses Babylon.js.

The delivered song list is fixed to the sixteen requested vocal tracks; source audio remains untouched. Runtime data stays in the browser. Public assets and imports must work beneath a GitHub Pages repository path.

The scene API is WorldRenderer(canvas), load(level), render(snapshot, options), resize(), dispose(). Main owns the animation frame loop and Web Audio is the authoritative playback clock. Scene placement must agree with engine path geometry.

Preserve existing work when changing modules. Keep song analysis, deterministic game judgment, model construction, rendering, UI, storage and deployment responsibilities separate. Before publishing changes, run the relevant tests, build, browser journeys, and scene/resource audit.
