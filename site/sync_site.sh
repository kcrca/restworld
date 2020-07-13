#!/bin/sh
set -e
cd `dirname $0`
./build.sh
./update_version.sh 1.16.1
./favicon.sh
dst_dir="restworld"
rsync -c -avz --delete --exclude=src --exclude='.??*' --exclude='*'.sh --exclude='?' --exclude='.?' --exclude='favicon.p*' . kcrca_claritypack@ssh.phx.nearlyfreespeech.net:$dst_dir/
