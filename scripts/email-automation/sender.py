#!/usr/bin/env python3
"""
Script básico para envío de emails
"""

import smtplib
import yagmail
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
from dotenv import load_dotenv
import json

load_dotenv()

class EmailSender:
    def __init__(self, config_file="config/email_config.yaml"):
        self.sender_email = os.getenv('EMAIL_USER')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        
    def send_basic_email(self, recipient, subject, body):
        """
        Envía un email básico usando SMTP
        """
        try:
            # Usando yagmail (más simple)
            yag = yagmail.SMTP(self.sender_email, self.sender_password)
            yag.send(
                to=recipient,
                subject=subject,
                contents=body
            )
            print(f"✅ Email enviado a: {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False
    
    def send_html_email(self, recipient, subject, html_content):
        """
        Envía un email con formato HTML
        """
        try:
            yag = yagmail.SMTP(self.sender_email, self.sender_password)
            yag.send(
                to=recipient,
                subject=subject,
                contents=html_content
            )
            print(f"✅ Email HTML enviado a: {recipient}")
            return True
        except Exception as e:
            print(f"❌ Error enviando email HTML: {e}")
            return False

# Ejemplo de uso
if __name__ == "__main__":
    email_sender = EmailSender()
    
    # Email básico
    email_sender.send_basic_email(
        recipient="destinatario@ejemplo.com",
        subject="Prueba de automatización",
        body="Hola, este es un email automatizado."
    )
