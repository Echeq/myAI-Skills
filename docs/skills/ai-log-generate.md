# ai-log-generate

Log every AI interaction — prompt, response, affected file, code before/after, and metadata.

> **Trigger:** `@ai-log`

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

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
