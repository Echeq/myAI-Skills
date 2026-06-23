# myAI-Skills Docs

Bienvenido a la documentación del repositorio de skills.

## Contenido

| Documento | Descripción |
|-----------|-------------|
| [usage.md](usage.md) | Cómo consumir las skills desde proyectos externos |
| [creating-skills.md](creating-skills.md) | Guía para crear y publicar nuevas skills |
| [conventions.md](conventions.md) | Convenciones, estándares y tecnologías |

## Estructura del Repositorio

```
.agents/skills/<name>/
├── SKILL.md        # Definición del skill (frontmatter + instrucciones)
├── README.md       # Documentación de la skill
├── src/            # Código fuente (cuando aplique)
├── tests/          # Tests (cuando aplique)
└── package.json    # Dependencias (cuando aplique)
```

> **Nota:** Actualmente las 4 skills existentes son archivos `.md` sin código empaquetado. La estructura con `src/`, `tests/` y `package.json` es el objetivo para skills futuras.
