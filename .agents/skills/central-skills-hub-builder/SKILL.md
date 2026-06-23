---
name: Central Skills Hub Builder
description: Arquitecto para construir un repositorio de skills modulares, reutilizables y autocontenidas.
allowed-tools: Read, Write, Bash, Python, TypeScript
---

# Central Skills Hub Builder

## 🎯 Misión
Construir skills modulares, autocontenidas y reutilizables dentro de `.agents/skills/<name>/`. Cada skill debe ser empaquetable (NPM, pip), probada y documentada para consumo desde cualquier otro proyecto.

---

## 🏗️ Estructura del Hub

```
.agents/skills/<skill-name>/
├── SKILL.md       # Definición del agente (frontmatter + instrucciones)
├── src/
├── tests/
├── README.md
└── package.json (o requirements.txt, Cargo.toml)
```

## 📐 Principios de Diseño para cada Skill creada

1.  **Autocontención (Self-contained):** Cada skill vive en su propia carpeta raíz. Tiene sus propias dependencias y no comparte `node_modules` o `site-packages` con las demás (a menos que uses monorepos tipo pnpm workspaces, pero aislado en su definición).
2.  **Inyección de Configuración:** Nunca uses variables de entorno globales del sistema (`process.env.DB_URL`) directamente. Usa un patrón de fábrica o constructor que reciba la configuración por parámetro (ej. `createClient({ host, port })`), y provee un archivo `.env.example` dentro de la skill.
3.  **Interfaz Clara (API explícita):** Expón funciones/classes con tipado estricto (TypeScript o Python type hints). El `README.md` debe mostrar al menos 2 ejemplos de uso práctico.
4.  **Testing en el ADN:** Cada skill debe tener al menos un test unitario y un test de integración básico dentro de su carpeta `/tests`.
5.  **Versionado Semántico:** Al crear o modificar una skill, debes asignarle una versión inicial `v1.0.0` y explicar en el `README` cómo se actualizará (siguiendo SemVer).

---

## 🔄 Flujo de Trabajo al Recibir una Petición

Cuando el usuario te pida crear una nueva skill para este Hub:

1.  **Definición de requisitos:** Pregunta al usuario el **nombre**, **propósito** y **lenguaje/tecnología** preferida (si no lo especifica, usa TypeScript/Node.js por defecto, o Python si pide scripts de datos).
2.  **Generación de estructura:** Crea la carpeta dentro de `.agents/skills/<skill-name>/` con `SKILL.md` (frontmatter + instrucciones) más los subdirectorios y archivos mínimos (`src/index.ts`, `tests/index.test.ts`, `README.md`, `package.json`).
3.  **Escritura de código:** Escribe el código limpio, con JSDoc/docstrings, manejo de errores explícito y validación de entradas.
4.  **Documentación:** Escribe el `README.md` con:
    - Título y descripción.
    - Instalación (ej. `npm install ../.agents/skills/skill-name` o copiar la carpeta).
    - Ejemplo de consumo desde un repositorio externo (`import { miFuncion } from '@hub/skill-name'`).
    - Variables de entorno necesarias (si las hay, inyectadas).

---

## 🧠 Reglas de Estilo y Calidad de Código

- **Funciones puras:** Favorece funciones puras sobre efectos secundarios.
- **Logs estructurados:** Si la skill genera logs, que sean en formato JSON.
- **Manejo de errores:** Nunca uses `throw new Error('generic')`; usa errores personalizados con códigos claros.
- **Nombres en inglés:** Todo el código, comentarios y nombres de variables deben estar en **inglés**, aunque la documentación para el usuario pueda estar en español si el usuario lo prefiere.

---

## ⚠️ Comportamiento ante Ambigüedades

Si el usuario te pide una skill que suena similar a algo existente:
- **NO** intentes adivinar cómo funciona.
- Pregunta directamente: *"¿Cuáles son las especificaciones exactas de entrada/salida para esta nueva skill?"* y constrúyela basándote **únicamente** en la respuesta del usuario y las mejores prácticas modernas.

---

## ✅ Criterio de Éxito

El Hub estará completo cuando:
1. Tenga al menos 3 skills funcionales, probadas y documentadas.
2. Un desarrollador externo pueda clonar este repositorio, navegar a `.agents/skills/<cualquiera>/` y entender cómo usarla en menos de 5 minutos sin leer el código fuente.
