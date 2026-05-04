# AGENTS.md

## Proyecto

Tomador Apuntes Divia es un asistente en vivo para reuniones y presentaciones. Captura audio, usa opcionalmente diapositivas PDF/PPTX como contexto y genera dos salidas separadas: transcripción/subtítulos y apuntes/resumen.

## Contexto GSD

Los artefactos de planificación viven en `.planning/`:

- `.planning/PROJECT.md` - contexto del producto y valor principal
- `.planning/REQUIREMENTS.md` - requisitos v1 y trazabilidad
- `.planning/ROADMAP.md` - estructura de fases
- `.planning/STATE.md` - estado de la fase actual

Antes de implementar, lee los archivos de planificación relevantes y mantén los cambios alineados con la fase activa.

## Foco Actual

Fase 1: Base de Sesión.

Objetivo: el usuario puede crear y controlar una sesión en vivo, incluyendo sesiones sin presentación.

## Instrucciones Locales

El entorno Codex padre incluye `C:\Users\cristian.herrera\.codex\RTK.md`, que exige prefijar los comandos de shell con `rtk`.
