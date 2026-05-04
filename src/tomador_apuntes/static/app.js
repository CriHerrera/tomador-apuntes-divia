const state = {
  session: null,
  timer: null,
};

const elements = {
  createForm: document.querySelector("#create-session-form"),
  sessionTitle: document.querySelector("#session-title"),
  sessionStatus: document.querySelector("#session-status"),
  elapsedTime: document.querySelector("#elapsed-time"),
  startButton: document.querySelector("#start-button"),
  pauseButton: document.querySelector("#pause-button"),
  resumeButton: document.querySelector("#resume-button"),
  stopButton: document.querySelector("#stop-button"),
  presentationForm: document.querySelector("#presentation-form"),
  presentationName: document.querySelector("#presentation-name"),
  presentationButton: document.querySelector("#presentation-button"),
  presentationUploadForm: document.querySelector("#presentation-upload-form"),
  presentationFile: document.querySelector("#presentation-file"),
  presentationUploadButton: document.querySelector("#presentation-upload-button"),
  presentationStatus: document.querySelector("#presentation-status"),
  presentationText: document.querySelector("#presentation-text"),
  previousSlide: document.querySelector("#previous-slide"),
  nextSlide: document.querySelector("#next-slide"),
  currentSlide: document.querySelector("#current-slide"),
  speakerForm: document.querySelector("#speaker-form"),
  speakerName: document.querySelector("#speaker-name"),
  speakerButton: document.querySelector("#speaker-button"),
  speakerSelect: document.querySelector("#speaker-select"),
  captureState: document.querySelector("#capture-state"),
  sessionMode: document.querySelector("#session-mode"),
  speechSupport: document.querySelector("#speech-support"),
  voiceStartButton: document.querySelector("#voice-start-button"),
  voiceStopButton: document.querySelector("#voice-stop-button"),
  liveSubtitle: document.querySelector("#live-subtitle"),
  transcriptList: document.querySelector("#transcript-list"),
  eventLog: document.querySelector("#event-log"),
};

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let voiceActive = false;
let segmentStartSeconds = 0;

function formatSeconds(totalSeconds) {
  const hours = Math.floor(totalSeconds / 3600).toString().padStart(2, "0");
  const minutes = Math.floor((totalSeconds % 3600) / 60).toString().padStart(2, "0");
  const seconds = Math.floor(totalSeconds % 60).toString().padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
}

function statusLabel(status) {
  const labels = {
    creada: "Creada",
    en_vivo: "En vivo",
    pausada: "Pausada",
    detenida: "Detenida",
  };
  return labels[status] || "Sin sesión";
}

function eventLabel(event) {
  const labels = {
    sesion_creada: "Sesión creada",
    sesion_iniciada: "Sesión iniciada",
    sesion_pausada: "Sesión pausada",
    sesion_reanudada: "Sesión reanudada",
    sesion_detenida: "Sesión detenida",
    presentacion_actualizada: "Presentación actualizada",
    presentacion_pdf_cargada: "PDF cargado",
    diapositiva_actualizada: "Diapositiva actualizada",
    presentador_agregado: "Presentador agregado",
    presentador_activo: "Presentador activo",
    transcripcion_guardada: "Transcripción guardada",
  };
  return labels[event.type] || event.type;
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Error inesperado");
  }
  return payload;
}

async function createSession(event) {
  event.preventDefault();
  const payload = await request("/api/sessions", {
    method: "POST",
    body: JSON.stringify({ title: elements.sessionTitle.value }),
  });
  setSession(payload.session);
}

async function runAction(action, body = {}) {
  if (!state.session) return;
  const payload = await request(`/api/sessions/${state.session.id}/${action}`, {
    method: "POST",
    body: JSON.stringify(body),
  });
  setSession(payload.session);
}

function setSession(session) {
  state.session = session;
  if (!voiceActive) {
    segmentStartSeconds = session.elapsed_seconds || 0;
  }
  render();
}

function render() {
  const session = state.session;
  if (!session) {
    return;
  }

  elements.sessionStatus.textContent = statusLabel(session.status);
  elements.elapsedTime.textContent = formatSeconds(session.elapsed_seconds);
  elements.captureState.textContent = session.transcription_state.replaceAll("_", " ");
  elements.sessionMode.textContent = session.presentation_name ? "Con presentación" : "Sin presentación";
  elements.currentSlide.textContent = session.current_slide
    ? `Diapositiva ${session.current_slide}`
    : "Sin presentación";

  elements.startButton.disabled = !["creada", "pausada"].includes(session.status);
  elements.pauseButton.disabled = session.status !== "en_vivo";
  elements.resumeButton.disabled = session.status !== "pausada";
  elements.stopButton.disabled = !["creada", "en_vivo", "pausada"].includes(session.status);
  elements.presentationButton.disabled = session.status === "detenida";
  elements.presentationUploadButton.disabled = session.status === "detenida";
  elements.speakerButton.disabled = session.status === "detenida";
  elements.speakerSelect.disabled = session.status === "detenida";
  elements.previousSlide.disabled = !session.presentation_name || session.status === "detenida";
  elements.nextSlide.disabled = !session.presentation_name || session.status === "detenida";
  elements.voiceStartButton.disabled = !SpeechRecognition || voiceActive || session.status !== "en_vivo";
  elements.voiceStopButton.disabled = !SpeechRecognition || !voiceActive;

  renderPresentation(session);
  renderSpeakers(session);
  renderTranscript(session.transcript_segments || []);
  elements.eventLog.innerHTML = "";
  for (const item of [...session.events].reverse()) {
    const li = document.createElement("li");
    const time = new Date(item.timestamp).toLocaleTimeString("es-CL", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
    li.textContent = `${time} - ${eventLabel(item)}${item.detail ? `: ${item.detail}` : ""}`;
    elements.eventLog.appendChild(li);
  }
}

function renderPresentation(session) {
  const statusLabels = {
    sin_presentacion: "Sin PDF cargado.",
    texto_extraido: "Texto extraído correctamente.",
    pypdf_no_instalado: "PDF guardado. Falta instalar pypdf para extraer texto.",
    sin_texto_extraible: "PDF guardado, pero no se encontró texto extraíble.",
  };
  elements.presentationStatus.textContent =
    statusLabels[session.presentation_text_status] || session.presentation_text_status || "Sin PDF cargado.";
  elements.presentationText.textContent = session.presentation_text || "Sube un PDF para extraer su texto.";
}

function renderSpeakers(session) {
  const currentValue = session.active_speaker || "";
  elements.speakerSelect.innerHTML = "";
  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.textContent = "Sin presentador";
  elements.speakerSelect.appendChild(emptyOption);

  for (const speaker of session.speakers || []) {
    const option = document.createElement("option");
    option.value = speaker;
    option.textContent = speaker;
    elements.speakerSelect.appendChild(option);
  }
  elements.speakerSelect.value = currentValue;
}

function renderTranscript(segments) {
  elements.transcriptList.innerHTML = "";
  for (const segment of [...segments].reverse()) {
    const li = document.createElement("li");
    const meta = document.createElement("span");
    const slideText = segment.slide ? `Diapositiva ${segment.slide}` : "Sin presentación";
    const speakerText = segment.speaker_name || "Sin presentador";
    meta.textContent = `${formatSeconds(segment.started_at_seconds)} - ${formatSeconds(segment.ended_at_seconds)} · ${slideText} · ${speakerText}`;
    li.appendChild(meta);
    li.append(document.createTextNode(segment.text));
    elements.transcriptList.appendChild(li);
  }
}

async function refreshSession() {
  const payload = await request("/api/sessions");
  if (payload.sessions.length > 0) {
    setSession(payload.sessions[0]);
  }
}

function setupSpeechRecognition() {
  if (!SpeechRecognition) {
    elements.speechSupport.textContent = "Este navegador no soporta reconocimiento de voz local. Prueba con Chrome o Edge.";
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = "es-CL";
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  elements.speechSupport.textContent = "Reconocimiento disponible. Inicia una sesión y activa voz.";

  recognition.addEventListener("result", handleSpeechResult);
  recognition.addEventListener("end", () => {
    if (voiceActive) {
      recognition.start();
    }
  });
  recognition.addEventListener("error", (event) => {
    elements.speechSupport.textContent = `Error de voz: ${event.error}`;
    voiceActive = false;
    render();
  });
}

function handleSpeechResult(event) {
  let interimText = "";
  for (let index = event.resultIndex; index < event.results.length; index += 1) {
    const result = event.results[index];
    const text = result[0].transcript.trim();
    if (!text) continue;
    if (result.isFinal) {
      saveTranscriptSegment(text);
    } else {
      interimText += `${text} `;
    }
  }
  elements.liveSubtitle.textContent = interimText.trim() || "Escuchando...";
}

async function saveTranscriptSegment(text) {
  if (!state.session) return;
  const endedAt = state.session.elapsed_seconds || 0;
  const startedAt = Math.min(segmentStartSeconds, endedAt);
  elements.liveSubtitle.textContent = text;
  await runAction("transcript", {
    text,
    started_at_seconds: startedAt,
    ended_at_seconds: endedAt,
  });
  segmentStartSeconds = state.session?.elapsed_seconds || endedAt;
}

function startVoice() {
  if (!recognition || !state.session || state.session.status !== "en_vivo") return;
  voiceActive = true;
  segmentStartSeconds = state.session.elapsed_seconds || 0;
  elements.liveSubtitle.textContent = "Escuchando...";
  elements.speechSupport.textContent = "Voz activa. Habla cerca del micrófono.";
  recognition.start();
  render();
}

function stopVoice() {
  if (!recognition) return;
  voiceActive = false;
  recognition.stop();
  elements.liveSubtitle.textContent = "Voz detenida.";
  elements.speechSupport.textContent = "Reconocimiento disponible. Puedes reactivar voz cuando la sesión esté en vivo.";
  render();
}

elements.createForm.addEventListener("submit", createSession);
elements.startButton.addEventListener("click", () => runAction("start"));
elements.pauseButton.addEventListener("click", () => runAction("pause"));
elements.resumeButton.addEventListener("click", () => runAction("resume"));
elements.stopButton.addEventListener("click", () => runAction("stop"));
elements.voiceStartButton.addEventListener("click", startVoice);
elements.voiceStopButton.addEventListener("click", stopVoice);
elements.presentationForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runAction("presentation", { presentation_name: elements.presentationName.value });
});
elements.presentationUploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.session || elements.presentationFile.files.length === 0) return;
  const formData = new FormData();
  formData.append("file", elements.presentationFile.files[0]);
  const response = await fetch(`/api/sessions/${state.session.id}/presentation-file`, {
    method: "POST",
    body: formData,
  });
  const payload = await response.json();
  if (!response.ok) {
    elements.presentationStatus.textContent = payload.error || "No se pudo subir el PDF.";
    return;
  }
  setSession(payload.session);
});
elements.speakerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runAction("speakers", { name: elements.speakerName.value });
  elements.speakerName.value = "";
});
elements.speakerSelect.addEventListener("change", () => {
  runAction("active-speaker", { name: elements.speakerSelect.value });
});
elements.previousSlide.addEventListener("click", () => {
  const current = state.session?.current_slide || 1;
  runAction("slide", { slide: Math.max(1, current - 1) });
});
elements.nextSlide.addEventListener("click", () => {
  const current = state.session?.current_slide || 0;
  runAction("slide", { slide: current + 1 });
});

window.addEventListener("keydown", (event) => {
  if (event.target instanceof HTMLInputElement) return;
  if (event.key === "ArrowLeft" && !elements.previousSlide.disabled) {
    runAction("slide", { slide: Math.max(1, (state.session?.current_slide || 1) - 1) });
  }
  if (event.key === "ArrowRight" && !elements.nextSlide.disabled) {
    runAction("slide", { slide: (state.session?.current_slide || 0) + 1 });
  }
});

setInterval(refreshSession, 1000);
setupSpeechRecognition();
refreshSession();
