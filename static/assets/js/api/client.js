/**
 * Cliente HTTP base para llamadas a la API.
 */
import { config } from '../config.js';

/**
 * Realiza una petición HTTP
 */
async function request(endpoint, options = {}) {
  // Usar la URL base dinámicamente para evitar problemas de CORS
  // config.API_URL es un getter que retorna window.location.origin
  const apiUrl = config.API_URL;
  const url = `${apiUrl}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  };
  
  // Para FormData, no incluir Content-Type (el navegador lo hace automáticamente)
  if (options.body instanceof FormData) {
    delete defaultOptions.headers['Content-Type'];
  }
  
  const finalOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  };
  
  try {
    const response = await fetch(url, finalOptions);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    // Intentar parsear como JSON, si falla retornar texto
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return await response.blob();
  } catch (error) {
    console.error('Error en request:', error);
    throw error;
  }
}

/**
 * GET request
 */
export function get(endpoint, options = {}) {
  return request(endpoint, {
    ...options,
    method: 'GET'
  });
}

/**
 * POST request
 */
export function post(endpoint, data, options = {}) {
  const body = data instanceof FormData ? data : JSON.stringify(data);
  
  return request(endpoint, {
    ...options,
    method: 'POST',
    body
  });
}
