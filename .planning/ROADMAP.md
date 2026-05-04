# Roadmap: Tomador Apuntes Divia

**Creado:** 2026-05-04
**Alcance:** v1 de asistente en vivo para reuniones y presentaciones

## Resumen

5 fases | 22 requisitos v1 mapeados | Todos los requisitos v1 cubiertos

| # | Fase | Objetivo | Requisitos |
|---|------|----------|------------|
| 1 | Base de Sesión | El usuario puede ejecutar una sesión en vivo básica con controles claros | SESS-01, SESS-02, SESS-03, SESS-04 |
| 2 | Contexto de Presentación | El usuario puede cargar PDF/PPTX y marcar manualmente la diapositiva activa | PRES-01, PRES-02, PRES-03, PRES-04, PRES-05, PRES-06 |
| 3 | Transcripción en Vivo | El sistema captura audio, lo transcribe en vivo y guarda segmentos con marcas de tiempo | TRNS-01, TRNS-02, TRNS-03, TRNS-04, TRNS-05 |
| 4 | Inteligencia de Apuntes | El sistema genera apuntes contextualizados desde transcripción y contexto de diapositivas | NOTE-01, NOTE-02, NOTE-03, NOTE-04 |
| 5 | Revisión y Exportación | El usuario puede revisar y exportar transcripción/subtítulos y apuntes/resumen por separado | EXPT-01, EXPT-02, EXPT-03 |

## Detalle de Fases

### Fase 1: Base de Sesión

**Objetivo:** Construir la base usable para sesiones en vivo antes de integrar comportamiento pesado de IA.

**Requisitos:** SESS-01, SESS-02, SESS-03, SESS-04

**Criterios de éxito:**
1. El usuario puede crear una sesión y ver el espacio de trabajo.
2. El usuario puede iniciar, pausar, reanudar y detener una sesión.
3. El usuario puede ejecutar la sesión sin cargar una presentación.
4. La interfaz muestra claramente estado de grabación/transcripción y tiempo transcurrido.

**UI hint:** yes

### Fase 2: Contexto de Presentación

**Objetivo:** Agregar carga de presentación y el flujo manual de señalización de diapositiva con baja fricción.

**Requisitos:** PRES-01, PRES-02, PRES-03, PRES-04, PRES-05, PRES-06

**Criterios de éxito:**
1. El usuario puede cargar archivos PDF y PPTX.
2. El usuario puede revisar diapositivas mediante miniaturas o lista.
3. El usuario puede marcar rápidamente la diapositiva activa con controles y atajos de teclado.
4. Cada cambio de diapositiva queda registrado con marca de tiempo.

**UI hint:** yes

### Fase 3: Transcripción en Vivo

**Objetivo:** Capturar audio del micrófono y convertirlo en transcripción/subtítulos en vivo con marcas de tiempo.

**Requisitos:** TRNS-01, TRNS-02, TRNS-03, TRNS-04, TRNS-05

**Criterios de éxito:**
1. El usuario concede permiso de micrófono y la captura de audio inicia de forma confiable.
2. La transcripción/subtítulos aparecen durante la sesión.
3. Los segmentos de transcripción persisten con marcas de tiempo.
4. Los segmentos se vinculan a la diapositiva activa cuando existe presentación.
5. Los segmentos se agrupan por rango de tiempo cuando no existe presentación.

**UI hint:** yes

### Fase 4: Inteligencia de Apuntes

**Objetivo:** Generar apuntes/resumen contextualizados desde la transcripción y el contexto de diapositivas o segmentos.

**Requisitos:** NOTE-01, NOTE-02, NOTE-03, NOTE-04

**Criterios de éxito:**
1. Los apuntes se agrupan por diapositiva cuando existe presentación.
2. Los apuntes se agrupan por segmento de reunión cuando no existe presentación.
3. Los apuntes incluyen puntos clave, explicaciones, preguntas y seguimientos.
4. Los apuntes conservan referencias a diapositivas o rangos de tiempo cuando corresponde.

**UI hint:** yes

### Fase 5: Revisión y Exportación

**Objetivo:** Permitir que el usuario revise y exporte transcripción/subtítulos y apuntes/resumen por separado.

**Requisitos:** EXPT-01, EXPT-02, EXPT-03

**Criterios de éxito:**
1. El usuario puede revisar transcripción/subtítulos antes de exportar.
2. El usuario puede revisar apuntes/resumen antes de exportar.
3. El usuario puede exportar los dos documentos de forma independiente.

**UI hint:** yes

## Validación de Cobertura

Los 22 requisitos v1 están mapeados exactamente a una fase.

---
*Última actualización: 2026-05-04 después de crear el roadmap*
