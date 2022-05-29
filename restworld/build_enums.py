import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout

import requests
from bs4 import BeautifulSoup


class EnumDesc(ABC):
    def __init__(self, name, url, data_desc: str):
        self.name = name
        self.url = url
        self.data_desc = data_desc

    def fetch(self):
        html = requests.get(self.url).text
        return BeautifulSoup(html, 'html.parser')

    def generate(self):
        raise RuntimeError('oops')

    def replace(self, name: str, value: str):
        return name

    @abstractmethod
    def is_name_col(self, text: str):
        pass

    @abstractmethod
    def is_value_col(self, text: str):
        pass

    @abstractmethod
    def is_desc_col(self, text: str):
        pass

    def is_filter_col(self, text: str):
        return False

    def filter_out(self, text: str):
        return True

    def generate(self):
        soup = self.fetch()
        tables = soup.find_all('table', attrs={'data-description': self.data_desc})
        found = {}
        filter_col = None
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    for i in range(0, len(headers)):
                        th = headers[i]
                        text = th.text.strip()
                        if self.is_name_col(text):
                            name_col = i
                        elif self.is_value_col(text):
                            value_col = i
                        elif self.is_desc_col(text):
                            desc_col = i
                        elif self.is_filter_col(text):
                            filter_col = i
                else:
                    cells = row.find_all('td')
                    if filter_col is not None and self.filter_out(cells[filter_col]):
                        continue
                    raw_name = clean(cells[name_col].text)
                    value = clean(cells[value_col].text)
                    desc = to_desc(clean(cells[desc_col].text))
                    name = re.sub(junk, '', raw_name).upper().replace(' ', '_')
                    name = self.replace(name, value)
                    if name in found:
                        raise KeyError("Duplicate name: %s (%s, %s)" % (name, value, found[name]))
                    found[name] = (value, desc)
        return found


def clean(text: str) -> str:
    return re.sub(r'\[.*', '', text.strip().replace(u'\u200c', ''), flags=re.DOTALL)


def to_desc(text):
    text = re.sub(r'\[[^]]*]', '', text)
    if text[-1] not in '.!?':
        return text + '.'
    return text


class Advancements(EnumDesc):
    def __init__(self):
        super().__init__('Advancement', 'https://minecraft.fandom.com/wiki/Advancement#List_of_advancements',
                         'advancements')

    def is_name_col(self, text: str):
        return text == 'Advancement'

    def is_value_col(self, text: str):
        return text.startswith('Resource')

    def is_desc_col(self, text: str):
        return text.find('description') >= 0

    def filter_out(self, text: str):
        pass

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Effects(EnumDesc):
    def __init__(self):
        super().__init__('Effects', 'https://minecraft.fandom.com/wiki/Effect?so=search#Effect_list', 'Effects')

    def is_name_col(self, text: str):
        return text == 'Display name'

    def is_value_col(self, text: str):
        return text.startswith('Name')

    def is_desc_col(self, text: str):
        return text.find('Effect') >= 0

    def is_filter_col(self, text: str):
        return text.find('ID (J.E.)')

    def filter_out(self, text: str):
        return text == 'N/A'

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Enchantments(EnumDesc):
    def __init__(self):
        super().__init__('Enchantments', 'https://minecraft.fandom.com/wiki/Enchanting#Summary_of_enchantments',
                         'Summary of enchantments ')

    def is_name_col(self, text: str):
        return text == 'Name'

    def is_value_col(self, text: str):
        return text.startswith('Name')

    def is_desc_col(self, text: str):
        return text.find('Effect') >= 0

    def is_filter_col(self, text: str):
        return text.find('ID (J.E.)')

    def filter_out(self, text: str):
        return text == 'N/A'

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


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
