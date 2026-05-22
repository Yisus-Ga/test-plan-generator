/**
 * Modal de chat compartido (Generador e Historial).
 * Se inicializa al cargar la app para que el chat esté disponible en cualquier página.
 * Incluye modo reporte de bugs independiente del historial de chat normal.
 */
import { sendChatMessage } from '../api/chat.js';
import { sendBugReport } from '../api/bug_report.js';

let chatModalEl, chatModalProject, chatModalHu, chatMessagesEl, chatInputEl, chatSendBtn;
let chatModalClose, chatModalBackdrop, chatLoadingIndicator, chatModalBody;
let bugReportBtn, bugReportBadge, bugReportExitBtn, copyToast;

let chatMessagesArray = [];
let chatContext = null;

// Estado del modo reporte
let bugReportMode = false;

// ─────────────────────────────────────────────
// Helpers de DOM
// ─────────────────────────────────────────────

function getElements() {
  chatModalEl        = document.getElementById('chatModal');
  chatModalProject   = document.getElementById('chatModalProject');
  chatModalHu        = document.getElementById('chatModalHu');
  chatMessagesEl     = document.getElementById('chatMessages');
  chatInputEl        = document.getElementById('chatInput');
  chatSendBtn        = document.getElementById('chatSendBtn');
  chatModalClose     = document.getElementById('chatModalClose');
  chatModalBackdrop  = document.getElementById('chatModalBackdrop');
  chatLoadingIndicator = document.getElementById('chatLoadingIndicator');
  chatModalBody      = document.getElementById('chatModalBody');
  bugReportBtn       = document.getElementById('bugReportBtn');
  bugReportBadge     = document.getElementById('bugReportBadge');
  bugReportExitBtn   = document.getElementById('bugReportExitBtn');
  copyToast          = document.getElementById('copyToast');
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

// ─────────────────────────────────────────────
// Modo reporte de bugs
// ─────────────────────────────────────────────

function enterBugReportMode() {
  bugReportMode = true;

  if (bugReportBadge) bugReportBadge.classList.add('visible');
  if (bugReportExitBtn) bugReportExitBtn.classList.add('visible');
  if (chatModalBody) chatModalBody.classList.add('bug-report-mode');
  if (chatInputEl) {
    chatInputEl.placeholder = 'Describe el bug o mejora encontrada...';
    chatInputEl.value = '';
    chatInputEl.style.height = 'auto';
  }

  // Mensaje introductorio en el chat
  appendChatMessage('assistant', '🐛 Modo Reporte activo. Describe la incidencia y presioná Enviar para generar el reporte formal.');
  if (chatInputEl) chatInputEl.focus();
}

function exitBugReportMode() {
  bugReportMode = false;

  if (bugReportBadge) bugReportBadge.classList.remove('visible');
  if (bugReportExitBtn) bugReportExitBtn.classList.remove('visible');
  if (chatModalBody) chatModalBody.classList.remove('bug-report-mode');
  if (chatInputEl) {
    chatInputEl.placeholder = 'Escribe una consulta sobre el test plan...';
    chatInputEl.value = '';
    chatInputEl.style.height = 'auto';
  }
  if (chatInputEl) chatInputEl.focus();
}

function appendBugReportCard(reportContent) {
  if (!chatMessagesEl) return;

  const wrapper = document.createElement('div');
  wrapper.className = 'chat-message assistant';

  const card = document.createElement('pre');
  card.className = 'bug-report-card';
  card.textContent = reportContent;

  const actions = document.createElement('div');
  actions.className = 'bug-report-card-actions';

  const copyBtn = document.createElement('button');
  copyBtn.className = 'btn-copy-report';
  copyBtn.innerHTML = '📋 Copiar reporte';
  copyBtn.addEventListener('click', () => copyReportToClipboard(reportContent));

  const newBtn = document.createElement('button');
  newBtn.className = 'btn-new-report';
  newBtn.innerHTML = '🔄 Nuevo reporte';
  newBtn.addEventListener('click', () => {
    if (chatInputEl) {
      chatInputEl.value = '';
      chatInputEl.style.height = 'auto';
      chatInputEl.focus();
    }
  });

  actions.appendChild(copyBtn);
  actions.appendChild(newBtn);
  wrapper.appendChild(card);
  wrapper.appendChild(actions);
  chatMessagesEl.appendChild(wrapper);
  chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
}

function copyReportToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showCopyToast();
  }).catch(() => {
    // Fallback para entornos sin Clipboard API
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showCopyToast();
  });
}

function showCopyToast() {
  if (!copyToast) return;
  copyToast.classList.add('show');
  setTimeout(() => copyToast.classList.remove('show'), 2200);
}

// ─────────────────────────────────────────────
// Envío de mensajes
// ─────────────────────────────────────────────

async function handleChatSend() {
  if (!chatContext || !chatInputEl || !chatSendBtn) return;
  const text = chatInputEl.value.trim();
  if (!text) return;

  if (bugReportMode) {
    await handleBugReportSend(text);
  } else {
    await handleNormalChatSend(text);
  }
}

async function handleNormalChatSend(text) {
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

async function handleBugReportSend(text) {
  appendChatMessage('user', text);
  chatInputEl.value = '';
  chatInputEl.style.height = 'auto';
  chatSendBtn.disabled = true;
  showChatLoading();

  try {
    const res = await sendBugReport(chatContext.testPlanId, text);
    const content = (res && res.content) ? res.content : 'No se recibió respuesta.';
    appendBugReportCard(content);
  } catch (err) {
    const msg = err.message || 'Error al generar el reporte de bug.';
    appendChatMessage('assistant', `⚠️ ${msg}`);
  } finally {
    hideChatLoading();
    chatSendBtn.disabled = false;
    if (chatInputEl) chatInputEl.focus();
  }
}

// ─────────────────────────────────────────────
// Apertura del modal
// ─────────────────────────────────────────────

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

  // Salir del modo reporte si estaba activo de una sesión anterior
  exitBugReportMode();

  chatModalEl.classList.add('is-open');
  chatModalEl.setAttribute('aria-hidden', 'false');
  if (chatInputEl) chatInputEl.focus();
}

// ─────────────────────────────────────────────
// Inicialización
// ─────────────────────────────────────────────

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

  if (bugReportBtn) bugReportBtn.addEventListener('click', enterBugReportMode);
  if (bugReportExitBtn) bugReportExitBtn.addEventListener('click', exitBugReportMode);

  window.openChatModalWithContext = openChatModalWithContext;
}
