import asyncio
import json
#import logging
from loguru import logger

import smtplib
from email.mime.text import MIMEText


async def send_email_to_me(msg: str, email_info: map):
    '''
        向指定的smtp服务器发送电子邮件
    '''
    email_host = email_info["email_host"]
    port = email_info["port"]
    email = email_info["email"]
    auth = email_info["auth"]

    mime_msg = MIMEText(msg)
    mime_msg['subject'] = msg
    mime_msg['from'] = email
    mime_msg['to'] = email

    s = smtplib.SMTP_SSL(email_host, port)
    s.login(email, auth)
    s.sendmail(
        email, email, mime_msg.as_string()
    )
    logger.info("Sent email({}) to {}", msg, email)

