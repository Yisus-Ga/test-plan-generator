/**
 * Componente FormInput reutilizable.
 */
import { createElement } from '../utils/dom.js';

export class FormInput {
  constructor({
    id,
    label,
    type = 'text',
    placeholder = '',
    value = '',
    required = false,
    error = null,
    helperText = null,
    onChange = null,
    onBlur = null,
    maxLength = null,
    rows = null
  }) {
    this.id = id;
    this.label = label;
    this.type = type;
    this.placeholder = placeholder;
    this.value = value;
    this.required = required;
    this.error = error;
    this.helperText = helperText;
    this.onChange = onChange;
    this.onBlur = onBlur;
    this.maxLength = maxLength;
    this.rows = rows;
    this.inputElement = null;
  }
  
  render() {
    const container = createElement('div', { className: 'form-group' });
    
    // Label
    const labelEl = createElement('label', {
      htmlFor: this.id,
      className: 'form-label'
    });
    
    const labelText = document.createTextNode(this.label);
    labelEl.appendChild(labelText);
    
    if (this.required) {
      const requiredSpan = createElement('span', {
        className: 'text-error',
        textContent: ' *'
      });
      labelEl.appendChild(requiredSpan);
    }
    
    container.appendChild(labelEl);
    
    // Input o Textarea
    const inputTag = this.rows ? 'textarea' : 'input';
    const inputAttrs = {
      id: this.id,
      className: `form-input ${this.error ? 'form-input-error' : ''}`.trim(),
      placeholder: this.placeholder,
      value: this.value,
      required: this.required
    };
    
    if (this.rows) {
      inputAttrs.rows = this.rows;
    } else {
      inputAttrs.type = this.type;
    }
    
    if (this.maxLength) {
      inputAttrs.maxLength = this.maxLength;
    }
    
    const input = createElement(inputTag, inputAttrs);
    this.inputElement = input;
    
    if (this.onChange) {
      input.addEventListener('input', (e) => {
        this.value = e.target.value;
        if (this.onChange) this.onChange(e.target.value);
      });
    }
    
    if (this.onBlur) {
      input.addEventListener('blur', (e) => {
        if (this.onBlur) this.onBlur(e.target.value);
      });
    }
    
    container.appendChild(input);
    
    // Error message
    if (this.error) {
      const errorEl = createElement('span', {
        className: 'form-error',
        textContent: this.error
      });
      container.appendChild(errorEl);
    }
    
    // Helper text
    if (this.helperText && !this.error) {
      const helperEl = createElement('span', {
        className: 'form-helper',
        textContent: this.helperText
      });
      container.appendChild(helperEl);
    }
    
    return container;
  }
  
  setError(error) {
    this.error = error;
    // Actualizar visualmente si el elemento ya está renderizado
    if (this.inputElement) {
      if (error) {
        this.inputElement.classList.add('form-input-error');
      } else {
        this.inputElement.classList.remove('form-input-error');
      }
    }
  }
  
  getValue() {
    return this.inputElement ? this.inputElement.value : this.value;
  }
}
