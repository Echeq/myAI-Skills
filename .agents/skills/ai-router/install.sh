#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SKILL_DIR/../../.." && pwd)"

cat > "$ROOT_DIR/opencode.json" <<EOF
{
  "\$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": [".agents/skills"]
  }
}
EOF

echo "Created $ROOT_DIR/opencode.json"
echo "ai-router installed. Restart opencode, then run @ai-router --init to set up sub-agents interactively."
