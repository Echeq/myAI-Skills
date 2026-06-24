# ai-log-generate

Log every AI interaction — prompt, response, affected file, code before/after, and metadata.

> **Trigger:** `@ai-log`

## Quick Start

1. After any AI interaction (changes made, files edited), type `@ai-log`.
2. The agent auto-detects your PC name, date, git branch, and reads the conversation.
3. A log file is saved to `docs/log/AI-LOG-{timestamp}.txt` with prompt, response, and code diffs.

**Example:** `@ai-log` → `docs/log/AI-LOG-2026-06-23-093931-DESKTOP-CR24C6G.txt`

## Description

Captures the full conversation context of an AI interaction and writes a structured log file to `docs/log/`.

## Usage

Invoke `@ai-log` after any AI interaction. The agent auto-detects system info (PC name, date, git branch), extracts prompt and response from conversation history, reads `git diff` for code before/after, and writes a timestamped log file.

## Configuration

No parameters required. Output auto-generated to:

`docs/log/AI-LOG-YYYY-MM-DD-HHMMSS-PCNAME.txt`

## Output Format

> [!NOTE]
> Logs are stored locally in `docs/log/` and are not committed by default. Add `docs/log/` to `.gitignore` if needed.

> [!TIP]
> Use `@ai-commit` before `@ai-log` to ensure your changes are staged first.

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
