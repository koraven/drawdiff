import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import quote
import re


def get_diagram_from_attachments(page_title, space='', version=''):
    DIAGRAM_NUMBER = None
    with open('drawdiff_conf.json','r') as conf:
        config = json.load(conf)

    auth = HTTPBasicAuth(config['auth']['username'], config['auth']['password'])
    confluence_url = config['confluence']['url']
    resp = requests.get(
            url = f"{confluence_url}/rest/api/content/?title={page_title}",
            auth = auth
        )
    #TODO: may be fix [0] is necessary
    page_id = json.loads(resp.text)['results'][0]['id']

    resp = requests.get(
            url = f"{confluence_url}/rest/api/content/{page_id}/child?expand=attachment",
            auth = auth
        )

    attachments = json.loads(resp.text)
    diagrams = list()
    for attach in attachments['attachment']['results']:
        if attach['metadata']['mediaType'] == 'application/vnd.jgraph.mxfile' or attach['metadata']['mediaType'] == 'application/drawio':
            diagrams.append({
                'name': attach['title'],
                'download': attach['_links']['download']
                })
    print(*diagrams, sep='\n')
    if len(diagrams) == 1:
        if version != '':
            download_path = re.sub(r"version=\d*",f"version={version}",diagrams[0]['download'])
        else:
            download_path = diagrams[0]['download']
    elif not DIAGRAM_NUMBER:
        print('There are more than 1 diagram on the page. Please, enter a number of your diagram from list below:')
        it = 1
        for diagram in diagrams:
            print(f"{it}. {diagram['name']}")
            it += 1
        while True:
            try:
                DIAGRAM_NUMBER = int(input())
                break
            except ValueError:
                print('Enter number.')
        download_path = re.sub(r"version=\d*",f"version={version}",diagrams[DIAGRAM_NUMBER-1]['download'])
    resp = requests.get(
            url = confluence_url + download_path,
            auth = auth
        )
    return resp.text
