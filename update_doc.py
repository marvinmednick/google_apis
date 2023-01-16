from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Build the credentials object
creds = Credentials.from_authorized_user_info(info=info)

# Build the Docs API client
docs_service = build('docs', 'v1', credentials=creds)

# The ID of the document to update
document_id = 'DOCUMENT_ID'

# The text to insert
text = 'This is a pre-formatted paragraph.'

# The formatting of the text
requests = [
    {
        'insertText': {
            'text': text,
            'endOfSegmentLocation': {}}
    },
    {
        'updateTextStyle': {
            'range': {
                'startIndex': text.index('paragraph'),
                'endIndex': text.index('paragraph') + len('paragraph')
            },
            'textStyle': {
                'bold': True
            },
            'fields': 'bold'
        }
    }
]

# Execute the request to insert the text
result = docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

