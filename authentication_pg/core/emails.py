import smtplib
from email.mime.text import MIMEText
from random import randint

code = []

def gerar_codigo():
    code.clear()
    for _ in range(4):
        code.append(str(randint(0, 9)))
    return ''.join(code)

def send_email(destinatario):
    codigo = gerar_codigo()

    subject = "Código de segurança"
    body = f"Este é o seu código de segurança:\n\n{codigo}\n\nNão compartilhe com ninguém."
    sender = "viniciuscba04@gmail.com"
    password = "ifrt utpz mqjz xskz"  # App Password

    msg = MIMEText(body)    
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = destinatario

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, destinatario, msg.as_string())
    print('email enviado')