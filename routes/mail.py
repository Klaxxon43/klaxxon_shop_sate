import smtplib

def send_mail(mail):
    try:
        tema='Тема'
        text ='СПАСИБО ЗА РЕГИСТРАЦИЮ'
        mail_sender='artax7878@gmail.com'
        password = 'cndm mpfr dfah mneo'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(mail_sender, password)

        subject = tema
        body = text
        message = f'Subject: {subject}\n\n{body}'.encode('utf-8')
        

        server.sendmail(mail_sender, mail, message)
        server.quit()

        return 'good'

    except Exception as e:
        print(e)
        return 'bad'