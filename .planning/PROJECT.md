# Tomador Apuntes Divia

## Qué Es

Tomador Apuntes Divia es un asistente en vivo para reuniones y presentaciones. Escucha el audio del presentador o de la reunión, genera subtítulos/transcripción y usa una presentación PDF/PPTX como contexto cuando existe.

La herramienta también debe funcionar sin presentación, para que pueda producir transcripción y apuntes útiles de reuniones normales solo con audio. Cuando hay presentación, el usuario señaliza manualmente la diapositiva activa de la forma más rápida posible para conectar lo que se dice con el contexto correcto.

## Valor Principal

Convertir audio hablado en vivo en documentos útiles y estructurados sin que el usuario tenga que tomar apuntes durante la sesión.

## Requisitos

### Validados

(Ninguno todavía - hay que construir y validar)

### Activos

- [ ] El usuario puede iniciar una sesión en vivo que captura audio del micrófono.
- [ ] El usuario puede cargar una presentación PDF o PPTX antes o durante una sesión.
- [ ] El usuario puede señalizar rápidamente qué diapositiva está tratando el presentador.
- [ ] El sistema puede funcionar sin presentación y aun así generar transcripción y apuntes.
- [ ] El sistema puede generar dos documentos separados: transcripción/subtítulos y apuntes/resumen.
- [ ] Cuando hay diapositivas, los apuntes y resúmenes se contextualizan por diapositiva.
- [ ] El usuario puede exportar los documentos generados al terminar la sesión.

### Fuera de Alcance

- Detección automática de cambio de diapositiva en v1 - es útil después, pero la señalización manual es el camino más confiable para el MVP.
- Análisis completo de video en v1 - audio más contexto de presentación es suficiente para validar el valor principal.
- Diarización multi-hablante en tiempo real como requisito duro de v1 - las etiquetas de hablante pueden mejorar después de que funcione el flujo básico de transcripción y apuntes.
- Generación de acta formal - el usuario hará el acta por su cuenta usando la transcripción y los apuntes generados.
- Aplicaciones móviles nativas en v1 - web o escritorio primero mantiene el alcance enfocado.

## Contexto

El producto está pensado para presentaciones, clases, reuniones o charlas en vivo donde el usuario necesita registros precisos, pero no puede tomar apuntes manualmente mientras escucha. La presentación no es la única entrada; el sistema debe seguir siendo útil para reuniones sin diapositivas.

El flujo crítico es:

1. El usuario inicia una sesión.
2. El usuario opcionalmente carga un PDF o PPTX.
3. La herramienta captura audio en vivo y muestra subtítulos/transcripción.
4. El usuario marca la diapositiva activa a medida que el presentador avanza.
5. La herramienta usa el audio más la diapositiva actual para crear salidas estructuradas.
6. El usuario exporta dos documentos separados:
   - Transcripción/subtítulos.
   - Apuntes/resumen por diapositiva o por segmento de reunión.

La interacción para marcar diapositivas debe tener muy baja fricción. Controles candidatos: atajos de teclado, botones anterior/siguiente, ingreso directo de número de diapositiva e indicador visible de diapositiva actual.

## Restricciones

- **Entrada de presentación**: v1 debe soportar PDF y PPTX porque ambos fueron pedidos explícitamente.
- **Primero en vivo**: v1 debe priorizar captura de audio en vivo y señalización contextual en vivo; el procesamiento post-evento puede reutilizar la misma arquitectura después.
- **Modo sin presentación**: v1 no puede asumir que existe una presentación; transcripción y apuntes para reuniones normales son obligatorios.
- **Documentos separados**: las salidas deben generarse como dos artefactos distintos: transcripción/subtítulos y apuntes/resumen.
- **Confiabilidad**: se prefiere señalización manual de diapositiva en v1 porque la detección automática agregaría complejidad frágil de visión/computación.

## Decisiones Clave

| Decisión | Razonamiento | Resultado |
|----------|--------------|-----------|
| Construir primero el flujo en vivo, con arquitectura compatible con post-evento | El usuario quiere audio y contexto de diapositivas durante la sesión; post-evento es útil pero secundario | - Pendiente |
| Soportar carga de PDF y PPTX | El usuario pidió explícitamente ambos formatos | - Pendiente |
| El usuario señaliza manualmente la diapositiva actual en v1 | Es la forma más confiable de alinear habla y contexto de diapositiva rápidamente | - Pendiente |
| Soportar sesiones sin presentación | El usuario indicó explícitamente que la herramienta debe servir para reuniones normales | - Pendiente |
| Generar dos documentos separados | El usuario quiere transcripción/subtítulos y apuntes/resumen; el acta queda a cargo del usuario | - Pendiente |
| Sacar acta formal del alcance | El usuario hará la generación de acta por su cuenta | - Pendiente |

## Evolución

Este documento evoluciona en transiciones de fase y cierres de hito.

**Después de cada transición de fase**:
1. ¿Requisitos invalidados? -> mover a Fuera de Alcance con razón.
2. ¿Requisitos validados? -> mover a Validados con referencia de fase.
3. ¿Surgieron requisitos nuevos? -> agregar a Activos.
4. ¿Hay decisiones que registrar? -> agregar a Decisiones Clave.
5. ¿"Qué Es" sigue siendo correcto? -> actualizar si cambió la realidad del producto.

**Después de cada hito**:
1. Revisión completa de todas las secciones.
2. Chequeo del valor principal.
3. Auditoría de Fuera de Alcance.
4. Actualización del contexto con el estado actual.

---
*Última actualización: 2026-05-04 después de la inicialización*
