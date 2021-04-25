#!/usr/bin/python
# coding=utf-8

import json
import os
import re
from shutil import copyfile

import urllib.request
import yaml

card_id_regex = re.compile('.*/card/([^/]*/[0-9a-zA-Z%]*).*')

ends_in_letter_regex = re.compile('.*([a-z]+)$')

number_regex = re.compile('([0-9]+).*')

binders_db_path = '_data/binders.yml'

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def load_data():
    data = []

    if os.path.exists(binders_db_path):
        stream = open(binders_db_path, 'r')
        data = yaml.load(stream)
        stream.close()

    return data


def update_binders(data):
    new_data = []

    binders_dict = {}
    for binder in data:
        binders_dict[binder['name']] = binder

    binders_directories = [x for x in os.walk('_binders')][1:]

    binders_directories.sort(key=lambda y: y[0])

    for binder in binders_directories:
        new_binder_data, updated = update_binder(binder, binders_dict)

        new_data.append(new_binder_data)

        if updated:
            with open(binders_db_path, 'w') as outfile:
                yaml.dump(new_data, outfile, default_flow_style=False)

    return new_data


def update_binder(binder, binders_dict):
    binder_name = binder[0][binder[0].rfind(os.sep) + 1:]

    print(binder_name)

    page_files = binder[2]

    page_files.sort(key=lambda x: x[0])

    binder_data = {'name': binder_name, 'pages': []}

    if binder_name in binders_dict:
        binder_data = binders_dict[binder_name]

    pages_dict = {}
    for page in binder_data['pages']:
        if 'name' in page:
            pages_dict[page['name']] = page

    new_binder_data = {'name': binder_name, 'pages': []}
    updated = False
    for page_file in page_files:
        new_page, page_updated = update_page(page_file, pages_dict, binder_name)
        updated = updated or page_updated

        new_binder_data['pages'].append(new_page)

    return new_binder_data, updated


def update_page(page_file, pages_dict, binder_name):
    page_name = page_file
    page_file_extension_index = page_file.rfind('.')
    if page_file_extension_index > 0:
        page_name = page_file[0:page_file_extension_index]

    print('\t' + page_name)

    page = {'name': page_name, 'cards': []}

    if page_name in pages_dict:
        page = pages_dict[page_name]

    cards_dict = {}

    new_page = {'name': page_name, 'cards': []}
    for card in page['cards']:
        cards_dict[card['card_id']] = card

    f = open(os.path.join('_binders', binder_name, page_file), 'r')

    updated = False
    for url in f:
        card_id = card_id_regex.match(url).group(1)
        print('\t\t' + card_id)
        if card_id in cards_dict:
            print('\t\t\t' + 'card found in database')
            card = cards_dict[card_id]
        else:
            api_url = "https://api.scryfall.com/cards/" + card_id
            print('\t\t\t' + 'fetching ' + api_url)
            card = json.loads(urllib.request.urlopen(api_url).read())
            updated = True
        card['card_id'] = card_id
        new_page['cards'].append(card)

    f.close()

    return new_page, updated


def run():
    data = load_data()

    data = update_binders(data)

    for binder in data:
        binder_filename = str(binder['name']) + '.md'
        copyfile('binder.md', binder_filename)

    print('Finished')


if __name__ == '__main__':
    run()
