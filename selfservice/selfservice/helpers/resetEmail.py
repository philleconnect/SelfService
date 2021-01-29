#!/usr/bin/env python3

# SchoolConnect SelfService API
# Password reset E-Mail sending functions
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
import smtplib
import ssl
import os
from socket import gaierror


# Send mail
def sendResetEmail(receiver, token, firstname):
    sender = os.environ.get("SMTP_SENDER") if os.environ.get("SMTP_SENDER") is not None else "noreply@philleconnect"
    domain = os.environ.get("EXTERNAL_DOMAIN")
    content = f"""\
Subject: PhilleConnect Passwort zurücksetzen: Bitte bestätigen.
To: {receiver}
From: {sender}

Hallo {firstname},

Du erhälst diese E-Mail, da du dein PhilleConnect-Passwort zurücksetzen möchtest. Mit dem Klick auf den folgenden Link wird dein neues Passwort gültig.
Achtung: Solltest du kein neues Passwort angefordert haben, klicke bitte nicht auf den Link, sondern lösche diese E-Mail.

https://{domain}/#page/confirmreset/{token}

Der Link ist 24 Stunden gültig, danach musst du einen neuen Link anfordern. Diese Nachricht wurde automatisch generiert, bitte nicht darauf antworten. """
    try:
        with smtplib.SMTP_SSL(os.environ.get("SMTP_SERVER"), int(os.environ.get("SMTP_PORT")), context=ssl.create_default_context()) as server:
            server.login(os.environ.get("SMTP_LOGIN"), os.environ.get("SMTP_PASSWORD"))
            server.sendmail(sender, receiver, content.encode("UTF-8"))
            return 0
    except (gaierror, ConnectionRefusedError):
        return -1
    except smtplib.SMTPServerDisconnected:
        return -2
    except smtplib.SMTPException as e:
        return -3
    except e:
        return -4
