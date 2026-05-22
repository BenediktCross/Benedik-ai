# CS2 Case Overlay (Windows-only, external)

Dieses Repository enthält ein **modulares Grundgerüst** für eine externe, rein kosmetische Case-Opening-Overlay-App für Counter-Strike 2.

## Ziele

- Keine Injection
- Kein Renderer-Hooking
- Kein Gameplay-Vorteil
- Nur read-only Detection + visuelles Overlay

## Architektur

1. **Detection Layer** (`detection/`)
   - Externe Erkennung der Case-Sequenz (Platzhalter-Service vorhanden)
2. **Overlay Renderer** (`overlay/`)
   - Borderless Fullscreen-Overlay (PySide6), dunkler Cinematic-Look, zentraler grüner Marker
3. **Asset Manager** (`assets/`)
   - Lokale JSON-Daten + Bild-Cache (Preload)
4. **Audio System** (`audio/`)
   - Für spätere Sound-Integration vorbereitet

## Aktueller Stand

- Event-getriebene Struktur (`AsyncEventBus`)
- Basales Overlay-Rendering mit horizontaler Skin-Leiste
- Deterministisches Enden auf erkanntem finalen Skin
- Klick zum sofortigen Skippen
- Lokale Case-Daten via JSON

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python -m cs2_case_overlay.main
```

## Wichtige Hinweise

- Diese Codebasis ist ein **Starter** und enthält bewusst nur einen simulierten Detection-Flow.
- Für produktive Memory-Detection müssen Offsets/Signatures robust gepflegt werden.
- Der Overlay-Fokus liegt auf niedriger Latenz und klarer Trennung zwischen Detection und Rendering.
