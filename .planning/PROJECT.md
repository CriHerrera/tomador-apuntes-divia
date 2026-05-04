# Tomador Apuntes Divia

## What This Is

Tomador Apuntes Divia is a live meeting and presentation assistant. It listens to the presenter or meeting audio, produces subtitles/transcription, and uses an uploaded PDF/PPTX presentation as context when available.

The tool must also work without a presentation, so it can produce useful meeting records from normal audio-only meetings. When a presentation exists, the user manually signals the current slide in the most efficient way possible so the system can connect what is said with the right slide context.

## Core Value

Turn live spoken audio into useful, structured meeting outputs without requiring the user to write notes during the session.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] User can run a live session that captures microphone audio.
- [ ] User can load a PDF or PPTX presentation before or during a session.
- [ ] User can quickly signal which slide the presenter is currently discussing.
- [ ] System can continue without a presentation and still produce a meeting acta.
- [ ] System can generate three separate documents: transcription/subtitles, formal acta, and notes/resumen.
- [ ] When slides are present, notes and summaries are contextualized by slide.
- [ ] User can export the generated documents after the session.

### Out of Scope

- Automatic slide-change detection in v1 - useful later, but manual signaling is the fastest reliable MVP path.
- Full video analysis in v1 - audio plus presentation context is enough to validate core value.
- Real-time multi-speaker diarization as a hard v1 requirement - speaker labels can be improved after the basic acta flow works.
- Native mobile apps in v1 - web or desktop-first keeps the build focused.

## Context

The product is intended for live presentations, classes, meetings, or talks where the user wants accurate records but cannot manually take notes while listening. The presentation is not the only input; the system must remain useful for meetings with no deck.

The critical workflow is:

1. User starts a session.
2. User optionally uploads a PDF or PPTX.
3. Tool captures live audio and shows subtitles/transcription.
4. User marks the active slide as the presenter moves through the deck.
5. Tool uses audio plus current slide context to create structured outputs.
6. User exports three separate documents:
   - Transcription/subtitles.
   - Formal acta.
   - Notes/resumen by slide or by meeting segment.

The slide-marker interaction needs to be very low friction. Candidate controls include keyboard shortcuts, previous/next buttons, direct slide number entry, and a visible current-slide indicator.

## Constraints

- **Presentation input**: v1 must support PDF and PPTX - these are the formats explicitly requested.
- **Live-first**: v1 should prioritize live audio capture and live context marking - post-event processing can reuse the same pipeline later.
- **No-presentation mode**: v1 cannot assume a deck exists - normal meeting acta generation is required.
- **Document separation**: outputs must be generated as three distinct artifacts - transcription/subtitles, formal acta, and notes/resumen.
- **Reliability**: manual slide signaling is preferred for v1 because automatic slide detection would add fragile computer-vision complexity.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build live-first, with post-event as future-compatible architecture | User wants live audio and slide context during the event; post-event is useful but secondary | - Pending |
| Support PDF and PPTX deck upload | User explicitly requested both formats | - Pending |
| User manually signals the current slide in v1 | Most reliable way to align speech with slide context quickly | - Pending |
| Support sessions without presentation | User explicitly said acta must work for normal meetings | - Pending |
| Generate three separate documents | User wants transcription/subtitles, acta, and notes/resumen separately | - Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-04 after initialization*
