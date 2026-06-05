/**
 * Página de generación de Test Plans
 */
import { config } from '../config.js';
import { validateForm, validators } from '../utils/validation.js';
import { analyzeUserStory, downloadTestPlan } from '../api/test_plans.js';
import { listActiveProjects } from '../api/projects.js';

// Referencias a elementos del DOM
let huId, huTitle, huDescription, huAC, projectCode;
let analyzeBtn, downloadBtn, downloadFormat, clearBtn, chatBtn;
let statusEl, analysisEl;

// Estado de la aplicación
let currentToken = null;
let currentFilename = null;
let currentTestPlanId = null;
let fieldErrors = {};

/**
 * Inicializar página de generación
 */
export function initGeneratorPage() {
  // Obtener referencias a elementos
  projectCode = document.getElementById("projectCode");
  huId = document.getElementById("huId");
  huTitle = document.getElementById("huTitle");
  huDescription = document.getElementById("huDescription");
  huAC = document.getElementById("huAC");
  analyzeBtn = document.getElementById("analyzeBtn");
  downloadBtn = document.getElementById("downloadBtn");
  clearBtn = document.getElementById("clearBtn");
  chatBtn = document.getElementById("chatBtn");
  statusEl = document.getElementById("status");
  analysisEl = document.getElementById("analysis");
  
  // Cargar proyectos
  loadProjects();
  
  // Configurar event listeners
  setupEventListeners();
  setupChatButton();
  
  // Validar formulario inicial
  validateFormFields();
  
  // Exponer función para recargar proyectos desde otras páginas
  window.loadProjectsInGenerator = loadProjects;
}

/**
 * Cargar proyectos desde la API
 */
async function loadProjects() {
  try {
    const projects = await listActiveProjects();
    console.log('Proyectos cargados:', projects);
    
    // Limpiar opciones actuales
    projectCode.innerHTML = '<option value="">Selecciona un proyecto</option>';
    
    if (!projects || projects.length === 0) {
      projectCode.innerHTML = '<option value="">No hay proyectos disponibles</option>';
      setStatus('No hay proyectos disponibles. Crea uno primero.', 'error');
      return;
    }
    
    // Agregar proyectos
    projects.forEach(project => {
      const option = document.createElement('option');
      option.value = project.code;
      option.textContent = `${project.code} - ${project.name}`;
      projectCode.appendChild(option);
    });
    
    // Si solo hay un proyecto (AEROMAN), seleccionarlo por defecto
    if (projects.length === 1) {
      projectCode.value = projects[0].code;
      validateFormFields();
    }
  } catch (error) {
    console.error('Error cargando proyectos:', error);
    projectCode.innerHTML = '<option value="">Error al cargar proyectos</option>';
    const errorMsg = error.message || 'Error desconocido';
    console.error('Detalles del error:', errorMsg);
    if (statusEl) {
      setStatus('Error al cargar proyectos: ' + errorMsg, 'error');
    }
  }
}

/**
 * Configurar event listeners
 */
function setupEventListeners() {
  // Validación en tiempo real
  projectCode.addEventListener('change', () => {
    validateFormFields();
  });
  
  huId.addEventListener('input', () => {
    validateField('hu_id', huId.value);
    validateFormFields();
  });
  
  huTitle.addEventListener('input', () => {
    validateField('title', huTitle.value);
    validateFormFields();
  });
  
  huDescription.addEventListener('input', () => {
    validateField('description', huDescription.value);
    validateFormFields();
  });
  
  huAC.addEventListener('input', () => {
    validateField('acceptance_criteria', huAC.value);
    validateFormFields();
  });
  
  // Botón Analizar
  analyzeBtn.addEventListener('click', handleAnalyze);
  
  // Botón Descargar
  downloadBtn.addEventListener('click', handleDownload);
  
  // Botón Limpiar
  clearBtn.addEventListener('click', handleClear);
  // Botón Chat: abre modal compartido con contexto del formulario
  if (chatBtn) chatBtn.addEventListener('click', openChatFromGenerator);
}

/**
 * Validar un campo individual
 */
function validateField(fieldName, value) {
  let validation;
  
  switch(fieldName) {
    case 'hu_id':
      validation = validators.userStoryId(value);
      break;
    case 'title':
      validation = validators.title(value);
      break;
    case 'description':
      validation = validators.description(value);
      break;
    case 'acceptance_criteria':
      validation = validators.acceptanceCriteria(value);
      break;
    default:
      return;
  }
  
  if (!validation.valid) {
    fieldErrors[fieldName] = validation.error;
    showFieldError(fieldName, validation.error);
  } else {
    delete fieldErrors[fieldName];
    clearFieldError(fieldName);
  }
}

/**
 * Mostrar error de campo
 */
function showFieldError(fieldName, error) {
  const fieldMap = {
    'project_code': projectCode,
    'hu_id': huId,
    'title': huTitle,
    'description': huDescription,
    'acceptance_criteria': huAC
  };
  
  const field = fieldMap[fieldName];
  if (!field) return;
  
  // Agregar clase de error
  field.classList.add('form-input-error');
  
  // Mostrar mensaje de error si no existe
  let errorEl = field.parentElement.querySelector('.form-error');
  if (!errorEl) {
    errorEl = document.createElement('span');
    errorEl.className = 'form-error';
    field.parentElement.appendChild(errorEl);
  }
  errorEl.textContent = error;
}

/**
 * Limpiar error de campo
 */
function clearFieldError(fieldName) {
  const fieldMap = {
    'project_code': projectCode,
    'hu_id': huId,
    'title': huTitle,
    'description': huDescription,
    'acceptance_criteria': huAC
  };
  
  const field = fieldMap[fieldName];
  if (!field) return;
  
  field.classList.remove('form-input-error');
  
  const errorEl = field.parentElement.querySelector('.form-error');
  if (errorEl) {
    errorEl.remove();
  }
}

/**
 * Validar todo el formulario
 */
function validateFormFields() {
  const formData = {
    project_code: projectCode.value.trim(),
    hu_id: huId.value.trim(),
    title: huTitle.value.trim(),
    description: huDescription.value.trim(),
    acceptance_criteria: huAC.value.trim()
  };
  
  // Validar proyecto
  if (!formData.project_code) {
    analyzeBtn.disabled = true;
    return;
  }
  
  // Validar resto del formulario
  const validation = validateForm({
    hu_id: formData.hu_id,
    title: formData.title,
    description: formData.description,
    acceptance_criteria: formData.acceptance_criteria
  });
  
  analyzeBtn.disabled = !validation.valid;
}

/**
 * Manejar clic en Analizar
 */
async function handleAnalyze() {
  // Deshabilitar botones
  analyzeBtn.disabled = true;
  downloadBtn.disabled = true;
  
  // Limpiar análisis anterior
  analysisEl.innerHTML = '';
  currentToken = null;
  currentFilename = null;
  
  // Mostrar estado de carga
  setStatus(config.messages.loading, 'loading');
  
  try {
    const formData = {
      project_code: projectCode.value.trim(),
      hu_id: huId.value.trim(),
      title: huTitle.value.trim(),
      description: huDescription.value.trim(),
      acceptance_criteria: huAC.value.trim()
    };
    
    // Validar proyecto
    if (!formData.project_code) {
      setStatus('Por favor, selecciona un proyecto', 'error');
      showFieldError('project_code', 'El proyecto es obligatorio');
      return;
    }
    
    // Validar antes de enviar
    const validation = validateForm({
      hu_id: formData.hu_id,
      title: formData.title,
      description: formData.description,
      acceptance_criteria: formData.acceptance_criteria
    });
    
    if (!validation.valid) {
      setStatus('Por favor, corrija los errores en el formulario', 'error');
      Object.keys(validation.errors).forEach(field => {
        showFieldError(field, validation.errors[field]);
      });
      return;
    }
    
    // Llamar a la API
    const result = await analyzeUserStory(formData);
    
    // Guardar datos de sesión
    currentToken = result.token;
    currentFilename = result.filename || "resultado.xlsx";
    currentTestPlanId = result.test_plan_id ?? null;
    
    // Renderizar análisis
    if (typeof marked !== 'undefined') {
      analysisEl.innerHTML = marked.parse(result.analysis || "No se devolvió texto de análisis.");
    } else {
      analysisEl.textContent = result.analysis || "No se devolvió texto de análisis.";
    }
    
    // Mostrar éxito
    setStatus(config.messages.success, 'success');
    
    // Habilitar botón de descarga y chat cuando haya resultado
    if (currentToken) {
      downloadBtn.disabled = false;
      if (chatBtn && currentTestPlanId != null) chatBtn.disabled = false;
    }
    
    // Descarga automática (siempre en Excel)
    if (result.download_url || result.token) {
      try {
        const { blob, filename } = await downloadTestPlan(result.token || currentToken, 'xlsx');
        triggerDownload(blob, filename);
        setStatus(`Descarga automática iniciada (${filename})`, 'success');
      } catch (err) {
        console.error("Error en descarga automática:", err);
        setStatus("Fallo la descarga automática, puede usar el botón Descargar", 'error');
        // El botón ya está habilitado arriba
      }
    }
    
  } catch (err) {
    console.error("Error general:", err);
    setStatus(config.messages.error + ": " + (err.message || "Problema de conexión"), 'error');
    analysisEl.textContent = "No se generó análisis debido a un error.";
  } finally {
    validateFormFields();
  }
}

/**
 * Manejar clic en Descargar
 */
async function handleDownload() {
  if (!currentToken) {
    alert("No hay un resultado disponible para descargar.");
    return;
  }

  // Leer formato del combobox en el momento del clic (por si el DOM cambió)
  const formatEl = document.getElementById("downloadFormat");
  const format = formatEl ? formatEl.value : "xlsx";
  const formatLabel = formatEl && formatEl.options[formatEl.selectedIndex] ? formatEl.options[formatEl.selectedIndex].textContent : format;

  setStatus(`Preparando descarga (${formatLabel})...`, "loading");
  downloadBtn.disabled = true;

  try {
    const { blob, filename } = await downloadTestPlan(currentToken, format);
    triggerDownload(blob, filename);
    setStatus(`${config.messages.downloadSuccess} — ${filename}`, "success");
  } catch (err) {
    console.error(err);
    setStatus(`${config.messages.downloadError}: ${err.message || "problema"}`, "error");
  } finally {
    downloadBtn.disabled = false;
  }
}

/**
 * Manejar clic en Limpiar
 */
function handleClear() {
  // Limpiar inputs
  projectCode.value = '';
  huId.value = '';
  huTitle.value = '';
  huDescription.value = '';
  huAC.value = '';
  
  // Limpiar errores
  Object.keys(fieldErrors).forEach(field => {
    clearFieldError(field);
  });
  fieldErrors = {};
  
  // Limpiar estado
  currentToken = null;
  currentFilename = null;
  currentTestPlanId = null;
  analyzeBtn.disabled = true;
  downloadBtn.disabled = true;
  if (chatBtn) chatBtn.disabled = true;
  
  // Limpiar visual
  setStatus('', 'info');
  analysisEl.innerHTML = "Aquí aparecerá el análisis.";
}

/**
 * Mostrar mensaje de estado
 */
function setStatus(message, type = 'info') {
  statusEl.textContent = message;
  statusEl.className = type;
}

/**
 * Descargar un blob como archivo
 */
function triggerDownload(blob, filename) {
  const a = document.createElement("a");
  const url = window.URL.createObjectURL(blob);
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}

// --- Chat: abre el modal compartido con contexto del generador ---
function setupChatButton() {
  // El modal y sus listeners se inicializan en main.js (chatModal.js)
}

function openChatFromGenerator() {
  if (!currentTestPlanId || !window.openChatModalWithContext) return;
  const projectLabel = projectCode && projectCode.options[projectCode.selectedIndex]
    ? projectCode.options[projectCode.selectedIndex].text.trim()
    : projectCode?.value || 'Proyecto';
  const huIdVal = huId?.value?.trim() || '—';
  const huTitleVal = huTitle?.value?.trim() || '—';
  window.openChatModalWithContext({
    testPlanId: currentTestPlanId,
    projectLabel,
    huId: huIdVal,
    huTitle: huTitleVal
  });
}
