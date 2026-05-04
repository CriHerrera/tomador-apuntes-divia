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

Fase 1: Base de Sesión.

El objetivo de esta fase es construir la base usable para crear una sesión, controlar su estado y permitir el modo sin presentación antes de integrar transcripción, presentaciones e IA documental.

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

La captura real de micrófono y la transcripción en vivo quedan para la fase de transcripción. La generación de acta formal queda fuera del producto: el usuario la hará por su cuenta a partir de la transcripción y los apuntes generados.
