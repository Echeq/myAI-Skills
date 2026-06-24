---
name: ai-release
description: Generate conventional changelogs, bump SemVer versions, create git tags, and publish GitHub releases from git history.
allowed-tools: Read, Write, Bash, Glob, Grep
triggers:
  - "@ai-release"
  - "@ai-release --changelog"
  - "@ai-release --bump"
  - "@ai-release --release"
  - "@ai-release --tag"
---

# ROLE: Release Manager

You manage releases from git history. Read commits since last tag, parse conventional commits, generate changelogs, bump versions, and create releases.

## Quick Start

| Mode | Trigger | What happens |
|---|---|---|
| Interactive | `@ai-release` | Show commits → suggest version → generate changelog → confirm → tag → optional release |
| Changelog | `@ai-release --changelog` | Generate `CHANGELOG.md` from git log since last tag |
| Bump | `@ai-release --bump patch` | Version bump + git tag (no changelog, no release) |
| Full release | `@ai-release --release` | Changelog + bump + tag + GitHub release |
| List tags | `@ai-release --tag` | Show existing tags with dates |

## Workflow

### 1. Read git history

```
# Get latest tag
git describe --tags --abbrev=0 2>$null

# Commits since that tag
git log <tag>..HEAD --oneline

# Full conventional commit parsing
git log <tag>..HEAD --format="%s%n%b---"
```

If no tags exist, use `git log --oneline` from the beginning.

### 2. Parse conventional commits

| Type | Section in changelog | Version impact |
|---|---|---|
| `feat` | Features | minor |
| `fix` | Bug Fixes | patch |
| `perf` | Performance | patch |
| `BREAKING CHANGE` or `!` | ⚠ BREAKING CHANGES | major |
| `docs`, `style`, `refactor`, `test`, `chore` | Other Changes | none |

### 3. Suggest version bump

Based on commits since last tag:
- Any breaking change → major (X.0.0)
- Any feat → minor (0.X.0)
- Only fixes/refactors/docs → patch (0.0.X)
- No changes → warn "No new commits since last tag"

Show: "Suggested bump: patch (0.0.X) based on 3 fixes and 1 refactor."

### 4. Generate changelog

```
# CHANGELOG.md

## [0.2.0] - 2026-06-24

### ⚠ BREAKING CHANGES

- `login()` now returns Promise instead of callback (#42)

### Features

- add rate limiting middleware (#45)
- expose user preferences API (#40)

### Bug Fixes

- fix race condition in token refresh (#41)
- correct null pointer on empty state (#38)
```

### 5. Execute

After user confirms:

```
# Bump version
git tag v<version>

# Generate CHANGELOG.md
# Save to: CHANGELOG.md

# GitHub release (if --release)
gh release create v<version> --title "v<version>" --notes-file CHANGELOG.md
```

### Bump modes

| Subcommand | What it does |
|---|---|
| `--bump major` | Bump X.0.0 + tag |
| `--bump minor` | Bump 0.X.0 + tag |
| `--bump patch` | Bump 0.0.X + tag |
| `--bump` (no value) | Suggest + ask |

## Error Handling

| Issue | Action |
|---|---|
| No tags exist | Start from first commit. Suggest v0.1.0 |
| No conventional commits | Show raw git log. Suggest patch bump manually |
| Not a git repo | Abort. Run `git init` first |
| `gh` not found for release | Generate changelog + tag only. Print `gh release create` command for manual use |
| Dirty working tree | Warn: "Uncommitted changes. Commit or stash before release." |
| Tag already exists | Suggest: "v0.2.0 exists. Try v0.2.1 or --force?" |
