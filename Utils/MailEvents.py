import json
import logging
from Service.MailService import MailService
from Service.ConfigurationService import ConfigurationService
from Utils import Constants

def mail_userCreated(body):
    config = ConfigurationService().GetConfig()
    bodyaux = body.decode("utf-8")
    body = json.loads(body.decode("utf-8"))
    destination = body["destination"]
    name = body["user_name"]
    keyurl = config[Constants.NOTIFICATION][Constants.ENDPOINTS]["user_created"]
    keyurl += body["key"]
    asunto = "Please "+name+" validate your email"
    msg = """
    <html>
        <head>
        </head>
        <body>
            <table width='100%' bgcolor='#f6f8f1' border='0' cellpadding='0' cellspacing='0'>
                <tr>
                    <td>
                        <table cellpadding='0' cellspacing='0' border='0'>
                            <tr>
                                <td>
                                  <p style="color:#E28900;font-family:sans-serif; font-size:300%">
                                   {name},<br>
                                    <a style="color:#E28900;" href={url}> confirm your email. </a>
                                  </p><br>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>"""
    msg = msg.format(name=name,url=keyurl)
    try:
        MailService().sendMail(destination,asunto,msg)
        logging.info("Mail is sent: "+bodyaux)
    except Exception:
        logging.warning("Fail to send mail: "+bodyaux)