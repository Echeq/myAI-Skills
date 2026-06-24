---
name: ai-log-generate
description: Log every AI interaction — prompt, response, affected file, code before/after, and metadata. Triggers on "@ai-log".
triggers:
  - "@ai-log"
  - "@ai-log --list"
  - "@ai-log --search"
  - "@ai-log --last"
  - "@ai-log --no-prompt"
---

## Workflow

When user says `@ai-log`, generate a log file. Support these flags:

| Flag | Action |
|---|---|
| `@ai-log` | Log current interaction |
| `@ai-log --list` | List all past logs with date, file count |
| `@ai-log --search <term>` | Search log contents for term |
| `@ai-log --last` | Show the most recent log content |
| `@ai-log --no-prompt` | Log everything except the prompt text (privacy) |

### 1. Security — filter secrets

Before writing any log, scan prompt + response + git diff for sensitive patterns. **Mask** any matches:

| Pattern | Mask with |
|---|---|
| `api[_-]?key` | `API_KEY_REDACTED` |
| `secret` | `SECRET_REDACTED` |
| `password` | `PASSWORD_REDACTED` |
| `token` | `TOKEN_REDACTED` |
| `-----BEGIN.*KEY-----` | `CERTIFICATE_REDACTED` |
| Email regex | `EMAIL_REDACTED` |

Apply this filter to the prompt, the AI response, and the git diff output before logging. If `--no-prompt` is used, skip prompt entirely.

### 2. Auto-detect

| Field | Windows | Mac/Linux |
|---|---|---|
| PC Name | `$env:COMPUTERNAME` | `hostname` |
| Date | `Get-Date -Format "yyyy-MM-dd"` | `date +%F` |
| Time | `Get-Date -Format "HHmmss"` | `date +%H%M%S` |
| Git Branch | `git branch --show-current` | `git branch --show-current` |

If the user requests privacy, use `LOCAL` instead of PC name.

### 3. Read conversation

Extract from chat — do NOT ask the user:
- **Prompt** — User's messages (skip if `--no-prompt`)
- **AI Response** — Your replies
- **File Path** — Files created or edited
- **Code Before** — `git diff` (or `git diff --cached` if staged, or `git diff HEAD` for committed+unstaged)
- **Code After** — New content
- **AI Tool** — Always `OpenCode`

Run `git diff --name-only` for file list. If git diff is empty (new files not staged), read files before/after via `read`.

### 4. Generate filename

Format: `AI-LOG-YYYY-MM-DD-HHMMSS-PCNAME.md`

Extension is `.md` (not `.txt`) for readable rendering. Example: `AI-LOG-2026-06-12-093931-DESKTOP-CR24C6G.md`

### 5. Write the log

Save to `docs/log/<filename>` with this template:

```markdown
# AI Interaction Log — {date}

| Field | Value |
|---|---|
| PC Name | {pc_name} |
| Date | {date} |
| Time | {time} |
| Branch | {branch} |
| Tool | OpenCode |

## Prompt
{prompt}

## AI Response
{response}

## Files Affected
{files}

## Code Before
```diff
{before}
```

## Code After
```
{after}
```
```

### 6. Rotate warning

If `docs/log/` contains >50 files, warn:
> "⚠️ Over 50 log files. Consider archiving or deleting old logs with `@ai-log --list`."

### 7. Confirm

> ✅ Log saved to `docs/log/AI-LOG-2026-06-12-093931-DESKTOP-CR24C6G.md`
