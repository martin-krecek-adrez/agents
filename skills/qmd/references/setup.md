# qmd Setup

## Install

```bash
brew install sqlite
bun install -g github:tobi/qmd
```

Ensure bun global bin is in PATH:

```bash
export PATH="$HOME/.bun/bin:$PATH"
```

## Sanity Checks

```bash
qmd --help
qmd --index adrez collection list --json
qmd --index adrez stats --json
```

## Debugging

- Empty query results:
  - Check collections: `qmd --index adrez collection list`
  - Refresh index: `qmd --index adrez update`
  - Refresh embeddings: `qmd --index adrez embed`
- Wrong or stale hits:
  - Confirm source files are in included collection paths.
  - Remove stale collections and re-add correct paths.
