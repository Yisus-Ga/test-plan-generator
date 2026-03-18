/**
 * API client para Test Plans.
 */
import { post, get } from './client.js';
import { config } from '../config.js';

/**
 * Analiza una Historia de Usuario y genera un Test Plan
 */
export async function analyzeUserStory(formData) {
  const form = new FormData();
  form.append('hu_id', formData.hu_id);
  form.append('title', formData.title);
  form.append('description', formData.description);
  form.append('acceptance_criteria', formData.acceptance_criteria);
  form.append('project_code', formData.project_code); // Proyecto obligatorio
  
  return await post(config.endpoints.analyze, form);
}

/**
 * Descarga el Test Plan en el formato indicado.
 * @param {string} token - Token de descarga
 * @param {string} format - xlsx | csv | jira | json (default: xlsx)
 * @returns {Promise<{blob: Blob, filename: string}>}
 */
export async function downloadTestPlan(token, format = 'xlsx') {
  const url = `${config.API_URL}/api/v1/download/${token}?format=${encodeURIComponent(format)}`;
  const response = await fetch(url);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Error al descargar');
  }
  const blob = await response.blob();
  let filename = `test_plan.${format === 'jira' ? 'csv' : format}`;
  const disposition = response.headers.get('Content-Disposition');
  if (disposition) {
    const match = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
    if (match && match[1]) {
      filename = match[1].replace(/['"]/g, '').trim();
      if (!filename.toLowerCase().endsWith('.xlsx') && !filename.toLowerCase().endsWith('.csv') && !filename.toLowerCase().endsWith('.json')) {
        const ext = format === 'jira' ? 'csv' : format;
        filename = filename.replace(/\.[^.]+$/, '') + '.' + ext;
      }
    }
  }
  return { blob, filename };
}
