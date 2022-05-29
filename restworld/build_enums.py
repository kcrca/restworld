import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout

import requests
from bs4 import BeautifulSoup, Tag


class EnumDesc(ABC):
    def __init__(self, name, url, data_desc: str):
        self.name = name
        self.url = url
        self.data_desc = data_desc

    def fetch(self):
        html = requests.get(self.url).text
        return BeautifulSoup(html, 'html.parser')

    def replace(self, name: str, value: str):
        return name

    @abstractmethod
    def note_header(self, col: int, text: str):
        pass

    @abstractmethod
    def extract(self, cols):
        pass

    def generate(self):
        soup = self.fetch()
        tables = soup.find_all('table', attrs={'data-description': self.data_desc})
        found = {}
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    for i in range(0, len(headers)):
                        th = headers[i]
                        text = th.text.strip()
                        self.note_header(i, text)
                else:
                    cells = row.find_all('td')
                    extracted = self.extract(cells)
                    if not extracted:
                        continue
                    name, value, desc = (clean(x) for x in extracted)
                    name = re.sub(junk, '', name).upper().replace(' ', '_')
                    name = self.replace(name, value)
                    if desc[-1] not in '.?!':
                        desc += '.'
                    if name in found:
                        raise KeyError("Duplicate name: %s (%s, %s)" % (name, value, found[name]))
                    found[name] = (value, desc)
        return found


def clean(cell: Tag) -> str:
    return re.sub(r'\[.*', '', cell.text.strip().replace(u'\u200c', ''), flags=re.DOTALL)


def to_desc(text):
    text = re.sub(r'\[[^]]*]', '', text)
    if text[-1] not in '.!?':
        return text + '.'
    return text


class Advancements(EnumDesc):
    def __init__(self):
        super().__init__('Advancement', 'https://minecraft.fandom.com/wiki/Advancement#List_of_advancements',
                         'advancements')
        self.value_col = None
        self.desc_col = None
        self.name_col = None

    def note_header(self, col: int, text: str):
        if text == 'Advancement':
            self.name_col = col
        elif text.startswith('Resource'):
            self.value_col = col
        elif text.find('description') >= 0:
            self.desc_col = col

    def extract(self, cols):
        return cols[self.name_col], cols[self.value_col], cols[self.desc_col]

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Effects(EnumDesc):
    def __init__(self):
        super().__init__('Effects', 'https://minecraft.fandom.com/wiki/Effect?so=search#Effect_list', 'Effects')
        self.filter_col = None
        self.desc_col = None
        self.value_col = None
        self.name_col = None

    def note_header(self, col: int, text: str):
        if text == 'Display name':
            self.name_col = col
        elif text.startswith('Name'):
            self.value_col = col
        elif text.find('Effect') >= 0:
            self.desc_col = col
        elif text.find('ID (J.E.)'):
            self.filter_col = col

    def extract(self, cols):
        if cols[self.filter_col] == 'N/A':
            return None
        return cols[self.name_col], cols[self.value_col], cols[self.desc_col]


class Enchantments(EnumDesc):
    def __init__(self):
        super().__init__('Enchantments', 'https://minecraft.fandom.com/wiki/Enchanting#Summary_of_enchantments',
                         'Summary of enchantments ')

    def note_header(self, col: int, text: str):
        pass

    def extract(self, cols):
        pass


if __name__ == '__main__':
    junk = re.compile(r'[^\w\s]')
    with open('enums.py', 'w') as out:
        with redirect_stdout(out):
            print('from enum import Enum')
            print("\n")
            print("class ValueEnum(Enum):")
            print("    def __str__(self):")
            print("        return super().value")
            for tab in (Advancements(), Effects()):
                fields = tab.generate()
                print('\n\nclass %s(ValueEnum):' % tab.name)
                for key in fields:
                    value, desc = fields[key]
                    print('    %s = "%s"\n    """%s"""' % (key, value, desc))
