import smtplib
from email.mime.text import MIMEText

class StmtMail:
    def __init__(self, STMT_HOST, PORT, ID, PW):
        self.stmt_host = STMT_HOST
        self.port = PORT
        self.sender_id = ID
        self.sender_pw = PW

    def sendmail(self, to_user, subject, contents):
        try:
            msg = MIMEText(contents)
            msg["From"] = self.sender_id
            msg["To"] = to_user
            msg["Subject"] = subject
 
            smtp = smtplib.SMTP(self.stmt_host, self.port)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.sender_id, self.sender_pw)
            smtp.sendmail(self.sender_id, to_user, msg.as_string())
            smtp.close()
        except Exception as e:
            print("[-] Error       : %s " %e)