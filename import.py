#!/usr/bin/env python3
import argparse
import messages.core
import messages.facebook
import messages.whatsapp

parser = argparse.ArgumentParser()
parser.add_argument("--facebook", help="the Facebook-specific name of the messages to import")
parser.add_argument("--whatsapp", help="the WhatsApp-specific name of the messages to import")
args = parser.parse_args()

if args.facebook is None and args.whatsapp is None:
    print('No arguments specified. Using defaults.')
    args.facebook = 'catrineiraconroy_c6sobr4xpw'
    args.whatsapp = 'Catrin Eira Conroy'

importedMessages = []

if args.facebook:
    importedMessages += messages.facebook.importFacebookMessagerJson(args.facebook)
    print(f'Imported Facebook Messages for \'{args.facebook}\'.')

if args.whatsapp:
    importedMessages += messages.whatsapp.importWhatsAppChat(args.whatsapp)
    print(f'Imported WhatsApp Messages for \'{args.whatsapp}\'.')

importedMessages.sort(key = lambda message: message.timestamp)

messages.core.writeCsvFile(importedMessages)
print(f'Messages imported to \'{messages.core.CSV_FILE_NAME}\'.')
