#!/usr/bin/python

import urllib2
import json
import sys
import re
import os
import yaml
from shutil import copyfile

card_id_regex = re.compile(".*/card/([^/]*/[0-9]*).*")

binders_directories = [x for x in os.walk('_binders')][1:]

binders_directories.sort(key=lambda x:x[0])

data = []

binders_db_path = '_data/binders.yml'

if (os.path.exists(binders_db_path)):
    stream = file(binders_db_path, 'r')
    data = yaml.load(stream)

binders_dict = {}
for binder in data:
    binders_dict[binder['name']] = binder

new_data = []

for binder in binders_directories:
    binder_name = binder[0][binder[0].rfind(os.sep)+1:]

    print binder_name

    page_files = binder[2]

    page_files.sort(key=lambda x:x[0])
    
    binder_data = {'name': binder_name, 'pages': []}

    if binder_name in binders_dict:
        binder_data = binders_dict[binder_name]

    pages_dict = {}
    for page in binder_data['pages']:
        pages_dict[page['name']] = page
    
    new_binder_data = {'name': binder_name, 'pages': []}
    for page_file in page_files:
        page_name = page_file[0:page_file.rfind('.')]
        
        print '\t' + page_name

        page = {'name': page_name, 'cards': []}

        if page_name in pages_dict:
            page = pages_dict[page_name]

        cards_dict = {}

        new_page = {'name': page_name, 'cards': []}
        for card in page['cards']:
            cards_dict[card['card_id']] = card

        f = open(os.path.join('_binders', binder_name, page_file), 'r')
        
        for url in f:
            card_id = card_id_regex.match(url).group(1)
            print '\t\t' + card_id
            card = {}
            if card_id in cards_dict:
                print '\t\t\t' + 'card found in database'
                card = cards_dict[card_id]
            else:
                api_url = "https://api.scryfall.com/cards/" + card_id
                print '\t\t\t' + 'fetching ' + api_url
                card = json.loads(urllib2.urlopen(api_url).read())
            card['card_id'] = card_id
            new_page['cards'].append(card)

        f.close()

        new_binder_data['pages'].append(new_page)

    new_data.append(new_binder_data)

data = new_data

with open(binders_db_path, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

for binder in data:
    copyfile('binder.md', binder['name'] + '.md')

print 'Finished'