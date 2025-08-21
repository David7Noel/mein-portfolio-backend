from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

# Configure CORS to allow your frontend to communicate with the backend
origins = [
    "http://127.0.0.1:5500",  # For local development (e.g., Live Server extension)
    "http://localhost:5500", # Alternative for local development
    "null",                  # CRUCIAL FOR LOCAL FILE-BASED ORIGINS!
    "https://mein-portfolio.vercel.app" # Your deployed Vercel application URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

# Pydantic model to validate the incoming form data
class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# API endpoint to handle the form submission
# Changed endpoint to /api/send_email to match frontend
@app.post("/api/send_email")
async def send_email(form: ContactForm):
    try:
        # Get credentials from the .env file
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_APP_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        # Check if environment variables are loaded
        if not all([sender_email, sender_password, receiver_email]):
            raise HTTPException(status_code=500, detail="Email credentials not configured in .env file.")

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Contact Form Message: {form.subject}"

        email_content = f"Name: {form.name}\nEmail: {form.email}\n\nSubject: {form.subject}\n\nMessage:\n{form.message}"
        message.attach(MIMEText(email_content, "plain"))

        # Connect to Gmail's SMTP server
        smtp_server = "smtp.gmail.com"
        port = 587  # Standard port for TLS
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection using TLS
            server.login(sender_email, sender_password)
            server.send_message(message)

        return {"message": "Email sent successfully!"}
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Email authentication failed. Check SENDER_EMAIL and SENDER_APP_PASSWORD in .env (App Password needed for Gmail).")
    except smtplib.SMTPConnectError:
        raise HTTPException(status_code=502, detail="Could not connect to SMTP server. Check server address or network connection.")
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")