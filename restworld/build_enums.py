import re
from contextlib import redirect_stdout

import requests
from bs4 import BeautifulSoup


class EnumDesc:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def fetch(self):
        html = requests.get(self.url).text
        return BeautifulSoup(html, 'html.parser')

    def generate(self):
        raise RuntimeError('oops')


def to_desc(text):
    text = re.sub(r'\[[^]]*]', '', text)
    if text[-1] not in '.!?':
        return text + '.'
    return text


class Advancements(EnumDesc):
    def __init__(self):
        super().__init__('Advancement', 'https://minecraft.fandom.com/wiki/Advancement#List_of_advancements')

    def generate(self):
        soup = self.fetch()
        tables = soup.find_all('table', attrs={'data-description': 'advancements'})
        advancements = {}
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    for i in range(0, len(headers)):
                        th = headers[i]
                        text = th.text.strip()
                        if text == 'Advancement':
                            name_col = i
                        elif text.startswith('Resource'):
                            str_col = i
                        elif text.find('description') >= 0:
                            desc_col = i
                else:
                    cells = row.find_all('td')
                    raw_name = cells[name_col].text.strip()
                    string = cells[str_col].text.strip()
                    desc = to_desc(cells[desc_col].text.strip())
                    name = re.sub(junk, '', raw_name).upper().replace(' ', '_')
                    name = self.replace(name, string)
                    if name in advancements:
                        raise KeyError("Duplicate name: %s (%s, %s)" % (name, string, advancements[name]))
                    advancements[name] = (string, desc)
        return advancements

    def replace(self, name, string):
        if name == 'THE_END' and string.startswith('story'):
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
            print("\n")
            for tab in (Advancements(),):
                fields = tab.generate()
                print('\n\nclass %s(ValueEnum):' % tab.name)
                for key in fields:
                    value, desc = fields[key]
                    print('    %s = "%s"\n    """%s"""' % (key, value, desc))
