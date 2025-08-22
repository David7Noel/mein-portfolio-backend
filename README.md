# 📬 Mein Portfolio Backend API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-purple)

Eine Backend-API mit **FastAPI (Python)**, die Kontaktformular-Nachrichten per E-Mail versendet. Das Projekt ist für eine einfache Integration und ein schnelles Deployment optimiert.

---

### 🚀 Features

-   **API mit FastAPI**: Eine schnelle, asynchrone Python-Web-API.
-   **Kontaktformular-Endpoint**: Ermöglicht den Versand von E-Mails aus dem Frontend.
-   **Sichere Konfiguration**: Verwendet Umgebungsvariablen (`.env`) zum Schutz sensibler Daten.
-   **Deployment-ready**: Erfolgreich auf Railway gehostet.

---

### ⚙️ Installation & Lokales Setup

Um dieses Projekt lokal auszuführen, folge diesen Schritten:

```bash
# Repo klonen
git clone https://github.com/David7Noel/mein-portfolio-backend.git

cd mein-portfolio-backend

# Abhängigkeiten installieren
pip install -r requirements.txt

# .env-Datei erstellen und Umgebungsvariablen setzen
# Beispiel: SENDER_EMAIL="deine-email@gmail.com"
uvicorn main:app --reload

Die API ist danach lokal unter http://127.0.0.1:8000 erreichbar.

🔌 API Endpunkte
POST /api/send_email

Dieser Endpunkt verarbeitet Kontaktformular-Anfragen.

Body (JSON):

JSON

{
  "name": "Max Mustermann",
  "email": "max@example.com",
  "subject": "Interesse am Portfolio",
  "message": "Hallo, ich bin an einer Zusammenarbeit interessiert!"
}
Antwort:

JSON

{
  "message": "Email sent successfully!"
}
🌐 Deployment-Hinweise
Dieses Projekt wurde von Fly.io zu Railway migriert, um ein hartnäckiges Deployment-Problem zu lösen.

Ursprüngliches Problem auf Fly.io: Die Anwendung konnte nicht starten (exit code 1), da es einen Konflikt zwischen der CORS-Konfiguration und der Fly.io-Umgebung gab.

Die Lösung: Das Deployment auf Railway funktionierte reibungslos und ohne zusätzliche Konfiguration.

Wichtiger Hinweis: Bei der Verknüpfung des Repos mit Railway muss der GitHub-App Zugriff auf dieses spezielle Repository erteilt werden.

📜 Lizenz
Dieses Projekt steht unter der MIT-Lizenz.

Aktualisiert am 23. August 2025