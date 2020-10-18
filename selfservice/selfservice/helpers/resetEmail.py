#!/usr/bin/env python3

# SchoolConnect SelfService API
# Password reset E-Mail sending functions
# © 2020 Johannes Kreutz.

# Include dependencies
import smtplib
from email.message import EmailMessage
import os

# Send mail
def sendResetEmail(receiver, token, firstname):
    msg = EmailMessage()
    sender = os.environ.get("SMTP_SENDER") if not os.environ.get("SMTP_SENDER") == None else "noreply@philleconnect"
    msg["Subject"] = "PhilleConnect Passwort zurücksetzen: Bitte bestätigen."
    msg["From"] = sender
    msg["To"] = receiver
    content = """ Hallo FIRSTNAME_REPLACE,
    Du erhälst diese E-Mail, da du dein PhilleConnect-Passwort zurücksetzen möchtest. Mit dem Klick auf den folgenden Link wird dein neues Passwort gültig.
    Achtung: Solltest du kein neues Passwort angefordert haben, klicke bitte nicht auf den Link, sondern lösche diese E-Mail.

    https://DOMAIN_REPLACE/api/reset/confirm/TOKEN_REPLACE

    Der Link ist 24 Stunden gültig. Diese Nachricht wurde automatisch generiert, bitte nicht darauf antworten. """
    content.replace("FIRSTNAME_REPLACE", firstname)
    content.replace("DOMAIN_REPLACE", os.environ.get("EXTERNAL_DOMAIN"))
    content.replace("TOKEN_REPLACE", token)
    msg.set_content(content)
    s = smtplib.SMTP(os.environ.get("SMTP_SERVER"))
    s.send_message(msg)
    s.quit()
