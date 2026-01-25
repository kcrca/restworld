#!/bin/zsh
set -e

cd `dirname $0`

./build.sh
./favicon.sh

reminder=$(<<\EOF
Required:

(*) Reset books to page 1
(*) switched to default textures and reset the paintings room
(*) run function restworld:ready

Did you? 
EOF
)
read -q "v?$reminder"
echo ""
if [[ $v != 'y' ]] then 
    exit 1
fi

rwback -q
dst_dir="restworld"
rsync -c -avz --delete --exclude=src --exclude='.??*' --exclude='*'.sh --exclude='?' --exclude='favicon.p*' . kcrca_claritypack@ssh.nyc1.nearlyfreespeech.net:$dst_dir/
