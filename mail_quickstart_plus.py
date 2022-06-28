from __future__ import print_function
import os.path
from dumper import dump   
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    label_map = {}
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            label_map[label['name']] = label['id']
            print(label['name'], label['id'])

    results = service.users().getProfile(userId='me').execute()
    print(f"Results {results}")
#
#{
#  "emailAddress": string,
#  "messagesTotal": integer,
#  "threadsTotal": integer,
#  "historyId": string
#}
    loop_cnt = 0
    done = False
    pageToken = ""
    total_messages = 0
    while not done:

        results = service.users().messages().list(userId='me', labelIds=[label_map['test1']],pageToken=pageToken,includeSpamTrash=False).execute()
        messages = results.get('messages')
        estCount = results.get('resultSizeEstimate')
        pageToken = results.get('pageToken')
        print(f"retrieved {len(messages)} {estCount} Pg: {pageToken}")

        if not messages:
            print('No more Messages found.')
            done = True
            
        else:
            count = 0
            print('Messages:')
            for msg in messages:
                count += 1
                if count > 100:
                    break
                print(msg['id'],msg['threadId'],end=" ")
                results = service.users().messages().get(userId='me',format="full",id=msg['id']).execute()
                payload = results.get('payload',[])
                for k in results.keys():
                    print(f"{k} ",end=" ")
                print()

                print("Payload Keys: ",end=" ")
                for k in payload.keys():
                    print(f"{k} ",end=" ")
                print()
                for k in payload.keys():
                    if k != 'body':
                        print(f"{k} {payload[k]}")
                    else:
                        decode = base64.urlsafe_b64decode(payload[k]['body']['data'])
                        print(f"{k} {decode}")
                print()
                # dump(payload)
                for hdr in payload['headers']:
                    # print ("HDR {} : {}".format(hdr['name'],hdr['value']))
                    for name in ["Cc","From","To","Subject"]:
                        if hdr['name'] ==  name:
                            print ("{} : {}   ".format(hdr['name'],hdr['value']),end=" ")
                print('--------------------\n')
                if "Cc" in hdr:
                    del hdr["Cc"]
                if "Bcc" in hdr:
                    del hdr["Bcc"]
                hdr["To"] = "dengizsj@gmail.com"
                results = service.users().messages().get(userId='me',id=msg['id']).execute()
                user_id='mmednick@gmail.com'
#                message = (service.users().messages().send(userId=user_id, body=msg).execute())
#                print('Message Id: %s' % message['id'])

        loop_cnt += 1
        if pageToken == None or loop_cnt > 1:
            done = True
        total_messages += len(messages)


    print(f"retrieved {total_messages}")


if __name__ == '__main__':
    main()
