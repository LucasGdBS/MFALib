from enum import Enum


class SMTPServer(Enum):
    GMAIL = "smtp.gmail.com"
    YAHOO = "smtp.mail.yahoo.com"
    OUTLOOK = "smtp-mail.outlook.com"
    ZOHO = "smtp.zoho.com"
    AOL = "smtp.aol.com"

    def __str__(self) -> str:
        return self.value
    
    @property
    def port(self) -> int:
        return 587