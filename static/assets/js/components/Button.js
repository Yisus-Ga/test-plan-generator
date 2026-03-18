/**
 * Componente Button reutilizable.
 */
import { createElement } from '../utils/dom.js';

export class Button {
  constructor({
    text,
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    onClick = null,
    className = ''
  }) {
    this.text = text;
    this.variant = variant;
    this.size = size;
    this.disabled = disabled;
    this.loading = loading;
    this.onClick = onClick;
    this.className = className;
    this.element = null;
  }
  
  render() {
    const button = createElement('button', {
      className: `btn btn-${this.variant} btn-${this.size} ${this.className}`.trim(),
      disabled: this.disabled || this.loading,
      type: 'button'
    });
    
    if (this.loading) {
      button.innerHTML = `
        <span class="spinner"></span>
        <span>Cargando...</span>
      `;
    } else {
      button.textContent = this.text;
    }
    
    if (this.onClick) {
      button.addEventListener('click', this.onClick);
    }
    
    this.element = button;
    return button;
  }
  
  setDisabled(disabled) {
    this.disabled = disabled;
    if (this.element) {
      this.element.disabled = disabled || this.loading;
    }
  }
  
  setLoading(loading) {
    this.loading = loading;
    if (this.element) {
      this.element.disabled = this.disabled || loading;
      if (loading) {
        this.element.innerHTML = `
          <span class="spinner"></span>
          <span>Cargando...</span>
        `;
      } else {
        this.element.textContent = this.text;
      }
    }
  }
}
