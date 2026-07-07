# Diagram Conventions

## Recommended `%%{init}%%` Directive

Place this at the **very top** of every Mermaid fenced code block, before any diagram content:

```yaml
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
```

This directive constrains diagram rendering so it never exceeds the container width and maintains proper aspect ratio.

## Examples

### Flowchart

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

### Sequence Diagram

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B->>A: Hi
```

### Class Diagram

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
classDiagram
    class Animal {
        +String name
        +makeSound()
    }
    class Dog {
        +bark()
    }
    Animal <|-- Dog
```

## Rule

> The `%%{init}%%` directive **must** be the first line of every Mermaid fenced code block. Without it, diagrams may render oversized or overflow their container.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
