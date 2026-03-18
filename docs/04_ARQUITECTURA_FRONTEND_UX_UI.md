# Arquitectura Frontend y UX/UI

## 🎯 Objetivo

Definir una arquitectura frontend moderna, escalable y con una experiencia de usuario profesional, preparada para evolucionar hacia una aplicación completa.

---

## 🏗️ Arquitectura Frontend Propuesta

### Opción A: Vanilla JS Modular (Recomendada para MVP Evolucionado)

**Justificación**:
- ✅ Sin dependencias pesadas
- ✅ Rápido y ligero
- ✅ Fácil de entender y mantener
- ✅ Escalable con organización adecuada
- ✅ Transición suave desde código actual

### Opción B: Framework Moderno (React/Vue/Svelte) - Futuro

**Justificación**:
- ✅ Componentización real
- ✅ Gestión de estado robusta
- ✅ Ecosistema maduro
- ⚠️ Requiere migración completa
- ⚠️ Curva de aprendizaje

**Recomendación**: Empezar con Vanilla JS modular, planificar migración a React/Vue cuando sea necesario.

---

## 📁 Estructura de Directorios (Frontend Modular)

```
frontend/
├── index.html                  # Punto de entrada
├── assets/
│   ├── css/
│   │   ├── main.css           # Estilos principales
│   │   ├── components.css     # Estilos de componentes
│   │   ├── utilities.css      # Utilidades (Bootstrap-like)
│   │   └── themes.css         # Variables de tema
│   │
│   ├── js/
│   │   ├── main.js            # Punto de entrada JS
│   │   ├── config.js          # Configuración (API URLs, etc.)
│   │   │
│   │   ├── api/               # Cliente API
│   │   │   ├── client.js      # Cliente HTTP base
│   │   │   ├── auth.js        # Endpoints de autenticación
│   │   │   ├── user-stories.js
│   │   │   ├── test-plans.js
│   │   │   └── exports.js
│   │   │
│   │   ├── services/          # Lógica de negocio (client-side)
│   │   │   ├── auth-service.js
│   │   │   ├── user-story-service.js
│   │   │   ├── test-plan-service.js
│   │   │   └── export-service.js
│   │   │
│   │   ├── components/        # Componentes reutilizables
│   │   │   ├── Button.js
│   │   │   ├── FormInput.js
│   │   │   ├── Textarea.js
│   │   │   ├── Card.js
│   │   │   ├── Modal.js
│   │   │   ├── Alert.js
│   │   │   ├── Spinner.js
│   │   │   └── UserStoryForm.js
│   │   │
│   │   ├── pages/             # Páginas/Vistas
│   │   │   ├── LoginPage.js
│   │   │   ├── DashboardPage.js
│   │   │   ├── ProjectsPage.js
│   │   │   ├── UserStoriesPage.js
│   │   │   ├── CreateUserStoryPage.js
│   │   │   ├── TestPlanPage.js
│   │   │   └── ExportPage.js
│   │   │
│   │   ├── utils/             # Utilidades
│   │   │   ├── dom.js         # Helpers DOM
│   │   │   ├── validation.js  # Validación de formularios
│   │   │   ├── storage.js     # LocalStorage/SessionStorage
│   │   │   └── format.js      # Formateo de datos
│   │   │
│   │   └── router.js          # Router simple (SPA básico)
│   │
│   └── images/
│       └── logo.svg
│
├── package.json                # Dependencias (si usamos bundler)
└── README.md
```

---

## 🎨 Sistema de Diseño (Design System)

### Paleta de Colores

```css
/* assets/css/themes.css */
:root {
  /* Colores principales */
  --color-primary: #2563eb;        /* Azul principal */
  --color-primary-dark: #1d4ed8;
  --color-primary-light: #3b82f6;
  
  /* Colores secundarios */
  --color-secondary: #64748b;      /* Gris azulado */
  --color-secondary-dark: #475569;
  --color-secondary-light: #94a3b8;
  
  /* Colores de estado */
  --color-success: #10b981;        /* Verde */
  --color-warning: #f59e0b;        /* Amarillo */
  --color-error: #ef4444;          /* Rojo */
  --color-info: #3b82f6;           /* Azul info */
  
  /* Colores neutros */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
  
  /* Fondos */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: var(--color-gray-50);
  --color-bg-tertiary: var(--color-gray-100);
  
  /* Texto */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-tertiary: var(--color-gray-500);
  --color-text-inverse: #ffffff;
  
  /* Bordes */
  --color-border: var(--color-gray-200);
  --color-border-light: var(--color-gray-100);
  --color-border-dark: var(--color-gray-300);
  
  /* Sombras */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Espaciado */
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */
  
  /* Tipografía */
  --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
  
  --font-size-xs: 0.75rem;     /* 12px */
  --font-size-sm: 0.875rem;    /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;    /* 18px */
  --font-size-xl: 1.25rem;     /* 20px */
  --font-size-2xl: 1.5rem;     /* 24px */
  --font-size-3xl: 1.875rem;   /* 30px */
  --font-size-4xl: 2.25rem;    /* 36px */
  
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
  
  /* Bordes */
  --border-radius-sm: 0.25rem;   /* 4px */
  --border-radius-md: 0.375rem;  /* 6px */
  --border-radius-lg: 0.5rem;    /* 8px */
  --border-radius-xl: 0.75rem;   /* 12px */
  --border-radius-full: 9999px;
  
  /* Transiciones */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  
  /* Z-index layers */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}
```

---

### Componentes Base

#### Button Component

```javascript
// assets/js/components/Button.js
export class Button {
  constructor({
    text,
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    icon = null,
    onClick = null,
    className = ''
  }) {
    this.text = text;
    this.variant = variant;
    this.size = size;
    this.disabled = disabled;
    this.loading = loading;
    this.icon = icon;
    this.onClick = onClick;
    this.className = className;
  }
  
  render() {
    const button = document.createElement('button');
    button.className = `btn btn-${this.variant} btn-${this.size} ${this.className}`;
    button.disabled = this.disabled || this.loading;
    
    if (this.loading) {
      button.innerHTML = `
        <span class="spinner spinner-sm"></span>
        <span>Cargando...</span>
      `;
    } else {
      button.innerHTML = this.icon 
        ? `<span class="icon">${this.icon}</span> ${this.text}`
        : this.text;
    }
    
    if (this.onClick) {
      button.addEventListener('click', this.onClick);
    }
    
    return button;
  }
}
```

#### FormInput Component

```javascript
// assets/js/components/FormInput.js
export class FormInput {
  constructor({
    id,
    label,
    type = 'text',
    placeholder = '',
    value = '',
    required = false,
    error = null,
    helperText = null,
    onChange = null,
    onBlur = null
  }) {
    this.id = id;
    this.label = label;
    this.type = type;
    this.placeholder = placeholder;
    this.value = value;
    this.required = required;
    this.error = error;
    this.helperText = helperText;
    this.onChange = onChange;
    this.onBlur = onBlur;
  }
  
  render() {
    const container = document.createElement('div');
    container.className = 'form-group';
    
    container.innerHTML = `
      <label for="${this.id}" class="form-label">
        ${this.label}
        ${this.required ? '<span class="text-error">*</span>' : ''}
      </label>
      <input
        type="${this.type}"
        id="${this.id}"
        class="form-input ${this.error ? 'form-input-error' : ''}"
        placeholder="${this.placeholder}"
        value="${this.value}"
        ${this.required ? 'required' : ''}
      />
      ${this.error ? `<span class="form-error">${this.error}</span>` : ''}
      ${this.helperText && !this.error ? `<span class="form-helper">${this.helperText}</span>` : ''}
    `;
    
    const input = container.querySelector('input');
    if (this.onChange) {
      input.addEventListener('input', (e) => this.onChange(e.target.value));
    }
    if (this.onBlur) {
      input.addEventListener('blur', (e) => this.onBlur(e.target.value));
    }
    
    return container;
  }
}
```

---

## 📱 Diseño de Pantallas Propuesto

### 1. Dashboard (Página Principal)

**Estructura**:
- Header con navegación principal
- Sidebar con proyectos
- Área principal con:
  - Cards de proyectos activos
  - Lista de HUs recientes
  - Test Plans recientes
  - Acciones rápidas

**Mockup conceptual**:
```
┌─────────────────────────────────────────────────────────┐
│ Header: [Logo] [Proyectos] [Test Plans] [Usuario ▼]    │
├──────────┬──────────────────────────────────────────────┤
│ Sidebar  │ Dashboard                                    │
│          │ ┌────────────────────────────────────────┐   │
│ Proyectos│ │ Proyecto: AER25                        │   │
│ - AER25  │ │ HUs: 15  |  Test Plans: 8             │   │
│ - BEP30  │ └────────────────────────────────────────┘   │
│          │                                              │
│ [+ Nuevo]│ ┌──────────────┐  ┌──────────────┐         │
│          │ │ HUs Recientes│  │ Test Plans   │         │
│          │ │ - AER25-101  │  │ Recientes    │         │
│          │ │ - AER25-102  │  │ - AER25-101  │         │
│          │ └──────────────┘  └──────────────┘         │
└──────────┴──────────────────────────────────────────────┘
```

---

### 2. Formulario de Creación de HU

**Mejoras vs. formulario actual**:

1. **Validación en tiempo real**
   - Validar formato de ID mientras se escribe
   - Contador de caracteres en descripción
   - Indicadores visuales de campos requeridos

2. **Mejor UX**
   - Placeholders más descriptivos
   - Agrupación visual de campos relacionados
   - Feedback inmediato

3. **Criterios de Aceptación mejorados**
   - Agregar/quitar criterios dinámicamente
   - Validar que haya al menos 1 criterio
   - Preview del formato final

**Código sugerido**:

```javascript
// assets/js/components/UserStoryForm.js
export class UserStoryForm {
  constructor({ onSubmit, onCancel }) {
    this.onSubmit = onSubmit;
    this.onCancel = onCancel;
    this.acceptanceCriteria = [];
  }
  
  render() {
    const form = document.createElement('form');
    form.className = 'user-story-form';
    form.innerHTML = `
      <div class="form-header">
        <h2>Nueva Historia de Usuario</h2>
        <p class="text-secondary">Completa los campos para generar el Test Plan</p>
      </div>
      
      <div class="form-body">
        <div class="form-row">
          ${new FormInput({
            id: 'hu-id',
            label: 'ID de la Historia de Usuario',
            placeholder: 'Ej: AER25-101',
            required: true,
            helperText: 'Formato: [CÓDIGO_PROYECTO]-[NÚMERO]',
            onChange: (value) => this.validateId(value)
          }).render().outerHTML}
        </div>
        
        <div class="form-row">
          ${new FormInput({
            id: 'hu-title',
            label: 'Título',
            placeholder: 'Ej: Frontend -> Pantalla principal Tipos de Reporte',
            required: true,
            onChange: (value) => this.validateTitle(value)
          }).render().outerHTML}
        </div>
        
        <div class="form-row">
          <label for="hu-description" class="form-label">
            Descripción
            <span class="text-error">*</span>
            <span class="char-count" id="desc-count">0 / 2000</span>
          </label>
          <textarea
            id="hu-description"
            class="form-textarea"
            placeholder="Describe la funcionalidad..."
            rows="6"
            required
            maxlength="2000"
          ></textarea>
          <span class="form-helper">Describe la funcionalidad de forma clara y completa</span>
        </div>
        
        <div class="form-row">
          <div class="acceptance-criteria-section">
            <label class="form-label">
              Criterios de Aceptación
              <span class="text-error">*</span>
            </label>
            <div id="acceptance-criteria-list" class="ac-list"></div>
            <button
              type="button"
              class="btn btn-secondary btn-sm"
              onclick="this.addCriterion()"
            >
              + Agregar Criterio
            </button>
            <span class="form-helper">Agrega al menos un criterio de aceptación</span>
          </div>
        </div>
      </div>
      
      <div class="form-footer">
        ${new Button({
          text: 'Cancelar',
          variant: 'secondary',
          onClick: this.onCancel
        }).render().outerHTML}
        
        ${new Button({
          text: 'Generar Test Plan',
          variant: 'primary',
          type: 'submit',
          onClick: (e) => {
            e.preventDefault();
            this.handleSubmit();
          }
        }).render().outerHTML}
      </div>
    `;
    
    return form;
  }
  
  addCriterion() {
    const criterionInput = document.createElement('div');
    criterionInput.className = 'ac-item';
    criterionInput.innerHTML = `
      <input type="text" class="form-input ac-input" placeholder="Criterio de aceptación...">
      <button type="button" class="btn-icon" onclick="this.removeCriterion(this)">
        <span class="icon">×</span>
      </button>
    `;
    document.getElementById('acceptance-criteria-list').appendChild(criterionInput);
  }
  
  handleSubmit() {
    const data = {
      story_id: document.getElementById('hu-id').value.trim(),
      title: document.getElementById('hu-title').value.trim(),
      description: document.getElementById('hu-description').value.trim(),
      acceptance_criteria: Array.from(document.querySelectorAll('.ac-input'))
        .map(input => input.value.trim())
        .filter(val => val.length > 0)
    };
    
    if (this.validate(data)) {
      this.onSubmit(data);
    }
  }
  
  validate(data) {
    // Validación completa
    if (!data.story_id.match(/^[A-Z0-9]+-\d+$/)) {
      this.showError('hu-id', 'Formato de ID inválido');
      return false;
    }
    // ... más validaciones
    return true;
  }
}
```

---

### 3. Página de Visualización de Test Plan

**Mejoras vs. actual**:

1. **Mejor organización visual**
   - Resumen ejecutivo en card destacado
   - Estadísticas (conteos por prioridad)
   - Secciones colapsables

2. **Análisis mejorado**
   - Renderizado markdown mejorado
   - Resaltado de sintaxis
   - Links clickeables

3. **Acciones de exportación**
   - Múltiples formatos (Excel, CSV, Jira, etc.)
   - Preview antes de descargar
   - Historial de exportaciones

**Mockup conceptual**:
```
┌─────────────────────────────────────────────────────────┐
│ Test Plan: AER25-101 - Frontend -> Pantalla principal  │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Resumen                                             │ │
│ │ Total de casos: 15  │  Alta: 5  │  Media: 7  │ 3   │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Objetivo del Test Plan ▼                            │ │
│ │ [Contenido del análisis...]                         │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Casos de Prueba                                      │ │
│ │ [Tabla con casos - oculta en front, solo exportable]│ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [⬇️ Descargar Excel]  [📋 Copiar a Jira]  [📄 Exportar CSV]│
└─────────────────────────────────────────────────────────┘
```

---

### 4. Página de Lista de Proyectos

**Estructura**:
- Grid de proyectos
- Filtros (búsqueda, estado)
- Acciones rápidas (crear proyecto, ver HUs, etc.)

---

## 🎯 Mejoras de UX Específicas

### 1. Validación de Formularios Mejorada

**Campos del formulario (mantener igual que ahora)**:
- ID
- Título
- Descripción
- Criterios de Aceptación

**Validaciones agregadas**:

```javascript
// assets/js/utils/validation.js
export const validators = {
  userStoryId: (value) => {
    if (!value) return { valid: false, error: 'El ID es requerido' };
    if (!/^[A-Z0-9]+-\d+$/.test(value)) {
      return { valid: false, error: 'Formato inválido. Ej: AER25-101' };
    }
    return { valid: true };
  },
  
  title: (value) => {
    if (!value || value.trim().length === 0) {
      return { valid: false, error: 'El título es requerido' };
    }
    if (value.length < 5) {
      return { valid: false, error: 'El título debe tener al menos 5 caracteres' };
    }
    if (value.length > 200) {
      return { valid: false, error: 'El título no puede exceder 200 caracteres' };
    }
    return { valid: true };
  },
  
  description: (value) => {
    if (!value || value.trim().length === 0) {
      return { valid: false, error: 'La descripción es requerida' };
    }
    if (value.length < 20) {
      return { valid: false, error: 'La descripción debe tener al menos 20 caracteres' };
    }
    if (value.length > 2000) {
      return { valid: false, error: 'La descripción no puede exceder 2000 caracteres' };
    }
    return { valid: true };
  },
  
  acceptanceCriteria: (criteria) => {
    if (!criteria || criteria.length === 0) {
      return { valid: false, error: 'Debe agregar al menos un criterio de aceptación' };
    }
    const invalid = criteria.some(c => !c || c.trim().length < 5);
    if (invalid) {
      return { valid: false, error: 'Cada criterio debe tener al menos 5 caracteres' };
    }
    return { valid: true };
  }
};
```

---

### 2. Estados de UI Mejorados

**Estados**:
- Loading: Spinner y mensaje claro
- Success: Mensaje de éxito con detalles
- Error: Mensaje de error específico con acciones
- Empty: Estado vacío con CTAs

**Componente Alert**:

```javascript
// assets/js/components/Alert.js
export class Alert {
  constructor({ type, message, title = null, dismissible = true }) {
    this.type = type; // 'success', 'error', 'warning', 'info'
    this.message = message;
    this.title = title;
    this.dismissible = dismissible;
  }
  
  render() {
    const alert = document.createElement('div');
    alert.className = `alert alert-${this.type}`;
    alert.innerHTML = `
      ${this.title ? `<h4 class="alert-title">${this.title}</h4>` : ''}
      <p class="alert-message">${this.message}</p>
      ${this.dismissible ? '<button class="alert-dismiss" onclick="this.close()">×</button>' : ''}
    `;
    return alert;
  }
}
```

---

### 3. Manejo de Errores Mejorado

**Estrategia**:
- Errores de validación: Muestra inline en cada campo
- Errores de red: Mensaje global con opción de reintentar
- Errores del servidor: Mensaje específico con código de error

---

## 🔄 Flujos de Usuario Mejorados

### Flujo 1: Crear y Analizar HU

```
1. Usuario → Dashboard
   ↓
2. Click "Nueva HU"
   ↓
3. Formulario de creación
   - Validación en tiempo real
   - Feedback inmediato
   ↓
4. Click "Generar Test Plan"
   - Loading state (spinner + mensaje)
   ↓
5. Resultado mostrado
   - Resumen en card
   - Análisis renderizado
   - Acciones de exportación
   ↓
6. Descarga automática (opcional)
   - Excel generado
   - Notificación de éxito
```

---

### Flujo 2: Ver Test Plan Existente

```
1. Usuario → Dashboard
   ↓
2. Click en HU o Test Plan
   ↓
3. Página de detalle
   - Resumen ejecutivo
   - Análisis completo
   - Estadísticas
   ↓
4. Exportar en formato deseado
   - Seleccionar formato
   - Descargar
```

---

## 🎨 Framework CSS Recomendado

### Opción A: CSS Custom (Recomendada)

**Justificación**:
- ✅ Control total sobre estilos
- ✅ Sin dependencias externas
- ✅ Ligero y rápido
- ✅ Fácil de personalizar

**Implementación**: Sistema de diseño propio (mostrado arriba en themes.css)

---

### Opción B: Bootstrap 5

**Justificación**:
- ✅ Componentes listos para usar
- ✅ Sistema de grid robusto
- ✅ Responsive por defecto
- ⚠️ Puede ser pesado si no se usa todo

**Implementación**:

```html
<!-- En index.html -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Recomendación**: Usar Bootstrap solo para grid y utilidades, componentes custom para mejor control.

---

### Opción C: Tailwind CSS (Futuro)

**Justificación**:
- ✅ Utility-first, muy flexible
- ✅ Muy popular y mantenido
- ⚠️ Requiere configuración de build
- ⚠️ Curva de aprendizaje

**Recomendación**: Considerar cuando se migre a framework JS con bundler.

---

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile First */
/* Default: mobile (< 640px) */

/* Tablet */
@media (min-width: 640px) {
  /* ... */
}

/* Desktop */
@media (min-width: 1024px) {
  /* ... */
}

/* Large Desktop */
@media (min-width: 1280px) {
  /* ... */
}
```

### Adaptaciones Responsive

1. **Mobile**:
   - Formulario en una columna
   - Sidebar colapsable
   - Botones de tamaño táctil

2. **Tablet**:
   - Dos columnas en dashboard
   - Formulario optimizado

3. **Desktop**:
   - Layout completo
   - Sidebar fijo
   - Grid de proyectos

---

## ✅ Ventajas de esta Arquitectura Frontend

1. **Modularidad**: Componentes reutilizables y organizados
2. **Mantenibilidad**: Código separado por responsabilidades
3. **Escalabilidad**: Fácil agregar nuevas páginas/componentes
4. **Performance**: Ligero, sin dependencias pesadas
5. **UX profesional**: Diseño moderno y consistente

---

Esta arquitectura frontend proporciona una base sólida para evolucionar hacia una aplicación completa manteniendo la simplicidad y performance.
