import os
import csv

NEW_LINE_REPLACEMENT = 'Þ'
CSV_FILE_NAME = 'messages.csv'

class Message:
    def __init__(self, timestamp, sender, content, source):
        if timestamp is None: raise ValueError("timestamp cannot be null.")
        if sender is None or sender.isspace(): raise ValueError("sender cannot be null or whitespace.")
        if content is None or content.isspace(): raise ValueError("content cannot be null or whitespace.")
        if source is None or source.isspace(): raise ValueError("source cannot be null or whitespace.")

        self.timestamp = timestamp
        self.sender = sender
        self.content = content.strip().replace('\r\n', '\n').replace('\n', NEW_LINE_REPLACEMENT)
        self.source = source

def readFilesInFolder(folder, encoding, fileParser):
    return [message for messageList in
        map(fileParser,
        map(lambda path: open(path, 'r', encoding=encoding),
        filter(lambda path: os.path.isfile(path),
        map(lambda name: os.path.join(folder, name),
        os.listdir(folder)))))
        for message in messageList
        if message is not None]

def writeCsvFile(messages):
    with open(CSV_FILE_NAME, 'w', encoding='utf8', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_ALL)
        csvWriter.writerow([ 'timestamp', 'source', 'sender', 'content' ])
        for message in messages:
            csvWriter.writerow([
                message.timestamp.replace(microsecond=0),
                message.source,
                message.sender, 
                message.content
            ])
