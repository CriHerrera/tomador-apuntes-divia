# Requisitos: Tomador Apuntes Divia

**Definido:** 2026-05-04
**Valor principal:** Convertir audio hablado en vivo en documentos útiles y estructurados sin que el usuario tenga que tomar apuntes durante la sesión.

## Requisitos v1

### Sesión

- [ ] **SESS-01**: El usuario puede crear una nueva sesión en vivo.
- [ ] **SESS-02**: El usuario puede iniciar, pausar, reanudar y detener la captura de audio en vivo.
- [ ] **SESS-03**: El usuario puede ejecutar una sesión sin cargar una presentación.
- [ ] **SESS-04**: El usuario puede ver el estado de la sesión, tiempo transcurrido y estado de grabación/transcripción.

### Presentación

- [ ] **PRES-01**: El usuario puede cargar una presentación PDF.
- [ ] **PRES-02**: El usuario puede cargar una presentación PPTX.
- [ ] **PRES-03**: El usuario puede ver miniaturas o una lista de diapositivas después de cargar la presentación.
- [ ] **PRES-04**: El usuario puede marcar la diapositiva actual con un control de baja fricción.
- [ ] **PRES-05**: El usuario puede avanzar o retroceder diapositivas con atajos de teclado o controles prominentes.
- [ ] **PRES-06**: El sistema registra marcas de tiempo para cada cambio de diapositiva durante la sesión.

### Transcripción en Vivo

- [ ] **TRNS-01**: El sistema captura audio del micrófono durante una sesión en vivo.
- [ ] **TRNS-02**: El sistema produce texto de transcripción/subtítulos mientras se captura audio.
- [ ] **TRNS-03**: El sistema guarda segmentos de transcripción con marcas de tiempo.
- [ ] **TRNS-04**: Cuando hay una diapositiva activa, los segmentos de transcripción se asocian a esa diapositiva.
- [ ] **TRNS-05**: Cuando no existe presentación, los segmentos de transcripción se asocian a rangos de tiempo de la reunión.

### Apuntes Contextuales

- [ ] **NOTE-01**: El sistema genera apuntes/resumen por diapositiva cuando existe una presentación.
- [ ] **NOTE-02**: El sistema genera apuntes/resumen por segmento de reunión cuando no existe una presentación.
- [ ] **NOTE-03**: Los apuntes incluyen puntos importantes, explicaciones, preguntas y seguimientos.
- [ ] **NOTE-04**: Los apuntes conservan suficiente contexto de diapositiva para explicar por qué un punto pertenece a esa diapositiva.

### Exportación

- [ ] **EXPT-01**: El usuario puede exportar la transcripción/subtítulos como documento separado.
- [ ] **EXPT-02**: El usuario puede exportar los apuntes/resumen como documento separado.
- [ ] **EXPT-03**: El usuario puede revisar los documentos generados antes de exportarlos.

## Requisitos v2

### Automatización

- **AUTO-01**: El sistema puede detectar automáticamente cambios de diapositiva desde pantalla o estado de presentación.
- **AUTO-02**: El sistema puede procesar grabaciones post-evento usando el mismo pipeline de documentos.
- **AUTO-03**: El sistema puede identificar hablantes automáticamente.

### Colaboración

- **COLL-01**: Múltiples usuarios pueden colaborar en la misma sesión.
- **COLL-02**: El usuario puede compartir documentos generados mediante enlace.
- **COLL-03**: El usuario puede editar apuntes colaborativamente después de la sesión.

## Fuera de Alcance

| Funcionalidad | Razón |
|---------------|-------|
| Detección automática de cambio de diapositiva en v1 | La señalización manual es más confiable y más rápida de validar. |
| Aplicación móvil nativa | Web o escritorio primero mantiene v1 enfocada. |
| Comprensión completa de video | Audio más contexto de diapositiva es suficiente para el valor inicial. |
| Dependencia obligatoria de una presentación | Las reuniones sin presentación deben funcionar. |

## Trazabilidad

| Requisito | Fase | Estado |
|-----------|------|--------|
| SESS-01 | Fase 1 | Pendiente |
| SESS-02 | Fase 1 | Pendiente |
| SESS-03 | Fase 1 | Pendiente |
| SESS-04 | Fase 1 | Pendiente |
| PRES-01 | Fase 2 | Pendiente |
| PRES-02 | Fase 2 | Pendiente |
| PRES-03 | Fase 2 | Pendiente |
| PRES-04 | Fase 2 | Pendiente |
| PRES-05 | Fase 2 | Pendiente |
| PRES-06 | Fase 2 | Pendiente |
| TRNS-01 | Fase 3 | Pendiente |
| TRNS-02 | Fase 3 | Pendiente |
| TRNS-03 | Fase 3 | Pendiente |
| TRNS-04 | Fase 3 | Pendiente |
| TRNS-05 | Fase 3 | Pendiente |
| NOTE-01 | Fase 4 | Pendiente |
| NOTE-02 | Fase 4 | Pendiente |
| NOTE-03 | Fase 4 | Pendiente |
| NOTE-04 | Fase 4 | Pendiente |
| EXPT-01 | Fase 5 | Pendiente |
| EXPT-02 | Fase 5 | Pendiente |
| EXPT-03 | Fase 5 | Pendiente |

**Cobertura:**
- Requisitos v1: 22 en total
- Mapeados a fases: 22
- Sin mapear: 0

---
*Requisitos definidos: 2026-05-04*
*Última actualización: 2026-05-04 después de la definición inicial*
