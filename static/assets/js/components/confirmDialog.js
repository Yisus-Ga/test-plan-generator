/**
 * Dialog de confirmación — reemplaza confirm() nativo.
 * Retorna Promise<boolean>: true si el usuario confirmó, false si canceló.
 *
 * Opciones:
 *   title       — título del dialog (opcional)
 *   message     — texto de la pregunta (soporta \n como salto de línea)
 *   confirmText — texto del botón de confirmar (default: 'Confirmar')
 *   cancelText  — texto del botón de cancelar (default: 'Cancelar')
 *   variant     — variante del botón de acción: 'danger' | 'warning' | 'success' (default: 'danger')
 */
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

export function showConfirm({
  title,
  message,
  confirmText = 'Confirmar',
  cancelText = 'Cancelar',
  variant = 'danger',
}) {
  return new Promise((resolve) => {
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.innerHTML = `
      <div class="confirm-dialog">
        ${title ? `<h4 class="confirm-title">${escapeHtml(title)}</h4>` : ''}
        <p class="confirm-message">${escapeHtml(message)}</p>
        <div class="confirm-actions">
          <button class="btn btn-secondary confirm-cancel">${escapeHtml(cancelText)}</button>
          <button class="btn btn-${variant} confirm-ok">${escapeHtml(confirmText)}</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    const close = (result) => { overlay.remove(); resolve(result); };

    overlay.querySelector('.confirm-ok').addEventListener('click', () => close(true));
    overlay.querySelector('.confirm-cancel').addEventListener('click', () => close(false));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(false); });
  });
}
