# ai-release

Generate conventional changelogs, bump SemVer versions, create git tags, and publish GitHub releases from git history.

> **Trigger:** `@ai-release` | `@ai-release --changelog` | `@ai-release --bump` | `@ai-release --release` | `@ai-release --tag`

## Quick Start

1. Type `@ai-release` for interactive release management.
2. The skill reads commits since last tag and parses conventional commit types.
3. A version bump is suggested based on the commits (major/minor/patch).
4. Confirm. The changelog is generated and tag is created.
5. Optionally, a GitHub release is published.

**Example:** `@ai-release` → reads 12 commits since v0.1.0 → suggests minor (0.2.0) based on 2 feats → confirm → `CHANGELOG.md` generated + tag `v0.2.0` created.

**Example (full):** `@ai-release --release` → changelog + bump + `git tag` + `gh release create` in one command.

## Description

Manages the full release lifecycle from git history. Reads commits since the last tag using `git describe`, parses conventional commit format (`feat:`, `fix:`, `BREAKING CHANGE`), suggests an appropriate SemVer bump, generates `CHANGELOG.md`, creates a git tag, and optionally publishes a GitHub release via `gh`.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-release` | Interactive: show commits, suggest version, confirm, tag |
| `@ai-release --changelog` | Generate `CHANGELOG.md` only |
| `@ai-release --bump <level>` | Bump version + tag (level: major, minor, patch) |
| `@ai-release --release` | Full pipeline: changelog + bump + tag + GitHub release |
| `@ai-release --tag` | List existing tags |

## Configuration

| Setting | Default | Notes |
| :--- | :--- | :--- |
| Changelog file | `CHANGELOG.md` | Overwritten each release (append mode optional) |
| Tag format | `v<version>` | e.g. `v0.2.0` |
| GitHub release | via `gh` | Falls back to tag-only if `gh` not found |

> [!NOTE]
> Conventional commit format required for automatic version suggestion: `type(scope): description`. Non-conventional commits are listed under "Other Changes".
> 
> The release is local-only unless `--release` is used. Use `git push --tags` to publish tags to remote.

> [!TIP]
> Use `@ai-commit` before `@ai-release` to ensure all changes are committed and ready for release.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
