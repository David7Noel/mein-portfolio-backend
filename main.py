from fastapi import FastAPI, HTTPException, Response, Request
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

# CORSMiddleware is still commented out as it caused a crash on Fly.io
# We will handle CORS headers manually for the contact endpoint.

# Pydantic model to validate the incoming form data
class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# Helper function to get the correct origin
def get_origin_header(request: Request):
    origin = request.headers.get("origin")
    if origin and "davidkruska.dev" in origin:
        return origin
    return "https://www.davidkruska.dev"

# Handler for the OPTIONS preflight request
@app.options("/api/send_email")
async def send_email_options(response: Response, request: Request):
    response.headers["Access-Control-Allow-Origin"] = get_origin_header(request)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return ""

# API endpoint to handle the form submission
@app.post("/api/send_email")
async def send_email(form: ContactForm, response: Response, request: Request):
    # Manually set CORS headers to allow requests from your domains
    response.headers["Access-Control-Allow-Origin"] = get_origin_header(request)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
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