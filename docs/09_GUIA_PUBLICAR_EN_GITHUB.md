# Guía: Publicar en GitHub sin exponer la API Key

Esta guía te lleva paso a paso para publicar tu proyecto en GitHub de forma segura, **sin subir nunca** tu archivo `.env` con la clave de OpenAI.

---

## ¿Por qué es importante?

- **API Key expuesta** = cualquiera puede usar tu cuenta de OpenAI y gastar tus créditos
- **`.gitignore`** evita que Git incluya ciertos archivos en los commits
- **`.env.example`** muestra qué variables necesita el proyecto, sin valores reales

---

## Resumen de lo que ya está configurado

| Elemento | Estado |
|----------|--------|
| `.gitignore` | ✅ Ya excluye `.env`, `.env.local`, `.env.*.local` |
| `.env.example` | ✅ Creado con placeholders (sin API key real) |
| Tu `.env` real | ✅ Queda solo en tu PC, no se sube |

---

## Paso a paso para publicar en GitHub

### Paso 1: Verificar que .env no se va a subir

Antes de inicializar Git, verifica que `.env` está en `.gitignore`:

1. Abre `.gitignore`
2. Busca la línea que dice `.env` (debe estar bajo "# Environment")

Si está, **estás protegido**. Git ignorará automáticamente tu archivo `.env`.

---

### Paso 2: Crear cuenta en GitHub (si no tienes)

1. Ve a [github.com](https://github.com)
2. Clic en **"Sign up"**
3. Completa el registro con tu email

---

### Paso 3: Crear el repositorio en GitHub

1. Inicia sesión en GitHub
2. Clic en el **+** (arriba a la derecha) → **New repository**
3. Completa:
   - **Repository name**: `test-plan-generator` (o el nombre que prefieras)
   - **Description**: "Plataforma de análisis de HUs y generación de Test Plans con IA"
   - **Visibility**: Private (recomendado al inicio) o Public
   - **NO marques** "Add a README file", "Add .gitignore", ni "Choose a license"
4. Clic en **Create repository**

GitHub te mostrará una página con instrucciones. **No las ejecutes aún**; seguimos en local.

---

### Paso 4: Inicializar Git en tu proyecto (local)

Abre **PowerShell** o **Símbolo del sistema** y navega a tu carpeta del proyecto:

```powershell
cd "C:\Users\jgallardo\OneDrive - ACCION POINT SA\Documentos\AP\IA\Agent\v5"
```

Luego ejecuta estos comandos **uno por uno**:

```powershell
# 1. Inicializar el repositorio Git
git init

# 2. (Opcional) Ver qué archivos detecta Git - .env NO debe aparecer
git status

# 3. Agregar todos los archivos (excepto los del .gitignore)
git add .

# 4. Verificar de nuevo: en la lista no debe estar .env
git status

# 5. Primer commit
git commit -m "Primer commit: proyecto base con configuración segura"
```

**Verificación crítica**: En el paso 4, cuando hagas `git status`, **NO debe aparecer** el archivo `.env` en la lista de "Changes to be committed". Si aparece, **detente** y revisa el `.gitignore` antes de hacer el commit.

---

### Paso 5: Conectar con GitHub y subir

Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub y `NOMBRE_REPO` con el nombre del repositorio que creaste:

```powershell
# Agregar el repositorio remoto de GitHub
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git

# Renombrar la rama principal a "main" (si GitHub lo pide)
git branch -M main

# Subir el código
git push -u origin main
```

**Ejemplo**: Si tu usuario es `jgallardo` y el repo se llama `test-plan-generator`:
```
git remote add origin https://github.com/jgallardo/test-plan-generator.git
```

---

### Paso 6: Autenticación con GitHub

Cuando hagas `git push`, GitHub te pedirá autenticarte.

**Opción A - HTTPS (más simple)**  
- Te pedirá usuario y contraseña  
- Para la contraseña, debes usar un **Personal Access Token** (no tu contraseña normal)  
- Crear token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token

**Opción B - GitHub Desktop**  
- Instala [GitHub Desktop](https://desktop.github.com)  
- Abre el proyecto, te guiará para conectar con tu cuenta

---

## Checklist de seguridad antes de cada push

Antes de hacer `git push` en el futuro, verifica:

- [ ] `.env` está en `.gitignore`
- [ ] No hay `git add .env` en tu historial reciente
- [ ] `git status` no muestra `.env`
- [ ] No pegaste la API key en el README ni en otro archivo del repo

---

## Si alguien más clona el proyecto

La otra persona debe:

1. Clonar el repo: `git clone https://github.com/TU_USUARIO/NOMBRE_REPO.git`
2. Copiar `.env.example` a `.env`: `copy .env.example .env` (en Windows)
3. Abrir `.env` y poner **su propia** API key de OpenAI

Tu `.env` nunca se sube, así que cada desarrollador usa su propia clave.

---

## Recomendación: Rotar tu API Key (por precaución)

Si en algún momento tu API key pudo haber sido vista (por ejemplo, compartiste una captura o el contenido del `.env`), es buena práctica **rotarla**:

1. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crea una nueva clave
3. Actualiza tu archivo `.env` local con la nueva clave
4. Revoca o elimina la clave anterior

---

## Próximos pasos

Una vez publicado en GitHub, puedes:
- Hacer commits y push regularmente
- Usar branches para nuevas funcionalidades
- Seguir con el Paso 2 del plan: Tests automatizados

---

**¿Dudas?** Consulta esta guía o pregúntame antes de ejecutar comandos si algo no queda claro.
