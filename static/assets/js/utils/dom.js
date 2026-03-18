/**
 * Utilidades para manipulación del DOM.
 */

/**
 * Crea un elemento HTML con atributos
 */
export function createElement(tag, attributes = {}, textContent = null) {
  const element = document.createElement(tag);
  
  for (const [key, value] of Object.entries(attributes)) {
    if (key === 'className') {
      element.className = value;
    } else if (key === 'dataset') {
      Object.assign(element.dataset, value);
    } else if (key.startsWith('on')) {
      element.addEventListener(key.substring(2).toLowerCase(), value);
    } else {
      element.setAttribute(key, value);
    }
  }
  
  if (textContent) {
    element.textContent = textContent;
  }
  
  return element;
}

/**
 * Muestra u oculta un elemento
 */
export function toggleElement(element, show) {
  if (element) {
    element.style.display = show ? '' : 'none';
  }
}

/**
 * Agrega o remueve una clase CSS
 */
export function toggleClass(element, className, add) {
  if (element) {
    if (add) {
      element.classList.add(className);
    } else {
      element.classList.remove(className);
    }
  }
}

/**
 * Limpia el contenido de un elemento
 */
export function clearElement(element) {
  if (element) {
    element.innerHTML = '';
  }
}
