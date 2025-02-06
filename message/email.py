import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


# Sent Email 

def send_mail(email, subject, message):
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = email
    password_email = settings.EMAIL_HOST_PASSWORD

    subject = subject
    message = message
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            
        return "Email sent successfully."
        
    except smtplib.SMTPAuthenticationError:
        return {"status": "error", "message": "Authentication failed, please check your email credentials."}
    except smtplib.SMTPException as e:
        return {"status": "error", "message": f"SMTP error occurred: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}