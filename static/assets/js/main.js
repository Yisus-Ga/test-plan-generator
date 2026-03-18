/**
 * Archivo principal de la aplicación frontend con router.
 */
import { router } from './router.js';
import { initGeneratorPage } from './pages/generator.js';
import { initHistoryPage } from './pages/history.js';
import { initProjectsPage } from './pages/projects.js';
import { initChatModal } from './components/chatModal.js';

/**
 * Inicializar la aplicación
 */
function init() {
  console.log('Inicializando aplicación...');
  initChatModal();

  // Configurar rutas
  router.route('/', () => {
    console.log('Navegando a página de generación');
    showPage('generator');
    initGeneratorPage();
  });
  
  router.route('/history', () => {
    console.log('Navegando a página de historial');
    showPage('history');
    initHistoryPage();
  });
  
  router.route('/projects', () => {
    console.log('Navegando a página de proyectos');
    showPage('projects');
    initProjectsPage();
  });
  
  // Inicializar router
  router.init();
  console.log('Aplicación inicializada');
}

/**
 * Mostrar una página específica
 */
function showPage(pageName) {
  console.log(`Mostrando página: ${pageName}`);
  
  // Ocultar todas las páginas
  const pages = ['generator', 'history', 'projects'];
  pages.forEach(page => {
    const el = document.getElementById(`page-${page}`);
    if (el) {
      el.style.display = page === pageName ? 'block' : 'none';
      console.log(`  - page-${page}: ${el.style.display}`);
    } else {
      console.error(`  - page-${page} NOT FOUND!`);
    }
  });
  
  // Actualizar navegación activa
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    const route = link.getAttribute('data-route') || link.getAttribute('href').slice(1) || '/';
    const routeMap = {
      '/': 'generator',
      '/history': 'history',
      '/projects': 'projects'
    };
    if (routeMap[route] === pageName) {
      link.classList.add('active');
    }
  });
}

// Exportar función para recargar proyectos (usada desde projects.js)
window.reloadProjectsInGenerator = function() {
  // Si estamos en la página de generación, recargar proyectos
  if (document.getElementById('page-generator')?.style.display !== 'none') {
    // Recargar proyectos en la página de generación
    const projectCode = document.getElementById('projectCode');
    if (projectCode && window.loadProjectsInGenerator) {
      window.loadProjectsInGenerator();
    }
  }
};

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
