# Tomador Apuntes Divia

Asistente en vivo para reuniones y presentaciones que captura audio, usa una presentación PDF/PPTX como contexto cuando existe y genera documentos separados para transcripción/subtítulos y apuntes/resumen.

## Objetivo

La herramienta busca que una persona pueda escuchar una reunión o presentación sin tomar apuntes manualmente. El sistema registra el audio, lo transcribe, permite marcar la diapositiva activa y luego produce documentos útiles para revisar, compartir o archivar.

## Alcance v1

- Sesiones en vivo con captura de audio.
- Funcionamiento con o sin presentación.
- Carga de presentaciones PDF y PPTX.
- Marcado manual rápido de la diapositiva activa.
- Transcripción/subtítulos con marcas de tiempo.
- Apuntes contextualizados por diapositiva o por segmento de reunión.
- Exportación de transcripción/subtítulos y apuntes/resumen por separado.

## Documentos de Planificación

La planificación del proyecto está en `.planning/`:

- `.planning/PROJECT.md`: visión, valor principal, contexto y decisiones.
- `.planning/REQUIREMENTS.md`: requisitos v1, v2 y trazabilidad.
- `.planning/ROADMAP.md`: fases de construcción.
- `.planning/STATE.md`: estado actual del trabajo.

## Fase Actual

Fase 3: Transcripción en Vivo.

La base de sesión ya existe. El foco actual es probar voz real desde el navegador, mostrar subtítulos en vivo y guardar segmentos de transcripción asociados a la diapositiva activa.

## Ejecutar en Local

Requisitos:

- Python 3.11 o superior.

Comando:

```powershell
python -m tomador_apuntes.app --port 8000
```

Si ejecutas desde el repositorio sin instalar el paquete:

```powershell
$env:PYTHONPATH="src"; python -m tomador_apuntes.app --port 8000
```

En esta máquina también puedes usar la instalación detectada de Python directamente:

```powershell
$env:PYTHONPATH="src"; & "C:\Users\cristian.herrera\AppData\Local\Programs\Python\Python314\python.exe" -m tomador_apuntes.app --port 8000
```

Luego abre:

```text
http://127.0.0.1:8000
```

## Probar Voz en Vivo

Usa Chrome o Edge, porque esta versión usa la Web Speech API del navegador.

Flujo recomendado:

1. Crea una sesión.
2. Presiona `Iniciar`.
3. Opcionalmente registra una presentación, por ejemplo `clase.pdf`.
4. Presiona `Activar voz`.
5. Acepta el permiso de micrófono del navegador.
6. Habla en español.
7. Cambia de diapositiva con los botones o con las flechas izquierda/derecha.
8. Revisa los segmentos guardados en la sección `Transcripción en vivo`.

Los segmentos se guardan automáticamente en:

```text
data/sessions.json
```

Cada segmento conserva texto, tiempo relativo de inicio/fin y diapositiva activa si corresponde.

## Pruebas

```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests
```

Con la ruta local detectada:

```powershell
$env:PYTHONPATH="src"; & "C:\Users\cristian.herrera\AppData\Local\Programs\Python\Python314\python.exe" -m unittest discover -s tests
```

## Estado Técnico

La primera base está implementada en Python usando solo librerías estándar:

- `http.server` para servir la app local.
- JSON local en `data/sessions.json` para persistir sesiones.
- HTML/CSS/JavaScript estático para la interfaz.

La captura de micrófono y transcripción en vivo inicial ya está integrada con Web Speech API. La generación de acta formal queda fuera del producto: el usuario la hará por su cuenta a partir de la transcripción y los apuntes generados.
