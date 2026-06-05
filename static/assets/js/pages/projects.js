/**
 * Página para gestión de proyectos
 */
import { listProjects, createProject, updateProject, deleteProject, toggleProjectStatus } from '../api/projects.js';
import { post } from '../api/client.js';
import { config } from '../config.js';

let projects = [];

/**
 * Inicializar página de proyectos
 */
export function initProjectsPage() {
  renderProjectsPage();
  setupEventListeners();
  loadProjects();
}

/**
 * Renderizar estructura de la página
 */
function renderProjectsPage() {
  const pageProjects = document.getElementById('page-projects');
  if (!pageProjects) return;
  
  pageProjects.innerHTML = `
    <div class="projects-container">
      <h2>Gestión de Proyectos</h2>
      
      <!-- Formulario para crear proyecto -->
      <div class="card">
        <h3>Crear Nuevo Proyecto</h3>
        <form id="project-form">
          <div class="form-group">
            <label for="project-code" class="form-label">
              Código del Proyecto
              <span class="text-error">*</span>
            </label>
            <input 
              type="text" 
              id="project-code" 
              class="form-input"
              placeholder="Ej: AER25, PROJ001"
              required
              maxlength="100"
            />
            <small class="form-help">Código único que identifica al proyecto</small>
          </div>
          
          <div class="form-group">
            <label for="project-name" class="form-label">
              Nombre del Proyecto
              <span class="text-error">*</span>
            </label>
            <input 
              type="text" 
              id="project-name" 
              class="form-input"
              placeholder="Ej: Proyecto AEROMAN"
              required
              maxlength="200"
            />
          </div>
          
          <div class="form-group">
            <label for="project-description" class="form-label">
              Descripción
            </label>
            <textarea 
              id="project-description" 
              class="form-textarea"
              placeholder="Descripción del proyecto (opcional)"
              maxlength="1000"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="submit" id="btn-create-project" class="btn btn-primary">Crear Proyecto</button>
            <button type="button" id="btn-clear-form" class="btn btn-secondary">Limpiar</button>
          </div>
          
          <div id="project-status"></div>
        </form>
      </div>
      
      <!-- Lista de proyectos existentes -->
      <div class="card" style="margin-top: var(--spacing-lg);">
        <h3>Proyectos Existentes</h3>
        <div id="projects-list">
          <div class="loading">Cargando proyectos...</div>
        </div>
      </div>
    </div>
  `;
  
  pageProjects.style.display = 'block';
}

/**
 * Configurar event listeners
 */
function setupEventListeners() {
  // Esperar un momento para que el DOM se renderice
  setTimeout(() => {
    const form = document.getElementById('project-form');
    const clearBtn = document.getElementById('btn-clear-form');
    
    if (form) {
      form.addEventListener('submit', handleCreateProject);
      console.log('Formulario de proyecto configurado');
    } else {
      console.error('project-form not found');
    }
    
    if (clearBtn) {
      clearBtn.addEventListener('click', clearForm);
    } else {
      console.error('btn-clear-form not found');
    }
  }, 100);
}

/**
 * Cargar proyectos desde la API
 */
async function loadProjects() {
  const listEl = document.getElementById('projects-list');
  if (!listEl) return;
  
  try {
    listEl.innerHTML = '<div class="loading">Cargando proyectos...</div>';
    
    projects = await listProjects();
    
    if (projects.length === 0) {
      listEl.innerHTML = '<div class="empty-state">No hay proyectos creados aún</div>';
      return;
    }
    
    renderProjectsList();
  } catch (error) {
    console.error('Error cargando proyectos:', error);
    listEl.innerHTML = `
      <div class="error">
        Error al cargar proyectos: ${error.message}
      </div>
    `;
  }
}

/**
 * Renderizar lista de proyectos
 */
function renderProjectsList() {
  const listEl = document.getElementById('projects-list');
  if (!listEl) return;
  
  const escapeJs = (str) => {
    if (!str) return '';
    return String(str)
      .replace(/\\/g, '\\\\')
      .replace(/'/g, "\\'")
      .replace(/"/g, '\\"')
      .replace(/\n/g, '\\n')
      .replace(/\r/g, '\\r');
  };

  listEl.innerHTML = projects.map(project => {
    const isActive = project.is_active !== false;
    const badgeHtml = isActive
      ? `<span class="project-status-badge project-status-active">Activo</span>`
      : `<span class="project-status-badge project-status-inactive">Inactivo</span>`;
    const toggleLabel = isActive ? 'Inactivar' : 'Reactivar';
    const toggleClass = isActive ? 'btn-warning' : 'btn-success';

    return `
    <div class="project-card" style="padding: var(--spacing-md); border-bottom: 1px solid var(--border);" data-project-id="${project.id}">
      <div style="display: flex; justify-content: space-between; align-items: start;">
        <div style="flex: 1;">
          <div style="display: flex; align-items: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-xs);">
            <h4 style="margin: 0; color: var(--color-primary);">
              ${project.code} - ${project.name}
            </h4>
            ${badgeHtml}
          </div>
          ${project.description ? `<p style="margin: 0; color: var(--color-text-secondary);">${project.description}</p>` : ''}
          <small style="color: var(--color-text-secondary);">
            Creado: ${formatDate(project.created_at)}
          </small>
        </div>
        <div style="margin-left: var(--spacing-md); display: flex; gap: var(--spacing-xs); flex-wrap: wrap; justify-content: flex-end;">
          <button
            class="btn btn-primary btn-sm"
            onclick="window.editProjectHandler(${project.id}, '${escapeJs(project.code)}', '${escapeJs(project.name)}', '${escapeJs(project.description)}')"
            title="Editar proyecto"
          >Editar</button>
          <button
            class="btn ${toggleClass} btn-sm"
            onclick="window.toggleProjectStatusHandler(${project.id}, '${escapeJs(project.code)}')"
            title="${toggleLabel} proyecto"
          >${toggleLabel}</button>
          <button
            class="btn btn-danger btn-sm"
            onclick="window.deleteProjectHandler(${project.id}, '${escapeJs(project.code)}')"
            title="Eliminar proyecto"
          >Eliminar</button>
        </div>
      </div>
    </div>
  `;
  }).join('');
}

/**
 * Manejar creación de proyecto
 */
async function handleCreateProject(e) {
  e.preventDefault();
  
  const code = document.getElementById('project-code').value.trim();
  const name = document.getElementById('project-name').value.trim();
  const description = document.getElementById('project-description').value.trim();
  const statusEl = document.getElementById('project-status');
  const submitBtn = document.getElementById('btn-create-project');
  
  // Validación básica
  if (!code || !name) {
    setProjectStatus('Por favor, completa todos los campos obligatorios', 'error');
    return;
  }
  
  // Deshabilitar botón
  submitBtn.disabled = true;
  setProjectStatus('Creando proyecto...', 'loading');
  
  try {
    const newProject = await createProject({
      code: code,
      name: name,
      description: description || null
    });
    
    setProjectStatus('Proyecto creado exitosamente', 'success');
    
    // Limpiar formulario
    clearForm();
    
    // Recargar lista
    await loadProjects();
    
    // Recargar proyectos en la página de generación si está activa
    if (window.reloadProjectsInGenerator) {
      window.reloadProjectsInGenerator();
    }
    
  } catch (error) {
    console.error('Error creando proyecto:', error);
    setProjectStatus('Error al crear proyecto: ' + (error.message || 'Error desconocido'), 'error');
  } finally {
    submitBtn.disabled = false;
  }
}

/**
 * Limpiar formulario
 */
function clearForm() {
  document.getElementById('project-code').value = '';
  document.getElementById('project-name').value = '';
  document.getElementById('project-description').value = '';
  setProjectStatus('', 'info');
}

/**
 * Mostrar estado del formulario
 */
function setProjectStatus(message, type = 'info') {
  const statusEl = document.getElementById('project-status');
  if (!statusEl) return;
  
  statusEl.textContent = message;
  statusEl.className = type;
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

/**
 * Escapar HTML para prevenir XSS
 */
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Manejar edición de proyecto
 */
window.editProjectHandler = function(projectId, projectCode, projectName, projectDescription) {
  // Crear modal de edición
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  `;
  
  modal.innerHTML = `
    <div class="card" style="max-width: 500px; width: 90%; max-height: 90vh; overflow-y: auto;">
      <h3>Editar Proyecto: ${projectCode}</h3>
      <form id="edit-project-form">
        <div class="form-group">
          <label for="edit-project-name" class="form-label">
            Nombre del Proyecto
            <span class="text-error">*</span>
          </label>
          <input 
            type="text" 
            id="edit-project-name" 
            class="form-input"
            value="${escapeHtml(projectName || '')}"
            required
            maxlength="200"
          />
        </div>
        
        <div class="form-group">
          <label for="edit-project-description" class="form-label">
            Descripción
          </label>
          <textarea 
            id="edit-project-description" 
            class="form-textarea"
            maxlength="1000"
            rows="3"
          >${escapeHtml(projectDescription || '')}</textarea>
        </div>
        
        <div class="form-actions">
          <button type="submit" id="btn-save-project" class="btn btn-primary">Guardar Cambios</button>
          <button type="button" id="btn-cancel-edit" class="btn btn-secondary">Cancelar</button>
        </div>
        
        <div id="edit-project-status"></div>
      </form>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  const form = modal.querySelector('#edit-project-form');
  const cancelBtn = modal.querySelector('#btn-cancel-edit');
  const statusEl = modal.querySelector('#edit-project-status');
  
  // Cerrar modal
  const closeModal = () => {
    document.body.removeChild(modal);
  };
  
  cancelBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
  
  // Manejar envío
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('edit-project-name').value.trim();
    const description = document.getElementById('edit-project-description').value.trim();
    const saveBtn = document.getElementById('btn-save-project');
    
    if (!name) {
      statusEl.textContent = 'El nombre es obligatorio';
      statusEl.className = 'error';
      return;
    }
    
    saveBtn.disabled = true;
    statusEl.textContent = 'Guardando cambios...';
    statusEl.className = 'loading';
    
    try {
      await updateProject(projectId, {
        name: name,
        description: description || null
      });
      
      statusEl.textContent = 'Proyecto actualizado exitosamente';
      statusEl.className = 'success';
      
      // Cerrar modal después de un momento
      setTimeout(() => {
        closeModal();
        loadProjects();
        // Recargar proyectos en la página de generación si está activa
        if (window.reloadProjectsInGenerator) {
          window.reloadProjectsInGenerator();
        }
      }, 1000);
      
    } catch (error) {
      console.error('Error actualizando proyecto:', error);
      statusEl.textContent = 'Error al actualizar proyecto: ' + error.message;
      statusEl.className = 'error';
      saveBtn.disabled = false;
    }
  });
};

/**
 * Alternar estado activo/inactivo de un proyecto
 */
window.toggleProjectStatusHandler = async function(projectId, projectCode) {
  try {
    const updated = await toggleProjectStatus(projectId);
    const action = updated.is_active ? 'activado' : 'inactivado';
    const listEl = document.getElementById('projects-list');
    if (listEl) {
      const msg = document.createElement('div');
      msg.className = 'success';
      msg.textContent = `Proyecto "${projectCode}" ${action} exitosamente`;
      msg.style.marginBottom = 'var(--spacing-md)';
      listEl.insertBefore(msg, listEl.firstChild);
      setTimeout(() => msg.remove(), 3000);
    }
    await loadProjects();
    if (window.reloadProjectsInGenerator) window.reloadProjectsInGenerator();
  } catch (error) {
    alert('Error al cambiar estado del proyecto: ' + error.message);
  }
};

/**
 * Manejar eliminación de proyecto
 */
window.deleteProjectHandler = async function(projectId, projectCode) {
  if (!confirm(`¿Estás seguro de que deseas eliminar el proyecto "${projectCode}"?\n\nNota: No se puede eliminar un proyecto que tenga historias de usuario asociadas.`)) {
    return;
  }
  
  try {
    await deleteProject(projectId);
    
    // Mostrar mensaje de éxito
    const listEl = document.getElementById('projects-list');
    if (listEl) {
      const statusDiv = document.createElement('div');
      statusDiv.className = 'success';
      statusDiv.textContent = `Proyecto "${projectCode}" eliminado exitosamente`;
      statusDiv.style.marginBottom = 'var(--spacing-md)';
      listEl.insertBefore(statusDiv, listEl.firstChild);
      
      // Remover el mensaje después de 3 segundos
      setTimeout(() => {
        statusDiv.remove();
      }, 3000);
    }
    
    // Recargar lista
    await loadProjects();
    
    // Recargar proyectos en la página de generación si está activa
    if (window.reloadProjectsInGenerator) {
      window.reloadProjectsInGenerator();
    }
    
  } catch (error) {
    console.error('Error eliminando proyecto:', error);
    alert('Error al eliminar proyecto: ' + error.message);
  }
};
