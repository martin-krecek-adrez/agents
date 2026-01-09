# Agent Configuration

Configuration for Codex CLI usage.

## Setup

### [Codex](https://developers.openai.com/codex)

Copy skills (Codex [ignores symlinked directories](https://developers.openai.com/codex/skills/create-skill#skill-doesnt-appear))

```bash
ln -sf {baseDir}/AGENTS.md ~/.codex/AGENTS.md
cp -r {baseDir}/skills/ ~/.codex/skills/
```

See [Skills](https://developers.openai.com/codex/skills) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) for details.

## Skills

This repo keeps a minimal set of skills.

Current skills:
- beads
- compare-tech
- write-commit
- write-docs

## Credits

- michalvavra for the original structure
