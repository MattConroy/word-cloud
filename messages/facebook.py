import messages.core
import datetime
import json

def _deserialiseFacebookMessage(dict):
    if 'sender_name' in dict and 'content' in dict and 'timestamp_ms' in dict:
        return messages.core.Message(
            datetime.datetime.fromtimestamp(dict['timestamp_ms']/1000.0),
            dict['sender_name'], 
            dict['content'].encode('latin1').decode('utf8'), 
            "Facebook")

def _deserialiseFacebookMessages(dict):
    if 'messages' in dict:
        return map(_deserialiseFacebookMessage, dict['messages'])
    return dict

def _readFacebookMessagesFromFile(file):
    return json.load(file, object_hook=_deserialiseFacebookMessages)

def importFacebookMessagerJson(facebookName):
    return messages.core.readFilesInFolder(f'facebook\messages\inbox\{facebookName}', 'latin1', _readFacebookMessagesFromFile)
