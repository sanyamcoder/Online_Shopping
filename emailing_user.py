import smtplib


# smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials n5sm6038642pfo.40 - gsmtp') 
# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp 

content = ("Content to send")

mail = smtplib.SMTP('smtp.gmail.com',587)

mail.ehlo()

mail.starttls()

mail.login('sanyamcoder','Sanyam@99')

mail.sendmail('sanyamcoder@gmail.com','im7akash@gmail.com',content) 

mail.close()

print("Sent")