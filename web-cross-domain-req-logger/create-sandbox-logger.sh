#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

rm -rf firejail-home-logger

mkdir firejail-home-logger

cp create-profile-chromium.sh log-page.sh take-one-page-from-top-of-list-and-log.sh process-list-until-empty.sh firejail-home-logger/

cp page-list.txt firejail-home-logger/ || true

echo "entering sandbox"
firejail --profile=/usr/local/etc/firejail/chromium-browser.profile --x11 --private="${PWD}/firejail-home-logger" './create-profile-chromium.sh'
echo "end of sandbox"
