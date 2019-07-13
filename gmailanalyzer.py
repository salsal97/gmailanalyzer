from gmailutils import setup, query_for_emails, user_id
from logger import create_log
from my_sql import *
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

database_name = "Gmailanalyzer.db"
table_name = "sender_cardinality"
field_names = ["sender","cardinality"]

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

    filename = "log/gmail_analyzer_2019-07-12_2314.json"
    file = open(filename,"r")
    messages = json.load(file)
    total = len(messages)
    one_tenth = total/50

    # senderDict = set()
    i = 0
    count = 0

    # DEPRECATING FILE IO BECAUSE REAL DEVELOPERS USE DATABASES
    # file2 = create_log(log_prefix, log_csv_suffix)
    # file2.write("From"+delimiter+"Count\n")

    conn = create_db(database_name)
    cursor = cursor_to_db(conn)
    create_table(conn, table_name, field_names)
    if (not cursor):
        print("CURSOR IS NULL??????")
        exit()
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

        # get cardinality if sender exists
        cardinality = cursor.execute("SELECT ? FROM ? WHERE ? = ?", field_names[1], table_name, field_names[0], sender).fetchall()

        # Sender does not exist
        if (not cardinality):
            values = [sender, 1]
            add_values(cursor, table_name, values)
        else:
        # Sender exists
            num = cardinality[0][0]+1
            cursor.execute("UPDATE ? SET ? = ? WHERE ? = ?",table_name,field_names[1],num,field_names[0],sender)
            # senderDict.add(sender)
            # emails_from_sender = query_for_emails(service,"from:"+sender)
            # num = len(emails_from_sender)
            # count = count + num
            # line = sender + delimiter + str(num)+"\n"
            # file2.write(line)
    # json.dump(senderDict, file2, indent=4)
    # file2.close()
    print_table(cursor, table_name)

if __name__ == '__main__':
    main()
