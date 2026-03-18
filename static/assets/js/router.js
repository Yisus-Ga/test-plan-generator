/**
 * Router simple para navegación entre páginas.
 */
class Router {
  constructor() {
    this.routes = {};
    this.currentRoute = null;
    this.init();
  }
  
  init() {
    // Detectar ruta inicial
    const path = window.location.hash.slice(1) || '/';
    this.navigate(path, false);
    
    // Escuchar cambios en hash
    window.addEventListener('hashchange', () => {
      const path = window.location.hash.slice(1) || '/';
      this.navigate(path, false);
    });
  }
  
  /**
   * Registrar una ruta
   */
  route(path, handler) {
    this.routes[path] = handler;
  }
  
  /**
   * Navegar a una ruta
   */
  navigate(path, updateHash = true) {
    if (updateHash) {
      window.location.hash = path;
    }
    
    const handler = this.routes[path];
    if (handler) {
      this.currentRoute = path;
      handler();
    } else {
      // Ruta por defecto
      const defaultHandler = this.routes['/'];
      if (defaultHandler) {
        this.currentRoute = '/';
        defaultHandler();
      }
    }
  }
  
  /**
   * Obtener ruta actual
   */
  getCurrentRoute() {
    return this.currentRoute || '/';
  }
}

// Exportar instancia singleton
export const router = new Router();
