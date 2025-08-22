# Mein Portfolio Backend API
Diese API ist mit FastAPI in Python gebaut und dient dazu, E-Mails über ein Kontaktformular zu senden. Sie wird auf Railway deployed.

### Deployment-Hinweise
Dieses Projekt wurde von Fly.io zu Railway migriert, um ein hartnäckiges Deployment-Problem zu lösen.

* **Ursprüngliches Problem auf Fly.io:** Die Anwendung konnte aufgrund eines Konflikts zwischen der CORSMiddleware-Konfiguration und der Fly.io-Umgebung nicht starten. Dies führte zu einem `Process completed with exit code 1`-Fehler während des Deployments.
* **Die Lösung:** Das Deployment der API auf Railway löste das Problem vollständig. Die Plattform konnte die Anwendung ohne Konfigurationsänderungen erfolgreich starten.
* **Wichtiger Hinweis:** Bei der erstmaligen Verbindung mit Railway muss sichergestellt werden, dass die GitHub-App die Berechtigung hat, auf dieses spezifische Repository zuzugreifen.