import base64
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(to_email, subject, body, reg, name, year, logo_path, attachment_path):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'cybertrixofficials@gmail.com'
    smtp_password = 'xnfm wrbs jjii dwtp '

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    body_with_logo = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Congratulations!</title>
    </head>
    <body style="font-family: 'Roboto Mono', monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0;">
    
    <div class="card" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 30px; transition: transform 0.3s ease; width: 300px;">
        <h2 style="color: #333; margin-bottom: 15px; font-size: 1.5rem;">Congratulations!</h2>
        <p style="margin-bottom: 10px; font-size: 1rem; color: #000;">Mr/Ms {name},</p>
        <p style="margin-bottom: 10px; font-size: 1rem; color: #000;text-align: justify;">Congratulations on getting shortlisted and selected to be part of the Cybertrix Club. Looking forward to working with you in future events and club activities!</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin-bottom: 15px;">
        <p><b style="font-size: 1rem;">Name:</b> {name}</p>
        <p><b style="font-size: 1rem;">Register Number:</b> {reg}</p>
        <p><b style="font-size: 1rem;">Team:</b> {year}</p>
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{encode_image_as_base64(logo_path)}" alt="Club Logo">
        </div>
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{encode_image_as_base64(attachment_path)}" alt="QR Code">
        </div>
    </div>
    
    </body>
    </html>
    """

    message.attach(MIMEText(body_with_logo, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

    print(f'Email to {to_email} with body and logo sent successfully!')


def encode_image_as_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image



