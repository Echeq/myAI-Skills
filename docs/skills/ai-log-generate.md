# ai-log-generate

Log every AI interaction — prompt, response, affected file, code before/after, and metadata. Includes secrets redaction, log management, and privacy flags.

> **Trigger:** `@ai-log` | `@ai-log --list` | `@ai-log --search <term>` | `@ai-log --last` | `@ai-log --no-prompt`

## Quick Start

1. After any AI interaction (changes made, files edited), type `@ai-log`.
2. The agent auto-detects your PC name, date, git branch, and reads the conversation.
3. Secrets are automatically redacted (API keys, passwords, tokens).
4. Log saved to `docs/log/AI-LOG-{timestamp}.md` with prompt, response, and code diffs.

**Example:** `@ai-log` → secrets filtered → `docs/log/AI-LOG-2026-06-23-093931-DESKTOP-CR24C6G.md`

## Description

Captures the full conversation context of an AI interaction, applies secrets redaction, and writes a structured Markdown log file to `docs/log/`. Supports log listing, search, and privacy modes.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-log` | Log current interaction with secrets redacted |
| `@ai-log --list` | List all past logs with date and file count |
| `@ai-log --search <term>` | Search log contents for a keyword |
| `@ai-log --last` | Show the most recent log |
| `@ai-log --no-prompt` | Log everything except the prompt (privacy mode) |

## Configuration

| Setting | Details |
| :--- | :--- |
| Output | `docs/log/AI-LOG-YYYY-MM-DD-HHMMSS-PCNAME.md` (Markdown) |
| Secrets | Auto-redacted: api_key, secret, password, token, certificate, email |
| Privacy | Use `--no-prompt` to exclude prompt text. PC Name replaced with `LOCAL` on request |
| Rotation | Warns when >50 log files exist |

## Redacted Patterns

| Pattern | Mask |
| :--- | :--- |
| `api_key`, `api-key`, `apikey` | `API_KEY_REDACTED` |
| `secret` | `SECRET_REDACTED` |
| `password` | `PASSWORD_REDACTED` |
| `token` | `TOKEN_REDACTED` |
| `-----BEGIN * KEY-----` | `CERTIFICATE_REDACTED` |
| Email addresses | `EMAIL_REDACTED` |

> [!NOTE]
> Logs are stored locally in `docs/log/`. Add `docs/log/` to `.gitignore` if they should not be committed.
> The `.md` format makes logs readable in any Markdown viewer.

> [!TIP]
> Use `@ai-commit` before `@ai-log` to ensure your changes are staged first.
> Use `@ai-log --no-prompt` when discussing sensitive information.

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
