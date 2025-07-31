# Google Cloud Translation API Setup

## Schritt-für-Schritt Anleitung

### 1. Google Cloud Console öffnen
- Gehen Sie zu: https://console.cloud.google.com/
- Melden Sie sich mit Ihrem Google-Account an

### 2. Projekt auswählen/erstellen
- Wählen Sie Ihr bestehendes Projekt aus (ID: 342173301757)
- Oder erstellen Sie ein neues Projekt für die Übersetzungen

### 3. Translation API aktivieren
- Gehen Sie zu: **APIs & Services > Library**
- Suchen Sie nach "Cloud Translation API"
- Klicken Sie auf "Cloud Translation API"
- Klicken Sie auf **"ENABLE"** (Aktivieren)

### 4. Service Account erstellen (falls noch nicht vorhanden)
- Gehen Sie zu: **APIs & Services > Credentials**
- Klicken Sie auf **"Create Credentials" > "Service Account"**
- Name: `translation-service`
- Rolle: **"Cloud Translation API User"**
- Klicken Sie auf **"Done"**

### 5. JSON-Schlüssel herunterladen
- Klicken Sie auf den erstellten Service Account
- Gehen Sie zu **"Keys"**
- Klicken Sie auf **"Add Key" > "Create New Key"**
- Wählen Sie **"JSON"**
- Die Datei wird automatisch heruntergeladen

### 6. Schlüsseldatei konfigurieren
- Benennen Sie die heruntergeladene Datei um zu: `client_secret.json`
- Verschieben Sie sie in den Ordner: `Rise-of-Nations/`

### 7. Billing aktivieren (erforderlich)
⚠️ **Wichtig:** Google Cloud Translation ist kostenpflichtig
- Gehen Sie zu: **Billing**
- Verknüpfen Sie eine Zahlungsmethode mit dem Projekt
- **Erste 500,000 Zeichen pro Monat sind kostenlos**

## Kosten-Information

### Google Cloud Translation Preise (Stand 2024):
- **Kostenlos:** Erste 500,000 Zeichen/Monat
- **Danach:** $20 pro 1 Million Zeichen
- **Schätzung für Rise of Nations:** ~200,000-300,000 Zeichen = **KOSTENLOS**

## Troubleshooting

### Fehler: "API not enabled"
```bash
# Lösung: API aktivieren (siehe Schritt 3)
https://console.developers.google.com/apis/api/translate.googleapis.com/overview?project=YOUR_PROJECT_ID
```

### Fehler: "Authentication failed"
```bash
# Lösung: Überprüfen Sie client_secret.json
# Datei muss im Projektroot liegen
# Pfad: Rise-of-Nations/client_secret.json
```

### Fehler: "Quota exceeded"
```bash
# Lösung: Warten Sie bis zum nächsten Monat oder aktivieren Sie Billing
```

## Testen der Konfiguration

Nach dem Setup können Sie testen:

```bash
# Aktivieren Sie die Conda-Umgebung
conda activate riseofnations

# Starten Sie eine kleine Übersetzung
python scripts/translate_directory_to_german_improved.py localisation/english localisation/german 2
```

## Alternative: Offline-Übersetzung

Falls Sie keine Google Cloud API verwenden möchten, können Sie:

1. **LibreTranslate** (kostenlos, offline)
2. **DeepL API** (bessere Qualität, begrenzt kostenlos)
3. **Manuelle Übersetzung** wichtiger Dateien

## Support

Bei Problemen:
1. Überprüfen Sie die Google Cloud Console auf Fehlermeldungen
2. Stellen Sie sicher, dass Billing aktiviert ist
3. Warten Sie 5-10 Minuten nach API-Aktivierung