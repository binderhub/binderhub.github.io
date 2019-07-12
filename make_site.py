#!/usr/bin/python

import urllib2
import json
import sys
import re
import os
import yaml
from shutil import copyfile

card_id_regex = re.compile('.*/card/([^/]*/[0-9a-zA-Z]*).*')

ends_in_letter_regex = re.compile('.*([a-z]+)$')

number_regex = re.compile('([0-9]+).*')

binders_db_path = '_data/binders.yml'

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def load_data():
    data = []

    if (os.path.exists(binders_db_path)):
        stream = file(binders_db_path, 'r')
        data = yaml.load(stream)

    return data

def update_binders(data):
    new_data = []

    binders_dict = {}
    for binder in data:
        binders_dict[binder['name']] = binder

    binders_directories = [x for x in os.walk('_binders')][1:]

    binders_directories.sort(key=lambda x:x[0])

    for binder in binders_directories:
        new_binder_data = update_binder(binder, binders_dict)

        new_data.append(new_binder_data)

    return new_data

def update_binder(binder, binders_dict):
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
        new_page = update_page(page_file, pages_dict, binder_name)

        new_binder_data['pages'].append(new_page)

    return new_binder_data

def update_page(page_file, pages_dict, binder_name):
    page_name = page_file
    page_file_extension_index = page_file.rfind('.')
    if (page_file_extension_index > 0):
        page_name = page_file[0:page_file_extension_index]
    
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
        collector_number = card['collector_number']
        if (isinstance(collector_number, basestring)):
            collector_number = collector_number.replace('#', '')
            card['collector_number_string'] = collector_number
            if ends_in_letter_regex.search(collector_number):
                number = number_regex.match(collector_number).group(1)
                letters = ends_in_letter_regex.match(collector_number).group(1)
                for i in range(0, len(alphabet)):
                    letters = letters.replace(alphabet[i], str(i + 1))
                collector_number = number + '.' + letters
        card['collector_number'] = float(collector_number)
        new_page['cards'].append(card)

    f.close()

    return new_page

def run():
    data = load_data()

    data = update_binders(data)

    with open(binders_db_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    for binder in data:
        copyfile('binder.md', binder['name'] + '.md')

    print 'Finished'

if __name__ == '__main__':
    run()