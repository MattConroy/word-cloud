#!/usr/bin/env python3
import argparse
import configparser
import messages.core
import messages.facebook
import messages.whatsapp

parser = argparse.ArgumentParser()
parser.add_argument("--profile", help="the name of the import profile to use")
parser.add_argument("--facebook", help="the Facebook-specific name of the messages to import")
parser.add_argument("--whatsapp", help="the WhatsApp-specific name of the messages to import")
args = parser.parse_args()

if args.profile:
    config = configparser.ConfigParser()
    config.read('profiles.ini')
    if args.profile in config: 
        args.facebook = config[args.profile]['Facebook']
        args.whatsapp = config[args.profile]['WhatsApp']
    else:
        raise ValueError(f'Could not find profile named \'{args.profile}\'.')

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
