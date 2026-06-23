# Conventions

## Technologies

| Type | Default |
| :--- | :--- |
| General skills | TypeScript + Node.js |
| Data/scripting | Python |

## Code Style

- **Language**: English for all code, comments, and variable names.
- **Pure functions**: favor functions without side effects.
- **Logs**: JSON structure if the skill generates logs.
- **Errors**: custom errors with clear codes, not `throw new Error('generic')`.

## Versioning

Semantic Versioning (SemVer). Every skill starts at `1.0.0`.

## Configuration

Never use `process.env.X` or global variables. All configuration is injected:

```typescript
// Good
const client = createClient({ host, port, ssl: true });

// Bad
const client = createClient(); // uses process.env internally
```

## Dependencies

Each skill is self-contained with its own dependencies. Does not share `node_modules` or `site-packages` with other skills.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
