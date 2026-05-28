"""
Contexto de estándares ISO para inyección en prompts de IA.
ISO/IEC 25000 (SQuaRE) e ISO/IEC/IEEE 29119.
"""

ISO_25010_CHARACTERISTICS = """
## Marco de Calidad ISO/IEC 25010 (SQuaRE)
Al analizar, clasificar o reportar defectos, considerá las siguientes características de calidad:

1. **Adecuación funcional**: ¿La funcionalidad cumple con lo especificado? (completitud, corrección, pertinencia)
2. **Eficiencia de desempeño**: ¿Los tiempos de respuesta y uso de recursos son aceptables?
3. **Compatibilidad**: ¿Coexiste e interopera correctamente con otros sistemas o componentes?
4. **Usabilidad**: ¿El usuario puede operar el sistema de forma eficaz, eficiente y satisfactoria?
5. **Fiabilidad**: ¿El sistema opera sin fallos bajo condiciones normales? (madurez, disponibilidad, tolerancia a fallos, recuperabilidad)
6. **Seguridad**: ¿Protege la información y los datos? ¿Controla el acceso correctamente? (confidencialidad, integridad, no repudio, autenticidad)
7. **Mantenibilidad**: ¿Puede ser modificado de forma eficaz y eficiente? (modularidad, reusabilidad, analizabilidad, modificabilidad, capacidad de prueba)
8. **Portabilidad**: ¿Puede ser trasladado a otro entorno de hardware, software u operacional?
"""

ISO_29119_TEST_PLAN_STRUCTURE = """
## Estructura de Plan de Pruebas según ISO/IEC/IEEE 29119-3
El plan de pruebas debe contemplar los siguientes elementos obligatorios del estándar:

1. **Objetivo de prueba**: Qué se quiere verificar y por qué.
2. **Alcance**: Funcionalidades incluidas y excluidas del plan.
3. **Criterios de entrada**: Condiciones previas necesarias para comenzar las pruebas.
4. **Criterios de salida**: Condiciones que determinan que las pruebas están completas.
5. **Niveles de prueba aplicables**: Unitaria, Integración, Sistema, Aceptación.
6. **Técnicas de diseño de pruebas** (ISO 29119-4):
   - Basadas en especificación (caja negra): partición de equivalencia, análisis de valores límite, tabla de decisión.
   - Basadas en estructura (caja blanca): cobertura de sentencias, ramas, condiciones.
   - Basadas en experiencia: pruebas exploratorias, basadas en defectos.
7. **Clasificación de riesgo**: Alta / Media / Baja según impacto en el negocio y probabilidad de fallo.
8. **Tipos de prueba requeridos**: Funcionales, No funcionales (rendimiento, seguridad, usabilidad), Regresión, Compatibilidad.
9. **Estimación de esfuerzo**: Número de casos por prioridad y nivel de prueba.
10. **Notas relevantes**: Dependencias, supuestos, restricciones o riesgos identificados.
"""
