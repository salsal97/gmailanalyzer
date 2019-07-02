from gmailutils import setup, query_for_emails, user_id
from logger import create_log
import json
import base64
import sys

query = ''
log_prefix = 'log/gmail_analyzer_'
log_suffix = '.json'
service = setup()

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
    msg = service.users().messages().get(userId=user_id, id=id, format='full').execute()
    return msg

def main():

    # filename = get_emails_json()
    # print("Results printed to "+filename)

    filename = "log/gmail_analyzer_2019-07-01_2245.json"
    file = open(filename,"r")
    messages = json.load(file)
    total = len(messages)/10
    one_tenth = total/10

    senderDict = {}
    i = 0
    count = 0
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

        headers = msg['payload']['headers']
        for names in headers:
            if (names['name'] == "From"):
                sender = names['value']
                if sender in senderDict:
                    senderDict[sender] += 1
                else:
                    senderDict[sender] = 1
                break
        i = i + 1
        count = count + 1

    file2 = open("result.json", "w")
    json.dump(senderDict, file2, indent=4)
    file2.close()

if __name__ == '__main__':
    main()
