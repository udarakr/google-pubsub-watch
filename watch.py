#!/usr/bin/env python

import sys
import configparser

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from oauth2client.client import HttpAccessTokenRefreshError

def main(argv):
    #TODO handle IO errors
    #parse the config and get the topic
    parser = configparser.ConfigParser()
    parser.read_file(open('config'))
    topic = parser.get('configs', 'TOPIC')
    label = parser.get('configs', 'LABEL')

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'creds.json', scopes='https://mail.google.com')
        credentials = credentials.create_delegated(argv[1])

        service = build('gmail', 'v1', credentials=credentials)

        request = {
            'labelIds': [label],
            'topicName': topic
        }

        # Call the Gmail API to watch given mailbox label
        result = service.users().watch(userId='me', body=request).execute()
        print(result)
    except HttpAccessTokenRefreshError as e:
        print('An error occurred HttpAccessTokenRefreshError: %s' % e)
    except HttpError as err:
        print('An error occurred HttpError: %s' % err)
if __name__ == '__main__':
    main(sys.argv)
