# Requirements: Tomador Apuntes Divia

**Defined:** 2026-05-04
**Core Value:** Turn live spoken audio into useful, structured meeting outputs without requiring the user to write notes during the session.

## v1 Requirements

### Session

- [ ] **SESS-01**: User can create a new live session.
- [ ] **SESS-02**: User can start, pause, resume, and stop live audio capture.
- [ ] **SESS-03**: User can run a session without uploading a presentation.
- [ ] **SESS-04**: User can see session status, elapsed time, and recording/transcription state.

### Presentation

- [ ] **PRES-01**: User can upload a PDF presentation.
- [ ] **PRES-02**: User can upload a PPTX presentation.
- [ ] **PRES-03**: User can view slide thumbnails or a slide list after upload.
- [ ] **PRES-04**: User can mark the current slide using a low-friction control.
- [ ] **PRES-05**: User can move to previous/next slide with keyboard shortcuts or prominent controls.
- [ ] **PRES-06**: System records timestamps for slide changes during the session.

### Live Transcription

- [ ] **TRNS-01**: System captures microphone audio during a live session.
- [ ] **TRNS-02**: System produces live transcript/subtitle text while audio is captured.
- [ ] **TRNS-03**: System stores transcript segments with timestamps.
- [ ] **TRNS-04**: When a slide is active, transcript segments are associated with the current slide.
- [ ] **TRNS-05**: When no presentation exists, transcript segments are associated with meeting time ranges.

### Contextual Notes

- [ ] **NOTE-01**: System generates notes/resumen by slide when a presentation exists.
- [ ] **NOTE-02**: System generates notes/resumen by meeting segment when no presentation exists.
- [ ] **NOTE-03**: Notes include important points, explanations, questions, and follow-ups.
- [ ] **NOTE-04**: Notes preserve enough slide context to explain why a point belongs to that slide.

### Formal Acta

- [ ] **ACTA-01**: System generates a formal meeting acta from the session transcript.
- [ ] **ACTA-02**: Acta includes meeting summary, topics covered, agreements, decisions, action items, and unresolved questions.
- [ ] **ACTA-03**: Acta works whether or not a presentation was used.
- [ ] **ACTA-04**: Acta references slide numbers or titles when relevant.

### Export

- [ ] **EXPT-01**: User can export transcription/subtitles as a separate document.
- [ ] **EXPT-02**: User can export formal acta as a separate document.
- [ ] **EXPT-03**: User can export notes/resumen as a separate document.
- [ ] **EXPT-04**: User can review generated documents before export.

## v2 Requirements

### Automation

- **AUTO-01**: System can detect slide changes automatically from screen or presentation state.
- **AUTO-02**: System can process uploaded post-event recordings using the same document pipeline.
- **AUTO-03**: System can identify speakers automatically.
- **AUTO-04**: System can support multiple simultaneous note-taking templates.

### Collaboration

- **COLL-01**: Multiple users can collaborate in the same session.
- **COLL-02**: User can share generated documents through a link.
- **COLL-03**: User can edit acta and notes collaboratively after the session.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automatic slide-change detection in v1 | Manual signaling is more reliable and faster to validate. |
| Native mobile app | Web or desktop-first keeps v1 focused. |
| Full video understanding | Audio plus slide context is enough for initial value. |
| Hard dependency on a presentation | Meetings without a deck must work. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SESS-01 | Phase 1 | Pending |
| SESS-02 | Phase 1 | Pending |
| SESS-03 | Phase 1 | Pending |
| SESS-04 | Phase 1 | Pending |
| PRES-01 | Phase 2 | Pending |
| PRES-02 | Phase 2 | Pending |
| PRES-03 | Phase 2 | Pending |
| PRES-04 | Phase 2 | Pending |
| PRES-05 | Phase 2 | Pending |
| PRES-06 | Phase 2 | Pending |
| TRNS-01 | Phase 3 | Pending |
| TRNS-02 | Phase 3 | Pending |
| TRNS-03 | Phase 3 | Pending |
| TRNS-04 | Phase 3 | Pending |
| TRNS-05 | Phase 3 | Pending |
| NOTE-01 | Phase 4 | Pending |
| NOTE-02 | Phase 4 | Pending |
| NOTE-03 | Phase 4 | Pending |
| NOTE-04 | Phase 4 | Pending |
| ACTA-01 | Phase 4 | Pending |
| ACTA-02 | Phase 4 | Pending |
| ACTA-03 | Phase 4 | Pending |
| ACTA-04 | Phase 4 | Pending |
| EXPT-01 | Phase 5 | Pending |
| EXPT-02 | Phase 5 | Pending |
| EXPT-03 | Phase 5 | Pending |
| EXPT-04 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 27 total
- Mapped to phases: 27
- Unmapped: 0

---
*Requirements defined: 2026-05-04*
*Last updated: 2026-05-04 after initial definition*
