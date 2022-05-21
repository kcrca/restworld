#!/bin/sh
#
# This script translates a JimStoneCraft book into a book we can use, reading
# unicode_text.txt and producing unicode_text.mcftmpl
#
# unicode_text.txt is downloaded from https://www.johnsmithlegacy.co.uk/jimstonecraft.php
set -x
src="unicode_text.txt"
if [[ ! -f $src ]]; then
    echo "$src: No such file"
    exit 1
fi

tr -d \\r < $src > /tmp/ut$$
mv /tmp/ut$$ $src
ex - $src <<\EOF
1i
<%namespace name="base" file="../base.mcftmpl"/>

.
g/^===/s//## &/
0/^## ===/+1;/^## ===/-1s/^/## /
/^.give @p/c
<%
book = r'''
.
$a
'''.replace('\n', '').replace('.png', '').replace('.otf', '')
%>
<%base.ensure("~0 ~2 ~0", 'lectern[facing=east,has_book=true]', nbt='Book:{id:"minecraft:written_book", Count:1, tag: %s}' % book)%>
.
wq! unicode_text.mcftmpl
EOF
