import dns.resolver
import base64
import sys
from alive_progress import alive_bar
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import json

filename = str(sys.argv[1])

credentials = GoogleCredentials.get_application_default()

service = discovery.build('dns', 'v1', credentials=credentials)

# Identifies the project addressed by this request.
project = 'dnstxt'  # TODO: Update placeholder value.

# Identifies the managed zone addressed by this request. Can be the managed zone name or id.
managed_zone = 'txt'  # TODO: Update placeholder value.

def delete():
    with open(filename + ".json") as json_file:
        data = json.load(json_file)
        change_body_remove = {"deletions": [data]}
        request = service.changes().create(project=project, managedZone=managed_zone, body=change_body_remove)
        response = request.execute()
