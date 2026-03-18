/**
 * Configuración centralizada de la aplicación frontend.
 */
export const config = {
  // URL base del backend - usar la misma URL que el frontend para evitar CORS
  // Se detecta dinámicamente para usar la misma URL que el navegador
  get API_URL() {
    return window.location.origin;
  },
  
  // Endpoints
  endpoints: {
    analyze: "/api/v1/analyze/",
    download: (token) => `/api/v1/download/${token}`
  },
  
  // Configuración de validación
  validation: {
    minIdLength: 3,
    maxIdLength: 100,
    minTitleLength: 5,
    maxTitleLength: 200,
    minDescriptionLength: 20,
    maxDescriptionLength: 2000,
    minAcceptanceCriteria: 1
  },
  
  // Mensajes
  messages: {
    loading: "Procesando... esto puede tardar unos segundos",
    success: "Análisis completado",
    error: "Ocurrió un error al procesar la solicitud",
    downloadSuccess: "Descarga completada",
    downloadError: "Error al descargar el archivo"
  }
};
