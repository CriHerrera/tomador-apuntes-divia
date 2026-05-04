# AGENTS.md

## Project

Tomador Apuntes Divia is a live meeting and presentation assistant. It captures audio, optionally uses PDF/PPTX slides as context, and generates three separate outputs: transcription/subtitles, formal acta, and notes/resumen.

## GSD Context

Planning artifacts live in `.planning/`:

- `.planning/PROJECT.md` - product context and core value
- `.planning/REQUIREMENTS.md` - v1 requirements and traceability
- `.planning/ROADMAP.md` - phase structure
- `.planning/STATE.md` - current phase state

Before implementation, read the relevant planning files and keep changes aligned with the active phase.

## Current Focus

Phase 1: Session Shell.

Goal: user can create and control a live session, including sessions without a presentation.

## Local Instructions

The parent Codex environment includes `C:\Users\cristian.herrera\.codex\RTK.md`, which requires shell commands to be prefixed with `rtk`.
