#!/bin/zsh

set -e

cd `dirname $0`

ver_cur="$1"
[ x"$ver_cur" != x"" ] || (echo Must specify version ; exit 1)
ver_old=$(sed -E -n -e 's/^<.-- version: ([^ ]*) -->/\1/p' < index.html)
ver_old_re=$(echo "$ver_old" | sed -e 's/[.]/\\./g')

ts_cur=$(stat -f '%Sm' index.html)

rm -f index.html.new
ex - index.html <<EOF || true
g/\\<$ver_old_re\\>/s//$ver_cur/g
g/_$ver_old_re\\>/s//_$ver_cur/g
/CopyrightBegin/+,/CopyrightEnd/-d
/CopyrightBegin/r ../License.html
/\\(<p class="timestamp">\\).*/s//\1Page Last Edited: $ts_cur/
w index.html.new
q!
EOF

(
    echo /-- Start downloads/+,/-- End downloads/-c
    for f in Rest?orld*.zip; do
        name=${f:s,RestWorld_,}
        name=${name:s,.zip,}
        cat <<EOF
                        <a class="download_pack" href="$f">$name</a>,
EOF
    done
    echo .
    echo w
    echo q
) | ed - index.html.new

# If it's been changed, update the edit date
if cmp -s index.html index.html.new; then
    rm index.html.new
else
    mv index.html.new index.html
fi
