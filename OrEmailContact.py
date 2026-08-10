
import streamlit as st
import gettext
import validators

localizator = gettext.translation('messages', localedir='locales', languages=[st.session_state.sellang])
localizator.install() 
_ = localizator.gettext 

st.title(_("Contact Form"))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication

SENDER_ADDRESS="arnchessclub@gmail.com"
# google Sign in with app passwords
SENDER_PASSWORD="aajqopqlwbapjnce"
SMTP_SERVER_ADDRESS="smtp.gmail.com"
PORT=587

def send_email(sender, password, receiver, smtp_server, 
smtp_port, email_message, subject, attachment=None):
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From']  = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message,'plain', 'utf-8'))
    if attachment:
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
  
if __name__ == '__main__':
    with st.form (_("Email Form")):
        subject = st.text_input(label=_("Subject"), placeholder=(_("Please enter subject of your mail")))
        fullName = st.text_input(label=_("Full Name"), placeholder=(_("Please enter your full name")))
        email = st.text_input(label=_("Email Address"), placeholder=(_("Please enter your email address")))
        text = st.text_area(label=_("Email Text"), placeholder=(_("Please enter your text here")))
        uploaded_file = st.file_uploader(label=_("Attachment"), type="txt")
        submit_res = st.form_submit_button(label=_("Send"))
        
        if submit_res and validators.email(email):
            extra_info = """
            -----------------------------
            Email Address of Sender {} \n
            Sender Full Name {} \n
            -----------------------------
            """.format(email, fullName)
            
            message = extra_info + text
            try:                
                send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD, receiver=SENDER_ADDRESS, smtp_server=SMTP_SERVER_ADDRESS, 
#                send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD, receiver=email, smtp_server=SMTP_SERVER_ADDRESS, 
                smtp_port=PORT, email_message=message, subject=subject, attachment=uploaded_file)
        
                st.success(_("Email sent successfully!") + ' 🚀')
            except Exception as e:
                st.error(f"Failed to send email:\n {e}")
        else:
            st.error(_("Please enter your email address"))


