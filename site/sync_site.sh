#!/bin/sh
set -e
./build.sh
cd `dirname $0`
dst_dir="restworld"
rsync -c -avz --delete --exclude=src --exclude='.??*' --exclude='*'.sh --exclude='?' --exclude='.?' --exclude='favicon.p*' . kcrca_claritypack@ssh.phx.nearlyfreespeech.net:$dst_dir/
