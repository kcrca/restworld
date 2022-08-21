import datetime
import re

import requests
from bs4 import BeautifulSoup


def fetch_blocks():
    global url, html, start, elem, fp, id
    url = 'https://minecraft.fandom.com/wiki/Block#List_of_blocks'
    html = requests.get(url).text
    page = BeautifulSoup(html, 'html.parser')
    start = page.find('h2', text='List of blocks')
    elem = start.next_sibling
    no_item_blocks = {'Bamboo Shoot', 'Cave Vines', 'Cocoa', 'Fire', 'Lava', 'Melon Stem', 'Pumpkin Stem', 'Potatoes', 'Powder Snow',
                      'Redstone Wire', 'Soul Fire', 'Sweet Berry Bush', 'Tall Seagrass', 'Tripwire', 'Water'}
    with open('all_blocks.txt', 'w') as fp:
        fp.write(f'# Fetched at {datetime.datetime.now()} from {url}\n')
        for elem in start.find_next_siblings():
            if elem.name == 'h2' or 'Technical blocks' in elem.text:
                break
            for li in elem.find_all('li'):
                raw_text = li.text
                m = re.search(r'\[(.*) only]', raw_text, re.IGNORECASE)
                if m and not ('Java' in m.group(1) or 'JE' in m.group(1)):
                    continue
                if 'Air' in raw_text:
                    continue

                id = desc = raw_text.strip()
                id = id.replace("'", '_')

                if 'Ominous' in id:
                    continue
                if id in no_item_blocks:
                    continue

                # Special cases
                if 'Lapis' in id and id != 'Lapis Lazuli':
                    id = id.replace('Lapis Lazuli', 'Lapis')
                elif 'Bale' in desc:
                    id = id.replace('Bale', 'Block')
                elif 'Redstone' in id:
                    id = re.sub(r'Redstone (Repeater|Comparator)', r'\1', id)
                if 'Block' in id or 'Crops' in id:
                    id = re.sub(r'Block of (.*)', r'\1 Block', id)
                    id = re.sub(r'(Jigsaw|Light|Smooth Quartz|Wheat) (Block|Crops)', r'\1', id)
                id = re.sub(r'^(Beetroot|Carrot|Vine)s', r'\1', id)

                fp.write(id)
                if id != desc:
                    fp.write(' / ')
                    fp.write(desc)
                fp.write('\n')


def fetch_items():
    global url, html, start, elem, fp, id
    url = 'https://minecraft.fandom.com/wiki/Item?so=search#List_of_items'
    html = requests.get(url).text
    page = BeautifulSoup(html, 'html.parser')
    start = page.find('h2', text='List of items')
    elem = start.next_sibling
    id_replace = {'Redstone Dust': 'Redstone', 'Book and Quill': 'Writable Book', 'Empty Map': 'Map',
                  'Steak': 'Cooked Beef', 'Turtle Shell': 'Turtle Helmet', 'Disc Fragment': 'Disc Fragment 5',
                  'Nether Quartz': 'Quartz', 'Slimeball': 'Slime Ball'}
    with open('all_items.txt', 'w') as fp:
        fp.write(f'# Fetched at {datetime.datetime.now()} from {url}\n')
        for elem in start.find_next_siblings():
            if elem.name == 'h2' or 'Education Edition' in elem.text:
                break
            for li in elem.find_all('li'):
                raw_text = li.text
                m = re.search(r'\[(.*) only]', raw_text, re.IGNORECASE)
                if m and not ('Java' in m.group(1) or 'JE' in m.group(1)):
                    continue
                if 'Spawn Egg' in raw_text or 'Potions' in raw_text:
                    continue

                id = None
                if 'Music Disc' in raw_text:
                    raw_text = raw_text.replace('(', '').replace(')', '')
                elif 'Banner Pattern ' in raw_text:
                    m = re.fullmatch(r'Banner Pattern \(([^ ]+)( .*)?.*\)', raw_text)
                    id = f'{m.group(1)} Banner Pattern'.replace('Snout', 'Piglin').replace('Thing', 'Mojang')
                    desc = m.group(1)
                raw_text = re.sub(r'\s*[([].*', '', raw_text)
                raw_text = raw_text.replace(u'\u200c', '')  # Discard the zero-width non-joiners

                if id is None:
                    id = desc = raw_text.strip()

                # Special cases
                if 'Explorer Map' in id:
                    # This shows up twice
                    continue
                elif id in id_replace:
                    id = id_replace[id]
                elif 'Bottle o\'' in desc:
                    id = 'Experience Bottle'
                elif 'Banner Pattern ' in id:
                    m = re.fullmatch(r'Banner Pattern \(([^ ]+)( .*)?.*\)', id)
                    id = f'{m.group(1)} Banner Pattern'
                    desc = m.group(1)
                elif 'Boat with Chest' in id:
                    id = re.sub(r'(.*) Boat with Chest', r'\1 Chest Boat', id)
                elif ' with ' in id:
                    id = re.sub(r'(.*) with (.*)', r'\2 \1', id)
                elif 'Redstone Dust' in id:
                    id = 'Redstone'
                elif 'Book and Quill' in id:
                    id = 'Writable Book'
                elif ' Cap' in id:
                    id = id.replace('Cap', 'Helmet')
                elif ' Pants' in id:
                    id = id.replace('Pants', 'Leggings')
                elif ' Tunic' in id:
                    id = id.replace('Tunic', 'Chestplate')
                elif 'Bucket of' in id or 'Eye of' in id:
                    id = re.sub(r'(Bucket|Eye) of (.*)', r'\2 \1', id)
                elif "'s" in id:
                    id = id.replace("'s", '')
                elif 'Raw ' in id:
                    m = re.fullmatch('Raw (Copper|Iron|Gold)', id)
                    if not m:
                        id = id[4:]

                fp.write(id)
                if id != desc:
                    fp.write(' / ')
                    fp.write(desc)
                fp.write('\n')


fetch_items()
fetch_blocks()
