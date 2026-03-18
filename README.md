# Test Plan Generator

Plataforma de análisis de Historias de Usuario (HU) con IA para generar Test Plans estructurados.

## Configuración rápida

1. **Clonar** el repositorio.
2. **Copiar** `.env.example` a `.env`:
   ```powershell
   copy .env.example .env
   ```
3. **Editar** `.env` y completar tu `OPENAI_API_KEY` (obtenerla en [platform.openai.com/api-keys](https://platform.openai.com/api-keys)).
4. **Instalar** dependencias e iniciar:
   ```powershell
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

> ⚠️ **Nunca** subas tu archivo `.env` a GitHub. Ya está excluido en `.gitignore`.

## Documentación

- [Guía: Publicar en GitHub sin exponer la API Key](docs/09_GUIA_PUBLICAR_EN_GITHUB.md)
- [Índice de documentación arquitectónica](docs/README.md)
