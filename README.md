# Tomador Apuntes Divia

Asistente en vivo para reuniones y presentaciones que captura audio, usa una presentación PDF/PPTX como contexto cuando existe y genera documentos separados para transcripción/subtítulos, acta formal y apuntes/resumen.

## Objetivo

La herramienta busca que una persona pueda escuchar una reunión o presentación sin tomar apuntes manualmente. El sistema registra el audio, lo transcribe, permite marcar la diapositiva activa y luego produce documentos útiles para revisar, compartir o archivar.

## Alcance v1

- Sesiones en vivo con captura de audio.
- Funcionamiento con o sin presentación.
- Carga de presentaciones PDF y PPTX.
- Marcado manual rápido de la diapositiva activa.
- Transcripción/subtítulos con marcas de tiempo.
- Apuntes contextualizados por diapositiva o por segmento de reunión.
- Acta formal con temas, acuerdos, decisiones, tareas y preguntas abiertas.
- Exportación de los tres documentos por separado.

## Documentos de Planificación

La planificación del proyecto está en `.planning/`:

- `.planning/PROJECT.md`: visión, valor principal, contexto y decisiones.
- `.planning/REQUIREMENTS.md`: requisitos v1, v2 y trazabilidad.
- `.planning/ROADMAP.md`: fases de construcción.
- `.planning/STATE.md`: estado actual del trabajo.

## Fase Actual

Fase 1: Base de Sesión.

El objetivo de esta fase es construir la base usable para crear una sesión, controlar su estado y permitir el modo sin presentación antes de integrar transcripción, presentaciones e IA documental.
