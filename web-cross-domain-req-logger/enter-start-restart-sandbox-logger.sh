#!/bin/bash

# exit on empty variables
set -u

# exit on non-zero status
set -e

echo "entering sandbox, you can run log-page.sh there"
firejail --profile=/usr/local/etc/firejail/chromium-browser.profile --x11 --private="${PWD}/firejail-home-logger" './process-list-until-empty.sh'
echo "end of sandbox"
