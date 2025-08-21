from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

# Sichere CORS-Konfiguration für die Produktion.
# Erlaubt nur deine Domains und lokale Entwicklungsumgebungen.
origins = [
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
    "null",
    "https://www.davidkruska.dev",
    "https://davidkruska.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to validate the incoming form data
class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# API endpoint to handle the form submission
@app.post("/api/send_email")
async def send_email(form: ContactForm):
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_APP_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        if not all([sender_email, sender_password, receiver_email]):
            raise HTTPException(status_code=500, detail="Email credentials not configured in .env file.")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Contact Form Message: {form.subject}"

        email_content = f"Name: {form.name}\nEmail: {form.email}\n\nSubject: {form.subject}\n\nMessage:\n{form.message}"
        message.attach(MIMEText(email_content, "plain"))

        smtp_server = "smtp.gmail.com"
        port = 587
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return {"message": "Email sent successfully!"}
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Email authentication failed. Check SENDER_EMAIL and SENDER_APP_PASSWORD in .env (App Password needed for Gmail).")
    except smtplib.SMTPConnectError:
        raise HTTPException(status_code=502, detail="Could not connect to SMTP server. Check server address or network connection.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")