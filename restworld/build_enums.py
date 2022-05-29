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

    def replace(self, name: str, string: str):
        return name

    @abstractmethod
    def is_name_col(self, text: str):
        pass

    @abstractmethod
    def is_string_col(self, text: str):
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
                        elif self.is_string_col(text):
                            str_col = i
                        elif self.is_desc_col(text):
                            desc_col = i
                        elif self.is_filter_col(text):
                            filter_col = i
                else:
                    cells = row.find_all('td')
                    if filter_col is not None and self.filter_out(cells[filter_col]):
                        continue
                    raw_name = clean(cells[name_col].text)
                    string = clean(cells[str_col].text)
                    desc = to_desc(clean(cells[desc_col].text))
                    name = re.sub(junk, '', raw_name).upper().replace(' ', '_')
                    name = self.replace(name, string)
                    if name in found:
                        raise KeyError("Duplicate name: %s (%s, %s)" % (name, string, found[name]))
                    found[name] = (string, desc)
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

    def is_string_col(self, text: str):
        return text.startswith('Resource')

    def is_desc_col(self, text: str):
        return text.find('description') >= 0

    def filter_out(self, text: str):
        pass

    def replace(self, name, string):
        if name == 'THE_END' and string.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Effects(EnumDesc):
    def __init__(self):
        super().__init__('Effects', 'https://minecraft.fandom.com/wiki/Effect?so=search#Effect_list', 'Effects')

    def is_name_col(self, text: str):
        return text == 'Display name'

    def is_string_col(self, text: str):
        return text.startswith('Name')

    def is_desc_col(self, text: str):
        return text.find('Effect') >= 0

    def is_filter_col(self, text: str):
        return text.find('ID (J.E.)')

    def filter_out(self, text: str):
        return text == 'N/A'

    def replace(self, name, string):
        if name == 'THE_END' and string.startswith('story'):
            return 'ENTER_THE_END'
        return name


# class Enchantments(EnumDesc):
#     def __init__(self):
#         super().__init__('Enchantments', 'https://minecraft.fandom.com/wiki/Enchanting#Summary_of_enchantments')
#
#     def is_name_col(self, text: str):
#         return text == 'Display name'
#
#     def is_string_col(self, text: str):
#         return text.startswith('Name')
#
#     def is_desc_col(self, text: str):
#         return text.find('Effect') >= 0
#
#     def is_filter_col(self, text: str):
#         return text.find('ID (J.E.)')
#
#     def filter_out(self, text: str):
#         return text == 'N/A'
#
#     def replace(self, name, string):
#         if name == 'THE_END' and string.startswith('story'):
#             return 'ENTER_THE_END'
#         return name
#
#     def generate(self):
#         soup = self.fetch()
#         tables = soup.find_all('table', attrs={'data-description': 'Effects'})
#         found = {}
#         for table in tables:
#             rows = table.find_all('tr')
#             for row in rows:
#                 headers = row.find_all('th')
#                 if headers:
#                     for i in range(0, len(headers)):
#                         th = headers[i]
#                         text = th.text.strip()
#                         if text == 'Display name':
#                             name_col = i
#                         elif text.startswith('Name'):
#                             str_col = i
#                         elif text.find('Effect') >= 0:
#                             desc_col = i
#                         elif text.find('ID (J.E.)'):
#                             id_col = i
#                 else:
#                     cells = row.find_all('td')
#                     id = cells[id_col].text.strip()
#                     if id == 'N/A':
#                         continue
#                     raw_name = cells[name_col].text.strip()
#                     string = cells[str_col].text.strip()
#                     string = re.sub(r'\[.*', '', string, flags=re.DOTALL)
#                     desc = to_desc(cells[desc_col].text.strip())
#                     name = re.sub(junk, '', raw_name).upper().replace(' ', '_')
#                     name = self.replace(name, string)
#                     if name in found:
#                         raise KeyError("Duplicate name: %s (%s, %s)" % (name, string, found[name]))
#                     found[name] = (string, desc)
#         return found


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
