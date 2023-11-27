#!/bin/sh
set -e
cd `dirname $0`
./build.sh
./favicon.sh
dst_dir="restworld"
rsync -c -avz --delete --exclude=src --exclude='.??*' --exclude='*'.sh --exclude='?' --exclude='.?' --exclude='favicon.p*' . kcrca_claritypack@ssh.nyc1.nearlyfreespeech.net:$dst_dir/
