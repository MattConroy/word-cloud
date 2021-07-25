import messages.core
import datetime
import re

TIMESTAMP_REGEX = '\[([0-9]{2}\/[0-9]{2}\/[0-9]{4}, [0-9]{1,2}:[0-9]{2}:[0-9]{2} (?:am|pm))\]'
MESSAGE_REGEX = f'{TIMESTAMP_REGEX} (.*): ([\s\S]+?)(?={TIMESTAMP_REGEX})'
FAKE_DATE = '[99/99/9999, 99:99:99 pm]'

def _readWhatsAppMessagesFromFile(file):
    fileContents = file.read().replace('\u200e', '') + FAKE_DATE
    return \
        filter(lambda message: not message.content.endswith('omitted'),
        map(lambda message: messages.core.Message(
            datetime.datetime.strptime(message[0].upper(),'%d/%m/%Y, %I:%M:%S %p'),
            message[1],
            message[2],
            "WhatsApp"),
        re.findall(MESSAGE_REGEX, fileContents)))

def importWhatsAppChat(whatsAppName):
    return messages.core.readFilesInFolder(f'whatsapp\WhatsApp Chat - {whatsAppName}', 'utf8', _readWhatsAppMessagesFromFile)
