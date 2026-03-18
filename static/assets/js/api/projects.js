/**
 * API client para Proyectos
 */
import { config } from '../config.js';
import { get, post } from './client.js';

/**
 * Listar todos los proyectos
 */
export async function listProjects() {
  return await get('/api/v1/projects/');
}

/**
 * Obtener proyecto por código
 */
export async function getProjectByCode(code) {
  return await get(`/api/v1/projects/code/${code}`);
}

/**
 * Crear un nuevo proyecto
 */
export async function createProject(projectData) {
  return await post('/api/v1/projects/', projectData);
}

/**
 * Actualizar un proyecto
 */
export async function updateProject(projectId, projectData) {
  return await fetch(`${config.API_URL}/api/v1/projects/${projectId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(projectData)
  }).then(async response => {
    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = 'Error al actualizar proyecto';
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.detail || errorMessage;
      } catch {
        errorMessage = errorText || errorMessage;
      }
      throw new Error(errorMessage);
    }
    return response.json();
  });
}

/**
 * Eliminar un proyecto
 */
export async function deleteProject(projectId) {
  const response = await fetch(`${config.API_URL}/api/v1/projects/${projectId}`, {
    method: 'DELETE'
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = 'Error al eliminar proyecto';
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.detail || errorMessage;
    } catch {
      errorMessage = errorText || errorMessage;
    }
    throw new Error(errorMessage);
  }
  
  return true;
}
