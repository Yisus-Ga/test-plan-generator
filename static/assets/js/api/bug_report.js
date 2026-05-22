/**
 * API client para generación de reportes de bugs formales.
 */
import { post } from './client.js';

/**
 * Genera un reporte de bug técnico a partir de una descripción informal.
 * El contexto (HU, criterios, resumen) se obtiene en el backend por test_plan_id.
 * @param {number} testPlanId - ID del Test Plan activo
 * @param {string} descripcionInformal - Descripción del bug escrita por el tester
 * @returns {Promise<{content: string}>}
 */
export async function sendBugReport(testPlanId, descripcionInformal) {
  return await post('/api/v1/reporte-bug', {
    test_plan_id: testPlanId,
    descripcion_informal: descripcionInformal,
  });
}
