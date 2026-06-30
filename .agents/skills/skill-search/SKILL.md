---
name: skill-search
description: >-
  Browse, install, and update skills from the Echeq/myAI-Skills GitHub
  repository. Acts as a package manager for OpenCode skills.
allowed-tools: Read, Write, Bash, Glob, Grep
triggers:
  - "@skill-search"
  - "@skill-search --list"
  - "@skill-search --search"
  - "@skill-search --install"
  - "@skill-search --update"
  - "@skill-search --info"
---

# Skill Search

Package manager for OpenCode skills. Fetches skills from the
[Echeq/myAI-Skills](https://github.com/Echeq/myAI-Skills) GitHub repository
and installs them locally into `.agents/skills/<name>/`.

## Commands

| Command | Action |
|---|---|
| `@skill-search` | Interactive: pick a command from the list |
| `@skill-search --list` | List all available skills with descriptions |
| `@skill-search --search <query>` | Search skills by name or keyword |
| `@skill-search --install <name>` | Download and install a skill from GitHub |
| `@skill-search --update <name>` | Re-download and overwrite an installed skill |
| `@skill-search --info <name>` | Show frontmatter details of a remote skill |

## How it works

Uses two sources from the GitHub repo:

- **GitHub API** (`api.github.com/repos/Echeq/myAI-Skills/contents/...`) to list
  directories (rate-limited to 60 req/hr unauthenticated)
- **Raw content** (`raw.githubusercontent.com/Echeq/myAI-Skills/main/...`) to
  download file contents (no rate limit)

For each skill, it reads the YAML frontmatter from `SKILL.md` to extract
`name`, `description`, and `triggers`.

### --list

1. Fetch `https://api.github.com/repos/Echeq/myAI-Skills/contents/.agents/skills`
2. For each directory, fetch the `SKILL.md` frontmatter via raw URL
3. Print table with name, description, triggers

```
| ai-docs | Generates documentation | @ai-docs, @ai-docs pro... |
| ai-git  | Git/GitHub skill hub   | @ai-git, @ai-git --commit... |
```

### --search <query>

Same as `--list` but filter results by matching query against name or
description. Case-insensitive.

### --info <name>

1. Fetch `https://raw.githubusercontent.com/Echeq/myAI-Skills/main/.agents/skills/<name>/SKILL.md`
2. Parse and display frontmatter + line count

### --install <name>

1. Check if skill already exists in `.agents/skills/<name>/`:
   - If yes → warn "Already installed. Use --update to overwrite."
   - If no → proceed
2. Fetch the directory listing via API to find all files
3. Download each file via raw URL, preserving subdirectory structure
4. Create `.agents/skills/<name>/` and write all files
5. Report: "Installed <name> from GitHub (X files)"

Also handle multi-file skills like `ai-git` (which has `commit.md`, `branch.md`,
`pr.md`, `release.md` alongside `SKILL.md`).

### --update <name>

1. Warn: "This will overwrite local changes to <name>."
2. If user confirms → same as --install but skips the "already exists" check

## Error handling

- GitHub API rate limited → fall back to raw.githubusercontent.com listing
  (not always possible for directories). Warn user if list unavailable.
- Network failure → "Cannot reach GitHub. Check your connection."
- Skill not found → "No skill named '<name>' found in the repository."
- Write fails → check `.agents/skills/` exists and is writable

## Examples

```
@skill-search --list
@skill-search --search audit
@skill-search --info ai-git
@skill-search --install ai-audit
@skill-search --update ai-docs
```

Base directory: D:\myAI-Skills\.agents\skills\skill-search
