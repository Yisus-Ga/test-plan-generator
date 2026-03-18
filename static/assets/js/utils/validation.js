/**
 * Utilidades de validación de formularios.
 */
import { config } from '../config.js';

export const validators = {
  /**
   * Valida el ID de la Historia de Usuario
   */
  userStoryId(value) {
    if (!value || value.trim().length === 0) {
      return { valid: false, error: 'El ID es requerido' };
    }
    
    const trimmed = value.trim();
    
    if (trimmed.length < config.validation.minIdLength) {
      return { 
        valid: false, 
        error: `El ID debe tener al menos ${config.validation.minIdLength} caracteres` 
      };
    }
    
    if (trimmed.length > config.validation.maxIdLength) {
      return { 
        valid: false, 
        error: `El ID no puede exceder ${config.validation.maxIdLength} caracteres` 
      };
    }
    
    // Validar formato básico (ej: AER25-101)
    if (!/^[A-Za-z0-9_-]+$/.test(trimmed)) {
      return { 
        valid: false, 
        error: 'El ID solo puede contener letras, números, guiones y guiones bajos' 
      };
    }
    
    return { valid: true };
  },
  
  /**
   * Valida el título de la HU
   */
  title(value) {
    if (!value || value.trim().length === 0) {
      return { valid: false, error: 'El título es requerido' };
    }
    
    const trimmed = value.trim();
    
    if (trimmed.length < config.validation.minTitleLength) {
      return { 
        valid: false, 
        error: `El título debe tener al menos ${config.validation.minTitleLength} caracteres` 
      };
    }
    
    if (trimmed.length > config.validation.maxTitleLength) {
      return { 
        valid: false, 
        error: `El título no puede exceder ${config.validation.maxTitleLength} caracteres` 
      };
    }
    
    return { valid: true };
  },
  
  /**
   * Valida la descripción
   */
  description(value) {
    if (!value || value.trim().length === 0) {
      return { valid: false, error: 'La descripción es requerida' };
    }
    
    const trimmed = value.trim();
    
    if (trimmed.length < config.validation.minDescriptionLength) {
      return { 
        valid: false, 
        error: `La descripción debe tener al menos ${config.validation.minDescriptionLength} caracteres` 
      };
    }
    
    if (trimmed.length > config.validation.maxDescriptionLength) {
      return { 
        valid: false, 
        error: `La descripción no puede exceder ${config.validation.maxDescriptionLength} caracteres` 
      };
    }
    
    return { valid: true };
  },
  
  /**
   * Valida los criterios de aceptación
   */
  acceptanceCriteria(value) {
    if (!value || value.trim().length === 0) {
      return { 
        valid: false, 
        error: 'Debe agregar al menos un criterio de aceptación' 
      };
    }
    
    // Separar por líneas y filtrar vacíos
    const criteria = value
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);
    
    if (criteria.length < config.validation.minAcceptanceCriteria) {
      return { 
        valid: false, 
        error: `Debe agregar al menos ${config.validation.minAcceptanceCriteria} criterio de aceptación` 
      };
    }

    // ✅ A partir de aquí no se valida la longitud mínima de cada criterio.
    // Solo se requiere que exista al menos un criterio no vacío.

    return { valid: true };
  }
};

/**
 * Valida todo el formulario
 */
export function validateForm(formData) {
  const errors = {};
  
  const idValidation = validators.userStoryId(formData.hu_id);
  if (!idValidation.valid) errors.hu_id = idValidation.error;
  
  const titleValidation = validators.title(formData.title);
  if (!titleValidation.valid) errors.title = titleValidation.error;
  
  const descValidation = validators.description(formData.description);
  if (!descValidation.valid) errors.description = descValidation.error;
  
  const acValidation = validators.acceptanceCriteria(formData.acceptance_criteria);
  if (!acValidation.valid) errors.acceptance_criteria = acValidation.error;
  
  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
}
