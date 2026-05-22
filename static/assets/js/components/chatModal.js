/**
 * Modal de chat compartido (Generador e Historial).
 * Se inicializa al cargar la app para que el chat esté disponible en cualquier página.
 */
import { sendChatMessage } from '../api/chat.js';

let chatModalEl, chatModalProject, chatModalHu, chatMessagesEl, chatInputEl, chatSendBtn;
let chatModalClose, chatModalBackdrop, chatLoadingIndicator;
let chatMessagesArray = [];
let chatContext = null;

function getElements() {
  chatModalEl = document.getElementById('chatModal');
  chatModalProject = document.getElementById('chatModalProject');
  chatModalHu = document.getElementById('chatModalHu');
  chatMessagesEl = document.getElementById('chatMessages');
  chatInputEl = document.getElementById('chatInput');
  chatSendBtn = document.getElementById('chatSendBtn');
  chatModalClose = document.getElementById('chatModalClose');
  chatModalBackdrop = document.getElementById('chatModalBackdrop');
  chatLoadingIndicator = document.getElementById('chatLoadingIndicator');
}

function appendChatMessage(role, content) {
  if (!chatMessagesEl) return;
  const div = document.createElement('div');
  div.className = `chat-message ${role}`;
  div.textContent = content;
  chatMessagesEl.appendChild(div);
  chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
}

function showChatLoading() {
  if (chatLoadingIndicator) {
    chatLoadingIndicator.style.display = 'flex';
    if (chatMessagesEl) chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
  }
}

function hideChatLoading() {
  if (chatLoadingIndicator) chatLoadingIndicator.style.display = 'none';
}

function closeChatModal() {
  if (!chatModalEl) return;
  chatModalEl.classList.remove('is-open');
  chatModalEl.setAttribute('aria-hidden', 'true');
}

/**
 * Abre el modal de chat con el contexto indicado.
 * @param {Object} context - { testPlanId: number, projectLabel: string, huId: string, huTitle: string }
 */
function openChatModalWithContext(context) {
  if (!context || context.testPlanId == null) return;
  getElements();
  if (!chatModalEl || !chatModalProject || !chatModalHu) return;

  chatContext = context;
  chatModalProject.textContent = context.projectLabel || 'Proyecto';
  chatModalHu.textContent = [context.huId || '—', context.huTitle || '—'].filter(Boolean).join(' | ');
  chatMessagesEl.innerHTML = '';
  chatMessagesArray = [];
  if (chatInputEl) chatInputEl.value = '';
  hideChatLoading();

  chatModalEl.classList.add('is-open');
  chatModalEl.setAttribute('aria-hidden', 'false');
  if (chatInputEl) chatInputEl.focus();
}

async function handleChatSend() {
  if (!chatContext || !chatInputEl || !chatSendBtn) return;
  const text = chatInputEl.value.trim();
  if (!text) return;

  chatMessagesArray.push({ role: 'user', content: text });
  appendChatMessage('user', text);
  chatInputEl.value = '';
  chatInputEl.style.height = 'auto';
  chatSendBtn.disabled = true;
  showChatLoading();

  try {
    const res = await sendChatMessage(chatContext.testPlanId, chatMessagesArray);
    const content = (res && res.content) ? res.content : 'No se recibió respuesta.';
    chatMessagesArray.push({ role: 'assistant', content });
    appendChatMessage('assistant', content);
  } catch (err) {
    const msg = err.message || 'Error al enviar el mensaje.';
    chatMessagesArray.push({ role: 'assistant', content: msg });
    appendChatMessage('assistant', msg);
  } finally {
    hideChatLoading();
    chatSendBtn.disabled = false;
    if (chatInputEl) chatInputEl.focus();
  }
}

/**
 * Inicializa el modal de chat (listeners y API global).
 * Llamar una vez al cargar la aplicación.
 */
export function initChatModal() {
  getElements();
  if (!chatModalEl || !chatSendBtn) return;

  if (chatModalClose) chatModalClose.addEventListener('click', closeChatModal);
  if (chatModalBackdrop) chatModalBackdrop.addEventListener('click', closeChatModal);
  chatSendBtn.addEventListener('click', handleChatSend);
  if (chatInputEl) {
    chatInputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleChatSend();
      }
    });
  }

  window.openChatModalWithContext = openChatModalWithContext;
}
