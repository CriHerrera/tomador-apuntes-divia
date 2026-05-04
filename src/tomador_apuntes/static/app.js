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
  previousSlide: document.querySelector("#previous-slide"),
  nextSlide: document.querySelector("#next-slide"),
  currentSlide: document.querySelector("#current-slide"),
  captureState: document.querySelector("#capture-state"),
  sessionMode: document.querySelector("#session-mode"),
  eventLog: document.querySelector("#event-log"),
};

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
    diapositiva_actualizada: "Diapositiva actualizada",
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
  elements.previousSlide.disabled = !session.presentation_name || session.status === "detenida";
  elements.nextSlide.disabled = !session.presentation_name || session.status === "detenida";

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

async function refreshSession() {
  const payload = await request("/api/sessions");
  if (payload.sessions.length > 0) {
    setSession(payload.sessions[0]);
  }
}

elements.createForm.addEventListener("submit", createSession);
elements.startButton.addEventListener("click", () => runAction("start"));
elements.pauseButton.addEventListener("click", () => runAction("pause"));
elements.resumeButton.addEventListener("click", () => runAction("resume"));
elements.stopButton.addEventListener("click", () => runAction("stop"));
elements.presentationForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runAction("presentation", { presentation_name: elements.presentationName.value });
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
refreshSession();

