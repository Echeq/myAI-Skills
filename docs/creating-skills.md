# Creating Skills

Guía para crear una nueva skill en este repositorio.

## Estructura Mínima

```
.agents/skills/<skill-name>/
├── SKILL.md          # Metadatos: nombre, descripción, herramientas permitidas
├── src/index.ts      # Código principal (o .py si es Python)
├── tests/index.test.ts
├── README.md         # Documentación con ejemplos de uso
└── package.json      # Dependencias y scripts (o requirements.txt)
```

## SKILL.md

Archivo con frontmatter YAML que define el skill como agente OpenCode:

```yaml
---
name: my-skill
description: Breve descripción de lo que hace
allowed-tools: Read, Write, Bash
---
```

## Requisitos

1. **Tests**: mínimo un test unitario y uno de integración en `tests/`.
2. **Documentación**: el `README.md` debe incluir al menos 2 ejemplos de uso.
3. **Config inyectable**: la skill recibe configuración por parámetro, nunca de variables globales.
4. **Tipado**: TypeScript strict types o Python type hints.
5. **SemVer**: versión inicial `1.0.0`; documenta en el README cómo se versiona.

## Scripts Recomendados (package.json)

```json
{
  "scripts": {
    "test": "jest",
    "build": "tsc",
    "lint": "eslint src/"
  }
}
```
