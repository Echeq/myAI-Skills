# Usage

Skills are designed to be consumed from any external project.

## Local Installation

Each skill is an independent package. To use it in another project:

```bash
# npm (TypeScript/Node.js)
npm install --save <repo-path>/.agents/skills/<skill-name>

# pip (Python)
pip install -e <repo-path>/.agents/skills/<skill-name>
```

## Import

```typescript
// TypeScript — exact API depends on each skill
import { createClient } from '@hub/skill-name';

const client = createClient({ host: 'localhost', port: 5432 });
```

```python
# Python
from skill_name import create_client

client = create_client(host='localhost', port=5432)
```

## Configuration

Skills never read global environment variables. All configuration is injected via parameters.

```typescript
// Good — injected config
const logger = createLogger({ level: 'info', format: 'json' });

// Bad — depends on global env
const logger = createLogger(); // process.env.LOG_LEVEL internally
```

Each skill documents its configuration options in its own `README.md`.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
