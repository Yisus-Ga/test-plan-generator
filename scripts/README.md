# Scripts de Utilidad

## 📊 Ver Datos de la Base de Datos

### Opción 1: Script Python (Recomendado)

Ejecuta el script que creamos:

```bash
python scripts/view_db.py
```

Este script muestra:
- Resumen general (cantidad de HUs, Test Plans, casos de prueba)
- Todas las Historias de Usuario con detalles
- Todos los Test Plans con estadísticas
- Primeros 20 casos de prueba

---

### Opción 2: DB Browser for SQLite (GUI Gráfica)

**Descargar**: https://sqlitebrowser.org/

1. Instala DB Browser for SQLite
2. Abre la aplicación
3. Click en "Open Database"
4. Selecciona `test_plan_generator.db` en el directorio raíz del proyecto
5. Explora las tablas:
   - `user_stories`
   - `test_plans`
   - `test_cases`

**Ventajas**:
- Interfaz gráfica amigable
- Puedes ejecutar queries SQL personalizados
- Ver y editar datos directamente
- Exportar datos a CSV, JSON, etc.

---

### Opción 3: Línea de Comandos SQLite

Si tienes SQLite instalado, puedes usar:

```bash
sqlite3 test_plan_generator.db
```

Luego ejecuta queries SQL:

```sql
-- Ver todas las tablas
.tables

-- Ver estructura de una tabla
.schema user_stories

-- Ver todas las Historias de Usuario
SELECT * FROM user_stories;

-- Ver todos los Test Plans con su HU
SELECT tp.id, tp.user_story_id, us.story_id, us.title, tp.total_cases
FROM test_plans tp
JOIN user_stories us ON tp.user_story_id = us.id;

-- Contar casos de prueba por prioridad
SELECT priority, COUNT(*) as cantidad
FROM test_cases
GROUP BY priority;

-- Ver casos de prueba de un Test Plan específico
SELECT * FROM test_cases WHERE test_plan_id = 1;

-- Salir
.quit
```

---

### Opción 4: Explorar desde Python

Puedes crear tu propio script:

```python
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import UserStoryORM, TestPlanORM

db = SessionLocal()

# Ver todas las HUs
stories = db.query(UserStoryORM).all()
for story in stories:
    print(f"{story.story_id}: {story.title}")

# Ver Test Plans
plans = db.query(TestPlanORM).all()
for plan in plans:
    print(f"Test Plan {plan.id}: {plan.total_cases} casos")

db.close()
```

---

## 📝 Queries Útiles

### Ver Test Plans con su HU asociada:

```sql
SELECT 
    tp.id,
    us.story_id,
    us.title,
    tp.total_cases,
    tp.high_priority_count,
    tp.medium_priority_count,
    tp.low_priority_count,
    tp.created_at
FROM test_plans tp
JOIN user_stories us ON tp.user_story_id = us.id
ORDER BY tp.created_at DESC;
```

### Ver casos de prueba de un Test Plan:

```sql
SELECT 
    tc.tc_id,
    tc.priority,
    tc.title,
    tc.expected_validation
FROM test_cases tc
WHERE tc.test_plan_id = 1
ORDER BY 
    CASE tc.priority
        WHEN 'Alta' THEN 1
        WHEN 'High' THEN 1
        WHEN 'Media' THEN 2
        WHEN 'Medium' THEN 2
        WHEN 'Baja' THEN 3
        WHEN 'Low' THEN 3
        ELSE 4
    END,
    tc.id;
```

### Estadísticas generales:

```sql
SELECT 
    COUNT(DISTINCT us.id) as total_historias,
    COUNT(DISTINCT tp.id) as total_test_plans,
    COUNT(tc.id) as total_casos_prueba,
    AVG(tp.total_cases) as promedio_casos_por_plan
FROM user_stories us
LEFT JOIN test_plans tp ON us.id = tp.user_story_id
LEFT JOIN test_cases tc ON tp.id = tc.test_plan_id;
```

---

## 🗂️ Ubicación de la Base de Datos

La base de datos SQLite se encuentra en:

```
test_plan_generator.db
```

En el directorio raíz del proyecto.

---

## 🔍 Notas

- El script `view_db.py` es la forma más rápida de ver un resumen
- DB Browser for SQLite es la mejor opción para explorar datos en detalle
- La línea de comandos SQLite es útil para queries personalizados
