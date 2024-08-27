from mailersend import emails
from dotenv import load_dotenv
import os

mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))

def send_mail(to_name, to_email, subject, html = "", text = ""):
    mail_body = {}

    mail_from = {
        "name": "Jeremiah from CraftMyCV",
        "email": "jeremiah@trial-z86org8660z4ew13.mlsender.net",
    }

    recipients = [
        {
            "name": to_name,
            "email": to_email,
        }
    ]


    if text == "":
        text = f"Welcome {to_name}! Congrats for sending test email with Mailtrap!\n\nInspect it using the tabs you see above and learn how this email can be improved."
    
    if html == "": 
        html = """
    <!doctype html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head>
        <body style="font-family: sans-serif;">
            <div style="display: block; margin: auto; max-width: 600px;" class="main">
                <h1 style="font-size: 18px; font-weight: bold; margin-top: 20px">
                    Congrats for sending test email with Mailtrap!
                </h1>
                <p>Inspect it using the tabs you see above and learn how this email can be improved.</p>
                <p>Now send your email using our fake SMTP server and integration of your choice!</p>
                <p>Good luck! Hope it works.</p>
            </div>
        </body>
        </html>
    """
    
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html, mail_body)
    mailer.set_plaintext_content(text, mail_body)
    
    return mailer.send(mail_body)
