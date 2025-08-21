from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# CORS konfigurieren – erlaubt nur deine Domain + Subdomains
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*\.?davidkruska\.dev",
    allow_credentials=True,
    allow_methods=["*"],   # * erlaubt auch OPTIONS
    allow_headers=["*"],
)

# Einfacher Root-Endpoint, damit Fly.io Free Tier App nicht stoppt
@app.get("/")
async def root():
    return {"status": "ok"}

# Pydantic Model für Kontaktformular
class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# Endpoint für Kontaktformular
@app.post("/api/send_email")
async def send_email(form: ContactForm):
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_APP_PASSWORD")  # Gmail App Password
        receiver_email = os.getenv("RECEIVER_EMAIL")

        if not all([sender_email, sender_password, receiver_email]):
            raise HTTPException(status_code=500, detail="Email credentials missing in .env")

        # Email vorbereiten
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Contact Form Message: {form.subject}"
        email_content = f"Name: {form.name}\nEmail: {form.email}\n\nSubject: {form.subject}\n\nMessage:\n{form.message}"
        message.attach(MIMEText(email_content, "plain"))

        # SMTP senden
        smtp_server = "smtp.gmail.com"
        port = 587
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return {"message": "Email sent successfully!"}

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Email authentication failed. Check credentials.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
