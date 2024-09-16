import resend
import os


def send_mail(to_name, to_email, subject, html = "", text = ""):
    resend.api_key = os.getenv("RESEND_API_KEY")
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
    
    params: resend.Emails.SendParams = {
        "from": "Jeremiah <test@craftmycv.xyz>",
        "to": [to_email],
        "subject": subject,
        "html": html,
        "text": text,
        "reply_to": "jeremiahlena13@gmail.com"
    }

    email = resend.Emails.send(params=params)
    print(email, "resend email res")
    return email
