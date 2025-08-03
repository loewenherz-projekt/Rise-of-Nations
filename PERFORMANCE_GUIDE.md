# Performance-Optimierungsguide für Rise of Nations

## Steam Launch Options

Füge diese Launch-Parameter in Steam hinzu:
```
--gc-heap-size=16384 --max-ram=32768 --threading-mode=multi --cpu-cores=8 --disable-audio-driver-workaround --opengl
```

**Parameter-Erklärung:**
- `--gc-heap-size=16384`: 16GB Heap für Garbage Collection
- `--max-ram=32768`: Maximaler RAM-Verbrauch (32GB)  
- `--threading-mode=multi`: Multi-Threading aktivieren
- `--cpu-cores=8`: Nutzt alle 8 physischen Kerne
- `--disable-audio-driver-workaround`: Deaktiviert Audio-Fixes
- `--opengl`: Nutzt OpenGL statt DirectX (kann schneller sein)

## Windows-Systemoptimierungen

### Energieoptionen
1. Windows-Suche: "Energieoptionen"
2. Plan auswählen: "Höchstleistung"
3. Erweiterte Einstellungen → Prozessor → Min: 100%, Max: 100%

### Task-Manager Priorität
1. Task-Manager öffnen während HOI4 läuft
2. Prozess "hoi4.exe" → Rechtsklick → "Hohe Priorität"

### GPU-Optimierung (RTX 4070)
**NVIDIA Control Panel:**
- Energieverwaltung: "Maximale Leistung bevorzugen"
- Threaded Optimization: "Ein"
- Texture Filtering - Quality: "Performance"
- Maximum Pre-rendered Frames: "1"

## In-Game Settings

### Grafik (für RTX 4070 Laptop GPU)
- **Auflösung**: 1920x1080 (optimal für deine Hardware)
- **Vollbild**: Ja
- **V-Sync**: Aus
- **Multisampling**: Aus (wichtig für Performance!)
- **Einheitendetails**: Niedrig
- **Kartendetails**: Mittel
- **Gebäudedetails**: Niedrig
- **Wasserqualität**: Niedrig
- **Himmelqualität**: Niedrig
- **3D-Einheiten**: Aus
- **Wetter**: Aus

### Audio
- **Mastervolumen**: 50%
- **Musik**: 30% (oder aus für max. Performance)
- **Soundeffekte**: 70%
- **UI-Sounds**: 50%

### Gameplay
- **Autosave**: Alle 6 Monate (statt jährlich)
- **Historischer KI-Fokus**: Ein (reduziert KI-Berechnungen)
- **Eisenmann-Modus**: Aus (außer gewünscht)

## Mod-spezifische Optimierungen

### Rise of Nations Performance
- Spiele nicht über 1940 hinaus (Spätspiel wird sehr langsam)
- Nutze kleinere Nationen für bessere Performance
- Deaktiviere unnötige Mods während des Spielens
- Lösche regelmäßig alte Savegames

### Zusätzliche empfohlene Mods
1. **"Improved Performance"** (Steam Workshop)
2. **"FPS and Clock"** (zeigt FPS-Counter)
3. **"Better Zoom"** (Performance-freundlicheres Zooming)

## System-Monitoring

### Task-Manager überwachen
- CPU-Auslastung sollte bei 70-90% liegen
- RAM-Verbrauch: Normal 8-16GB
- GPU-Auslastung: 50-80%

### Kritische Temperaturen
- CPU: Unter 85°C
- GPU: Unter 83°C (Laptop-Throttling)

## Troubleshooting

### Bei Lag/Rucklern
1. F3 drücken → FPS prüfen
2. Speed 3 statt Speed 5 nutzen
3. Mehr Pausen einlegen
4. Weniger gleichzeitige Kriege

### Bei Memory-Leaks
1. Spiel alle 2-3 Stunden neustarten
2. Andere Programme schließen
3. Browser-Tabs reduzieren

### Bei Crashes
1. Mod-Kompatibilität prüfen
2. Steam-Files verifizieren
3. Savegame-Backup nutzen

## Hardware-spezifische Tipps (Ryzen 7 7435HS + RTX 4070)

- **CPU-Threads**: Lasse 2-4 Threads für System frei
- **RAM**: 16GB für HOI4, Rest für System
- **SSD**: Installiere HOI4 auf schnellster SSD
- **Cooling**: Laptop-Lüfter auf "Performance-Modus"
- **Battery**: Immer Netzteil nutzen, nie Batterie

## Erwartete Performance

Mit diesen Optimierungen:
- **Speed 1-3**: Flüssig (60 FPS)
- **Speed 4**: Gut spielbar (30-45 FPS)  
- **Speed 5**: Akzeptabel bis 1940 (20-30 FPS)
- **Ladezeiten**: 60-90 Sekunden für großen Mod

## Updates und Wartung

- Monatlich: GPU-Treiber aktualisieren
- Wöchentlich: Windows Updates
- Nach jedem HOI4-Update: Mod-Kompatibilität prüfen
- Regelmäßig: Temp-Dateien löschen