# Conventions

## Tecnologías

| Tipo | Por Defecto |
|------|-------------|
| Skills generales | TypeScript + Node.js |
| Scripts/datos | Python |

## Estilo de Código

- **Idioma**: todo en inglés (código, comentarios, variables).
- **Funciones puras**: favorecer funciones sin efectos secundarios.
- **Logs**: estructura JSON si la skill genera logs.
- **Errores**: errores personalizados con códigos claros, no `throw new Error('generic')`.

## Versionado

Semantic Versioning (SemVer). Toda skill comienza en `1.0.0`.

## Configuración

Nunca usar `process.env.X` o variables globales. Toda configuración se inyecta:

```typescript
// Bien
const client = createClient({ host, port, ssl: true });

// Mal (no hacer)
const client = createClient(); // usa process.env internamente
```

## Dependencias

Cada skill es autocontenida con sus propias dependencias. No comparte `node_modules` ni `site-packages` con otras skills.
