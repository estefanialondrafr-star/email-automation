#!/usr/bin/env python3
"""
Sistema de envío masivo de emails
"""

import pandas as pd
import time
from sender import EmailSender
import json

class BulkEmailSender:
    def __init__(self):
        self.sender = EmailSender()
        
    def send_bulk_from_csv(self, csv_file, subject_template, body_template):
        """
        Envía emails masivos desde un archivo CSV
        """
        try:
            df = pd.read_csv(csv_file)
            
            for index, row in df.iterrows():
                # Personalizar el email
                subject = subject_template.format(**row.to_dict())
                body = body_template.format(**row.to_dict())
                
                # Enviar email
                self.sender.send_basic_email(
                    recipient=row['email'],
                    subject=subject,
                    body=body
                )
                
                # Pequeña pausa para no saturar
                time.sleep(2)
                
            print(f"✅ Envío masivo completado. Total: {len(df)} emails")
            
        except Exception as e:
            print(f"❌ Error en envío masivo: {e}")
    
    def send_newsletter(self, contacts_list, html_template_path):
        """
        Envía newsletter a lista de contactos
        """
        with open(html_template_path, 'r', encoding='utf-8') as file:
            html_template = file.read()
        
        for contact in contacts_list:
            # Personalizar template
            personalized_html = html_template.format(
                nombre=contact['nombre'],
                email=contact['email']
            )
            
            self.sender.send_html_email(
                recipient=contact['email'],
                subject="Nuestro Newsletter Semanal",
                html_content=personalized_html
            )
            time.sleep(1)

# Ejemplo de uso
if __name__ == "__main__":
    bulk_sender = BulkEmailSender()
    
    # Ejemplo de CSV debería tener columnas: nombre,email,empresa,etc.
    bulk_sender.send_bulk_from_csv(
        csv_file="config/contacts.csv",
        subject_template="Hola {nombre} - Oferta especial",
        body_template="""
        Hola {nombre},
        
        Nos complace contactarte con una oferta especial para {empresa}.
        
        Saludos,
        El equipo de automatización
        """
    )
