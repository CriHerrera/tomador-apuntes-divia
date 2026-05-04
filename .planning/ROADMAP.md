# Roadmap: Tomador Apuntes Divia

**Created:** 2026-05-04
**Scope:** v1 live meeting/presentation assistant

## Summary

5 phases | 27 v1 requirements mapped | All v1 requirements covered

| # | Phase | Goal | Requirements |
|---|-------|------|--------------|
| 1 | Session Shell | User can run a basic live session with clear session controls | SESS-01, SESS-02, SESS-03, SESS-04 |
| 2 | Presentation Context | User can upload PDF/PPTX and manually mark the active slide | PRES-01, PRES-02, PRES-03, PRES-04, PRES-05, PRES-06 |
| 3 | Live Transcription | System captures audio, transcribes it live, and stores timestamped segments | TRNS-01, TRNS-02, TRNS-03, TRNS-04, TRNS-05 |
| 4 | Document Intelligence | System generates contextual notes and formal acta from transcript and slide context | NOTE-01, NOTE-02, NOTE-03, NOTE-04, ACTA-01, ACTA-02, ACTA-03, ACTA-04 |
| 5 | Review and Export | User can review and export the three separate documents | EXPT-01, EXPT-02, EXPT-03, EXPT-04 |

## Phase Details

### Phase 1: Session Shell

**Goal:** Build the usable shell for live sessions before integrating AI-heavy behavior.

**Requirements:** SESS-01, SESS-02, SESS-03, SESS-04

**Success Criteria:**
1. User can create a session and see the session workspace.
2. User can start, pause, resume, and stop a session.
3. User can run the session without uploading a presentation.
4. UI clearly shows recording/transcription state and elapsed time.

**UI hint:** yes

### Phase 2: Presentation Context

**Goal:** Add deck upload and the low-friction manual slide signaling flow.

**Requirements:** PRES-01, PRES-02, PRES-03, PRES-04, PRES-05, PRES-06

**Success Criteria:**
1. User can upload PDF and PPTX files.
2. User can inspect slides through thumbnails or a slide list.
3. User can quickly mark the active slide with controls and keyboard shortcuts.
4. Every slide change is recorded with a timestamp.

**UI hint:** yes

### Phase 3: Live Transcription

**Goal:** Capture microphone audio and convert it into live timestamped transcript/subtitles.

**Requirements:** TRNS-01, TRNS-02, TRNS-03, TRNS-04, TRNS-05

**Success Criteria:**
1. User grants microphone permission and audio capture starts reliably.
2. Transcript/subtitle text appears during the session.
3. Transcript segments persist with timestamps.
4. Transcript segments are linked to the active slide when present.
5. Transcript segments are grouped by time range when no presentation exists.

**UI hint:** yes

### Phase 4: Document Intelligence

**Goal:** Generate the two structured outputs that require interpretation: notes/resumen and formal acta.

**Requirements:** NOTE-01, NOTE-02, NOTE-03, NOTE-04, ACTA-01, ACTA-02, ACTA-03, ACTA-04

**Success Criteria:**
1. Notes are grouped by slide when a presentation exists.
2. Notes are grouped by meeting segment when no presentation exists.
3. Notes include key points, explanations, questions, and follow-ups.
4. Acta includes summary, topics, agreements, decisions, action items, and open questions.
5. Acta references slide numbers or titles when relevant.

**UI hint:** yes

### Phase 5: Review and Export

**Goal:** Let the user review and export the three required documents separately.

**Requirements:** EXPT-01, EXPT-02, EXPT-03, EXPT-04

**Success Criteria:**
1. User can review transcription/subtitles before export.
2. User can review formal acta before export.
3. User can review notes/resumen before export.
4. User can export all three documents independently.

**UI hint:** yes

## Coverage Validation

All 27 v1 requirements are mapped to exactly one phase.

---
*Last updated: 2026-05-04 after roadmap creation*
