/**
 * Página de historial de Test Plans.
 */
import { config } from '../config.js';
import { get } from '../api/client.js';
import { listProjects } from '../api/projects.js';
import { showToast } from '../components/toast.js';
import { showConfirm } from '../components/confirmDialog.js';

let testPlans = [];
let filteredTestPlans = [];
let projects = [];

/**
 * Inicializar página de historial
 */
export function initHistoryPage() {
  renderHistoryPage();
  setupEventListeners();
  loadProjects();
  loadTestPlans();
}

/**
 * Renderizar estructura de la página
 */
function renderHistoryPage() {
  const pageHistory = document.getElementById('page-history');
  if (!pageHistory) {
    console.error('page-history element not found');
    return;
  }
  
  pageHistory.innerHTML = `
    <div class="history-container">
      <h2>Historial de Test Plans</h2>
      
      <!-- Filtros -->
      <div class="filters-card card">
        <h3>Filtros</h3>
        <div class="filters-grid">
          <div class="form-group">
            <label for="filter-project" class="form-label">Proyecto</label>
            <select id="filter-project" class="form-input">
              <option value="">Todos los proyectos</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="filter-story-id" class="form-label">ID de HU</label>
            <input type="text" id="filter-story-id" class="form-input" placeholder="Ej: AER25-101">
          </div>
          
          <div class="form-group">
            <label for="filter-search" class="form-label">Búsqueda</label>
            <input type="text" id="filter-search" class="form-input" placeholder="Buscar en títulos...">
          </div>
          
          <div class="form-group">
            <label for="filter-date-from" class="form-label">Fecha Desde</label>
            <input type="date" id="filter-date-from" class="form-input">
          </div>
          
          <div class="form-group">
            <label for="filter-date-to" class="form-label">Fecha Hasta</label>
            <input type="date" id="filter-date-to" class="form-input">
          </div>
        </div>
        
        <div class="filters-actions">
          <button id="btn-apply-filters" class="btn btn-primary">Aplicar Filtros</button>
          <button id="btn-clear-filters" class="btn btn-secondary">Limpiar</button>
        </div>
      </div>
      
      <!-- Lista de Test Plans -->
      <div class="test-plans-list" id="test-plans-list">
        <div class="loading">Cargando Test Plans...</div>
      </div>
    </div>
  `;
  
  // Asegurar que la página sea visible
  pageHistory.style.display = 'block';
}

/**
 * Abrir modal de chat desde un botón de la lista (delegación de eventos)
 */
function handleListClick(e) {
  const btn = e.target.closest('.btn-chat-history');
  if (!btn || !window.openChatModalWithContext) return;
  const testPlanId = parseInt(btn.dataset.testPlanId, 10);
  const projectLabel = btn.dataset.projectName || 'Proyecto';
  const huId = btn.dataset.huId || '—';
  const huTitle = btn.dataset.huTitle || '—';
  window.openChatModalWithContext({ testPlanId, projectLabel, huId, huTitle });
}

/**
 * Configurar event listeners
 */
function setupEventListeners() {
  // Esperar un momento para que el DOM se renderice
  setTimeout(() => {
    const applyBtn = document.getElementById('btn-apply-filters');
    const clearBtn = document.getElementById('btn-clear-filters');
    const listEl = document.getElementById('test-plans-list');

    if (applyBtn) {
      applyBtn.addEventListener('click', applyFilters);
    } else {
      console.error('btn-apply-filters not found');
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', clearFilters);
    } else {
      console.error('btn-clear-filters not found');
    }

    if (listEl) {
      listEl.addEventListener('click', handleListClick);
    }

    // Enter en campos de filtro
    ['filter-project', 'filter-story-id', 'filter-search'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            applyFilters();
          }
        });
      }
    });
  }, 100);
}

/**
 * Cargar proyectos para el filtro
 */
async function loadProjects() {
  try {
    projects = await listProjects();
    const projectSelect = document.getElementById('filter-project');
    if (projectSelect && projects.length > 0) {
      // Agregar proyectos al select (mantener la opción "Todos los proyectos")
      const currentValue = projectSelect.value;
      // Limpiar opciones excepto la primera
      while (projectSelect.children.length > 1) {
        projectSelect.removeChild(projectSelect.lastChild);
      }
      // Agregar proyectos
      projects.forEach(project => {
        const option = document.createElement('option');
        option.value = project.code;
        option.textContent = `${project.code} - ${project.name}`;
        projectSelect.appendChild(option);
      });
      // Restaurar valor si existía
      if (currentValue) {
        projectSelect.value = currentValue;
      }
    }
  } catch (error) {
    console.error('Error cargando proyectos para filtro:', error);
  }
}

/**
 * Cargar Test Plans desde la API
 */
async function loadTestPlans() {
  const listEl = document.getElementById('test-plans-list');
  if (!listEl) {
    console.error('test-plans-list element not found');
    return;
  }
  
  try {
    listEl.innerHTML = '<div class="loading">Cargando Test Plans...</div>';
    
    const data = await get('/api/v1/test-plans/');
    console.log('Test Plans cargados:', data);
    
    if (!data || !Array.isArray(data)) {
      throw new Error('Formato de respuesta inválido');
    }
    
    testPlans = data;
    filteredTestPlans = data;
    
    renderTestPlansList();
  } catch (error) {
    console.error('Error cargando Test Plans:', error);
    listEl.innerHTML = `
      <div class="error">
        Error al cargar Test Plans: ${error.message || 'Error desconocido'}
      </div>
    `;
  }
}

/**
 * Escapar para uso en atributos HTML (evitar romper data-hu-title, etc.)
 */
function escapeHtmlAttr(str) {
  if (str == null) return '';
  const s = String(str);
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/**
 * Renderizar lista de Test Plans
 */
function renderTestPlansList() {
  const listEl = document.getElementById('test-plans-list');
  
  if (filteredTestPlans.length === 0) {
    listEl.innerHTML = '<div class="empty-state">No se encontraron Test Plans</div>';
    return;
  }
  
  listEl.innerHTML = filteredTestPlans.map(tp => `
    <div class="test-plan-card card" data-test-plan-id="${tp.id}">
      <div class="test-plan-header">
        <div class="test-plan-id">ID: ${tp.id}</div>
        <div class="test-plan-date">${formatDate(tp.created_at)}</div>
      </div>
      
      <div class="test-plan-body">
        <div class="test-plan-hu">
          <strong>HU:</strong> ${tp.user_story_story_id} - ${tp.user_story_title}
        </div>
        <div class="test-plan-project">
          <strong>Proyecto:</strong> ${tp.project_code} (${tp.project_name})
        </div>
        <div class="test-plan-stats">
          <span style="color: var(--color-text-secondary);">${tp.total_cases} casos de prueba</span>
        </div>
      </div>
      
      <div class="test-plan-actions" style="display: flex; align-items: center; gap: var(--spacing-xs); flex-wrap: wrap;">
        <select id="format-${tp.id}" class="form-input" style="width: auto; min-width: 120px; padding: 4px 8px;" title="Formato de descarga">
          <option value="xlsx">Excel (.xlsx)</option>
          <option value="csv">CSV</option>
          <option value="jira">Jira (CSV)</option>
          <option value="json">JSON</option>
        </select>
        <button class="btn btn-secondary btn-sm" onclick="downloadTestPlan(${tp.id})">Descargar</button>
        <button type="button" class="btn btn-secondary btn-sm btn-chat-history" data-test-plan-id="${tp.id}" data-project-name="${escapeHtmlAttr(tp.project_name)}" data-hu-id="${escapeHtmlAttr(tp.user_story_story_id)}" data-hu-title="${escapeHtmlAttr(tp.user_story_title)}" title="Chat sobre este Test Plan">💬 Chat</button>
        <button class="btn btn-danger btn-sm" onclick="deleteTestPlan(${tp.id})">Eliminar</button>
      </div>
    </div>
  `).join('');
}

/**
 * Aplicar filtros
 */
function applyFilters() {
  const projectFilter = document.getElementById('filter-project').value.trim().toLowerCase();
  const storyIdFilter = document.getElementById('filter-story-id').value.trim().toLowerCase();
  const searchFilter = document.getElementById('filter-search').value.trim().toLowerCase();
  const dateFrom = document.getElementById('filter-date-from').value;
  const dateTo = document.getElementById('filter-date-to').value;
  
  filteredTestPlans = testPlans.filter(tp => {
    // Filtro por proyecto (ahora es un select, comparar código exacto)
    if (projectFilter) {
      if (tp.project_code.toLowerCase() !== projectFilter) {
        return false;
      }
    }
    
    // Filtro por ID de HU
    if (storyIdFilter) {
      if (!tp.user_story_story_id.toLowerCase().includes(storyIdFilter)) {
        return false;
      }
    }
    
    // Búsqueda general
    if (searchFilter) {
      const searchMatch = 
        tp.user_story_story_id.toLowerCase().includes(searchFilter) ||
        tp.user_story_title.toLowerCase().includes(searchFilter) ||
        tp.project_code.toLowerCase().includes(searchFilter) ||
        tp.project_name.toLowerCase().includes(searchFilter);
      if (!searchMatch) return false;
    }
    
    // Filtro por fecha
    if (dateFrom || dateTo) {
      const tpDate = new Date(tp.created_at);
      if (dateFrom && tpDate < new Date(dateFrom)) return false;
      if (dateTo && tpDate > new Date(dateTo + 'T23:59:59')) return false;
    }
    
    return true;
  });
  
  renderTestPlansList();
}

/**
 * Limpiar filtros
 */
function clearFilters() {
  document.getElementById('filter-project').value = '';
  document.getElementById('filter-story-id').value = '';
  document.getElementById('filter-search').value = '';
  document.getElementById('filter-date-from').value = '';
  document.getElementById('filter-date-to').value = '';
  
  filteredTestPlans = testPlans;
  renderTestPlansList();
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Descargar Test Plan
 */
window.downloadTestPlan = async function(testPlanId) {
  try {
    const formatEl = document.getElementById(`format-${testPlanId}`);
    const format = formatEl ? formatEl.value : 'xlsx';

    const testPlan = await get(`/api/v1/test-plans/${testPlanId}`);
    if (!testPlan.download_token) {
      throw new Error('Token no disponible');
    }

    const url = `${config.API_URL}/api/v1/download/${testPlan.download_token}?format=${encodeURIComponent(format)}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Error al descargar');

    const blob = await response.blob();
    let filename = `test_plan_${testPlanId}.${format === 'jira' ? 'csv' : format}`;
    const contentDisposition = response.headers.get('Content-Disposition');
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '').trim();
        if (!filename.toLowerCase().endsWith('.xlsx') && !filename.toLowerCase().endsWith('.csv') && !filename.toLowerCase().endsWith('.json')) {
          filename = filename.replace(/\.[^.]+$/, '') + '.' + (format === 'jira' ? 'csv' : format);
        }
      }
    }

    const a = document.createElement('a');
    const urlObj = window.URL.createObjectURL(blob);
    a.href = urlObj;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(urlObj);
  } catch (error) {
    showToast('Error al descargar: ' + error.message, 'error');
  }
};

/**
 * Eliminar Test Plan
 */
window.deleteTestPlan = async function(testPlanId) {
  const tp = testPlans.find(t => t.id === testPlanId);
  const label = tp ? `${tp.user_story_story_id} - ${tp.user_story_title}` : `#${testPlanId}`;

  const confirmed = await showConfirm({
    title: 'Eliminar Test Plan',
    message: `¿Estás seguro que querés eliminar el Test Plan "${label}"?`,
    confirmText: 'Eliminar',
    cancelText: 'Cancelar',
    variant: 'danger',
  });

  if (!confirmed) return;

  try {
    const response = await fetch(`${config.API_URL}/api/v1/test-plans/${testPlanId}`, {
      method: 'DELETE'
    });

    if (!response.ok) {
      throw new Error('Error al eliminar Test Plan');
    }

    await loadTestPlans();
    showToast('Test Plan eliminado exitosamente', 'success');
  } catch (error) {
    showToast('Error al eliminar: ' + error.message, 'error');
  }
};
