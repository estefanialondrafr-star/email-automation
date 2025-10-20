#!/usr/bin/env python3
"""
Sistema de respuesta automática a emails entrantes
"""

import imaplib
import email
from email.header import decode_header
import time
from sender import EmailSender

class AutoResponder:
    def __init__(self):
        self.sender = EmailSender()
        
    def monitor_inbox_and_respond(self, check_interval=300):  # 5 minutos
        """
        Monitorea la bandeja de entrada y responde automáticamente
        """
        while True:
            try:
                # Conectar al servidor IMAP
                mail = imaplib.IMAP4_SSL("imap.gmail.com")
                mail.login(self.sender.sender_email, self.sender.sender_password)
                mail.select("inbox")
                
                # Buscar emails no leídos
                status, messages = mail.search(None, 'UNSEEN')
                email_ids = messages[0].split()
                
                for email_id in email_ids:
                    # Obtener el email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    email_body = msg_data[0][1]
                    mail_message = email.message_from_bytes(email_body)
                    
                    # Extraer información del remitente
                    sender = mail_message['From']
                    subject = mail_message['Subject']
                    
                    print(f"📧 Nuevo email de: {sender} - Asunto: {subject}")
                    
                    # Enviar respuesta automática
                    self.send_auto_response(sender, subject)
                
                mail.close()
                mail.logout()
                
            except Exception as e:
                print(f"❌ Error monitoreando inbox: {e}")
            
            # Esperar antes de revisar again
            time.sleep(check_interval)
    
    def send_auto_response(self, recipient, original_subject):
        """
        Envía respuesta automática
        """
        response_subject = f"Re: {original_subject} - Confirmación de recepción"
        response_body = f"""
        Hola,
        
        Gracias por tu email. Este es un mensaje automático para confirmar 
        que hemos recibido tu mensaje con asunto: "{original_subject}".
        
        Te responderemos personalmente dentro de las próximas 24 horas.
        
        Saludos cordiales,
        Sistema de Respuesta Automática
        """
        
        self.sender.send_basic_email(recipient, response_subject, response_body)
        print(f"✅ Respuesta automática enviada a: {recipient}")

# Ejemplo de uso
if __name__ == "__main__":
    responder = AutoResponder()
    # responder.monitor_inbox_and_respond()  # Descomentar para usar
