from gmailutils import setup, query_for_emails, user_id
from logger import create_log
import json
import base64
import sys
import datetime

query = ''
log_prefix = 'log/gmail_analyzer_'
log_suffix = '.json'
log_csv_suffix = '.csv'
service = setup()
delimiter = ", "

def get_emails_json():
    # check for token.pickle, setup service; Get all mail
    messages = query_for_emails(service=service, query='')

    # create json file, dump all message ids
    file = create_log(log_prefix, log_suffix)
    json.dump(messages, file, indent=4)
    filename = file.name
    file.close()
    return filename

def get_email(id):
    # Get the message object response
    msg = service.users().messages().get(userId=user_id, id=id, format='metadata', metadataHeaders=["From"]).execute()
    return msg

def main():

    # filename = get_emails_json()
    # print("Results printed to "+filename)

    filename = "log/gmail_analyzer_2019-07-01_2245.json"
    file = open(filename,"r")
    messages = json.load(file)
    total = len(messages)/10
    one_tenth = total/50

    senderDict = set()
    i = 0
    count = 0

    file2 = create_log(log_prefix, log_csv_suffix)
    file2.write("From"+delimiter+"Count\n")

    for msg in messages:
        if (i%one_tenth == 0):
            i = 0
            print("O",end="")
            sys.stdout.flush()
        if (count == total):
            break
        msg = get_email(msg["id"])
        # file1 = open("get_headers.json","w")
        # json.dump(msg['payload']['headers'], file1, indent=4)
        # file1.close()

        i = i + 1
        sender = msg['payload']['headers'][0]['value']
        if sender not in senderDict:
            senderDict.add(sender)
            emails_from_sender = query_for_emails(service,"from:"+sender)
            num = len(emails_from_sender)
            count = count + num
            line = sender + delimiter + str(num)+"\n"
            file2.write(line)
        else:
            continue
    # json.dump(senderDict, file2, indent=4)
    file2.close()

if __name__ == '__main__':
    main()
