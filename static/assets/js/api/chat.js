/**
 * API client para Chat con contexto del Test Plan.
 */
import { post } from './client.js';

/**
 * Envía mensajes al chat y obtiene la respuesta del modelo.
 * @param {number} testPlanId - ID del Test Plan (contexto)
 * @param {Array<{role: 'user'|'assistant', content: string}>} messages - Historial de mensajes
 * @returns {Promise<{content: string}>}
 */
export async function sendChatMessage(testPlanId, messages) {
  return await post('/api/v1/chat', { test_plan_id: testPlanId, messages });
}
