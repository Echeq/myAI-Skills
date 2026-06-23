# Usage

Las skills están diseñadas para consumirse desde cualquier proyecto externo.

## Instalación Local

Cada skill es un paquete independiente. Para usarla en otro proyecto:

```bash
# npm (TypeScript/Node.js)
npm install --save <ruta-al-repo>/.agents/skills/<skill-name>

# pip (Python)
pip install -e <ruta-al-repo>/.agents/skills/<skill-name>
```

## Importación

```typescript
// TypeScript — la API exacta depende de cada skill
import { createClient } from '@hub/skill-name';

const client = createClient({ host: 'localhost', port: 5432 });
```

```python
# Python
from skill_name import create_client

client = create_client(host='localhost', port=5432)
```

## Configuración

Las skills nunca leen variables de entorno globales. Toda configuración se inyecta por parámetro.

```typescript
// Bien — configuración inyectada
const logger = createLogger({ level: 'info', format: 'json' });

// Mal — depende de entorno global
const logger = createLogger(); // process.env.LOG_LEVEL internamente
```

Cada skill documenta sus opciones de configuración en su propio `README.md`.
